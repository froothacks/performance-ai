import { notFound } from 'next/navigation';
import { useSourceProvider } from '#/app/contexts/source-context';
import { BACKEND_URL } from '../utils';
import { Sources } from './source';

export async function generateSources(userId: number, prompt: string) {
  const res = await fetch(`${BACKEND_URL}/query-threads`, {
    headers: {
      'ngrok-skip-browser-warning': true,
      'Content-Type': 'application/json',
    } as any,
    method: 'POST',
    body: JSON.stringify({ user_id: userId, prompt: prompt }),
  });

  console.log({ res });
  if (!res.ok) {
    // Render the closest `error.js` Error Boundary
    throw new Error('Something went wrong!');
  }

  const sources = (await res.json()) as Sources[];

  console.log({ sources });

  if (sources.length === 0) {
    // Render the closest `not-found.js` Error Boundary
    notFound();
  }

  return sources;
}
