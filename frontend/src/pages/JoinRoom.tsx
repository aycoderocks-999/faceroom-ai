import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { useToast } from '@/components/ui/toast'
import api from '@/lib/api'

export function JoinRoom() {
  const [code, setCode] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const { toast } = useToast()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    try {
      const { data } = await api.post('/rooms/join', { room_code: code })
      toast({ title: 'Joined room', description: data.room_name })
      navigate(`/rooms/${data.id}`)
    } catch {
      toast({ title: 'Room not found', variant: 'destructive' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mx-auto max-w-md p-8">
      <Card>
        <CardHeader>
          <CardTitle>Join a Room</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="code">Room Code</Label>
              <Input id="code" value={code} onChange={(e) => setCode(e.target.value)} placeholder="ROOM-ABX72Z" required />
            </div>
            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? 'Joining...' : 'Join Room'}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
