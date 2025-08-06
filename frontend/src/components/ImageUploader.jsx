import React, { useState } from "react";

const BACKEND_URL = "http://localhost:8000";

const ImageUploader = ({ onAlbumsFetched, setError, setLoading }) => {
  const [images, setImages] = useState([]);
  const [uploaded, setUploaded] = useState(false);

  const handleImageChange = async (event) => {
    const files = Array.from(event.target.files);
    const imagePreviews = files.map((file) => ({
      file,
      url: URL.createObjectURL(file),
    }));
    setImages(imagePreviews);
    setUploaded(false);

    if (files.length === 0) return;

    const formData = new FormData();
    files.forEach((file) => formData.append("files", file));

    try {
      setLoading(true);
      setError("");

      const uploadRes = await fetch(`${BACKEND_URL}/upload`, {
        method: "POST",
        body: formData,
      });

      const uploadData = await uploadRes.json();
      if (!uploadRes.ok) {
        throw new Error(uploadData?.error || "Upload failed");
      }

      setUploaded(true);
    } catch (err) {
      setError(err.message || "Upload error");
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateAlbums = async () => {
    try {
      setLoading(true);
      setError("");

      const clusterRes = await fetch(`${BACKEND_URL}/cluster`);
      const data = await clusterRes.json();

      if (!clusterRes.ok) {
        throw new Error(data?.error || "Clustering failed");
      }

      onAlbumsFetched(data);
    } catch (err) {
      setError(err.message || "Clustering error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ textAlign: "center" }}>
      <h2>Upload Your Photos</h2>

      <input
        type="file"
        multiple
        accept="image/*"
        onChange={handleImageChange}
        style={{ margin: "1rem auto", display: "block" }}
      />

      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "center",
          gap: 10,
          marginTop: "1rem",
        }}
      >
        {images.slice(0, 10).map((img, idx) => (
          <img
            key={idx}
            src={img.url}
            alt={`preview-${idx}`}
            style={{
              width: 100,
              height: 100,
              objectFit: "cover",
              borderRadius: 8,
            }}
          />
        ))}
      </div>

      {/* Show button only after upload is complete */}
      {uploaded && (
        <button
          onClick={handleGenerateAlbums}
          style={{
            marginTop: "1.5rem",
            padding: "10px 20px",
            fontSize: "1rem",
            borderRadius: 6,
            border: "none",
            backgroundColor: "#333",
            color: "#fff",
            cursor: "pointer",
          }}
        >
          Generate Albums
        </button>
      )}
    </div>
  );
};

export default ImageUploader;
