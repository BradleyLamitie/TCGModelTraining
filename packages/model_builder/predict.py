# Example usage: py predict.py path/to/image.jpg

import torch
from torchvision import transforms, models
from PIL import Image
import sys
import json
from ocr_utils import extract_text, parse_card_info, extract_card_name
from db_utils import get_card_candidates
from classifier import predict_class, predict_class_without_candidates

# Identify a card based on image
def identify_card(image_path):

    # Load label map 
    with open('../../shared/labels.json') as f:
        idx_to_label = json.load(f)
    NUM_CLASSES = len(idx_to_label)

    # Load model and labels
    model = models.resnet18()
    model.fc = torch.nn.Linear(model.fc.in_features, NUM_CLASSES)  # Replace NUM_CLASSES accordingly
    model.load_state_dict(torch.load('models/classifier.pth', map_location='cpu'))
    model.eval()

    # Get the text from the card
    ocr_text = extract_card_name(image_path)

    # Massage the extracted text into card info properties
    card_info = parse_card_info(ocr_text)

    print("[OCR] Extracted:", card_info)

    # Use the cardInfo properties to grab any matching cards from mongo Cards database
    candidates = get_card_candidates(card_info['name'], card_info['set_number'])
    print(f"[DB] Found {len(candidates)} candidates")

    # If no matches are found, report no matches. 
    if len(candidates) == 0:
        print( "No match found.")
        prediction = predict_class_without_candidates(model, image_path, idx_to_label)
        return prediction if prediction is not None else "No match found"
    # If only one match is found, mission accomplished!
    elif len(candidates) == 1:
        return candidates[0]
    # If multiple matches exist, then try to narrow it down using the image prediction. 
    else:
        candidate_names = [c['name'] for c in candidates]
        prediction = predict_class(model, image_path, candidate_names, idx_to_label)
        return next((c for c in candidates if c['name'] == prediction), "No match found")

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python predict.py <image_path>")
    else:
        result = identify_card(sys.argv[1])
        print("\n[Result]", result)