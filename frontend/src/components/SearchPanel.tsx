import { useRef, useState } from 'react'
import { Search, Upload } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

interface SearchPanelProps {
  onSearch: (file: File) => void
  loading?: boolean
}

export function SearchPanel({ onSearch, loading }: SearchPanelProps) {
  const inputRef = useRef<HTMLInputElement>(null)
  const [preview, setPreview] = useState<string | null>(null)

  const handleFile = (file: File) => {
    setPreview(URL.createObjectURL(file))
    onSearch(file)
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Search className="h-5 w-5" />
          Find Me — Face Search
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <p className="text-sm text-[var(--color-muted-foreground)]">
          Upload a selfie to find every photo containing that person in this room.
        </p>
        <div
          className="flex flex-col items-center rounded-lg border-2 border-dashed border-[var(--color-border)] p-8"
          onDragOver={(e) => e.preventDefault()}
          onDrop={(e) => {
            e.preventDefault()
            const file = e.dataTransfer.files[0]
            if (file) handleFile(file)
          }}
        >
          {preview ? (
            <img src={preview} alt="Query" className="mb-4 h-32 w-32 rounded-full object-cover" />
          ) : (
            <Upload className="mb-4 h-12 w-12 text-[var(--color-muted-foreground)]" />
          )}
          <input
            ref={inputRef}
            type="file"
            accept="image/*"
            className="hidden"
            onChange={(e) => {
              const file = e.target.files?.[0]
              if (file) handleFile(file)
            }}
          />
          <Button variant="outline" onClick={() => inputRef.current?.click()} disabled={loading}>
            {loading ? 'Searching...' : 'Upload Selfie'}
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}
