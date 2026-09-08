import React, { useState } from 'react';
import { 
  FileCode2, 
  Copy, 
  Check, 
  Download, 
  Terminal, 
  CheckCircle2,
  FolderGit2
} from 'lucide-react';
import { PYTHON_FILES } from '../python_sources';

export const PythonSourceViewer: React.FC = () => {
  const [selectedFilename, setSelectedFilename] = useState<string>(PYTHON_FILES[0].filename);
  const [copied, setCopied] = useState(false);

  const currentFile = PYTHON_FILES.find((f) => f.filename === selectedFilename) || PYTHON_FILES[0];

  const handleCopy = () => {
    navigator.clipboard.writeText(currentFile.code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = (filename: string, content: string) => {
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const handleDownloadAll = () => {
    // Download each file in sequence
    PYTHON_FILES.forEach((file, index) => {
      setTimeout(() => {
        handleDownload(file.filename, file.code);
      }, index * 250);
    });
  };

  return (
    <div className="flex-1 overflow-hidden flex flex-col bg-[#09090b] text-[#e4e4e7]">
      {/* Top Banner with Run Instructions */}
      <div className="p-6 border-b border-[#27272a] bg-[#121212]">
        <div className="max-w-5xl mx-auto flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-xl font-bold text-white flex items-center gap-2 tracking-tight">
                <FileCode2 className="w-5 h-5 text-indigo-400" />
                Python Desktop Application Source Files
              </h2>
              <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 uppercase">
                PyQt6 / PySide6 Ready
              </span>
            </div>
            <p className="text-xs text-[#71717a] mt-1">
              Ready to execute directly on your desktop machine with embedded SQLite and isolated <code className="text-indigo-400 font-mono">./dsa_assets/</code> directory.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={handleDownloadAll}
              className="flex items-center gap-1.5 px-3.5 py-2 rounded text-xs font-medium bg-indigo-600 hover:bg-indigo-500 text-white shadow-lg shadow-indigo-900/20 transition-all"
            >
              <Download className="w-3.5 h-3.5" />
              Download All Files
            </button>
          </div>
        </div>

        {/* Quick Command Snippet */}
        <div className="max-w-5xl mx-auto mt-4 p-3 rounded-lg bg-[#18181b] border border-[#27272a] flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs">
          <div className="flex items-center gap-2 font-mono text-[#e4e4e7]">
            <Terminal className="w-4 h-4 text-emerald-400 shrink-0" />
            <span className="text-[#52525b]">Run locally:</span>
            <span className="text-emerald-400">pip install -r requirements.txt && python main.py</span>
          </div>
          <span className="text-[11px] text-[#52525b] font-sans">
            Auto-initializes <code className="text-[#a1a1aa]">dsa_notes.db</code> + <code className="text-[#a1a1aa]">dsa_assets/</code>
          </span>
        </div>
      </div>

      {/* Main File Explorer & Code Viewer */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Files Sidebar */}
        <div className="w-72 border-r border-[#27272a] bg-[#121212] p-3 overflow-y-auto space-y-1 shrink-0">
          <div className="text-[11px] font-bold uppercase tracking-widest text-[#52525b] px-3 py-2">
            Application Files
          </div>
          {PYTHON_FILES.map((file) => {
            const isSelected = file.filename === selectedFilename;
            return (
              <button
                key={file.filename}
                onClick={() => setSelectedFilename(file.filename)}
                className={`w-full text-left px-3 py-2 rounded-md text-sm font-medium transition-colors flex items-center justify-between ${
                  isSelected
                    ? 'bg-[#27272a] text-white'
                    : 'text-[#a1a1aa] hover:text-white hover:bg-[#18181b]'
                }`}
              >
                <div className="flex items-center gap-2 truncate">
                  <FileCode2 className={`w-4 h-4 shrink-0 ${isSelected ? 'text-indigo-400' : 'text-[#52525b]'}`} />
                  <span className="font-mono text-xs truncate">{file.filename}</span>
                </div>
              </button>
            );
          })}
        </div>

        {/* Right Code Area */}
        <div className="flex-1 flex flex-col overflow-hidden bg-black">
          <div className="p-3 bg-[#121212] border-b border-[#27272a] flex items-center justify-between text-xs">
            <div className="flex items-center gap-3">
              <span className="font-mono font-bold text-white">{currentFile.filename}</span>
              <span className="text-[#52525b] text-[11px]">• {currentFile.description}</span>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={handleCopy}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded bg-[#18181b] border border-[#27272a] hover:bg-[#27272a] text-[#a1a1aa] hover:text-white text-xs font-medium transition-colors"
              >
                {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                {copied ? 'Copied' : 'Copy Code'}
              </button>

              <button
                onClick={() => handleDownload(currentFile.filename, currentFile.code)}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded bg-[#18181b] border border-[#27272a] hover:bg-[#27272a] text-[#a1a1aa] hover:text-white text-xs font-medium transition-colors"
              >
                <Download className="w-3.5 h-3.5" />
                Download
              </button>
            </div>
          </div>

          <div className="flex-1 overflow-auto p-5 bg-black">
            <pre className="text-xs font-mono text-[#a5b4fc] leading-relaxed selection:bg-indigo-900 selection:text-white">
              <code>{currentFile.code}</code>
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
};
