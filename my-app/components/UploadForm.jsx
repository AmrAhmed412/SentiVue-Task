"use client"
import React from 'react'
import { useState } from 'react'

const UploadForm = () => {
  const [file, setFile] = useState(null);
  const [fileName, setFileName] = useState("");
  const [id, setId] = useState("");
  const [transcript, setTranscript] = useState("");
  const [loading, setLoading] = useState(false);

  const handleExport = (event) => {
    event.preventDefault();
    if (!id)
      return alert("Please transcribe a file first");
    fetch(`http://localhost:8000/export/${id}`, {
      method: "GET",
      headers: {
        'Content-Type': 'application/json'
      },
    })
    .then(response => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.blob();
    })
    .then(blob => {
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${fileName}.srt`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    })
    .catch(error => {
      console.error("There was a problem with the fetch operation:", error);
      alert("An error occurred while exporting the file. Please try again.");
    });
  }

  const handleSubmit =  (event) => {
    event.preventDefault();
    if(!file) {
      alert("Please upload a file first");
      return;
    }
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);
    fetch("http://localhost:8000/transcribe", {
      method: "POST",
      body: formData,
    })
    .then(response => {
      if (!response.ok) {
        setLoading(false);
        throw new Error("Network response was not ok");
      }
      return response
    })
    .then(data => data.json())
    .then(data=> {
      setFileName(data.fileName);
      setId(data.id);
      setTranscript(data.transcript);
      setLoading(false);
    })
    .catch(error => {
      console.error("There was a problem with the fetch operation:", error);
      alert("An error occurred while processing your request. Please try again.");
      setLoading(false);
    });
  }

  const handleUpload = (event)=> {
    event.preventDefault();
    if(event.target.files && event.target.files.length ==1) {
      setFile(event.target.files[0])
    }
  }
  return (
    <div>
      {loading && <div className="loading">
        <div class="loader"></div>
      </div>}
      <form method="POST" onSubmit={handleSubmit}>
        <div>
          <label htmlFor="file" >
            Upload File
          </label>
          <input
            type="file"
            id="file"
            name="file"
            accept="audio/*"
            onChange={handleUpload}
          />
        </div>
        <button
          type="submit"
        >
          Start Transcribing
        </button>
      </form>
      <div>
        <h2>Transcript</h2>
        <textarea
          value={transcript}
          rows="10"
          cols="50"
          placeholder="Your transcript will appear here..."
          disabled={true}
          />
        <button onClick={handleExport}>
          Export SRT file
        </button>
      </div>
    </div>
  )
}

export default UploadForm