import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { useTheme } from '@/lib/theme'

export function Settings() {
  const { theme, toggleTheme } = useTheme()

  return (
    <div className="mx-auto max-w-md space-y-6 p-8">
      <h1 className="text-2xl font-bold">Settings</h1>
      <Card>
        <CardHeader>
          <CardTitle>Appearance</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="mb-4 text-sm text-[var(--color-muted-foreground)]">
            Current theme: {theme}
          </p>
          <Button onClick={toggleTheme}>Toggle Dark / Light Mode</Button>
        </CardContent>
      </Card>
    </div>
  )
}
