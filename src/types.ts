export type Difficulty = 'Easy' | 'Medium' | 'Hard';

export interface DSAQuestion {
  id: string;
  title: string;
  difficulty: Difficulty;
  topic: string;
  problemStatement: string;
  examples: string;
  notes: string;
  code: string;
  imagePath?: string; // local relative path or data URL
  createdAt: string;
  updatedAt: string;
}

export interface TopicCount {
  name: string;
  count: number;
}

export type ActiveView = 'explorer' | 'form' | 'topics' | 'python_code';
