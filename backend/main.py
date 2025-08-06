from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from typing import List
import os
import shutil

from backend.clip_inference import get_image_embeddings, label_clusters_by_semantic_category
from backend.clustering import cluster_embeddings
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="data/uploads"), name="uploads")

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok = True)

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    
    for existing_file in os.listdir(UPLOAD_DIR):
        file_path = os.path.join(UPLOAD_DIR, existing_file)
        if os.path.isfile(file_path):
            os.remove(file_path)
    
    saved_files = []
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_files.append(file.filename)
    return {"message": "Files uploaded", "filenames": saved_files}

@app.get("/cluster")
def cluster_images():
    filenames, embeddings = get_image_embeddings()

    if not embeddings:
        return JSONResponse(status_code=400, content={"error": "No images uploaded"})

    num_images = len(embeddings)
    n_clusters = min(10, num_images) if num_images > 1 else 1

    labels = cluster_embeddings(embeddings, n_clusters=n_clusters)
 
    cluster_dict = {}
    for i, label in enumerate(labels):
        cluster_dict.setdefault(label, []).append(filenames[i])

    cluster_centers = [np.mean([embeddings[i] for i in range(len(labels)) if labels[i] == c], axis=0)
                         for c in cluster_dict.keys()]
    cluster_labels = label_clusters_by_semantic_category(
        cluster_centers=cluster_centers,
        csv_path="backend/data/clip_prompt_category_map.csv"
    )

    assert len(cluster_labels) == len(cluster_centers)

    labeled_albums = {}
    for i, cid in enumerate(cluster_dict.keys()):
        label = cluster_labels[i]
        if label not in labeled_albums:
            labeled_albums[label] = []
        labeled_albums[label].extend(cluster_dict[cid])

    return labeled_albums
    

@app.get("/")
def root():
    return {"message": "API working"}
