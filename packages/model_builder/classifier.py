import torch
from torchvision import transforms
from PIL import Image

def predict_class(model, image_path, candidate_classes, class_to_idx):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.5]*3, [0.5]*3)
    ])
    image = Image.open(image_path).convert("RGB")
    input_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(input_tensor)
        probs = torch.nn.functional.softmax(outputs, dim=1)

    class_probs = {cls: probs[0][class_to_idx[cls]].item() for cls in candidate_classes if cls in class_to_idx}
    best_class = max(class_probs, key=class_probs.get)
    return best_class

def predict_class_without_candidates(model, image_path, class_to_idx):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.5]*3, [0.5]*3)
    ])

    image = Image.open(image_path).convert("RGB")
    input_tensor = transform(image).unsqueeze(0)
    output = model(input_tensor)
    pred = torch.argmax(output, 1).item()

    print(f"Prediction: {class_to_idx[str(pred)]}")

    confidence = torch.softmax(output, dim=1)[0][pred].item()
    print(f"Confidence: {confidence:.2%}")
    return pred