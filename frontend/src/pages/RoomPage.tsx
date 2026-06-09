import { useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { Image, Search, Upload, Users } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Skeleton } from '@/components/ui/skeleton'
import { UploadModal } from '@/components/UploadModal'
import api from '@/lib/api'

export function RoomPage() {
  const { id } = useParams<{ id: string }>()
  const [uploadOpen, setUploadOpen] = useState(false)

  const { data: room, isLoading } = useQuery({
    queryKey: ['room', id],
    queryFn: () => api.get(`/rooms/${id}`).then((r) => r.data),
    enabled: !!id,
  })

  if (isLoading) return <div className="p-8"><Skeleton className="h-64 w-full" /></div>
  if (!room) return <div className="p-8">Room not found</div>

  return (
    <div className="mx-auto max-w-7xl space-y-6 p-4 md:p-8">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold">{room.room_name}</h1>
          <p className="font-mono text-[var(--color-muted-foreground)]">{room.room_code}</p>
        </div>
        <Button onClick={() => setUploadOpen(true)}>
          <Upload className="h-4 w-4" /> Upload
        </Button>
      </div>

      <div className="grid gap-4 sm:grid-cols-3">
        <Link to={`/rooms/${id}/gallery`}>
          <div className="flex items-center gap-4 rounded-lg border p-6 transition-shadow hover:shadow-md">
            <Image className="h-8 w-8 text-[var(--color-primary)]" />
            <div>
              <p className="font-semibold">Photo Gallery</p>
              <p className="text-sm text-[var(--color-muted-foreground)]">{room.image_count} images</p>
            </div>
          </div>
        </Link>
        <Link to={`/rooms/${id}/clusters`}>
          <div className="flex items-center gap-4 rounded-lg border p-6 transition-shadow hover:shadow-md">
            <Users className="h-8 w-8 text-[var(--color-primary)]" />
            <div>
              <p className="font-semibold">People</p>
              <p className="text-sm text-[var(--color-muted-foreground)]">{room.cluster_count} clusters</p>
            </div>
          </div>
        </Link>
        <Link to={`/rooms/${id}/search`}>
          <div className="flex items-center gap-4 rounded-lg border p-6 transition-shadow hover:shadow-md">
            <Search className="h-8 w-8 text-[var(--color-primary)]" />
            <div>
              <p className="font-semibold">Find Me</p>
              <p className="text-sm text-[var(--color-muted-foreground)]">Face search</p>
            </div>
          </div>
        </Link>
      </div>

      <UploadModal roomId={Number(id)} open={uploadOpen} onClose={() => setUploadOpen(false)} />
    </div>
  )
}
