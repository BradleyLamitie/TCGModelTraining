import pytesseract
from PIL import Image
import re

# Extract the text from an image
def extract_text(image_path): 
    image = Image.open(image_path)
    raw_text = pytesseract.image_to_string(image)
    return raw_text

# Try to extract the cardInfo from the ocr_text
def parse_card_info(ocr_text):
    lines = ocr_text.splitlines()
    name_candidates = [line for line in lines if re.match(r'^[A-Za-z]+', line)]
    set_number = next((line for line in lines if re.search(r'\d+/\d+', line)), None)
    
    return {
        'name': name_candidates[0] if name_candidates else None,
        'set_number': set_number
    }