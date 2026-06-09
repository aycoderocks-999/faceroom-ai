import { useState } from 'react'
import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { ImageGrid } from '@/components/ImageGrid'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Skeleton } from '@/components/ui/skeleton'
import { useToast } from '@/components/ui/toast'
import api from '@/lib/api'

export function ClusterDetail() {
  const { id } = useParams<{ id: string }>()
  const [name, setName] = useState('')
  const [page, setPage] = useState(1)
  const { toast } = useToast()

  const { data: cluster, isLoading } = useQuery({
    queryKey: ['cluster', id],
    queryFn: () => api.get(`/clusters/${id}`).then((r) => r.data),
    enabled: !!id,
  })

  const { data: images } = useQuery({
    queryKey: ['cluster-images', id, page],
    queryFn: () => api.get(`/clusters/${id}/images`, { params: { page } }).then((r) => r.data),
    enabled: !!id,
  })

  const rename = async () => {
    if (!name.trim()) return
    try {
      await api.patch(`/clusters/${id}`, { name })
      toast({ title: 'Renamed successfully' })
    } catch {
      toast({ title: 'Rename failed', variant: 'destructive' })
    }
  }

  if (isLoading) return <Skeleton className="m-8 h-64" />
  if (!cluster) return <div className="p-8">Cluster not found</div>

  return (
    <div className="mx-auto max-w-7xl space-y-6 p-4 md:p-8">
      <div className="flex flex-wrap items-center gap-4">
        {cluster.representative_face_url && (
          <img src={cluster.representative_face_url} alt="" className="h-20 w-20 rounded-full object-cover" />
        )}
        <div>
          <h1 className="text-2xl font-bold">{cluster.name}</h1>
          <p className="text-sm text-[var(--color-muted-foreground)]">
            {cluster.image_count} photos · {cluster.face_count} faces
          </p>
        </div>
      </div>
      <div className="flex gap-2">
        <Input placeholder="New name" value={name} onChange={(e) => setName(e.target.value)} className="max-w-xs" />
        <Button onClick={rename}>Rename</Button>
        <Button variant="outline" onClick={() => api.patch(`/clusters/${id}`, { mark_unknown: true })}>
          Mark Unknown
        </Button>
      </div>
      <ImageGrid images={images?.items ?? []} />
      {images && images.pages > 1 && (
        <div className="flex justify-center gap-2">
          <Button variant="outline" disabled={page <= 1} onClick={() => setPage((p) => p - 1)}>Previous</Button>
          <Button variant="outline" disabled={page >= images.pages} onClick={() => setPage((p) => p + 1)}>Next</Button>
        </div>
      )}
    </div>
  )
}
