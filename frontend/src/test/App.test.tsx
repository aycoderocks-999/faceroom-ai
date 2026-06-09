import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Landing } from '@/pages/Landing'
import { ThemeProvider } from '@/lib/theme'

describe('Landing page', () => {
  it('renders hero heading', () => {
    const queryClient = new QueryClient()
    render(
      <QueryClientProvider client={queryClient}>
        <ThemeProvider>
          <BrowserRouter>
            <Landing />
          </BrowserRouter>
        </ThemeProvider>
      </QueryClientProvider>
    )
    expect(screen.getByText(/Find yourself in every/i)).toBeInTheDocument()
  })
})
