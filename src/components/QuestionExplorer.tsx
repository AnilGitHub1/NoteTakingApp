import React, { useState } from 'react';
import { 
  Search, 
  Copy, 
  Check, 
  Pencil, 
  Trash2, 
  ImageIcon, 
  Clock, 
  ExternalLink,
  Code2,
  Tag,
  FileText,
  BookOpen
} from 'lucide-react';
import { DSAQuestion } from '../types';

interface QuestionExplorerProps {
  questions: DSAQuestion[];
  selectedQuestion: DSAQuestion | null;
  onSelectQuestion: (question: DSAQuestion) => void;
  onEditQuestion: (question: DSAQuestion) => void;
  onDeleteQuestion: (id: string) => void;
  searchTerm: string;
  onSearchChange: (val: string) => void;
  selectedTopic: string;
  onTopicChange: (topic: string) => void;
  allTopics: string[];
}

export const QuestionExplorer: React.FC<QuestionExplorerProps> = ({
  questions,
  selectedQuestion,
  onSelectQuestion,
  onEditQuestion,
  onDeleteQuestion,
  searchTerm,
  onSearchChange,
  selectedTopic,
  onTopicChange,
  allTopics
}) => {
  const [copied, setCopied] = useState(false);
  const [imageModalOpen, setImageModalOpen] = useState(false);

  const handleCopyCode = () => {
    if (!selectedQuestion?.code) return;
    navigator.clipboard.writeText(selectedQuestion.code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getDifficultyBadge = (diff: string) => {
    switch (diff) {
      case 'Easy':
        return (
          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 uppercase flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
            Easy
          </span>
        );
      case 'Medium':
        return (
          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/10 text-amber-400 border border-amber-500/20 uppercase flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-amber-500"></span>
            Medium
          </span>
        );
      case 'Hard':
        return (
          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-500/10 text-rose-400 border border-rose-500/20 uppercase flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-rose-500"></span>
            Hard
          </span>
        );
      default:
        return null;
    }
  };

  return (
    <div className="flex flex-col h-full overflow-hidden bg-[#09090b] text-[#e4e4e7]">
      {/* Top Filter Bar */}
      <div className="h-16 border-b border-[#27272a] flex items-center justify-between px-6 bg-[#09090b] shrink-0 gap-4">
        <div className="relative flex-1">
          <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-[#52525b]" />
          <input
            id="searchInput"
            type="text"
            placeholder="Search questions or topics..."
            value={searchTerm}
            onChange={(e) => onSearchChange(e.target.value)}
            className="w-full bg-[#18181b] border border-[#27272a] rounded-md py-1.5 pl-10 pr-4 text-sm text-[#e4e4e7] focus:outline-none focus:ring-1 focus:ring-indigo-500 placeholder-[#52525b] transition-all"
          />
        </div>

        {/* Topic Selector */}
        <select
          id="topicFilterDropdown"
          value={selectedTopic}
          onChange={(e) => onTopicChange(e.target.value)}
          className="bg-[#18181b] border border-[#27272a] rounded-md py-1.5 px-3 text-sm text-[#a1a1aa] hover:border-[#3f3f46] focus:outline-none focus:ring-1 focus:ring-indigo-500"
        >
          <option value="All">All Topics ({allTopics.length})</option>
          {allTopics.map((topic) => (
            <option key={topic} value={topic}>
              {topic}
            </option>
          ))}
        </select>
      </div>

      {/* Main Split Layout: Left List + Right Reader View */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left Column: Questions List */}
        <div className="w-80 border-r border-[#27272a] bg-[#0c0c0e] flex flex-col shrink-0 overflow-hidden">
          <div className="px-4 py-2.5 border-b border-[#27272a] text-[11px] font-bold uppercase tracking-widest text-[#52525b] flex items-center justify-between">
            <span>Questions ({questions.length})</span>
            <span className="text-[10px] text-[#52525b] font-mono">Recent</span>
          </div>

          <div className="flex-1 overflow-y-auto p-2 space-y-1">
            {questions.length === 0 ? (
              <div className="p-8 text-center text-[#52525b] text-sm flex flex-col items-center gap-2">
                <FileText className="w-8 h-8 text-[#3f3f46] stroke-1" />
                <span>No questions found matching criteria.</span>
              </div>
            ) : (
              questions.map((q) => {
                const isSelected = selectedQuestion?.id === q.id;
                return (
                  <div
                    key={q.id}
                    id={`question-card-${q.id}`}
                    onClick={() => onSelectQuestion(q)}
                    className={`p-3 rounded-lg cursor-pointer transition-colors ${
                      isSelected
                        ? 'bg-[#1e1e21] border border-indigo-500/30'
                        : 'bg-transparent hover:bg-[#18181b] border border-transparent'
                    }`}
                  >
                    <div className="flex items-start justify-between gap-2 mb-1.5">
                      <h3 className={`text-sm font-medium line-clamp-1 ${
                        isSelected ? 'text-white' : 'text-[#a1a1aa]'
                      }`}>
                        {q.title}
                      </h3>
                      {getDifficultyBadge(q.difficulty)}
                    </div>

                    <p className="text-xs text-[#71717a] line-clamp-2 mb-2 leading-relaxed">
                      {q.problemStatement || 'No description entered.'}
                    </p>

                    <div className="flex items-center justify-between text-[11px]">
                      <span className="px-1.5 py-0.5 rounded bg-[#27272a] text-[10px] text-[#a1a1aa] border border-[#3f3f46]">
                        {q.topic}
                      </span>
                      <div className="flex items-center gap-2 text-[#52525b] font-mono text-[10px]">
                        {q.imagePath && (
                          <span className="flex items-center gap-1 text-teal-400 font-sans">
                            <ImageIcon className="w-3 h-3" />
                            Diagram
                          </span>
                        )}
                        <span>{new Date(q.updatedAt).toLocaleDateString()}</span>
                      </div>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </div>

        {/* Right Column: Read-Only View Panel */}
        <div className="flex-1 overflow-y-auto p-8 bg-[#09090b]">
          {selectedQuestion ? (
            <div className="max-w-4xl mx-auto space-y-6">
              {/* Header: Title, Badges, Actions */}
              <div className="flex items-start justify-between gap-4 pb-6 border-b border-[#27272a]">
                <div className="space-y-3">
                  <div className="flex items-center gap-3">
                    {getDifficultyBadge(selectedQuestion.difficulty)}
                    <span className="text-[#52525b] text-xs font-mono">
                      Last edited {new Date(selectedQuestion.updatedAt).toLocaleDateString()}
                    </span>
                  </div>

                  <h2 className="text-3xl font-bold text-white tracking-tight">
                    {selectedQuestion.title}
                  </h2>

                  <div className="flex items-center gap-3">
                    <span className="px-2 py-1 rounded-md bg-[#18181b] text-xs text-[#a1a1aa] border border-[#27272a]">
                      {selectedQuestion.topic}
                    </span>
                    {selectedQuestion.imagePath && (
                      <span className="text-xs text-[#71717a] font-mono">
                        Relative Asset: {selectedQuestion.imagePath.startsWith('data:') ? './dsa_assets/diagram.png' : selectedQuestion.imagePath}
                      </span>
                    )}
                  </div>
                </div>

                {/* Edit & Delete Buttons */}
                <div className="flex items-center gap-2 shrink-0">
                  <button
                    id="editQuestionBtn"
                    onClick={() => onEditQuestion(selectedQuestion)}
                    className="px-3 py-1.5 text-sm bg-[#18181b] border border-[#27272a] rounded hover:bg-[#27272a] transition-colors text-[#a1a1aa] hover:text-white flex items-center gap-1.5"
                  >
                    <Pencil className="w-3.5 h-3.5 text-[#a1a1aa]" />
                    Edit
                  </button>
                  <button
                    id="deleteQuestionBtn"
                    onClick={() => {
                      if (window.confirm(`Delete question "${selectedQuestion.title}"?`)) {
                        onDeleteQuestion(selectedQuestion.id);
                      }
                    }}
                    className="px-3 py-1.5 text-sm bg-[#18181b] border border-rose-900/40 hover:bg-rose-950/40 rounded text-rose-400 transition-colors flex items-center gap-1.5"
                  >
                    <Trash2 className="w-3.5 h-3.5 text-rose-400" />
                    Delete
                  </button>
                </div>
              </div>

              {/* Problem Statement Card */}
              <div className="space-y-2">
                <div className="text-xs font-bold uppercase tracking-widest text-[#52525b] flex items-center gap-1.5">
                  <FileText className="w-3.5 h-3.5 text-indigo-400" />
                  Problem Statement
                </div>
                <div className="text-sm leading-relaxed text-[#d4d4d8] bg-[#18181b] p-4 rounded-lg border border-[#27272a] whitespace-pre-wrap">
                  {selectedQuestion.problemStatement || 'No problem statement provided.'}
                </div>
              </div>

              {/* Examples Card */}
              {selectedQuestion.examples && (
                <div className="space-y-2">
                  <div className="text-xs font-bold uppercase tracking-widest text-[#52525b] flex items-center gap-1.5">
                    <Tag className="w-3.5 h-3.5 text-amber-400" />
                    Examples & Test Cases
                  </div>
                  <div className="text-sm leading-relaxed text-[#d4d4d8] font-mono bg-[#18181b] p-4 rounded-lg border border-[#27272a] whitespace-pre-wrap">
                    {selectedQuestion.examples}
                  </div>
                </div>
              )}

              {/* Personal Notes & Approach */}
              {selectedQuestion.notes && (
                <div className="space-y-2">
                  <div className="text-xs font-bold uppercase tracking-widest text-[#52525b] flex items-center gap-1.5">
                    <BookOpen className="w-3.5 h-3.5 text-emerald-400" />
                    Personal Notes & Approach
                  </div>
                  <div className="text-sm leading-relaxed text-[#d4d4d8] bg-[#18181b] p-4 rounded-lg border border-[#27272a] whitespace-pre-wrap">
                    {selectedQuestion.notes}
                  </div>
                </div>
              )}

              {/* Attached Image Section */}
              {selectedQuestion.imagePath && (
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <div className="text-xs font-bold uppercase tracking-widest text-[#52525b] flex items-center gap-1.5">
                      <ImageIcon className="w-3.5 h-3.5 text-teal-400" />
                      Attached Diagram (./dsa_assets/)
                    </div>
                    <button
                      onClick={() => setImageModalOpen(true)}
                      className="text-xs text-indigo-400 hover:text-indigo-300 flex items-center gap-1"
                    >
                      <ExternalLink className="w-3 h-3" />
                      Expand Diagram
                    </button>
                  </div>
                  <div className="p-4 bg-[#18181b] rounded-lg border border-[#27272a] flex flex-col items-center justify-center overflow-hidden">
                    <img
                      src={selectedQuestion.imagePath}
                      alt="DSA Diagram"
                      className="max-h-72 object-contain rounded shadow cursor-pointer hover:opacity-95 transition-opacity"
                      onClick={() => setImageModalOpen(true)}
                    />
                    <span className="text-[11px] text-[#52525b] font-mono mt-3">
                      Stored in local execution folder: ./dsa_assets/
                    </span>
                  </div>
                </div>
              )}

              {/* Code Solution Block with Copy Button */}
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <div className="text-xs font-bold uppercase tracking-widest text-[#52525b] flex items-center gap-1.5">
                    <Code2 className="w-3.5 h-3.5 text-indigo-400" />
                    Solution Code
                  </div>

                  <button
                    id="copyCodeBtn"
                    onClick={handleCopyCode}
                    className="text-[11px] bg-[#27272a] hover:bg-[#3f3f46] text-[#a1a1aa] hover:text-white px-2.5 py-1 rounded border border-[#3f3f46] transition-colors flex items-center gap-1"
                  >
                    {copied ? (
                      <>
                        <Check className="w-3.5 h-3.5 text-emerald-400" />
                        <span className="text-emerald-400">Copied</span>
                      </>
                    ) : (
                      <>
                        <Copy className="w-3.5 h-3.5" />
                        <span>Copy Code</span>
                      </>
                    )}
                  </button>
                </div>

                <div className="p-5 bg-black rounded-xl border border-[#27272a] font-mono text-sm leading-relaxed text-[#a5b4fc] overflow-x-auto selection:bg-indigo-900 selection:text-white">
                  <pre>
                    <code>{selectedQuestion.code || '# No code provided yet.'}</code>
                  </pre>
                </div>
              </div>
            </div>
          ) : (
            <div className="h-full flex flex-col items-center justify-center text-[#52525b] text-sm space-y-3">
              <FileText className="w-12 h-12 text-[#3f3f46] stroke-1" />
              <span>Select any question from the list to review all notes and code.</span>
            </div>
          )}
        </div>
      </div>

      {/* Image Modal */}
      {imageModalOpen && selectedQuestion?.imagePath && (
        <div 
          className="fixed inset-0 z-50 bg-black/90 backdrop-blur-sm flex items-center justify-center p-6"
          onClick={() => setImageModalOpen(false)}
        >
          <div className="relative max-w-4xl max-h-[90vh] bg-[#18181b] p-4 rounded-xl border border-[#27272a] shadow-2xl flex flex-col items-center">
            <img
              src={selectedQuestion.imagePath}
              alt="Diagram Full Preview"
              className="max-h-[80vh] object-contain rounded"
            />
            <button
              onClick={() => setImageModalOpen(false)}
              className="mt-4 px-4 py-1.5 rounded bg-[#27272a] text-[#e4e4e7] hover:bg-[#3f3f46] text-xs font-medium border border-[#3f3f46]"
            >
              Close Preview
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
