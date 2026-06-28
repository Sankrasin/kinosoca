import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Menu, X, LogOut, User } from 'lucide-react'
import { useAuth } from '../../hooks/useAuth'

export default function Navbar() {
  const { user, logout } = useAuth()
  const [menuOpen, setMenuOpen] = useState(false)
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/')
    setMenuOpen(false)
  }

  return (
    <nav className="fixed w-full top-0 z-50 glass bg-primary/70 backdrop-blur-xl border-b border-white/5 transition-all duration-300">
      <div className="container mx-auto px-6 py-4 flex items-center justify-between">
        <Link to="/" className="text-3xl font-heading font-extrabold tracking-tighter text-transparent bg-clip-text bg-gradient-to-r from-white to-gray-400 hover:from-accent hover:to-blue-500 transition-all duration-300">
          KINOSOCA
        </Link>

        <button
          onClick={() => setMenuOpen(!menuOpen)}
          className="md:hidden p-2 text-gray-100 hover:text-accent transition-colors"
        >
          {menuOpen ? <X size={24} /> : <Menu size={24} />}
        </button>

        <div
          className={`${
            menuOpen ? 'absolute top-[72px] left-0 right-0 glass border-b border-white/10 p-6' : 'hidden'
          } md:flex md:static md:gap-8 md:items-center flex-col md:flex-row md:p-0 bg-primary md:bg-transparent`}
        >
          <Link
            to="/"
            onClick={() => setMenuOpen(false)}
            className="text-sm font-bold tracking-wide text-gray-300 hover:text-white transition-colors uppercase"
          >
            Home
          </Link>
          <Link
            to="/search"
            onClick={() => setMenuOpen(false)}
            className="text-sm font-bold tracking-wide text-gray-300 hover:text-white transition-colors uppercase"
          >
            The Observatory
          </Link>
          <Link
            to="/moods"
            onClick={() => setMenuOpen(false)}
            className="text-sm font-bold tracking-wide text-gray-300 hover:text-white transition-colors uppercase"
          >
            Moods
          </Link>

          {user && (
            <>
              <Link
                to="/watchlist"
                onClick={() => setMenuOpen(false)}
                className="text-sm font-bold tracking-wide text-gray-300 hover:text-white transition-colors uppercase"
              >
                Watchlist
              </Link>
              <div className="flex items-center gap-6 border-t border-white/10 pt-6 mt-2 md:border-t-0 md:pt-0 md:mt-0 md:ml-4">
                <Link
                  to="/profile"
                  onClick={() => setMenuOpen(false)}
                  className="flex items-center gap-2 text-sm font-bold text-accent hover:text-white transition-colors"
                >
                  <User size={18} />
                  {user.username}
                </Link>
                <button
                  onClick={handleLogout}
                  className="flex items-center gap-2 text-sm font-bold text-gray-400 hover:text-red-500 transition-colors"
                >
                  <LogOut size={18} />
                  Logout
                </button>
              </div>
            </>
          )}

          {!user && (
            <div className="flex flex-col md:flex-row gap-4 border-t border-white/10 pt-6 mt-2 md:border-t-0 md:pt-0 md:mt-0 md:ml-4">
              <Link
                to="/login"
                onClick={() => setMenuOpen(false)}
                className="text-sm font-bold text-gray-300 hover:text-white transition-colors md:px-4 py-2"
              >
                Sign In
              </Link>
              <Link
                to="/register"
                onClick={() => setMenuOpen(false)}
                className="btn-primary text-sm shadow-accent/20"
              >
                Get Started
              </Link>
            </div>
          )}
        </div>
      </div>
    </nav>
  )
}