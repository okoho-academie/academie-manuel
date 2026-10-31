import { notFound } from 'next/navigation';
import { readFileSync, existsSync } from 'fs';
import path from 'path';
import yaml from 'js-yaml';
import QuizClient from './QuizClient';

interface QuizQuestion {
  q: string;
  choix: string[];
  bonne: number;
  explication: string;
}

interface QuizData {
  code: string;
  titre: string;
  description: string;
  questions: QuizQuestion[];
}

export function generateMetadata({ params }: { params: { code: string } }) {
  return { title: `Quiz · ${params.code}` };
}

export default function QuizPage({ params }: { params: { code: string } }) {
  const quizPath = path.join(process.cwd(), '..', 'quiz', `${params.code}.yaml`);
  if (!existsSync(quizPath)) notFound();

  const raw = readFileSync(quizPath, 'utf-8');
  const data = yaml.load(raw) as QuizData;

  return (
    <div className="conteneur" style={{ paddingTop: '2rem', paddingBottom: '4rem' }}>
      <QuizClient data={data} />
    </div>
  );
}
