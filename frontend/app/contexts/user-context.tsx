'use client';

import React from 'react';
import { User } from '../api/users/user';

const DEFAULT_USERS: User[] = [
  {
    id: 'USLACKBOT',
    name: 'slackbot',
    profile_pic: 'https://a.slack-edge.com/80588/img/slackbot_32.png',
  },
  {
    id: 'U05P8LXRC9M',
    name: 'steven.xu1589',
    profile_pic:
      'https://avatars.slack-edge.com/2023-08-26/5805544754466_9eae1a406e26088ec0fc_32.jpg',
  },
  {
    id: 'U05PGHT8VF0',
    name: 'elliotfklein',
    profile_pic:
      'https://avatars.slack-edge.com/2023-08-26/5805151951139_341d57d53e65f00dc362_32.jpg',
  },
  {
    id: 'U05PLBZ0NMT',
    name: 'perfy',
    profile_pic:
      'https://secure.gravatar.com/avatar/3f03549709b0b8c32c1d6edc90e5c0db.jpg?s=32&d=https%3A%2F%2Fa.slack-edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0007-32.png',
  },
  {
    id: 'U05PP7C99PU',
    name: 'advait.maybhate9',
    profile_pic:
      'https://avatars.slack-edge.com/2023-08-26/5805154815971_3eb134f902f4f4c4e1fd_32.jpg',
  },
  {
    id: 'U05PRUP0Y68',
    name: 'advait',
    profile_pic:
      'https://avatars.slack-edge.com/2023-08-26/5807978041172_7cdf473ed1827aa92272_32.jpg',
  },
  {
    id: 'U05Q25AD9QR',
    name: 'advait429',
    profile_pic:
      'https://avatars.slack-edge.com/2023-08-26/5818184355121_84db3b6e7267485a65fc_32.jpg',
  },
  {
    id: 'U05Q29693RP',
    name: 'john_miller',
    profile_pic:
      'https://secure.gravatar.com/avatar/6412a7e41dc8b69a1999867f3a4c7ef2.jpg?s=32&d=https%3A%2F%2Fa.slack-edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0021-32.png',
  },
  {
    id: 'U05QCU28RQQ',
    name: 'acwangpython',
    profile_pic:
      'https://avatars.slack-edge.com/2023-08-26/5807762763780_de8209837dfd14fc41aa_32.png',
  },
];

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
