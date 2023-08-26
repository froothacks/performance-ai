import '#/styles/globals.css';
import TeamCard from '#/ui/team-card';
import { GlobalNav } from '#/ui/global-nav';
import { Metadata } from 'next';
import { UserProvider } from './contexts/user-context';
import { SourceProvider } from './contexts/source-context';

export const metadata: Metadata = {
  title: {
    default: 'Next.js App Router',
    template: '%s | Next.js App Router',
  },
  description:
    'A playground to explore new Next.js App Router features such as nested layouts, instant loading states, streaming, and component level data fetching.',
  openGraph: {
    title: 'Next.js App Router Playground',
    description:
      'A playground to explore new Next.js App Router features such as nested layouts, instant loading states, streaming, and component level data fetching.',
    images: [`/api/og?title=Next.js App Router`],
  },
  twitter: {
    card: 'summary_large_image',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="[color-scheme:dark]">
      <body className="bg-gray-1100 overflow-y-scroll bg-[url('/grid.svg')] pb-36">
        <UserProvider>
          <SourceProvider>
            <GlobalNav />
            <div className="lg:pl-72">
              <div className="mx-auto max-w-4xl space-y-8 px-2 pt-20 lg:px-8 lg:py-8">
                {children}
                <TeamCard className="fixed sm:hidden" />
              </div>
            </div>
          </SourceProvider>
        </UserProvider>
      </body>
    </html>
  );
}
