import { Link, useNavigate } from 'react-router-dom'
import { Camera, LogOut, Moon, Sun, User } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { useAuth } from '@/lib/auth'
import { useTheme } from '@/lib/theme'

export function Navbar() {
  const { isAuthenticated, logout } = useAuth()
  const { theme, toggleTheme } = useTheme()
  const navigate = useNavigate()

  return (
    <header className="sticky top-0 z-40 border-b border-[var(--color-border)] bg-[var(--color-background)]/80 backdrop-blur">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4">
        <Link to="/" className="flex items-center gap-2 font-bold text-lg">
          <Camera className="h-6 w-6 text-[var(--color-primary)]" />
          FaceRoom AI
        </Link>
        <nav className="flex items-center gap-2">
          <Button variant="ghost" size="icon" onClick={toggleTheme}>
            {theme === 'dark' ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
          </Button>
          {isAuthenticated ? (
            <>
              <Link to="/dashboard">
                <Button variant="ghost">Dashboard</Button>
              </Link>
              <Link to="/profile">
                <Button variant="ghost" size="icon">
                  <User className="h-5 w-5" />
                </Button>
              </Link>
              <Button
                variant="outline"
                size="sm"
                onClick={() => {
                  logout()
                  navigate('/login')
                }}
              >
                <LogOut className="h-4 w-4" />
                Logout
              </Button>
            </>
          ) : (
            <>
              <Link to="/login">
                <Button variant="ghost">Login</Button>
              </Link>
              <Link to="/register">
                <Button>Get Started</Button>
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  )
}
