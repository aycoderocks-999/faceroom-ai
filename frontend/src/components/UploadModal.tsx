import { useCallback, useState } from 'react'
import { Upload, X } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { useToast } from '@/components/ui/toast'
import api from '@/lib/api'

interface UploadModalProps {
  roomId: number
  open: boolean
  onClose: () => void
  onSuccess?: () => void
}

export function UploadModal({ roomId, open, onClose, onSuccess }: UploadModalProps) {
  const [files, setFiles] = useState<File[]>([])
  const [uploading, setUploading] = useState(false)
  const [dragOver, setDragOver] = useState(false)
  const { toast } = useToast()

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setDragOver(false)
    const dropped = Array.from(e.dataTransfer.files).filter((f) => f.type.startsWith('image/'))
    setFiles((prev) => [...prev, ...dropped])
  }, [])

  const handleUpload = async () => {
    if (!files.length) return
    setUploading(true)
    const formData = new FormData()
    formData.append('room_id', String(roomId))
    files.forEach((f) => formData.append('files', f))

    try {
      await api.post('/images/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      toast({ title: 'Upload started', description: `${files.length} image(s) queued for processing.` })
      setFiles([])
      onSuccess?.()
      onClose()
    } catch {
      toast({ title: 'Upload failed', variant: 'destructive' })
    } finally {
      setUploading(false)
    }
  }

  if (!open) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
      <div className="w-full max-w-lg rounded-lg border border-[var(--color-border)] bg-[var(--color-card)] p-6 shadow-xl">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-lg font-semibold">Upload Photos</h2>
          <button onClick={onClose}>
            <X className="h-5 w-5" />
          </button>
        </div>

        <div
          onDragOver={(e) => { e.preventDefault(); setDragOver(true) }}
          onDragLeave={() => setDragOver(false)}
          onDrop={handleDrop}
          className={`flex flex-col items-center justify-center rounded-lg border-2 border-dashed p-8 transition-colors ${
            dragOver ? 'border-[var(--color-primary)] bg-[var(--color-accent)]' : 'border-[var(--color-border)]'
          }`}
        >
          <Upload className="mb-2 h-10 w-10 text-[var(--color-muted-foreground)]" />
          <p className="mb-2 text-sm text-[var(--color-muted-foreground)]">Drag & drop images here</p>
          <label>
            <input
              type="file"
              multiple
              accept="image/jpeg,image/png,image/jpg"
              className="hidden"
              onChange={(e) => setFiles((prev) => [...prev, ...Array.from(e.target.files || [])])}
            />
            <Button variant="outline" size="sm" asChild>
              <span>Browse files</span>
            </Button>
          </label>
        </div>

        {files.length > 0 && (
          <div className="mt-4 max-h-32 overflow-y-auto text-sm">
            {files.map((f, i) => (
              <div key={i} className="flex justify-between py-1">
                <span className="truncate">{f.name}</span>
                <button onClick={() => setFiles((prev) => prev.filter((_, j) => j !== i))}>
                  <X className="h-4 w-4" />
                </button>
              </div>
            ))}
          </div>
        )}

        <div className="mt-4 flex justify-end gap-2">
          <Button variant="outline" onClick={onClose}>Cancel</Button>
          <Button onClick={handleUpload} disabled={!files.length || uploading}>
            {uploading ? 'Uploading...' : `Upload ${files.length || ''} file(s)`}
          </Button>
        </div>
      </div>
    </div>
  )
}
