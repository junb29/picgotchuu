import os
from PIL import Image
import pandas as pd
import torch
from torchvision import transforms
from transformers import CLIPProcessor, CLIPModel

device = "cuda" if torch.cuda.is_available() else "cpu"

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

IMAGE_DIR = "data/uploads"

def get_image_embeddings():
    image_embeddings = []
    filenames = []
    
    for fname in os.listdir(IMAGE_DIR):
        if fname.lower().endswith((".jpg", ".jpeg", ".png")):
            img_path = os.path.join(IMAGE_DIR, fname)
            image = Image.open(img_path).convert("RGB")
            
            inputs = processor(images = image, return_tensors = "pt").to(device)
            with torch.no_grad():
                outputs = model.get_image_features(**inputs)
                
            image_embeddings.append(outputs[0].cpu().numpy())
            filenames.append(fname)
    
    return filenames, image_embeddings

def label_clusters_by_semantic_category(cluster_centers, csv_path="backend/data/clip_prompt_category_map.csv"):

    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = model.to(device)

    df = pd.read_csv(csv_path)
    prompts = df["prompt"].tolist()
    categories = df["category"].tolist()
    prompt_to_category = dict(zip(prompts, categories))

    inputs = processor(text=prompts, return_tensors="pt", padding=True).to(device)
    with torch.no_grad():
        text_features = model.get_text_features(**inputs)
        text_features = text_features / text_features.norm(p=2, dim=-1, keepdim=True)

    labels = []
    for center in cluster_centers:
        center_tensor = torch.tensor(center).unsqueeze(0).to(device)
        center_tensor = center_tensor / center_tensor.norm(p=2, dim=-1, keepdim=True)

        sims = torch.matmul(center_tensor, text_features.T).squeeze(0)
        best_idx = torch.argmax(sims).item()
        best_prompt = prompts[best_idx]
        labels.append(prompt_to_category[best_prompt])

    return labels