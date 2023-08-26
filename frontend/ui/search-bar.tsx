'use client';

import React, { Suspense } from 'react';
import { usePathname, useSearchParams } from 'next/navigation';

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

export function SearchBar() {
  const onSubmit = () => {
    // TODO: Make API request
  };

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
