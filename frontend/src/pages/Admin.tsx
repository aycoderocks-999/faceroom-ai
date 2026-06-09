import { useQuery } from '@tanstack/react-query'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Skeleton } from '@/components/ui/skeleton'
import api from '@/lib/api'

export function Admin() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['admin-stats'],
    queryFn: () => api.get('/admin/stats').then((r) => r.data),
    retry: false,
  })

  if (error) {
    return <div className="p-8 text-center text-[var(--color-muted-foreground)]">Admin access required.</div>
  }

  return (
    <div className="mx-auto max-w-7xl space-y-6 p-8">
      <h1 className="text-2xl font-bold">Admin Dashboard</h1>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
        {['users', 'rooms', 'images', 'faces', 'failed_tasks'].map((key) => (
          <Card key={key}>
            <CardHeader>
              <CardTitle className="text-sm capitalize">{key.replace('_', ' ')}</CardTitle>
            </CardHeader>
            <CardContent>
              {isLoading ? <Skeleton className="h-8 w-12" /> : <p className="text-3xl font-bold">{data?.[key] ?? 0}</p>}
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
