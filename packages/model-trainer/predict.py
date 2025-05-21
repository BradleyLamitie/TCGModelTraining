# Example usage: py predict.py path/to/image.jpg

import torch
from torchvision import transforms, models
from PIL import Image
import sys
import json

# Load label map 
with open('../../shared/labels.json') as f:
    idx_to_label = json.load(f)
NUM_CLASSES = len(idx_to_label)

# Load model and labels
model = models.resnet18()
model.fc = torch.nn.Linear(model.fc.in_features, NUM_CLASSES)  # Replace NUM_CLASSES accordingly
model.load_state_dict(torch.load('models/classifier.pth', map_location='cpu'))
model.eval()

with open('../../shared/labels.json') as f:
    idx_to_label = json.load(f)

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.5]*3, [0.5]*3)
])

img_path = sys.argv[1]
image = Image.open(img_path).convert("RGB")
input_tensor = transform(image).unsqueeze(0)
output = model(input_tensor)
pred = torch.argmax(output, 1).item()

print(f"Prediction: {idx_to_label[str(pred)]}")

confidence = torch.softmax(output, dim=1)[0][pred].item()
print(f"Confidence: {confidence:.2%}")