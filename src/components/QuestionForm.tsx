import React, { useState, useRef, useEffect } from 'react';
import { 
  Save, 
  X, 
  Upload, 
  Trash2, 
  ImageIcon, 
  HelpCircle,
  FileCode,
  Tag
} from 'lucide-react';
import { DSAQuestion, Difficulty } from '../types';
import { STANDARD_TOPICS } from '../data';

interface QuestionFormProps {
  questionToEdit: DSAQuestion | null;
  onSave: (questionData: Omit<DSAQuestion, 'id' | 'createdAt' | 'updatedAt'>, existingId?: string) => void;
  onCancel: () => void;
}

export const QuestionForm: React.FC<QuestionFormProps> = ({
  questionToEdit,
  onSave,
  onCancel
}) => {
  const [title, setTitle] = useState('');
  const [difficulty, setDifficulty] = useState<Difficulty>('Medium');
  const [topic, setTopic] = useState('Array & Hash Table');
  const [customTopic, setCustomTopic] = useState('');
  const [isCustomTopic, setIsCustomTopic] = useState(false);
  const [problemStatement, setProblemStatement] = useState('');
  const [examples, setExamples] = useState('');
  const [notes, setNotes] = useState('');
  const [code, setCode] = useState('');
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [imageFileName, setImageFileName] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (questionToEdit) {
      setTitle(questionToEdit.title);
      setDifficulty(questionToEdit.difficulty);
      if (STANDARD_TOPICS.includes(questionToEdit.topic)) {
        setTopic(questionToEdit.topic);
        setIsCustomTopic(false);
      } else {
        setTopic('Other');
        setCustomTopic(questionToEdit.topic);
        setIsCustomTopic(true);
      }
      setProblemStatement(questionToEdit.problemStatement || '');
      setExamples(questionToEdit.examples || '');
      setNotes(questionToEdit.notes || '');
      setCode(questionToEdit.code || '');
      setImagePreview(questionToEdit.imagePath || null);
      setImageFileName(questionToEdit.imagePath ? 'dsa_assets/saved_diagram.png' : null);
    } else {
      // Reset
      setTitle('');
      setDifficulty('Medium');
      setTopic(STANDARD_TOPICS[0]);
      setIsCustomTopic(false);
      setCustomTopic('');
      setProblemStatement('');
      setExamples('');
      setNotes('');
      setCode('');
      setImagePreview(null);
      setImageFileName(null);
    }
  }, [questionToEdit]);

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Simulate safe local asset copy to ./dsa_assets/
    const sanitizedName = file.name.replace(/[^a-zA-Z0-9._-]/g, '_');
    setImageFileName(`dsa_assets/${sanitizedName}`);

    const reader = new FileReader();
    reader.onloadend = () => {
      setImagePreview(reader.result as string);
    };
    reader.readAsDataURL(file);
  };

  const handleRemoveImage = () => {
    setImagePreview(null);
    setImageFileName(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) {
      alert('Question title is required!');
      return;
    }

    const finalTopic = isCustomTopic ? customTopic.trim() || 'General' : topic;

    onSave(
      {
        title: title.trim(),
        difficulty,
        topic: finalTopic,
        problemStatement: problemStatement.trim(),
        examples: examples.trim(),
        notes: notes.trim(),
        code: code,
        imagePath: imagePreview || ''
      },
      questionToEdit ? questionToEdit.id : undefined
    );
  };

  return (
    <div className="flex-1 overflow-y-auto p-8 bg-[#09090b] text-[#e4e4e7]">
      <div className="max-w-3xl mx-auto bg-[#121212] border border-[#27272a] rounded-xl p-6 space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-[#27272a]">
          <div>
            <h2 className="text-xl font-bold text-white tracking-tight">
              {questionToEdit ? `Edit Question: ${questionToEdit.title}` : 'Add New DSA Question'}
            </h2>
            <p className="text-xs text-[#52525b] mt-0.5">
              Saved automatically into local SQLite database (<span className="font-mono text-[#a1a1aa]">dsa_notes.db</span>).
            </p>
          </div>
          <button
            type="button"
            onClick={onCancel}
            className="text-[#a1a1aa] hover:text-white p-1.5 rounded-lg hover:bg-[#27272a] transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-5">
          {/* Row 1: Title Input */}
          <div className="space-y-1.5">
            <label className="text-[11px] font-bold uppercase tracking-widest text-[#52525b]">
              Question Title <span className="text-rose-400">*</span>
            </label>
            <input
              id="formQuestionTitle"
              type="text"
              required
              placeholder="e.g. Longest Palindromic Substring, Word Break, Median of Two Sorted Arrays"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full bg-[#18181b] border border-[#27272a] rounded-md px-3.5 py-2 text-sm text-[#e4e4e7] placeholder-[#52525b] focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
            />
          </div>

          {/* Row 2: Difficulty & Topic */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Difficulty Level */}
            <div className="space-y-1.5">
              <label className="text-[11px] font-bold uppercase tracking-widest text-[#52525b]">
                Difficulty Level <span className="text-rose-400">*</span>
              </label>
              <div className="grid grid-cols-3 gap-2">
                <button
                  type="button"
                  id="diffRadioEasy"
                  onClick={() => setDifficulty('Easy')}
                  className={`py-2 px-3 rounded-md text-xs font-semibold border transition-all flex items-center justify-center gap-1.5 ${
                    difficulty === 'Easy'
                      ? 'bg-[#18181b] text-emerald-400 border-emerald-500/40 shadow-sm'
                      : 'bg-[#18181b] text-[#a1a1aa] border-[#27272a] hover:bg-[#27272a]'
                  }`}
                >
                  <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
                  Easy
                </button>

                <button
                  type="button"
                  id="diffRadioMedium"
                  onClick={() => setDifficulty('Medium')}
                  className={`py-2 px-3 rounded-md text-xs font-semibold border transition-all flex items-center justify-center gap-1.5 ${
                    difficulty === 'Medium'
                      ? 'bg-[#18181b] text-amber-400 border-amber-500/40 shadow-sm'
                      : 'bg-[#18181b] text-[#a1a1aa] border-[#27272a] hover:bg-[#27272a]'
                  }`}
                >
                  <span className="w-2 h-2 rounded-full bg-amber-500"></span>
                  Medium
                </button>

                <button
                  type="button"
                  id="diffRadioHard"
                  onClick={() => setDifficulty('Hard')}
                  className={`py-2 px-3 rounded-md text-xs font-semibold border transition-all flex items-center justify-center gap-1.5 ${
                    difficulty === 'Hard'
                      ? 'bg-[#18181b] text-rose-400 border-rose-500/40 shadow-sm'
                      : 'bg-[#18181b] text-[#a1a1aa] border-[#27272a] hover:bg-[#27272a]'
                  }`}
                >
                  <span className="w-2 h-2 rounded-full bg-rose-500"></span>
                  Hard
                </button>
              </div>
            </div>

            {/* Topic / Tag */}
            <div className="space-y-1.5">
              <label className="text-[11px] font-bold uppercase tracking-widest text-[#52525b]">
                Topic / Category <span className="text-rose-400">*</span>
              </label>
              <div className="flex gap-2">
                <select
                  id="formTopicSelect"
                  value={isCustomTopic ? 'Other' : topic}
                  onChange={(e) => {
                    if (e.target.value === 'Other') {
                      setIsCustomTopic(true);
                    } else {
                      setIsCustomTopic(false);
                      setTopic(e.target.value);
                    }
                  }}
                  className="flex-1 bg-[#18181b] border border-[#27272a] rounded-md px-3 py-2 text-sm text-[#a1a1aa] focus:outline-none focus:border-indigo-500"
                >
                  {STANDARD_TOPICS.map((t) => (
                    <option key={t} value={t}>
                      {t}
                    </option>
                  ))}
                  <option value="Other">+ Custom Topic...</option>
                </select>

                {isCustomTopic && (
                  <input
                    type="text"
                    placeholder="Enter topic name..."
                    value={customTopic}
                    onChange={(e) => setCustomTopic(e.target.value)}
                    className="w-1/2 bg-[#18181b] border border-indigo-500/80 rounded-md px-3 py-2 text-sm text-[#e4e4e7] focus:outline-none"
                  />
                )}
              </div>
            </div>
          </div>

          {/* Row 3: Problem Statement */}
          <div className="space-y-1.5">
            <label className="text-[11px] font-bold uppercase tracking-widest text-[#52525b]">
              Problem Statement
            </label>
            <textarea
              id="formProblemStatement"
              rows={4}
              placeholder="Paste or write problem description, constraints, and conditions..."
              value={problemStatement}
              onChange={(e) => setProblemStatement(e.target.value)}
              className="w-full bg-[#18181b] border border-[#27272a] rounded-md p-3 text-sm text-[#e4e4e7] placeholder-[#52525b] focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 leading-relaxed font-sans"
            />
          </div>

          {/* Row 4: Examples */}
          <div className="space-y-1.5">
            <label className="text-[11px] font-bold uppercase tracking-widest text-[#52525b]">
              Examples & Test Cases
            </label>
            <textarea
              id="formExamples"
              rows={3}
              placeholder={`Example 1:\nInput: nums = [1,2,3], k = 2\nOutput: [2,3]\n\nExample 2:...`}
              value={examples}
              onChange={(e) => setExamples(e.target.value)}
              className="w-full bg-[#18181b] border border-[#27272a] rounded-md p-3 text-xs font-mono text-[#d4d4d8] placeholder-[#52525b] focus:outline-none focus:border-indigo-500 leading-relaxed"
            />
          </div>

          {/* Row 5: Personal Notes / Approach */}
          <div className="space-y-1.5">
            <label className="text-[11px] font-bold uppercase tracking-widest text-[#52525b]">
              Personal Notes, Intuition & Complexity
            </label>
            <textarea
              id="formNotes"
              rows={3}
              placeholder="Key pattern, intuition, why greedy fails here, time complexity O(N log N), space complexity O(N)..."
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              className="w-full bg-[#18181b] border border-[#27272a] rounded-md p-3 text-sm text-[#d4d4d8] placeholder-[#52525b] focus:outline-none focus:border-indigo-500 leading-relaxed"
            />
          </div>

          {/* Row 6: Code Block Section (Courier/Monospace) */}
          <div className="space-y-1.5">
            <div className="flex items-center justify-between">
              <label className="text-[11px] font-bold uppercase tracking-widest text-[#52525b] flex items-center gap-1.5">
                <FileCode className="w-3.5 h-3.5 text-indigo-400" />
                Solution Code (Fixed-Width Monospace / Courier)
              </label>
              <span className="text-[10px] font-mono text-[#52525b]">Supports Python / C++ / Java syntax</span>
            </div>
            <textarea
              id="formCode"
              rows={6}
              placeholder={`def solve(self, nums: list[int]) -> int:\n    # Write algorithm implementation here\n    pass`}
              value={code}
              onChange={(e) => setCode(e.target.value)}
              className="w-full bg-black border border-[#27272a] rounded-lg p-3 text-xs font-mono text-[#a5b4fc] placeholder-[#52525b] focus:outline-none focus:border-indigo-500 leading-relaxed tracking-wide"
              style={{ fontFamily: '"Cascadia Code", "Courier New", Courier, monospace' }}
            />
          </div>

          {/* Row 7: Picture / Image Attachment (Local Assets) */}
          <div className="space-y-2 p-4 rounded-lg border border-dashed border-[#27272a] bg-[#18181b]">
            <div className="flex items-center justify-between">
              <div>
                <h4 className="text-xs font-bold uppercase tracking-wider text-[#e4e4e7] flex items-center gap-1.5">
                  <ImageIcon className="w-4 h-4 text-sky-400" />
                  Picture / Diagram Attachment
                </h4>
                <p className="text-[11px] text-[#71717a] mt-0.5">
                  Attach an image or diagram to illustrate the solution.
                </p>
              </div>

              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleImageUpload}
                className="hidden"
                id="fileUploadInput"
              />

              <button
                type="button"
                id="browseImageBtn"
                onClick={() => fileInputRef.current?.click()}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium bg-[#27272a] hover:bg-[#3f3f46] text-[#e4e4e7] border border-[#3f3f46] transition-colors"
              >
                <Upload className="w-3.5 h-3.5 text-indigo-400" />
                Browse Image...
              </button>
            </div>

            {/* Thumbnail Preview if attached */}
            {imagePreview && (
              <div className="pt-2 flex items-center justify-between gap-4 border-t border-[#27272a] mt-2">
                <div className="flex items-center gap-3">
                  <img
                    src={imagePreview}
                    alt="Uploaded Diagram"
                    className="w-16 h-16 object-cover rounded border border-[#27272a] shadow"
                  />
                  <div>
                    <p className="text-xs font-medium text-[#e4e4e7] truncate max-w-xs font-mono">
                      {imageFileName ? imageFileName.replace('dsa_assets/', '') : 'attached_diagram.png'}
                    </p>
                    <span className="text-[10px] text-emerald-400">Image attached successfully</span>
                  </div>
                </div>

                <button
                  type="button"
                  onClick={handleRemoveImage}
                  className="flex items-center gap-1 px-2.5 py-1 text-xs text-rose-400 hover:bg-rose-950/40 rounded border border-rose-900/40 transition-colors"
                >
                  <Trash2 className="w-3 h-3" />
                  Remove
                </button>
              </div>
            )}
          </div>

          {/* Action Buttons */}
          <div className="flex items-center justify-end gap-3 pt-4 border-t border-[#27272a]">
            <button
              type="button"
              onClick={onCancel}
              className="px-4 py-1.5 rounded text-sm text-[#a1a1aa] hover:text-white bg-[#18181b] border border-[#27272a] hover:bg-[#27272a] transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              id="saveQuestionSubmitBtn"
              className="flex items-center gap-2 px-5 py-1.5 rounded text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-500 shadow-lg shadow-indigo-900/20 transition-all"
            >
              <Save className="w-4 h-4" />
              Save Question
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
