export default function DashboardLoading() {
  return (
    <div className="space-y-6">
      <div className="h-40 animate-pulse rounded-lg bg-gray-200" />
      <div className="space-y-2">
        <div className="h-6 w-32 animate-pulse rounded bg-gray-200" />
        <div className="h-20 animate-pulse rounded-lg bg-gray-200" />
        <div className="h-20 animate-pulse rounded-lg bg-gray-200" />
        <div className="h-20 animate-pulse rounded-lg bg-gray-200" />
      </div>
    </div>
  );
}
