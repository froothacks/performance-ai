import { notFound } from 'next/navigation';
import { BACKEND_URL } from '../utils';
import { User } from './user';

export async function getUsers() {
  const res = await fetch(`${BACKEND_URL}/all-users`, {
    headers: {
      'ngrok-skip-browser-warning': true,
    },
  });

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
