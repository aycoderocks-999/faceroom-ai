import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { Image, Plus, Search, Users } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Skeleton } from '@/components/ui/skeleton'
import { RoomCard } from '@/components/RoomCard'
import api from '@/lib/api'

export function Dashboard() {
  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: () => api.get('/dashboard/stats').then((r) => r.data),
  })

  const { data: rooms, isLoading: roomsLoading } = useQuery({
    queryKey: ['rooms'],
    queryFn: () => api.get('/rooms').then((r) => r.data),
  })

  const statCards = [
    { label: 'Rooms', value: stats?.total_rooms ?? 0, icon: Users },
    { label: 'Images', value: stats?.total_images ?? 0, icon: Image },
    { label: 'Faces', value: stats?.total_faces ?? 0, icon: Users },
    { label: 'Clusters', value: stats?.total_clusters ?? 0, icon: Search },
  ]

  return (
    <div className="mx-auto max-w-7xl space-y-8 p-4 md:p-8">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <div className="flex gap-2">
          <Link to="/rooms/create">
            <Button><Plus className="h-4 w-4" /> Create Room</Button>
          </Link>
          <Link to="/rooms/join">
            <Button variant="outline">Join Room</Button>
          </Link>
        </div>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {statCards.map(({ label, value, icon: Icon }) => (
          <Card key={label}>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-[var(--color-muted-foreground)]">{label}</CardTitle>
              <Icon className="h-4 w-4 text-[var(--color-muted-foreground)]" />
            </CardHeader>
            <CardContent>
              {statsLoading ? <Skeleton className="h-8 w-16" /> : <p className="text-3xl font-bold">{value}</p>}
            </CardContent>
          </Card>
        ))}
      </div>

      <section>
        <h2 className="mb-4 text-xl font-semibold">Your Rooms</h2>
        {roomsLoading ? (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {Array.from({ length: 3 }).map((_, i) => <Skeleton key={i} className="h-32" />)}
          </div>
        ) : (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {rooms?.map((room: Parameters<typeof RoomCard>[0]) => (
              <RoomCard key={room.id} {...room} />
            ))}
          </div>
        )}
      </section>

      {stats?.recent_uploads?.length > 0 && (
        <section>
          <h2 className="mb-4 text-xl font-semibold">Recent Uploads</h2>
          <div className="flex gap-3 overflow-x-auto pb-2">
            {stats.recent_uploads.map((img: { id: number; image_url: string }) => (
              <img key={img.id} src={img.image_url} alt="" className="h-24 w-24 flex-shrink-0 rounded-lg object-cover" />
            ))}
          </div>
        </section>
      )}
    </div>
  )
}
