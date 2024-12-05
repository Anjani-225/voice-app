import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Link, Routes } from 'react-router-dom';
import axios from 'axios';
import './App.css';
import Profile from './Profile';
import AudioApp from './AudioApp';
import Inference from './Inference';
import MenuIcon from '@mui/icons-material/Menu';

function App() {
  const [examples, setExamples] = useState({ source_files: [], reference_files: [] });
  const [selectedSource, setSelectedSource] = useState('');
  const [selectedReference, setSelectedReference] = useState('');
  const [message, setMessage] = useState('');
  const [outputFile, setOutputFile] = useState('');
  const [sidebarOpen, setSidebarOpen] = useState(true); // Track sidebar visibility

  useEffect(() => {
    // Fetch example files
    axios.get("http://127.0.0.1:5000/list_examples")
      .then((response) => setExamples(response.data))
      .catch((error) => console.error(error));
  }, []);

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen); // Toggle sidebar visibility
  };

  return (
    <Router>
      <div className="app-container">
        <div className={`sidebar ${sidebarOpen ? 'open' : 'closed'}`}>
          <button className="toggle-button" onClick={toggleSidebar}>
            {/* {sidebarOpen ? '<<' : '>>'}  */}
          </button>
          <ul className="nav-tabs">
            <li><Link to="/" className="nav-link">Profile</Link></li>
            <li><Link to="/audio" className="nav-link">Audio App</Link></li>
            <li><Link to="/inference" className="nav-link">Run Inference</Link></li>
          </ul>
        </div>
        <div className="content">
          <Routes>
            <Route path="/" element={<Profile />} />
            <Route path="/audio" element={<AudioApp />} />
            <Route 
              path="/inference" 
              element={
                <Inference 
                  examples={examples} 
                  selectedSource={selectedSource}
                  setSelectedSource={setSelectedSource}
                  selectedReference={selectedReference}
                  setSelectedReference={setSelectedReference}
                  message={message}
                  setMessage={setMessage}
                  outputFile={outputFile}
                  setOutputFile={setOutputFile}
                />
              }
            />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
