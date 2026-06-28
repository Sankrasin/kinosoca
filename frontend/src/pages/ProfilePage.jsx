import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { LogOut } from 'lucide-react'
import Loader from '../components/common/Loader'
import { useAuth } from '../hooks/useAuth'
import { watchlistApi } from '../api/watchlistApi'

export default function ProfilePage() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadStats()
  }, [])

  const loadStats = async () => {
    try {
      setLoading(true)
      const response = await watchlistApi.getWatchlist()
      const watchlist = response.data.items || []

      const saved = watchlist.filter((item) => item.status === 'saved').length
      const watched = watchlist.filter((item) => item.status === 'watched').length

      const genres = {}
      const actors = {}

      watchlist.forEach((item) => {
        item.movie.genres?.forEach((genre) => {
          genres[genre.name] = (genres[genre.name] || 0) + 1
        })
        item.movie.cast?.slice(0, 5).forEach((actor) => {
          actors[actor.name] = (actors[actor.name] || 0) + 1
        })
      })

      const topGenres = Object.entries(genres)
        .sort(([, a], [, b]) => b - a)
        .slice(0, 5)
        .map(([name, count]) => ({ name, count }))

      const topActors = Object.entries(actors)
        .sort(([, a], [, b]) => b - a)
        .slice(0, 5)
        .map(([name, count]) => ({ name, count }))

      setStats({
        saved,
        watched,
        total: watchlist.length,
        topGenres,
        topActors,
      })
    } catch (error) {
      console.error('Failed to load stats:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  if (loading) {
    return <Loader />
  }

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold text-gray-100 mb-1">Profile</h1>
          <p className="text-gray-400">Welcome, {user?.username}</p>
        </div>
        <button
          onClick={handleLogout}
          className="flex items-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-700 rounded-lg font-semibold transition-colors"
        >
          <LogOut size={20} />
          Logout
        </button>
      </div>

      <div className="card p-6">
        <h2 className="text-2xl font-bold text-gray-100 mb-4">Account Info</h2>
        <div className="space-y-4">
          <div>
            <label className="text-sm font-medium text-gray-400">Username</label>
            <p className="text-lg text-gray-100">{user?.username}</p>
          </div>
          <div>
            <label className="text-sm font-medium text-gray-400">Email</label>
            <p className="text-lg text-gray-100">{user?.email}</p>
          </div>
          <div>
            <label className="text-sm font-medium text-gray-400">Member Since</label>
            <p className="text-lg text-gray-100">
              {user?.created_at
                ? new Date(user.created_at).toLocaleDateString()
                : 'Unknown'}
            </p>
          </div>
        </div>
      </div>

      {stats && (
        <>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="card p-6 text-center">
              <p className="text-4xl font-bold text-accent mb-2">{stats.total}</p>
              <p className="text-gray-400">Movies in Watchlist</p>
            </div>
            <div className="card p-6 text-center">
              <p className="text-4xl font-bold text-accent mb-2">{stats.saved}</p>
              <p className="text-gray-400">To Watch</p>
            </div>
            <div className="card p-6 text-center">
              <p className="text-4xl font-bold text-accent mb-2">{stats.watched}</p>
              <p className="text-gray-400">Already Watched</p>
            </div>
          </div>

          {stats.topGenres.length > 0 && (
            <div className="card p-6">
              <h3 className="text-2xl font-bold text-gray-100 mb-4">Favorite Genres</h3>
              <div className="space-y-3">
                {stats.topGenres.map((genre) => (
                  <div key={genre.name} className="flex items-center justify-between">
                    <span className="text-gray-300">{genre.name}</span>
                    <span className="text-accent font-semibold">{genre.count}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {stats.topActors.length > 0 && (
            <div className="card p-6">
              <h3 className="text-2xl font-bold text-gray-100 mb-4">Favorite Actors</h3>
              <div className="space-y-3">
                {stats.topActors.map((actor) => (
                  <div key={actor.name} className="flex items-center justify-between">
                    <span className="text-gray-300">{actor.name}</span>
                    <span className="text-accent font-semibold">{actor.count}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  )
}