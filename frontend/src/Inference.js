import React from 'react';
import axios from 'axios';
import './Inference.css'; // Assuming you create a CSS file for styling

function Inference({
  examples,
  selectedSource,
  setSelectedSource,
  selectedReference,
  setSelectedReference,
  message,
  setMessage,
  outputFile,
  setOutputFile
}) {
  const handleRunInference = () => {
    if (!selectedSource || !selectedReference) {
      setMessage("Please select both a source and a reference file.");
      return;
    }

    axios.post("http://127.0.0.1:5000/run_inference", {
      source_file: selectedSource,
      target_file: selectedReference
    })
    .then((response) => {
      setMessage(response.data.message);
      setOutputFile(response.data.output_file);
    })
    .catch((error) => {
      setMessage(`Error: ${error.response.data.error}`);
    });
  };

  const handleDownload = () => {
    if (!outputFile) {
      setMessage("No output file to download.");
      return;
    }

    const url = `http://127.0.0.1:5000/download_output?file=${encodeURIComponent(outputFile)}`;
    window.open(url, "_blank");
  };

  return (
    <div className="inference-container">
      <h2>Run Inference</h2>
      <div className="input-container">
        <div className="input-group">
          <label htmlFor="source-file" className="input-label">Source File:</label>
          <select 
            id="source-file" 
            className="file-select" 
            onChange={(e) => setSelectedSource(e.target.value)}
          >
            <option value="">Select Source</option>
            {examples.source_files.map((file) => (
              <option key={file} value={file}>{file}</option>
            ))}
          </select>
        </div>
        <div className="input-group">
          <label htmlFor="reference-file" className="input-label">Reference File:</label>
          <select 
            id="reference-file" 
            className="file-select" 
            onChange={(e) => setSelectedReference(e.target.value)}
          >
            <option value="">Select Reference</option>
            {examples.reference_files.map((file) => (
              <option key={file} value={file}>{file}</option>
            ))}
          </select>
        </div>
      </div>
      <div className="button-container">
        <button 
          className="action-button" 
          onClick={handleRunInference}
        >
          Run Inference
        </button>
        <button 
          className="action-button download-button" 
          onClick={handleDownload} 
          disabled={!outputFile}
        >
          Download Output
        </button>
      </div>
      {message && <p className={`message ${message.startsWith('Error') ? 'error' : 'success'}`}>{message}</p>}
    </div>
  );
}

export default Inference;
