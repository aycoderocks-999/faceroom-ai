import { useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { SearchPanel } from '@/components/SearchPanel'
import { useToast } from '@/components/ui/toast'
import api from '@/lib/api'

export function FaceSearch() {
  const { id } = useParams<{ id: string }>()
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const { toast } = useToast()

  const handleSearch = async (file: File) => {
    setLoading(true)
    const formData = new FormData()
    formData.append('room_id', id!)
    formData.append('query_image', file)

    try {
      const { data } = await api.post('/search/face', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      navigate(`/rooms/${id}/search/results`, { state: { results: data } })
    } catch {
      toast({ title: 'Search failed', description: 'No face detected or server error', variant: 'destructive' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mx-auto max-w-2xl p-4 md:p-8">
      <h1 className="mb-6 text-2xl font-bold">Find Me</h1>
      <SearchPanel onSearch={handleSearch} loading={loading} />
    </div>
  )
}
