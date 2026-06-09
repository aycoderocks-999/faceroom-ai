import { User } from 'lucide-react'
import { Card, CardContent } from '@/components/ui/card'

interface FaceCardProps {
  id: number
  name: string
  representative_face_url?: string | null
  face_count: number
  image_count: number
  onClick?: () => void
}

export function FaceCard({ name, representative_face_url, face_count, image_count, onClick }: FaceCardProps) {
  return (
    <Card className="cursor-pointer overflow-hidden transition-shadow hover:shadow-md" onClick={onClick}>
      <div className="aspect-square bg-[var(--color-muted)] flex items-center justify-center overflow-hidden">
        {representative_face_url ? (
          <img src={representative_face_url} alt={name} className="h-full w-full object-cover" loading="lazy" />
        ) : (
          <User className="h-16 w-16 text-[var(--color-muted-foreground)]" />
        )}
      </div>
      <CardContent className="p-3">
        <p className="font-medium truncate">{name}</p>
        <p className="text-xs text-[var(--color-muted-foreground)]">
          {image_count} photos · {face_count} faces
        </p>
      </CardContent>
    </Card>
  )
}
