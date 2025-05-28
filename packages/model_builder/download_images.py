import os
import requests
from pymongo import MongoClient
from urllib.parse import urlparse
from tqdm import tqdm
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
import argparse

from shared.set_stamp_coords import build_set_coords_map

load_dotenv()

sets_with_stamps = [
    "Base", "Jungle", "Fossil", "Team Rocket", "Gym Heroes", "Gym Challenge",
    "Neo Genesis", "Neo Discovery", "Neo Revelation", "Neo Destiny"
]

first_edition_crop_box = (22, 438, 72, 474)  # (left, upper, right, lower)

def sanitize_filename(name: str) -> str:
    return name.replace(" ", "_").replace("/", "_").replace(":", "_")

def set_up_cards_folder(base_dir):
    path = os.path.join(base_dir, "cards")
    os.makedirs(path, exist_ok=True)
    return path

def set_up_first_edition_folders(base_dir):
    base = os.path.join(base_dir, "first_edition")
    stamp = os.path.join(base, "with_stamp")
    no_stamp = os.path.join(base, "without_stamp")
    for path in [base, stamp, no_stamp]:
        os.makedirs(path, exist_ok=True)
    return stamp, no_stamp

def set_up_sets_folder(base_dir):
    path = os.path.join(base_dir, "sets")
    os.makedirs(path, exist_ok=True)
    return path

def initialize_mongo_collection():
    mongo_uri = os.getenv("MONGO_CONNECTION_STRING")
    client = MongoClient(mongo_uri)
    db = client["RemodeledTestDB"]
    return db["Cards"]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download and crop card images.")
    parser.add_argument("--card", action="store_true", help="Download full card images")
    parser.add_argument("--first_edition", action="store_true", help="Crop and download 1st edition stamps")
    parser.add_argument("--set", action="store_true", help="Crop and download set symbols")

    args = parser.parse_args()

    output_dir = "./datasets"
    os.makedirs(output_dir, exist_ok=True)

    mongo_collection = initialize_mongo_collection()
    coords_map = build_set_coords_map()

    # Setup folders
    card_folder = set_up_cards_folder(output_dir) if args.card else None
    stamp_folder, no_stamp_folder = set_up_first_edition_folders(output_dir) if args.first_edition else (None, None)
    sets_output_folder = set_up_sets_folder(output_dir) if args.set else None

    projection = {
        'cardInfo.set.name': 1,
        'cardInfo.set.series': 1,
        'cardInfo.name': 1,
        'cardInfo.number': 1,
        'cardInfo.images': 1,
        'cardInfo.supertype': 1
    }

    for doc in tqdm(mongo_collection.find({}, projection)):
        info = doc.get('cardInfo', {})
        set_name = info.get('set', {}).get('name', 'Unknown')
        series_name = info.get('set', {}).get('series', 'Unknown')
        card_name = info.get('name', 'Unknown')
        number = info.get('number', 'Unknown')
        supertype = info.get('supertype', 'Unknown')
        image_url = info.get('images', {}).get('large')

        if series_name == "NP":
            set_name = "Black Star Promos"

        if not image_url:
            continue

        try:
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))

            filename = sanitize_filename(f"{series_name}_{set_name}_{card_name}_{number}.png")

            # Save full card image
            if args.card:
                image.save(os.path.join(card_folder, filename))

            # 1st Edition stamp
            if args.first_edition and supertype == "Pokémon":
                target_folder = stamp_folder if set_name in sets_with_stamps else no_stamp_folder
                cropped = image.crop(first_edition_crop_box)
                cropped.save(os.path.join(target_folder, filename))

            # Set symbol
            if args.set and supertype == "Pokémon":
                crop_coords = coords_map.get(series_name)
                if crop_coords:
                    crop_box = (crop_coords.left, crop_coords.upper, crop_coords.right, crop_coords.lower)
                    cropped = image.crop(crop_box)
                    folder_name = sanitize_filename(f"{series_name}_{set_name}") or "unknown_set"
                    final_folder = os.path.join(sets_output_folder, folder_name)
                    os.makedirs(final_folder, exist_ok=True)
                    cropped.save(os.path.join(final_folder, filename))

        except Exception as e:
            print(f"Failed to process image: {image_url} - {e}")
