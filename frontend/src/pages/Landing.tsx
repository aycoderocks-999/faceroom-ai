import { Link } from 'react-router-dom'
import { Camera, Search, Users, Zap } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

export function Landing() {
  return (
    <div>
      <section className="mx-auto max-w-7xl px-4 py-20 text-center">
        <h1 className="mb-6 text-4xl font-bold tracking-tight sm:text-6xl">
          Find yourself in every{' '}
          <span className="text-[var(--color-primary)]">event photo</span>
        </h1>
        <p className="mx-auto mb-8 max-w-2xl text-lg text-[var(--color-muted-foreground)]">
          FaceRoom AI automatically detects faces, groups people, and lets you search event photos with a single selfie — like Google Photos for shared events.
        </p>
        <div className="flex justify-center gap-4">
          <Link to="/register">
            <Button size="lg">Get Started Free</Button>
          </Link>
          <Link to="/login">
            <Button size="lg" variant="outline">Sign In</Button>
          </Link>
        </div>
      </section>

      <section className="mx-auto grid max-w-7xl gap-6 px-4 py-12 sm:grid-cols-2 lg:grid-cols-4">
        {[
          { icon: Camera, title: 'Smart Upload', desc: 'Bulk upload with async face processing' },
          { icon: Users, title: 'Auto Grouping', desc: 'DBSCAN clustering groups unknown people' },
          { icon: Search, title: 'Face Search', desc: 'Find all photos of a person with one selfie' },
          { icon: Zap, title: 'Vector Search', desc: 'Sub-2s search powered by Qdrant' },
        ].map(({ icon: Icon, title, desc }) => (
          <Card key={title}>
            <CardHeader>
              <Icon className="mb-2 h-8 w-8 text-[var(--color-primary)]" />
              <CardTitle>{title}</CardTitle>
              <CardDescription>{desc}</CardDescription>
            </CardHeader>
          </Card>
        ))}
      </section>
    </div>
  )
}
