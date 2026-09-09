/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useMemo } from 'react';
import { Sidebar } from './components/Sidebar';
import { QuestionExplorer } from './components/QuestionExplorer';
import { QuestionForm } from './components/QuestionForm';
import { TopicsView } from './components/TopicsView';
import { PythonSourceViewer } from './components/PythonSourceModal';
import { DSAQuestion, ActiveView, TopicCount } from './types';
import { INITIAL_QUESTIONS, STANDARD_TOPICS } from './data';
import { Code2, RotateCcw, Download } from 'lucide-react';

const LOCAL_STORAGE_KEY = 'dsa_desktop_notes_questions_v1';

export default function App() {
  // Load questions from local storage or pre-seeded sample data
  const [questions, setQuestions] = useState<DSAQuestion[]>(() => {
    try {
      const saved = localStorage.getItem(LOCAL_STORAGE_KEY);
      if (saved) {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed) && parsed.length > 0) {
          return parsed;
        }
      }
    } catch (e) {
      console.error('Error reading localStorage:', e);
    }
    return INITIAL_QUESTIONS;
  });

  const [activeView, setActiveView] = useState<ActiveView>('explorer');
  const [selectedQuestionId, setSelectedQuestionId] = useState<string | null>(() => {
    return questions[0]?.id || null;
  });
  const [questionToEdit, setQuestionToEdit] = useState<DSAQuestion | null>(null);

  // Filters
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedDifficulty, setSelectedDifficulty] = useState('All');
  const [selectedTopic, setSelectedTopic] = useState('All');

  // Persist to localStorage on every change
  useEffect(() => {
    try {
      localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(questions));
    } catch (e) {
      console.error('Error writing to localStorage:', e);
    }
  }, [questions]);

  // Derived statistics
  const stats = useMemo(() => {
    const total = questions.length;
    const easy = questions.filter((q) => q.difficulty === 'Easy').length;
    const medium = questions.filter((q) => q.difficulty === 'Medium').length;
    const hard = questions.filter((q) => q.difficulty === 'Hard').length;
    return { total, easy, medium, hard };
  }, [questions]);

  // Derived topics
  const allTopics = useMemo(() => {
    const topicSet = new Set<string>();
    STANDARD_TOPICS.forEach((t) => topicSet.add(t));
    questions.forEach((q) => topicSet.add(q.topic));
    return Array.from(topicSet).sort();
  }, [questions]);

  const topicsWithCounts: TopicCount[] = useMemo(() => {
    const map = new Map<string, number>();
    questions.forEach((q) => {
      map.set(q.topic, (map.get(q.topic) || 0) + 1);
    });
    return Array.from(map.entries())
      .map(([name, count]) => ({ name, count }))
      .sort((a, b) => b.count - a.count);
  }, [questions]);

  // Filtered questions
  const filteredQuestions = useMemo(() => {
    return questions.filter((q) => {
      // Difficulty match
      if (selectedDifficulty !== 'All' && q.difficulty !== selectedDifficulty) {
        return false;
      }
      // Topic match
      if (selectedTopic !== 'All' && q.topic !== selectedTopic) {
        return false;
      }
      // Search term
      if (searchTerm.trim()) {
        const query = searchTerm.toLowerCase();
        const inTitle = q.title.toLowerCase().includes(query);
        const inProblem = (q.problemStatement || '').toLowerCase().includes(query);
        const inNotes = (q.notes || '').toLowerCase().includes(query);
        const inTopic = q.topic.toLowerCase().includes(query);
        if (!inTitle && !inProblem && !inNotes && !inTopic) {
          return false;
        }
      }
      return true;
    });
  }, [questions, selectedDifficulty, selectedTopic, searchTerm]);

  // Ensure an active question is selected
  useEffect(() => {
    if (filteredQuestions.length > 0) {
      const exists = filteredQuestions.some((q) => q.id === selectedQuestionId);
      if (!exists) {
        setSelectedQuestionId(filteredQuestions[0].id);
      }
    } else {
      setSelectedQuestionId(null);
    }
  }, [filteredQuestions, selectedQuestionId]);

  const selectedQuestion = useMemo(() => {
    return questions.find((q) => q.id === selectedQuestionId) || null;
  }, [questions, selectedQuestionId]);

  // Handlers
  const handleSaveQuestion = (
    data: Omit<DSAQuestion, 'id' | 'createdAt' | 'updatedAt'>,
    existingId?: string
  ) => {
    const timestamp = new Date().toISOString();
    if (existingId) {
      // Update
      setQuestions((prev) =>
        prev.map((q) =>
          q.id === existingId
            ? { ...q, ...data, updatedAt: timestamp }
            : q
        )
      );
      setSelectedQuestionId(existingId);
    } else {
      // Add new
      const newQuestion: DSAQuestion = {
        ...data,
        id: String(Date.now()),
        createdAt: timestamp,
        updatedAt: timestamp
      };
      setQuestions((prev) => [newQuestion, ...prev]);
      setSelectedQuestionId(newQuestion.id);
    }
    setQuestionToEdit(null);
    setActiveView('explorer');
  };

  const handleDeleteQuestion = (id: string) => {
    setQuestions((prev) => prev.filter((q) => q.id !== id));
    if (selectedQuestionId === id) {
      setSelectedQuestionId(null);
    }
  };

  const handleEditQuestion = (question: DSAQuestion) => {
    setQuestionToEdit(question);
    setActiveView('form');
  };

  const handleResetSampleData = () => {
    if (window.confirm('Reset questions back to default DSA seed questions?')) {
      setQuestions(INITIAL_QUESTIONS);
      setSelectedQuestionId(INITIAL_QUESTIONS[0].id);
    }
  };

  const handleExportBackup = () => {
    const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(questions, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute('href', dataStr);
    downloadAnchor.setAttribute('download', 'dsa_notes_backup.json');
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  };

  return (
    <div className="flex flex-col h-screen w-screen overflow-hidden bg-[#09090b] text-[#e4e4e7] font-sans select-none">
      {/* Native Desktop Window Header Bar */}
      <header className="h-10 bg-[#09090b] border-b border-[#27272a] flex items-center justify-between px-5 shrink-0 text-xs select-none">
        {/* Window controls (traffic lights) & Branding */}
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1.5">
            <div className="w-3 h-3 rounded-full bg-[#ff5f56] border border-[#e0443e]"></div>
            <div className="w-3 h-3 rounded-full bg-[#ffbd2e] border border-[#dea123]"></div>
            <div className="w-3 h-3 rounded-full bg-[#27c93f] border border-[#1aab29]"></div>
          </div>
          <span className="text-[#a1a1aa] font-medium tracking-tight">
            DSA Notes
          </span>
        </div>

        {/* Right quick actions */}
        <div className="flex items-center gap-2">
          <button
            onClick={handleExportBackup}
            title="Export questions to JSON"
            className="text-xs bg-[#18181b] border border-[#27272a] text-[#a1a1aa] hover:text-white flex items-center gap-1.5 px-3 py-1.5 rounded hover:bg-[#27272a] transition-colors"
          >
            <Download className="w-3.5 h-3.5 text-[#a1a1aa]" />
            Export DB
          </button>
          <button
            onClick={handleResetSampleData}
            title="Restore sample questions"
            className="text-xs bg-[#18181b] border border-[#27272a] text-[#a1a1aa] hover:text-white flex items-center gap-1.5 px-3 py-1.5 rounded hover:bg-[#27272a] transition-colors"
          >
            <RotateCcw className="w-3.5 h-3.5 text-[#a1a1aa]" />
            Reset Samples
          </button>
          <button
            onClick={() => setActiveView('python_code')}
            className="text-xs bg-indigo-600 text-white flex items-center gap-1.5 px-3.5 py-1.5 rounded font-medium shadow-lg shadow-indigo-900/20 hover:bg-indigo-500 transition-colors"
          >
            <Code2 className="w-3.5 h-3.5" />
            Python Files
          </button>
        </div>
      </header>

      {/* Main Desktop Interface */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left Sidebar */}
        <Sidebar
          activeView={activeView}
          onSelectView={(view) => {
            if (view === 'form') {
              setQuestionToEdit(null); // new question
            }
            setActiveView(view);
          }}
          selectedDifficulty={selectedDifficulty}
          onSelectDifficulty={(diff) => {
            setSelectedDifficulty(diff);
            setActiveView('explorer');
          }}
          stats={stats}
        />

        {/* Main Content Pane */}
        <main className="flex-1 flex flex-col overflow-hidden bg-[#0c0c0e]">
          {activeView === 'explorer' && (
            <QuestionExplorer
              questions={filteredQuestions}
              selectedQuestion={selectedQuestion}
              onSelectQuestion={(q) => setSelectedQuestionId(q.id)}
              onEditQuestion={handleEditQuestion}
              onDeleteQuestion={handleDeleteQuestion}
              searchTerm={searchTerm}
              onSearchChange={setSearchTerm}
              selectedTopic={selectedTopic}
              onTopicChange={setSelectedTopic}
              allTopics={allTopics}
            />
          )}

          {activeView === 'form' && (
            <QuestionForm
              questionToEdit={questionToEdit}
              onSave={handleSaveQuestion}
              onCancel={() => {
                setQuestionToEdit(null);
                setActiveView('explorer');
              }}
            />
          )}

          {activeView === 'topics' && (
            <TopicsView
              topics={topicsWithCounts}
              onSelectTopic={(topicName) => {
                setSelectedTopic(topicName);
                setActiveView('explorer');
              }}
            />
          )}

          {activeView === 'python_code' && (
            <PythonSourceViewer />
          )}
        </main>
      </div>

      {/* Bottom Desktop Status Bar */}
      <footer className="h-7 bg-[#09090b] border-t border-[#27272a] flex items-center justify-between px-4 text-[11px] text-[#52525b] font-mono select-none">
        <div className="flex items-center gap-4">
          <span className="flex items-center gap-1.5 text-emerald-400 font-medium">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
            Ready
          </span>
        </div>
        <div className="flex items-center gap-3">
          <span>{filteredQuestions.length} of {questions.length} questions visible</span>
        </div>
      </footer>
    </div>
  );
}
