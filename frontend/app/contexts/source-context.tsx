'use client';

import React, { useState } from 'react';
import { SourcesMap } from '../api/sources/source';
import { useLocalStorage } from 'usehooks-ts';

const SourceContext = React.createContext<
  [SourcesMap, React.Dispatch<React.SetStateAction<SourcesMap>>] | undefined
>(undefined);

export function SourceProvider({ children }: { children: React.ReactNode }) {
  const [sourcesMap, setSourcesMap] = useState<SourcesMap>({} as SourcesMap);

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
