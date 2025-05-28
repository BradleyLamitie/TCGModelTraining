import pytesseract
import torch
from torchvision import transforms
from PIL import Image
import re
import cv2

def extract_text(image):
    # Convert to Black and White so that it can be used with pytesseract (pytesseract is only trained on black and white)
    return pytesseract.image_to_string(image)

def parse_card_info(ocr_text):
    lines = ocr_text.splitlines()
    print(lines)
    name_candidates = [line.strip() for line in lines if re.match(r'^[A-Za-z ]{3,}$', line)]
    set_number = next((line.strip() for line in lines if re.search(r'\d+/\d+', line)), None)
    return {
        'name': name_candidates[0] if name_candidates else None,
        'set_number': set_number
    }

def extract_card_name(image_path):
    image = cv2.imread(image_path)
    # Coords for a regular base set card
    x, y, w, h = 125, 40, 280, 60 
    roi = image[y:y+h, x:x+w]
    cv2.imshow('ROI', roi)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print(extract_text(roi))
    return extract_text(roi)

def extract_set_name(image_path):
    image = cv2.imread(image_path)
    x, y, w, h = 148, 40, 245, 60 
    roi = image[y:y+h, x:x+w]
    cv2.imshow('ROI', roi)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print(extract_text(roi))
    return extract_text(roi)

#Goal: 
# Search for card name
# Search for Set
# Search for number
