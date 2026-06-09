import { Card } from '@/components/ui/card'
import { Skeleton } from '@/components/ui/skeleton'

interface ImageItem {
  id: number
  image_url: string
  filename?: string
  processing_status?: string
}

interface ImageGridProps {
  images: ImageItem[]
  loading?: boolean
  onImageClick?: (id: number) => void
}

export function ImageGrid({ images, loading, onImageClick }: ImageGridProps) {
  if (loading) {
    return (
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5">
        {Array.from({ length: 10 }).map((_, i) => (
          <Skeleton key={i} className="aspect-square rounded-lg" />
        ))}
      </div>
    )
  }

  if (!images.length) {
    return (
      <div className="flex flex-col items-center justify-center py-16 text-[var(--color-muted-foreground)]">
        <p>No images yet. Upload some photos to get started.</p>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5">
      {images.map((img) => (
        <Card
          key={img.id}
          className="group relative aspect-square overflow-hidden cursor-pointer p-0"
          onClick={() => onImageClick?.(img.id)}
        >
          <img
            src={img.image_url}
            alt={img.filename || 'Event photo'}
            className="h-full w-full object-cover transition-transform group-hover:scale-105"
            loading="lazy"
          />
          {img.processing_status && img.processing_status !== 'completed' && (
            <div className="absolute inset-0 flex items-center justify-center bg-black/50 text-white text-xs">
              {img.processing_status}
            </div>
          )}
        </Card>
      ))}
    </div>
  )
}
