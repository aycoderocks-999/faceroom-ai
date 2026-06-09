import { useNavigate, useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { FaceCard } from '@/components/FaceCard'
import { Skeleton } from '@/components/ui/skeleton'
import api from '@/lib/api'

export function ClusterGallery() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()

  const { data: clusters, isLoading } = useQuery({
    queryKey: ['room-clusters', id],
    queryFn: () => api.get(`/rooms/${id}/clusters`).then((r) => r.data),
    enabled: !!id,
  })

  return (
    <div className="mx-auto max-w-7xl space-y-6 p-4 md:p-8">
      <h1 className="text-2xl font-bold">People</h1>
      {isLoading ? (
        <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6">
          {Array.from({ length: 6 }).map((_, i) => <Skeleton key={i} className="aspect-square" />)}
        </div>
      ) : (
        <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6">
          {clusters?.map((c: Parameters<typeof FaceCard>[0]) => (
            <FaceCard
              key={c.id}
              {...c}
              onClick={() => navigate(`/clusters/${c.id}`)}
            />
          ))}
        </div>
      )}
    </div>
  )
}
