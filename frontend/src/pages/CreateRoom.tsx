import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { useToast } from '@/components/ui/toast'
import api from '@/lib/api'

export function CreateRoom() {
  const [name, setName] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const { toast } = useToast()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    try {
      const { data } = await api.post('/rooms/create', { room_name: name })
      toast({ title: 'Room created', description: `Code: ${data.room_code}` })
      navigate(`/rooms/${data.id}`)
    } catch {
      toast({ title: 'Failed to create room', variant: 'destructive' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mx-auto max-w-md p-8">
      <Card>
        <CardHeader>
          <CardTitle>Create a Room</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="name">Room Name</Label>
              <Input id="name" value={name} onChange={(e) => setName(e.target.value)} placeholder="Wedding 2026" required />
            </div>
            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? 'Creating...' : 'Create Room'}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
