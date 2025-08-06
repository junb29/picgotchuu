# Picgotchuu – AI Photo Organizer

Picgotchuu is an AI-powered web application that intelligently organizes your unstructured photo collection into categorized albums such as "Food", "People", "Nature", and more. It leverages computer vision and natural language models to cluster and label images without manual tagging.

Built using React, FastAPI, OpenAI CLIP, scikit-learn, and deployed via Vercel and Render.

Note: The backend currently exceeds the 512MiB memory limit on Render’s free tier during CLIP inference. As a result, even if you upload photos, the “Generate Albums” button won’t appear and album generation will fail. Deployment to Railway (or another memory-optimized platform) is planned soon. In the meantime, the frontend is fully functional and can be used to preview the UI/UX.

## Live Demo

- Frontend: https://picgotchuu.vercel.app
- Backend: https://picgotchuu-api.onrender.com

## Features

- Upload multiple photos from any device
- Automatic clustering using CLIP embeddings and KMeans
- Smart labeling using prompt-based similarity scoring
- Responsive UI for desktop and mobile
- Fully deployed and ready to use online

## Technical Stack

### Image Embedding

- Utilizes OpenAI CLIP (ViT-B/32) to encode uploaded images into 512-dimensional semantic vectors.

### Unsupervised Clustering

- Applies KMeans clustering (sklearn.cluster.KMeans) on the CLIP embeddings to group similar images together.

### Zero-Shot Labeling

- Each cluster center is matched against a list of prompts (e.g., "food", "a group of people", "screenshot") using cosine similarity in CLIP space.
- Supports semantic grouping via CSV mapping (e.g., "boy", "girl", "selfie" -> "People").

### Backend (FastAPI)

- `/upload`: Accepts photo uploads and stores them to `/data/uploads`
- `/cluster`: Generates embeddings, clusters them, assigns semantic labels, and returns grouped filenames

### Frontend (React + Vite)

- Choose file input to preview thumbnails
- One-click button to trigger album generation
- Albums shown with labels

## Project Structure

```
picgotchuu
├── backend
│   ├── main.py
│   ├── clustering.py
│   ├── clip_inference.py
│   ├── data/uploads
│   └── clip_prompt_category_map.csv
├── frontend
│   ├── src/components
│   │   ├── ImageUploader.jsx
│   │   └── AlbumView.jsx
│   ├── App.jsx
│   └── main.jsx
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup and Deployment

### Local Development

Backend:

```
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Frontend:

```
cd frontend
npm install
npm run dev
```

Note: In order to run it locally, change the BACKEND_URL in frontend to your local URL

## TODOs

- Add duplicate detection
- Implement automatic garbage photo filtering
- Improve UI responsiveness on very large image sets

## License

This project is licensed under the MIT License.

## Author

Made by Jun Bae (https://github.com/junb29)
