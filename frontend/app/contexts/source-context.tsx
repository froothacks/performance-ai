'use client';

import React from 'react';
import { SourceMap } from '../api/sources/source';
import { useLocalStorage } from 'usehooks-ts';

const SourceContext = React.createContext<
  [SourceMap, React.Dispatch<React.SetStateAction<SourceMap>>] | undefined
>(undefined);

export function SourceProvider({ children }: { children: React.ReactNode }) {
  const [sourceMap, setSourceMap] = useLocalStorage<SourceMap>('sources', {});

  return (
    <SourceContext.Provider value={[sourceMap, setSourceMap]}>
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
