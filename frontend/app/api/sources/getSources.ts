import { notFound } from 'next/navigation';
import { BACKEND_URL } from '../utils';
import { Sources } from './source';

// `server-only` guarantees any modules that import code in file
// will never run on the client. Even though this particular api
// doesn't currently use sensitive environment variables, it's
// good practise to add `server-only` preemptively.
import 'server-only';

export async function getSources(userId: number) {
  const [isDarkTheme, setDarkTheme] = useLocalStorage(`source-${userId}`, true);

  if (!res.ok) {
    // Render the closest `error.js` Error Boundary
    throw new Error('Something went wrong!');
  }

  const sources = (await res.json()) as Sources;

  if (sources.length === 0) {
    // Render the closest `not-found.js` Error Boundary
    notFound();
  }

  return sources;
}
