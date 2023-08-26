import { VercelLogo } from '#/ui/vercel-logo';

export default function TeamCard({ className }: { className: string }) {
  return (
    <div
      className={`${className} bg-vc-border-gradient inset-x-0 bottom-3 mx-3 rounded-lg p-px shadow-lg shadow-black/20`}
    >
      <div className="flex flex-col justify-between space-y-2 rounded-lg bg-black p-3.5 lg:px-5 lg:py-3">
        <div className="flex items-center gap-x-1.5">
          <div className="text-sm text-gray-400">By</div>
          <a href="https://vercel.com" title="Vercel">
            <div className="w-16 text-gray-100 hover:text-gray-50">
              Froothacks
            </div>
          </a>
        </div>

        <div className="text-sm text-gray-400">Advait Maybhate</div>
        <div className="text-sm text-gray-400">Andrew Wang</div>
        <div className="text-sm text-gray-400">Elliot Klein</div>
        <div className="text-sm text-gray-400">Steven Xu</div>
      </div>
    </div>
  );
}
