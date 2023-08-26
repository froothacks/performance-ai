import { notFound } from 'next/navigation';
import { BACKEND_URL } from '../utils';
import { User } from './user';

// `server-only` guarantees any modules that import code in file
// will never run on the client. Even though this particular api
// doesn't currently use sensitive environment variables, it's
// good practise to add `server-only` preemptively.
import 'server-only';

export async function getUsers() {
  const res = await fetch(`${BACKEND_URL}/all-users`);

  if (!res.ok) {
    // Render the closest `error.js` Error Boundary
    throw new Error('Something went wrong!');
  }

  const users = (await res.json()) as User[];

  if (users.length === 0) {
    // Render the closest `not-found.js` Error Boundary
    notFound();
  }

  return users;
}