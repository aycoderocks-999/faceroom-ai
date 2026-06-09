import { useState } from 'react'
import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { Button } from '@/components/ui/button'
import { ImageGrid } from '@/components/ImageGrid'
import { UploadModal } from '@/components/UploadModal'
import api from '@/lib/api'

export function GalleryPage() {
  const { id } = useParams<{ id: string }>()
  const [page, setPage] = useState(1)
  const [uploadOpen, setUploadOpen] = useState(false)

  const { data, isLoading, refetch } = useQuery({
    queryKey: ['room-images', id, page],
    queryFn: () => api.get(`/rooms/${id}/images`, { params: { page, page_size: 20 } }).then((r) => r.data),
    enabled: !!id,
  })

  return (
    <div className="mx-auto max-w-7xl space-y-6 p-4 md:p-8">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Photo Gallery</h1>
        <Button onClick={() => setUploadOpen(true)}>Upload</Button>
      </div>
      <ImageGrid images={data?.items ?? []} loading={isLoading} />
      {data && data.pages > 1 && (
        <div className="flex justify-center gap-2">
          <Button variant="outline" disabled={page <= 1} onClick={() => setPage((p) => p - 1)}>Previous</Button>
          <span className="flex items-center px-4 text-sm">Page {page} of {data.pages}</span>
          <Button variant="outline" disabled={page >= data.pages} onClick={() => setPage((p) => p + 1)}>Next</Button>
        </div>
      )}
      <UploadModal roomId={Number(id)} open={uploadOpen} onClose={() => setUploadOpen(false)} onSuccess={() => refetch()} />
    </div>
  )
}
