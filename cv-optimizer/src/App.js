// src/App.js

import React, { useState, useRef } from 'react';
import axios from 'axios';
import './App.css'; // Assurez-vous que ce fichier contient les directives Tailwind

function App() {
  const [cvFile, setCvFile] = useState(null);
  const [jobUrl, setJobUrl] = useState('');
  const [manualDescription, setManualDescription] = useState('');
  const [manualTitle, setManualTitle] = useState('');
  const [mode, setMode] = useState('automatic'); // 'automatic' ou 'manual'
  const [downloadLink, setDownloadLink] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Référence pour le champ de fichier
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    setCvFile(e.target.files[0]);
  };

  const handleModeChange = (e) => {
    setMode(e.target.value);
    setError(null);
    setDownloadLink(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!cvFile) {
      setError("Veuillez télécharger votre CV au format PDF.");
      return;
    }

    if (mode === 'automatic' && !jobUrl) {
      setError("Veuillez fournir l'URL de l'offre d'emploi.");
      return;
    }

    if (mode === 'manual' && (!manualDescription || !manualTitle)) {
      setError("Veuillez fournir la description et le titre du poste.");
      return;
    }

    setLoading(true);
    setError(null);
    setDownloadLink(null);

    const formData = new FormData();
    formData.append('file', cvFile);
    if (mode === 'automatic') {
      formData.append('job_url', jobUrl);
    } else {
      formData.append('manual_description', manualDescription);
      formData.append('manual_title', manualTitle);
    }

    try {
      const response = await axios.post('http://127.0.0.1:8000/process_cv/', formData, {
        responseType: 'blob', // Important pour gérer la réponse en tant que blob
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      // Extraire le nom du fichier à partir des en-têtes de réponse
      const disposition = response.headers['content-disposition'];
      let filename = 'CV_Optimisé.pdf'; // Nom par défaut

      if (disposition && disposition.indexOf('attachment') !== -1) {
        const filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
        const matches = filenameRegex.exec(disposition);
        if (matches != null && matches[1]) { 
          filename = matches[1].replace(/['"]/g, '');
        }
      }

      console.log('Disposition:', disposition);
      console.log('Filename:', filename);

      // Créer une URL pour le blob
      const url = window.URL.createObjectURL(new Blob([response.data], { type: 'application/pdf' }));
      setDownloadLink({ url, filename });

    } catch (err) {
      if (err.response && err.response.data) {
        setError(err.response.data.detail || "Une erreur s'est produite.");
      } else {
        setError("Impossible de se connecter au serveur.");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = () => {
    if (downloadLink) {
      const link = document.createElement('a');
      link.href = downloadLink.url;
      link.setAttribute('download', downloadLink.filename);
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
      window.URL.revokeObjectURL(downloadLink.url); // Libérer la mémoire
      setDownloadLink(null); // Réinitialiser le lien de téléchargement
    }
  };

  const handleRestart = () => {
    setCvFile(null);
    setJobUrl('');
    setManualDescription('');
    setManualTitle('');
    setMode('automatic');
    setDownloadLink(null);
    setError(null);
    
    // Réinitialiser la valeur du champ de fichier via la référence
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 dark:bg-gray-900 flex items-center justify-center p-4 transition-colors duration-300">
      <div className="bg-gray-800 dark:bg-gray-800 shadow-lg rounded-lg p-8 w-full max-w-2xl transition-colors duration-300">
        <h1 className="text-3xl font-bold text-center text-gray-100 mb-6">Optimisation de votre CV</h1>
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Upload CV */}
          <div>
            <label className="block text-gray-300 font-medium mb-2">Télécharger votre CV (PDF)</label>
            <div className="flex items-center">
              <label 
                htmlFor="file-upload" 
                className="cursor-pointer bg-blue-600 text-white px-4 py-2 rounded-md shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-opacity-75"
              >
                Choisir un fichier
              </label>
              <span className="ml-4 text-gray-300">
                {cvFile ? cvFile.name : "Aucun fichier choisi"}
              </span>
            </div>
            <input 
              id="file-upload" 
              type="file" 
              accept="application/pdf" 
              onChange={handleFileChange} 
              ref={fileInputRef} 
              required 
              className="hidden"
            />
          </div>

          {/* Mode de saisie */}
          <div>
            <label className="block text-gray-300 font-medium mb-2">Mode de saisie</label>
            <select 
              value={mode} 
              onChange={handleModeChange} 
              className="w-full px-3 py-2 border border-gray-600 rounded-md bg-gray-700 text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition-colors duration-300 appearance-none"
            >
              <option value="automatic">Automatique (URL de l'offre)</option>
              <option value="manual">Manuel (Description et Titre)</option>
            </select>
          </div>

          {/* Mode Automatique */}
          {mode === 'automatic' && (
            <div>
              <label className="block text-gray-300 font-medium mb-2">URL de l'offre d'emploi (LinkedIn)</label>
              <input 
                type="url" 
                value={jobUrl} 
                onChange={(e) => setJobUrl(e.target.value)} 
                placeholder="https://www.linkedin.com/jobs/view/..." 
                required 
                className="w-full px-3 py-2 border border-gray-600 rounded-md bg-gray-700 text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition-colors duration-300 appearance-none"
              />
            </div>
          )}

          {/* Mode Manuel */}
          {mode === 'manual' && (
            <>
              <div>
                <label className="block text-gray-300 font-medium mb-2">Description de l'offre d'emploi</label>
                <textarea 
                  value={manualDescription} 
                  onChange={(e) => setManualDescription(e.target.value)} 
                  placeholder="Entrez la description de l'annonce ici..." 
                  rows="5" 
                  required 
                  className="w-full px-3 py-2 border border-gray-600 rounded-md bg-gray-700 text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition-colors duration-300 appearance-none"
                />
              </div>
              <div>
                <label className="block text-gray-300 font-medium mb-2">Titre du poste</label>
                <input 
                  type="text" 
                  value={manualTitle} 
                  onChange={(e) => setManualTitle(e.target.value)} 
                  placeholder="Titre du poste" 
                  required 
                  className="w-full px-3 py-2 border border-gray-600 rounded-md bg-gray-700 text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition-colors duration-300 appearance-none"
                />
              </div>
            </>
          )}

          {/* Afficher l'erreur */}
          {error && <p className="text-red-500 text-sm">{error}</p>}

          {/* Bouton de soumission avec animation de chargement */}
          <button 
            type="submit" 
            disabled={loading}
            className={`w-full flex items-center justify-center py-2 px-4 bg-blue-600 text-white font-semibold rounded-md shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-opacity-75 transition-colors duration-300 appearance-none ${
              loading ? 'opacity-50 cursor-not-allowed' : ''
            }`}
          >
            {loading && (
              <svg 
                className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" 
                xmlns="http://www.w3.org/2000/svg" 
                fill="none" 
                viewBox="0 0 24 24"
              >
                <circle 
                  className="opacity-25" 
                  cx="12" 
                  cy="12" 
                  r="10" 
                  stroke="currentColor" 
                  strokeWidth="4"
                ></circle>
                <path 
                  className="opacity-75" 
                  fill="currentColor" 
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                ></path>
              </svg>
            )}
            {loading ? 'Processing...' : 'Optimiser mon CV'}
          </button>
        </form>

        {/* Section de téléchargement */}
        {downloadLink && (
          <div className="mt-6">
            <h2 className="text-2xl font-semibold text-gray-100 mb-4 text-center">CV Optimisé</h2>
            <div className="flex space-x-4">
              <button 
                onClick={handleDownload}
                className="flex-1 py-2 px-6 bg-green-500 text-white font-medium rounded-md shadow-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-opacity-75 transition-colors duration-300 appearance-none"
              >
                Télécharger le CV Optimisé
              </button>
              <button 
                onClick={handleRestart}
                className="flex-1 py-2 px-6 bg-gray-600 text-white font-medium rounded-md shadow-md hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-opacity-75 transition-colors duration-300 appearance-none"
              >
                Recommencer
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
