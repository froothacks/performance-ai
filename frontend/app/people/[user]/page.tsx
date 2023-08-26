import { getCategory } from '#/app/api/categories/getCategories';
import { SkeletonCard } from '#/ui/skeleton-card';

const PerformanceSourceCard = () => (
  <div className="space-y-4">
    <h1 className="text-xl font-medium text-gray-400/80">QUERY</h1>

    <div className="grid grid-cols-1 gap-6">
      {Array.from({ length: 3 }).map((_, i) => (
        <Boundary labels={[`Evidence ${i + 1}`]}>
          <SkeletonCard key={i} />
          <ExternalLink href="/">Slack</ExternalLink>
        </Boundary>
      ))}
    </div>
  </div>
);

export default async function Page({ params }: { params: { user: string } }) {
  // const previousQueries = await getCategory({ slug: params.user });

  return (
    <div className="mb-6 space-y-9 rounded-lg bg-black p-3.5 lg:p-6">
      <PerformanceSourceCard />
    </div>
  );
}

import { ExternalLink } from '#/ui/external-link';
import { Boundary } from '#/ui/boundary';

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
