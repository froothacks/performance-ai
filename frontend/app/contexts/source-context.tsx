'use client';

import React from 'react';
import { SourcesMap } from '../api/sources/source';
import { useLocalStorage } from 'usehooks-ts';
import { DEFAULT_SOURCE_MAP } from '../api/constants';

const SourceContext = React.createContext<
  [SourcesMap, React.Dispatch<React.SetStateAction<SourcesMap>>] | undefined
>(undefined);

export function SourceProvider({ children }: { children: React.ReactNode }) {
  const [sourcesMap, setSourcesMap] = useLocalStorage<SourcesMap>(
    'sources',
    DEFAULT_SOURCE_MAP,
  );

  return (
    <SourceContext.Provider value={[sourcesMap, setSourcesMap]}>
      {children}
    </SourceContext.Provider>
  );
}

export function useSourceProvider() {
  const context = React.useContext(SourceContext);
  if (context === undefined) {
    throw new Error('useSourceContext must be used within a SourceProvider');
  }
  return context;
}
