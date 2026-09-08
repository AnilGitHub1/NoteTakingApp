import React from 'react';
import { 
  BookOpen, 
  FolderKanban, 
  PlusCircle, 
  FileCode2, 
  HardDrive, 
  CheckCircle2
} from 'lucide-react';
import { ActiveView, Difficulty } from '../types';

interface SidebarProps {
  activeView: ActiveView;
  onSelectView: (view: ActiveView) => void;
  selectedDifficulty: string;
  onSelectDifficulty: (diff: string) => void;
  stats: {
    total: number;
    easy: number;
    medium: number;
    hard: number;
  };
}

export const Sidebar: React.FC<SidebarProps> = ({
  activeView,
  onSelectView,
  selectedDifficulty,
  onSelectDifficulty,
  stats
}) => {
  return (
    <aside 
      id="desktopSidebar"
      className="w-64 bg-[#121212] border-r border-[#27272a] flex flex-col justify-between shrink-0 select-none text-[#e4e4e7]"
    >
      {/* Top Section: App Branding & Navigation */}
      <div className="p-4 flex flex-col gap-5">
        {/* Branding Header with Desktop Window Accent */}
        <div className="px-2 pt-1 pb-1">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white shadow-lg shadow-indigo-900/30 font-bold text-sm">
              D
            </div>
            <div>
              <h1 className="text-base font-semibold tracking-tight text-white leading-tight">
                DSA Ledger
              </h1>
              <p className="text-[11px] text-[#52525b] font-mono">
                Desktop Study Suite (PyQt6)
              </p>
            </div>
          </div>
        </div>

        {/* Primary Navigation Views */}
        <div className="flex flex-col gap-1">
          <div className="text-[11px] uppercase tracking-widest text-[#52525b] font-bold mb-1 px-2">
            Navigation
          </div>

          <button
            id="navAllQuestionsBtn"
            onClick={() => onSelectView('explorer')}
            className={`w-full flex items-center justify-between px-3 py-2 rounded-md text-sm font-medium transition-colors ${
              activeView === 'explorer'
                ? 'bg-[#27272a] text-white'
                : 'text-[#a1a1aa] hover:text-white hover:bg-[#18181b]'
            }`}
          >
            <span className="flex items-center gap-2.5">
              <BookOpen className="w-4 h-4 text-indigo-400" />
              All Questions
            </span>
            <span className="text-[10px] px-1.5 py-0.5 rounded bg-[#18181b] border border-[#27272a] text-[#a1a1aa] font-mono">
              {stats.total}
            </span>
          </button>

          <button
            id="navCategoriesBtn"
            onClick={() => onSelectView('topics')}
            className={`w-full flex items-center justify-between px-3 py-2 rounded-md text-sm font-medium transition-colors ${
              activeView === 'topics'
                ? 'bg-[#27272a] text-white'
                : 'text-[#a1a1aa] hover:text-white hover:bg-[#18181b]'
            }`}
          >
            <span className="flex items-center gap-2.5">
              <FolderKanban className="w-4 h-4 text-sky-400" />
              Topics
            </span>
          </button>

          <button
            id="navAddQuestionBtn"
            onClick={() => onSelectView('form')}
            className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
              activeView === 'form'
                ? 'bg-[#27272a] text-white border border-indigo-500/40'
                : 'text-[#a1a1aa] hover:text-white hover:bg-[#18181b]'
            }`}
          >
            <PlusCircle className="w-4 h-4 text-emerald-400" />
            Add New
          </button>
        </div>

        {/* Quick Difficulty Filters Section */}
        <div className="flex flex-col gap-1 pt-3 border-t border-[#27272a]">
          <div className="text-[11px] uppercase tracking-widest text-[#52525b] font-bold mb-1 px-2">
            Difficulty
          </div>

          <div className="flex flex-col gap-0.5">
            <button
              id="filterDiffAll"
              onClick={() => {
                onSelectDifficulty('All');
                if (activeView !== 'explorer') onSelectView('explorer');
              }}
              className={`w-full flex items-center justify-between px-3 py-1.5 rounded-md text-sm transition-colors ${
                selectedDifficulty === 'All'
                  ? 'bg-[#27272a] text-white font-medium'
                  : 'text-[#a1a1aa] hover:text-white hover:bg-[#18181b]'
              }`}
            >
              <span>All Levels</span>
              <span className="text-[10px] font-mono text-[#52525b]">{stats.total}</span>
            </button>

            <button
              id="filterDiffEasy"
              onClick={() => {
                onSelectDifficulty('Easy');
                if (activeView !== 'explorer') onSelectView('explorer');
              }}
              className={`w-full flex items-center justify-between px-3 py-1.5 rounded-md text-sm transition-colors ${
                selectedDifficulty === 'Easy'
                  ? 'bg-[#18181b] text-emerald-400 font-medium border border-emerald-500/30'
                  : 'text-[#a1a1aa] hover:text-white hover:bg-[#18181b]'
              }`}
            >
              <span className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-emerald-500"></div>
                Easy
              </span>
              <span className="text-[10px] font-mono text-[#52525b]">{stats.easy}</span>
            </button>

            <button
              id="filterDiffMedium"
              onClick={() => {
                onSelectDifficulty('Medium');
                if (activeView !== 'explorer') onSelectView('explorer');
              }}
              className={`w-full flex items-center justify-between px-3 py-1.5 rounded-md text-sm transition-colors ${
                selectedDifficulty === 'Medium'
                  ? 'bg-[#18181b] text-amber-400 font-medium border border-amber-500/30'
                  : 'text-[#a1a1aa] hover:text-white hover:bg-[#18181b]'
              }`}
            >
              <span className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-amber-500"></div>
                Medium
              </span>
              <span className="text-[10px] font-mono text-[#52525b]">{stats.medium}</span>
            </button>

            <button
              id="filterDiffHard"
              onClick={() => {
                onSelectDifficulty('Hard');
                if (activeView !== 'explorer') onSelectView('explorer');
              }}
              className={`w-full flex items-center justify-between px-3 py-1.5 rounded-md text-sm transition-colors ${
                selectedDifficulty === 'Hard'
                  ? 'bg-[#18181b] text-rose-400 font-medium border border-rose-500/30'
                  : 'text-[#a1a1aa] hover:text-white hover:bg-[#18181b]'
              }`}
            >
              <span className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-rose-500"></div>
                Hard
              </span>
              <span className="text-[10px] font-mono text-[#52525b]">{stats.hard}</span>
            </button>
          </div>
        </div>

        {/* Python Source Code Navigator Button */}
        <div className="pt-3 border-t border-[#27272a]">
          <button
            id="navPythonFilesBtn"
            onClick={() => onSelectView('python_code')}
            className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
              activeView === 'python_code'
                ? 'bg-[#27272a] text-white border border-indigo-500/40'
                : 'text-[#a1a1aa] hover:text-white hover:bg-[#18181b]'
            }`}
          >
            <FileCode2 className="w-4 h-4 text-indigo-400" />
            <span>Python Desktop Files</span>
          </button>
        </div>
      </div>

      {/* Bottom Section: 100% Offline Status Pill */}
      <div className="p-4 border-t border-[#27272a] text-[11px] text-[#52525b] bg-[#121212]">
        <div className="flex items-center gap-2 text-xs text-emerald-400 font-medium mb-1">
          <CheckCircle2 className="w-3.5 h-3.5" />
          <span>Local SQLite Mode</span>
        </div>
        <div className="flex items-center gap-1.5 text-[11px] text-[#71717a]">
          <HardDrive className="w-3 h-3 text-[#52525b] shrink-0" />
          <span className="truncate">dsa_notes.db</span>
        </div>
        <div className="text-[10px] text-[#52525b] font-mono mt-0.5">
          Assets: ./dsa_assets/
        </div>
      </div>
    </aside>
  );
};
