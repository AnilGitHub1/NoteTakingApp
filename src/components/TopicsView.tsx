import React from 'react';
import { FolderKanban, ArrowRight, BookOpen } from 'lucide-react';
import { TopicCount } from '../types';

interface TopicsViewProps {
  topics: TopicCount[];
  onSelectTopic: (topic: string) => void;
}

export const TopicsView: React.FC<TopicsViewProps> = ({ topics, onSelectTopic }) => {
  return (
    <div className="flex-1 overflow-y-auto p-8 bg-[#09090b] text-[#e4e4e7]">
      <div className="max-w-5xl mx-auto space-y-6">
        <div>
          <h2 className="text-2xl font-bold text-white flex items-center gap-2.5 tracking-tight">
            <FolderKanban className="w-6 h-6 text-sky-400" />
            Categories & Topics
          </h2>
          <p className="text-xs text-[#71717a] mt-1">
            Browse and review your algorithmic problems organized by data structures and patterns.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {topics.map(({ name, count }) => (
            <div
              key={name}
              id={`topic-card-${name.replace(/\s+/g, '-').toLowerCase()}`}
              onClick={() => onSelectTopic(name)}
              className="p-5 rounded-lg bg-[#18181b] border border-[#27272a] hover:border-[#3f3f46] hover:bg-[#1e1e21] transition-all cursor-pointer group flex flex-col justify-between"
            >
              <div className="flex items-start justify-between gap-2">
                <div className="w-9 h-9 rounded-md bg-[#27272a] group-hover:bg-indigo-950/60 group-hover:text-indigo-400 text-[#a1a1aa] flex items-center justify-center transition-colors">
                  <BookOpen className="w-4 h-4" />
                </div>
                <span className="px-2 py-0.5 rounded bg-[#27272a] text-[11px] font-mono text-[#a1a1aa] border border-[#3f3f46]">
                  {count} {count === 1 ? 'question' : 'questions'}
                </span>
              </div>

              <div className="mt-4 flex items-center justify-between">
                <h3 className="text-sm font-medium text-[#e4e4e7] group-hover:text-white transition-colors">
                  {name}
                </h3>
                <ArrowRight className="w-4 h-4 text-[#52525b] group-hover:text-white group-hover:translate-x-1 transition-all" />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
