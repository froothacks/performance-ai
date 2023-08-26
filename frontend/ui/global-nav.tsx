'use client';

import { type User } from '#/lib/demos';
import { NextLogo } from '#/ui/next-logo';
import Link from 'next/link';
import { useSelectedLayoutSegment } from 'next/navigation';
import { MenuAlt2Icon, XIcon } from '@heroicons/react/solid';
import clsx from 'clsx';
import { useState } from 'react';
import TeamCard from './team-card';

const users: { name: string }[] = [
  {
    name: 'Advait Maybhate',
  },
  {
    name: 'Elliot Klein',
  },
  {
    name: 'Terrorist AI',
  },
  {
    name: 'Palantir AI',
  },
  {
    name: 'John',
  },
  {
    name: 'Sarah',
  },
  {
    name: 'David',
  },
  {
    name: 'Jessica',
  },
];

const nameToSlug = (name: string) => name.toLowerCase().split(' ').join('-');

export function GlobalNav() {
  const [isOpen, setIsOpen] = useState(false);
  const close = () => setIsOpen(false);

  return (
    <div className="fixed top-0 z-10 flex w-full flex-col border-b border-gray-800 bg-black lg:bottom-0 lg:z-auto lg:w-72 lg:border-b-0 lg:border-r lg:border-gray-800">
      <div className="flex h-14 items-center px-4 py-4 lg:h-auto">
        <Link
          href="/"
          className="group flex w-full items-center gap-x-2.5"
          onClick={close}
        >
          <div className="h-7 w-7 rounded-full border border-white/30 group-hover:border-white/50">
            <NextLogo />
          </div>

          <h3 className="font-semibold tracking-wide text-gray-400 group-hover:text-gray-50">
            Performance AI
          </h3>
        </Link>
      </div>
      <button
        type="button"
        className="group absolute right-0 top-0 flex h-14 items-center gap-x-2 px-4 lg:hidden"
        onClick={() => setIsOpen(!isOpen)}
      >
        <div className="font-medium text-gray-100 group-hover:text-gray-400">
          Menu
        </div>
        {isOpen ? (
          <XIcon className="block w-6 text-gray-400" />
        ) : (
          <MenuAlt2Icon className="block w-6 text-gray-400" />
        )}
      </button>

      <div
        className={clsx('overflow-y-auto lg:static lg:block', {
          'inst-x-0 fixed bottom-0 top-14 mt-px bg-black': isOpen,
          hidden: !isOpen,
        })}
      >
        <nav className="space-y-1 px-2 pb-24 pt-5">
          <div className="text-md mb-2 px-3 font-semibold uppercase tracking-wider text-gray-400/80">
            <div>People</div>
          </div>
          {/* TODO: Pull users */}
          {users.map((user) => {
            const slug = nameToSlug(user.name);
            return (
              <div key={user.name}>
                <GlobalNavItem key={slug} item={user} close={close} />
              </div>
            );
          })}
        </nav>

        <TeamCard className="absolute hidden sm:block" />
      </div>
    </div>
  );
}

function GlobalNavItem({
  item,
  close,
}: {
  item: User;
  close: () => false | void;
}) {
  const segment = useSelectedLayoutSegment();
  console.log({ segment });
  const slug = nameToSlug(item.name);
  const isActive = slug === segment;
  const route = `/people/${slug}`;

  return (
    <Link
      onClick={close}
      href={route}
      className={clsx(
        'block rounded-md px-3 py-2 text-sm font-medium hover:text-gray-300',
        {
          'text-gray-400 hover:bg-gray-800': !isActive,
          'text-white': isActive,
        },
      )}
    >
      {item.name}
    </Link>
  );
}
