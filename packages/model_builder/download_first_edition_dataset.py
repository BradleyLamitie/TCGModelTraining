import os
import requests
from pymongo import MongoClient
from urllib.parse import urlparse
from tqdm import tqdm
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

# TODO: Move these methods to a util
def cropImage(left, upper, right, lower, image) : 
    # Define crop box: (left, upper, right, lower)
    crop_box = (left, upper, right, lower)  # adjust these values as needed

    # Open and crop the image
    cropped = image.crop(crop_box)
    return cropped

def getImageFromURL(image_url, timeout=10) : 
    try:
        response = requests.get(image_url, timeout)
        response.raise_for_status()

        return response.content
    
    except Exception as e:
        raise Exception ("Encountered an error when retrieving image from " + image_url)

# def save_image(image, file_path) :
#     # Open and crop the image
#     with Image.open(image_path) as img:
#         cropped = img.crop(crop_box)
#         cropped.save(image_path)  # overwrite or use a new filename

load_dotenv()

mongo_uri=os.getenv('MONGO_CONNECTION_STRING')
db_name="RemodeledTestDB"
collection_name="Cards"

# Get the collection we will be querying
client = MongoClient(mongo_uri)
db = client[db_name]
collection = db[collection_name]

# Base output directory
output_dir = './datasets/first_edition'

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

stamp_folder = output_dir+"/with_stamp"
no_stamp_folder = output_dir+"/without_stamp"

os.makedirs(stamp_folder, exist_ok=True)
os.makedirs(no_stamp_folder, exist_ok=True)

sets_with_stamps=["Base", "Jungle", "Fossil", "Team Rocket", "Gym Heroes", "Gym Challenge", "Neo Genesis", "Neo Discovery", "Neo Revelation", "Neo Destiny"]
# query = {"cardInfo.supertype":"Pokémon", "cardInfo.set.name":{"$in":sets_with_stamps}}

# Download images
# Item and Energy cards have 
for doc in tqdm(collection.find({"cardInfo.supertype":"Pokémon"},{'cardInfo.set.name' : 1, 'cardInfo.name' : 1, 'cardInfo.number' : 1, 'cardInfo.images' : 1})):
    set_name = doc.get('cardInfo', {}).get('set', {}).get('name', 'Unknown')
    card_name = doc.get('cardInfo', {}).get('name', 'Unknown')
    number = doc.get('cardInfo', {}).get('number', 'Unknown')

    print(set_name + card_name + number)
    # Only certain cards have stamps
    if (set_name in sets_with_stamps) :
        folder = stamp_folder
        run = "first_edition"
    else :
        folder = no_stamp_folder
        run = "unlimited"

    image_url = doc.get('cardInfo', {}).get('images', {}).get('large', 'Unknown')

    if not image_url:
        continue

    try:
        # Get the image
        response = requests.get(image_url, timeout = 10)
        response.raise_for_status()

        image =  Image.open(BytesIO(response.content))

        parsed = urlparse(image_url)
        filename = set_name + "_" + card_name + "_" + number + ".png"
        filename = filename.replace(" ", "_")

        # Define crop box: (left, upper, right, lower)
        crop_box = (22, 438, 72, 474) 

        # Open and crop the image
        cropped_image = image.crop(crop_box)

        image_path = os.path.join(folder, filename)
        cropped_image.save(image_path)

    except Exception as e:
        print(f"Failed to download {image_url}: {e}")