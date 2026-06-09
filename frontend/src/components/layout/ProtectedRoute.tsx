import { Navigate } from 'react-router-dom'
import { useAuth } from '@/lib/auth'
import { Skeleton } from '@/components/ui/skeleton'

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, loading } = useAuth()

  if (loading) {
    return (
      <div className="mx-auto max-w-7xl space-y-4 p-8">
        <Skeleton className="h-8 w-48" />
        <Skeleton className="h-64 w-full" />
      </div>
    )
  }

  if (!isAuthenticated) return <Navigate to="/login" replace />
  return <>{children}</>
}
