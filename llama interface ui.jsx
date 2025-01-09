// src/components/CodeLlamaInterface.jsx
import React, { useState, useRef } from 'react';
import { Editor } from '@monaco-editor/react';
import { FiSend, FiCopy, FiRotateCw, FiCode, FiSettings } from 'react-icons/fi';

const CodeLlamaInterface = () => {
  // State management
  const [prompt, setPrompt] = useState('');
  const [generatedCode, setGeneratedCode] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [language, setLanguage] = useState('python');
  const [settings, setSettings] = useState({
    temperature: 0.7,
    maxLength: 512,
    topP: 0.95,
    mode: 'standard'
  });
  const [showSettings, setShowSettings] = useState(false);

  // Editor references
  const editorRef = useRef(null);

  // Handle code generation
  const generateCode = async () => {
    setIsLoading(true);
    try {
      // API call will go here
      // For now, simulating API call
      setTimeout(() => {
        setGeneratedCode('// Generated code will appear here');
        setIsLoading(false);
      }, 1000);
    } catch (error) {
      console.error('Generation failed:', error);
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Left Sidebar - Settings */}
      <div className="w-64 bg-white p-4 border-r">
        <div className="flex items-center space-x-2 mb-6">
          <FiCode className="text-2xl text-blue-600" />
          <h1 className="text-xl font-bold">CodeLlama</h1>
        </div>

        <div className="space-y-4">
          {/* Language Selection */}
          <div>
            <label className="block text-sm font-medium mb-2">Language</label>
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="w-full p-2 border rounded"
            >
              <option value="python">Python</option>
              <option value="javascript">JavaScript</option>
              <option value="java">Java</option>
              <option value="cpp">C++</option>
            </select>
          </div>

          {/* Model Settings */}
          <div>
            <button
              onClick={() => setShowSettings(!showSettings)}
              className="flex items-center space-x-2 text-sm"
            >
              <FiSettings />
              <span>Advanced Settings</span>
            </button>

            {showSettings && (
              <div className="mt-2 space-y-3">
                <div>
                  <label className="block text-sm">Temperature</label>
                  <input
                    type="range"
                    min="0"
                    max="1"
                    step="0.1"
                    value={settings.temperature}
                    onChange={(e) => setSettings({
                      ...settings,
                      temperature: parseFloat(e.target.value)
                    })}
                    className="w-full"
                  />
                </div>
                {/* Add more settings controls */}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Prompt Input */}
        <div className="p-4 border-b bg-white">
          <div className="flex space-x-2">
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Enter your code prompt here..."
              className="flex-1 p-2 border rounded resize-none h-20"
            />
            <button
              onClick={generateCode}
              disabled={isLoading}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
            >
              {isLoading ? (
                <FiRotateCw className="animate-spin" />
              ) : (
                <FiSend />
              )}
            </button>
          </div>
        </div>

        {/* Code Output */}
        <div className="flex-1 p-4">
          <div className="h-full border rounded bg-white">
            <Editor
              height="100%"
              defaultLanguage={language}
              value={generatedCode}
              theme="vs-dark"
              options={{
                readOnly: true,
                minimap: { enabled: false }
              }}
              onMount={(editor) => (editorRef.current = editor)}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default CodeLlamaInterface;
// src/components/CodeLlamaInterface.jsx
// Add to existing imports
import { codeLlamaService } from '../services/codeLlamaService';

// Update the generateCode function in the component
const generateCode = async () => {
    setIsLoading(true);
    try {
        const response = await codeLlamaService.generateCode({
            prompt,
            language,
            temperature: settings.temperature,
            max_length: settings.maxLength,
            top_p: settings.topP,
        });
        
        setGeneratedCode(response.generated_code);
    } catch (error) {
        console.error('Generation failed:', error);
        // Add error notification here
    } finally {
        setIsLoading(false);
    }
};

// Add useEffect to fetch model info
useEffect(() => {
    const fetchModelInfo = async () => {
        try {
            const info = await codeLlamaService.getModelInfo();
            // Update settings with model defaults if needed
        } catch (error) {
            console.error('Failed to fetch model info:', error);
        }
    };
    
    fetchModelInfo();
}, []);
