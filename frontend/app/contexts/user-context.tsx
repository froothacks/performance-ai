'use client';

import React from 'react';
import { User } from '../api/users/user';
import { DEFAULT_USERS } from '../api/constants';

const UserContextProvider = React.createContext<
  [User[], React.Dispatch<React.SetStateAction<User[]>>] | undefined
>(undefined);

export function UserProvider({ children }: { children: React.ReactNode }) {
  const [users, setUsers] = React.useState<User[]>(DEFAULT_USERS);
  return (
    <UserContextProvider.Provider value={[users, setUsers]}>
      {children}
    </UserContextProvider.Provider>
  );
}

export function useUserProvider() {
  const context = React.useContext(UserContextProvider);
  if (context === undefined) {
    throw new Error('useUserProvider must be used within a UserProvider');
  }
  return context;
}
