import { createContext, useCallback, useContext, useState, type ReactNode } from 'react'
import { X } from 'lucide-react'
import { cn } from '@/lib/utils'

interface Toast {
  id: string
  title: string
  description?: string
  variant?: 'default' | 'destructive'
}

interface ToastContextType {
  toast: (t: Omit<Toast, 'id'>) => void
}

const ToastContext = createContext<ToastContextType | null>(null)

export function ToastProvider({ children }: { children: ReactNode }) {
  const [toasts, setToasts] = useState<Toast[]>([])

  const toast = useCallback((t: Omit<Toast, 'id'>) => {
    const id = Math.random().toString(36).slice(2)
    setToasts((prev) => [...prev, { ...t, id }])
    setTimeout(() => setToasts((prev) => prev.filter((x) => x.id !== id)), 4000)
  }, [])

  const dismiss = (id: string) => setToasts((prev) => prev.filter((x) => x.id !== id))

  return (
    <ToastContext.Provider value={{ toast }}>
      {children}
      <div className="fixed bottom-4 right-4 z-50 flex flex-col gap-2">
        {toasts.map((t) => (
          <div
            key={t.id}
            className={cn(
              'flex w-80 items-start gap-3 rounded-lg border p-4 shadow-lg',
              t.variant === 'destructive'
                ? 'border-[var(--color-destructive)] bg-[var(--color-card)]'
                : 'border-[var(--color-border)] bg-[var(--color-card)]'
            )}
          >
            <div className="flex-1">
              <p className="font-medium">{t.title}</p>
              {t.description && <p className="text-sm text-[var(--color-muted-foreground)]">{t.description}</p>}
            </div>
            <button onClick={() => dismiss(t.id)} className="opacity-70 hover:opacity-100">
              <X className="h-4 w-4" />
            </button>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  )
}

export function useToast() {
  const ctx = useContext(ToastContext)
  if (!ctx) throw new Error('useToast must be used within ToastProvider')
  return ctx
}
