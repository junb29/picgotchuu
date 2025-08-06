import React from "react";

const BACKEND_URL = "https://picgotchuu.onrender.com";

const AlbumView = ({ albums }) => {
  if (!albums || Object.keys(albums).length === 0) return null;

  return (
    <div style={{ marginTop: "2rem", display: "flex", flexDirection: "column", alignItems: "center" }}>
      {Object.entries(albums).map(([label, filenames], idx) => (
        <div key={idx} style={{ marginBottom: "2rem", width: "100%" }}>
          <h3 style={{ textAlign: "center" }}>{label}</h3>
          <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center" }}>
            {filenames.map((fname, i) => (
              <img
                key={i}
                src={`${BACKEND_URL}/uploads/${fname}`}
                alt={fname}
                style={{ width: 100, height: 100, objectFit: "cover", margin: 5 }}
              />
            ))}
          </div>
        </div>
      ))}
    </div>
  );

};

export default AlbumView;
