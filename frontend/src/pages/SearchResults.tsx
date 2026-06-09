import { useLocation } from 'react-router-dom'
import { ImageGrid } from '@/components/ImageGrid'
import { Card, CardContent } from '@/components/ui/card'

interface SearchResult {
  matches: Array<{ image_id: number; image_url: string; similarity: number }>
  match_count: number
  search_time_ms: number
  threshold: number
}

export function SearchResults() {
  const location = useLocation()
  const results = location.state?.results as SearchResult | undefined

  if (!results) {
    return <div className="p-8 text-center text-[var(--color-muted-foreground)]">No search results. Run a search first.</div>
  }

  const images = results.matches.map((m) => ({
    id: m.image_id,
    image_url: m.image_url,
    filename: `${(m.similarity * 100).toFixed(0)}% match`,
  }))

  return (
    <div className="mx-auto max-w-7xl space-y-6 p-4 md:p-8">
      <h1 className="text-2xl font-bold">Search Results</h1>
      <div className="grid gap-4 sm:grid-cols-3">
        <Card>
          <CardContent className="pt-6">
            <p className="text-3xl font-bold">{results.match_count}</p>
            <p className="text-sm text-[var(--color-muted-foreground)]">Matches found</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <p className="text-3xl font-bold">{results.search_time_ms}ms</p>
            <p className="text-sm text-[var(--color-muted-foreground)]">Search time</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <p className="text-3xl font-bold">{(results.threshold * 100).toFixed(0)}%</p>
            <p className="text-sm text-[var(--color-muted-foreground)]">Similarity threshold</p>
          </CardContent>
        </Card>
      </div>
      <ImageGrid images={images} />
    </div>
  )
}
