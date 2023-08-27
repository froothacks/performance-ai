'use client';

import { SkeletonCard } from '#/ui/skeleton-card';

const PerformanceSourceCard = ({ sources }: { sources: Sources }) => (
  <div className="space-y-4">
    <h1 className="mb-6 text-xl font-medium text-gray-400">{sources.query}</h1>

    <div className="grid grid-cols-1 gap-6">
      {sources.threads.length
        ? sources.threads.map((source, i) => (
            <Boundary
              size="small"
              labels={[`Thread ${source.thread_id}`]}
              key={i}
            >
              <p className="mb-4 text-sm font-medium text-gray-400">
                {source.summarized}
              </p>
              <ExternalLink href={source.thread_link}>Slack</ExternalLink>
            </Boundary>
          ))
        : 'Nothing found. Try another search.'}
    </div>
  </div>
);

const SearchIconSVG = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    fill="none"
    viewBox="0 0 24 24"
    strokeWidth={1.5}
    stroke="currentColor"
    className="h-5 w-5"
  >
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"
    />
  </svg>
);

export function SearchBar({
  onSubmit,
}: {
  onSubmit: (e: React.FormEvent<HTMLFormElement>) => void;
}) {
  return (
    <form
      className="flex items-center gap-x-2 p-3.5 lg:px-5 lg:py-3"
      onSubmit={onSubmit}
    >
      <div className="text-gray-600">
        <SearchIconSVG />
      </div>
      <input
        type="text"
        id="search"
        className="relative w-full border-black bg-black py-0 text-sm text-gray-500 focus:border-black focus:ring-black"
        placeholder="Search"
        required
      />
      <div className="flex gap-x-1 text-sm font-medium"></div>
    </form>
  );
}

export default function Page({ params }: { params: { user: string } }) {
  const [users] = useUserProvider();
  const user = users.filter((u) => u.name === params.user)[0];
  const [sourceMap, saveSourceMap] = useSourceProvider();
  const sourcesList: SourcesList = sourceMap?.[user.id] ?? [];

  const onSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const prompt = e.target['search'].value;
    console.log({ prompt });
    const sources = await generateSources(user.id, prompt);
    console.log({ sources });
    // saveSourceMap({ ...sourceMap, [user.id]: [...sourcesList, sources] });
    // console.log({ answer: sourceMap?.[user.id] });
    // Save to sources
    // if (sources.threads.length === 0) {
    //   return;
    // }
    saveSourceMap({
      ...sourceMap,
      [user.id]: [{ query: prompt, threads: sources.threads }, ...sourcesList],
    });
  };

  // console.log({ user });
  return (
    <>
      <div className="bg-vc-border-gradient rounded-lg p-px shadow-lg shadow-black/20">
        <div className="rounded-lg bg-black">
          <SearchBar onSubmit={onSubmit} />
        </div>
      </div>
      {sourcesList.map((sources, i) => (
        <div
          className="mb-6 space-y-9 rounded-lg bg-black p-3.5 lg:p-6"
          key={i}
        >
          <PerformanceSourceCard sources={sources} />
        </div>
      ))}
    </>
  );
}

import { ExternalLink } from '#/ui/external-link';
import { Boundary } from '#/ui/boundary';
import { useEffect, useState } from 'react';
import { User } from '#/app/api/users/user';
import { useUserProvider } from '#/app/contexts/user-context';
import { useSourceProvider } from '#/app/contexts/source-context';
import { Source, Sources, SourcesList } from '#/app/api/sources/source';
import { generateSources } from '#/app/api/sources/getSources';

// export default function Page() {
//   return (
//     <div className="prose prose-sm prose-invert max-w-none">
//       <h1 className="text-xl font-bold">Layouts</h1>

//       <ul>
//         <li>
//           A layout is UI that is shared between multiple pages. On navigation,
//           layouts preserve state, remain interactive, and do not re-render. Two
//           or more layouts can also be nested.
//         </li>
//         <li>Try navigating between categories and sub categories.</li>
//       </ul>

//       <div className="flex gap-2">
//         {/* TODO: Pass down slack link */}
//         <ExternalLink href="/">
//           Slack
//         </ExternalLink>
//       </div>
//     </div>
//   );
// }
