'use client';

import React from 'react';
import { Sources } from '../api/sources/source';
import { useLocalStorage } from 'usehooks-ts';

const SourceContext = React.createContext<
  [Sources, React.Dispatch<React.SetStateAction<Sources>>] | undefined
>(undefined);

export function SourceProvider({ children }: { children: React.ReactNode }) {
  const [sources, setSources] = useLocalStorage<Sources>('sources', []);

  return (
    <SourceContext.Provider value={[sources, setSources]}>
      {children}
    </SourceContext.Provider>
  );
}

export function useSourceContext() {
  const context = React.useContext(SourceContext);
  if (context === undefined) {
    throw new Error('useSourceContext must be used within a SourceProvider');
  }
  return context;
}
