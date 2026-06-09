import { useAuth } from '@/lib/auth'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export function Profile() {
  const { user } = useAuth()

  return (
    <div className="mx-auto max-w-md p-8">
      <Card>
        <CardHeader>
          <CardTitle>Profile</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2">
          <p><span className="text-[var(--color-muted-foreground)]">Username:</span> {user?.username}</p>
          <p><span className="text-[var(--color-muted-foreground)]">Email:</span> {user?.email}</p>
          <p><span className="text-[var(--color-muted-foreground)]">Role:</span> {user?.role}</p>
        </CardContent>
      </Card>
    </div>
  )
}
