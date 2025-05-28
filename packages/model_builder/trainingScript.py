import os
import json
import torch
from torch import nn, optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split

# Paths
DATA_DIR = '../pokemon-dataset-downloader/dataset' # Where the card Image data lives
LABELS_FILE = '../../shared/labels.json' # Where the file that maps the label indiex to class name
MODEL_PATH = 'models/classifier.pth' # Where the trained model will be placed. 
BATCH_SIZE = 32 # number of images being processed at once
IMG_SIZE = 224 # Images will be resized to 224x224 which is standard for ResNet
NUM_EPOCHS = 10 # How many iterations of training
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu") # Use GPU if available, otherwise use CPU

# Transforms - Convert the dataset to a consistent size (224x224)
transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize([0.5]*3, [0.5]*3)
])

# Dataset - load in the image data and transforms the images based on transform above
full_dataset = datasets.ImageFolder(DATA_DIR, transform=transform)

# Save label map - map the labels to images in the labels.json file
idx_to_label = {v: k for k, v in full_dataset.class_to_idx.items()}
with open(LABELS_FILE, 'w') as f:
    json.dump(idx_to_label, f)

# Split into train/val - separates data into training and validation sets (80/20) Then prepares them to be fed in batches.
train_size = int(0.8 * len(full_dataset))
val_size = len(full_dataset) - train_size
train_dataset, val_dataset = torch.utils.data.random_split(full_dataset, [train_size, val_size])

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE)

# Load pre-trained model - Loads the model and moves to GPU if available
model = models.resnet18(pretrained=True)
model.fc = nn.Linear(model.fc.in_features, len(full_dataset.classes)) # Uses the number of classes
model = model.to(DEVICE)

# Loss and optimizer - Standard loss function for multi-class classification and then optimizes it with Adam. 
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-4)

# Training loop - Runs through the training data for the number of epochs, tracking the loss and accuraacy. 
for epoch in range(NUM_EPOCHS):
    model.train()
    total_loss = 0
    correct = 0
    for images, labels in train_loader:
        images, labels = images.to(DEVICE), labels.to(DEVICE)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        correct += (outputs.argmax(1) == labels).sum().item()

    acc = correct / len(train_loader.dataset)
    print(f"Epoch {epoch+1}, Loss: {total_loss:.4f}, Accuracy: {acc:.4f}")

# Save model - Save the model weights to disk. 
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
torch.save(model.state_dict(), MODEL_PATH)
print(f"Model saved to {MODEL_PATH}")