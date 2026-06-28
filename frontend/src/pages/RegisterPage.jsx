import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import Loader from '../components/common/Loader'
import { useAuth } from '../hooks/useAuth'
import { authApi } from '../api/authApi'

export default function RegisterPage() {
  const [email, setEmail] = useState('')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()
  const { login } = useAuth()

  const handleSubmit = async (e) => 
  {
  e.preventDefault()
  setError('')

  if (password !== confirmPassword) {
    setError('Passwords do not match')
    return
  }

  setLoading(true)

  try {
    await authApi.register(email, username, password)

    const loginResponse = await authApi.login(email, password)
    const { access_token, refresh_token } = loginResponse.data

    localStorage.setItem('access_token', access_token)

    const userResponse = await authApi.getCurrentUser()
    login(access_token, refresh_token, userResponse.data)

    navigate('/')
  } catch (err) {
    const errorMsg = err.response?.data?.detail
    if (typeof errorMsg === 'string') {
      setError(errorMsg)
    } else if (typeof errorMsg === 'object' && errorMsg?.msg) {
      setError(errorMsg.msg)
    } else {
      setError('Registration failed. Please try again.')
    }
  } finally {
    setLoading(false)
  }
 }

  if (loading) 
  {
    return <Loader />
  }

  return (
    <div className="min-h-[80vh] flex items-center justify-center relative -mt-6 pb-12">
      {/* Abstract Background Elements */}
      <div className="absolute top-1/4 right-1/4 w-96 h-96 bg-neon-cyan/20 rounded-full blur-[100px] pointer-events-none" />
      <div className="absolute bottom-1/4 left-1/4 w-96 h-96 bg-accent/10 rounded-full blur-[100px] pointer-events-none" />

      <div className="w-full max-w-md z-10 mt-12">
        <div className="glass-card p-10 animate-fade-in relative overflow-hidden">
          {/* Top highlight bar */}
          <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-accent to-blue-600" />

          <h1 className="text-4xl font-heading font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-white to-gray-400 mb-3 text-center tracking-tight">
            Create Account
          </h1>
          <p className="text-gray-400 text-center mb-8 font-medium">
            Join Kinosoca to save and rate movies
          </p>

          {error && (
            <div className="mb-6 p-4 bg-red-500/10 border border-red-500/30 rounded-xl text-red-400 text-sm font-semibold flex items-center gap-3">
              <span className="w-1.5 h-1.5 rounded-full bg-red-500"></span>
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            <div className="space-y-1">
              <label className="block text-sm font-bold text-gray-300 ml-1">
                Email Address
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-5 py-4 bg-white/5 border border-white/10 text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-accent/50 focus:border-accent/50 transition-all duration-300 shadow-inner placeholder-gray-500 font-medium"
                placeholder="hello@example.com"
                required
              />
            </div>

            <div className="space-y-1">
              <label className="block text-sm font-bold text-gray-300 ml-1">
                Username
              </label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full px-5 py-4 bg-white/5 border border-white/10 text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-accent/50 focus:border-accent/50 transition-all duration-300 shadow-inner placeholder-gray-500 font-medium"
                placeholder="Choose a username"
                required
              />
              <p className="text-xs text-gray-500 ml-1 mt-1">
                3-50 characters, letters, numbers, and underscores only
              </p>
            </div>

            <div className="space-y-1">
              <label className="block text-sm font-bold text-gray-300 ml-1">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-5 py-4 bg-white/5 border border-white/10 text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-accent/50 focus:border-accent/50 transition-all duration-300 shadow-inner placeholder-gray-500 font-medium"
                placeholder="••••••••"
                required
              />
              <p className="text-xs text-gray-500 ml-1 mt-1">
                At least 8 characters, with letters and numbers
              </p>
            </div>

            <div className="space-y-1">
              <label className="block text-sm font-bold text-gray-300 ml-1">
                Confirm Password
              </label>
              <input
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className="w-full px-5 py-4 bg-white/5 border border-white/10 text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-accent/50 focus:border-accent/50 transition-all duration-300 shadow-inner placeholder-gray-500 font-medium"
                placeholder="••••••••"
                required
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full btn-primary h-14 text-lg mt-6 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:-translate-y-0 disabled:hover:shadow-accent/30"
            >
              {loading ? 'Creating Account...' : 'Sign Up'}
            </button>
          </form>

          <div className="mt-8 pt-6 border-t border-white/10 text-center">
            <p className="text-gray-400 font-medium">
              Already have an account?{' '}
              <Link to="/login" className="text-white hover:text-accent font-bold transition-colors">
                Sign In
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}