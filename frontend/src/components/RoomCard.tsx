import { Link } from 'react-router-dom'
import { Images, Users } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

interface RoomCardProps {
  id: number
  room_name: string
  room_code: string
  member_count: number
  image_count: number
  cluster_count: number
}

export function RoomCard({ id, room_name, room_code, member_count, image_count, cluster_count }: RoomCardProps) {
  return (
    <Link to={`/rooms/${id}`}>
      <Card className="transition-shadow hover:shadow-md cursor-pointer h-full">
        <CardHeader>
          <CardTitle className="truncate">{room_name}</CardTitle>
          <CardDescription className="font-mono">{room_code}</CardDescription>
        </CardHeader>
        <CardContent className="flex gap-4 text-sm text-[var(--color-muted-foreground)]">
          <span className="flex items-center gap-1">
            <Users className="h-4 w-4" /> {member_count}
          </span>
          <span className="flex items-center gap-1">
            <Images className="h-4 w-4" /> {image_count}
          </span>
          <span>{cluster_count} people</span>
        </CardContent>
      </Card>
    </Link>
  )
}
