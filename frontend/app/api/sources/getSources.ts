import { notFound } from 'next/navigation';
import { useSourceProvider } from '#/app/contexts/source-context';

export async function getSourcesForUser(userId: number) {
  const [sourceMap] = useSourceProvider();

  const sources = sourceMap?.[userId] ?? [];

  if (sources.length === 0) {
    // Render the closest `not-found.js` Error Boundary
    notFound();
  }

  return sources;
}
