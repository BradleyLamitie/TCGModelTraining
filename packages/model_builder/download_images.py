import os
import requests
from pymongo import MongoClient
from urllib.parse import urlparse
from tqdm import tqdm
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

from shared.set_stamp_coords import build_set_coords_map

coords_map = build_set_coords_map()

# Define crop box for 1st edition stamps: (left, upper, right, lower)
first_edition_crop_box = (22, 438, 72, 474) 

load_dotenv()

mongo_uri=os.getenv('MONGO_CONNECTION_STRING')
db_name="RemodeledTestDB"
collection_name="Cards"

# Get the collection we will be querying
client = MongoClient(mongo_uri)
db = client[db_name]
collection = db[collection_name]

# Base output directory
output_dir = './datasets'
cards_output_dir = output_dir + "/cards"
sets_output_dir = output_dir + "/sets"
first_edition_output_dir = output_dir + "/first_edition"
stamp_folder = first_edition_output_dir + "/with_stamp"
no_stamp_folder = first_edition_output_dir + "/without_stamp"

# Ensure output directory exists
os.makedirs(stamp_folder, exist_ok=True)
os.makedirs(no_stamp_folder, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)
os.makedirs(cards_output_dir, exist_ok=True)
os.makedirs(sets_output_dir, exist_ok=True)
os.makedirs(first_edition_output_dir, exist_ok=True)

# Identify sets with 1st edition stamps
sets_with_stamps=["Base", "Jungle", "Fossil", "Team Rocket", "Gym Heroes", "Gym Challenge", "Neo Genesis", "Neo Discovery", "Neo Revelation", "Neo Destiny"]
# query = {"cardInfo.supertype":"Pokémon", "cardInfo.set.name":{"$in":sets_with_stamps}}

# Download images
# Item and Energy cards have 
for doc in tqdm(collection.find({},{'cardInfo.set.name' : 1, 'cardInfo.set.series' : 1,'cardInfo.set.series' : 1, 'cardInfo.name' : 1, 'cardInfo.number' : 1, 'cardInfo.images' : 1, 'cardInfo.supertype' : 1})):
    set_name = doc.get('cardInfo', {}).get('set', {}).get('name', 'Unknown')
    series_name = doc.get('cardInfo', {}).get('set', {}).get('series', 'Unknown')
    card_name = doc.get('cardInfo', {}).get('name', 'Unknown')
    number = doc.get('cardInfo', {}).get('number', 'Unknown')
    supertype = doc.get('cardInfo', {}).get('supertype', 'Unknown')
    image_url = doc.get('cardInfo', {}).get('images', {}).get('large', 'Unknown')

    print(set_name + card_name + number)

    add_edition = False
    add_sets = False
    first_edition_folder = no_stamp_folder


    if series_name == "NP" : 
        set_name = "Black Star Promos"

    if not image_url:
        continue

    try:
        # Get the image
        response = requests.get(image_url, timeout = 10)
        response.raise_for_status()

        image =  Image.open(BytesIO(response.content))

        parsed = urlparse(image_url)
        filename = series_name + "_" + set_name + "_" + card_name + "_" + number + ".png"
        filename = filename.replace(" ", "_")

        card_image_path = os.path.join(cards_output_dir, filename)
        image.save(card_image_path)

        if supertype == "Pokémon" :
            ###### Set Stamps ######
            # Open and crop the image of the set stamp
            if not set_name :
                folder = "unknown_set"
            else : 
                folder = series_name + "_" + set_name
            set_folder = sets_output_dir + "/" + folder.replace(" ", "_")
            os.makedirs(set_folder, exist_ok=True)

            # Define crop box: (left, upper, right, lower)
            crop_coords = coords_map.get(series_name)
            set_crop_box = (crop_coords.left, crop_coords.upper, crop_coords.right, crop_coords.lower) 

            cropped_set_image = image.crop(set_crop_box)
            image_path = os.path.join(set_folder, filename)
            cropped_set_image.save(image_path)

            ###### 1st Edition Stamps ######
            # Crop and save the image to get the first edition stamp area
            if set_name in sets_with_stamps :
                first_edition_folder = stamp_folder

            cropped_image = image.crop(first_edition_crop_box)
            image_path = os.path.join(first_edition_folder, filename)
            cropped_image.save(image_path)
        
    except Exception as e:
        print(f"Failed to download {image_url}: {e}")