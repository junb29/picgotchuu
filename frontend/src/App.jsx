import React, { useState } from "react";
import ImageUploader from "./components/ImageUploader";
import AlbumView from "./components/AlbumView";

const App = () => {
  const [albums, setAlbums] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        padding: "2rem",
        minHeight: "100vh",
        boxSizing: "border-box",
        fontFamily: "sans-serif",
      }}
    >
      <h1 style={{ fontSize: "2.5rem", marginBottom: "1.5rem" }}>
        PicGotchuu : AI Photo Organizer
      </h1>

      <ImageUploader
        onAlbumsFetched={setAlbums}
        setError={setError}
        setLoading={setLoading}
      />

      <h2 style={{ marginTop: "2rem" }}>Organized Albums</h2>

      {loading && <p>Clustering and labeling images...</p>}
      {!loading && error && <p style={{ color: "red" }}>{error}</p>}
      {!loading && Object.keys(albums).length === 0 && (
        <p>No albums yet. Upload some photos and they'll appear here.</p>
      )}
      {!loading && <AlbumView albums={albums} />}
    </div>
  );
};

export default App;
