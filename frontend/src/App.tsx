import { BrowserRouter, Route, Routes } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Navbar } from '@/components/layout/Navbar'
import { ProtectedRoute } from '@/components/layout/ProtectedRoute'
import { ToastProvider } from '@/components/ui/toast'
import { AuthProvider } from '@/lib/auth'
import { ThemeProvider } from '@/lib/theme'
import { Admin } from '@/pages/Admin'
import { ClusterDetail } from '@/pages/ClusterDetail'
import { ClusterGallery } from '@/pages/ClusterGallery'
import { CreateRoom } from '@/pages/CreateRoom'
import { Dashboard } from '@/pages/Dashboard'
import { FaceSearch } from '@/pages/FaceSearch'
import { GalleryPage } from '@/pages/GalleryPage'
import { JoinRoom } from '@/pages/JoinRoom'
import { Landing } from '@/pages/Landing'
import { Login } from '@/pages/Login'
import { Profile } from '@/pages/Profile'
import { Register } from '@/pages/Register'
import { RoomPage } from '@/pages/RoomPage'
import { SearchResults } from '@/pages/SearchResults'
import { Settings } from '@/pages/Settings'

const queryClient = new QueryClient({
  defaultOptions: { queries: { staleTime: 30_000, retry: 1 } },
})

function AppLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <Navbar />
      <main>{children}</main>
    </>
  )
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <AuthProvider>
          <ToastProvider>
            <BrowserRouter>
              <AppLayout>
                <Routes>
                  <Route path="/" element={<Landing />} />
                  <Route path="/login" element={<Login />} />
                  <Route path="/register" element={<Register />} />
                  <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
                  <Route path="/rooms/create" element={<ProtectedRoute><CreateRoom /></ProtectedRoute>} />
                  <Route path="/rooms/join" element={<ProtectedRoute><JoinRoom /></ProtectedRoute>} />
                  <Route path="/rooms/:id" element={<ProtectedRoute><RoomPage /></ProtectedRoute>} />
                  <Route path="/rooms/:id/gallery" element={<ProtectedRoute><GalleryPage /></ProtectedRoute>} />
                  <Route path="/rooms/:id/clusters" element={<ProtectedRoute><ClusterGallery /></ProtectedRoute>} />
                  <Route path="/rooms/:id/search" element={<ProtectedRoute><FaceSearch /></ProtectedRoute>} />
                  <Route path="/rooms/:id/search/results" element={<ProtectedRoute><SearchResults /></ProtectedRoute>} />
                  <Route path="/clusters/:id" element={<ProtectedRoute><ClusterDetail /></ProtectedRoute>} />
                  <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
                  <Route path="/settings" element={<ProtectedRoute><Settings /></ProtectedRoute>} />
                  <Route path="/admin" element={<ProtectedRoute><Admin /></ProtectedRoute>} />
                </Routes>
              </AppLayout>
            </BrowserRouter>
          </ToastProvider>
        </AuthProvider>
      </ThemeProvider>
    </QueryClientProvider>
  )
}
