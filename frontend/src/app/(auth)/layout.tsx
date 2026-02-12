import { Card } from "@/components/ui/Card";

export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen items-center justify-center px-4">
      <Card className="w-full max-w-md">
        {children}
      </Card>
    </div>
  );
}
