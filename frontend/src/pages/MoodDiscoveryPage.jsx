import { useState, useEffect } from 'react'
import { useSearchParams } from 'react-router-dom'
import MoodCard from '../components/mood/MoodCard'
import MovieGrid from '../components/movie/MovieGrid'
import Loader from '../components/common/Loader'
import { recommendationApi } from '../api/recommendationApi'

export default function MoodDiscoveryPage() {
  const [searchParams] = useSearchParams()
  const moodFromParam = searchParams.get('mood')
  const [moods, setMoods] = useState([])
  const [selectedMood, setSelectedMood] = useState(moodFromParam || null)
  const [movies, setMovies] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadMoods()
  }, [])

  useEffect(() => {
    if (selectedMood) {
      loadMoviesForMood(selectedMood)
    }
  }, [selectedMood])

  const loadMoods = async () => {
    try {
      setLoading(true)
      const response = await recommendationApi.getMoods()
      setMoods(response.data.moods || [])
      if (moodFromParam) {
        setSelectedMood(moodFromParam)
      } else if (response.data.moods.length > 0) {
        setSelectedMood(response.data.moods[0].name)
      }
    } catch (error) {
      console.error('Failed to load moods:', error)
    } finally {
      setLoading(false)
    }
  }

  const loadMoviesForMood = async (moodName) => {
    try {
      setLoading(true)
      const response = await recommendationApi.getMoviesForMood(moodName, 20)
      setMovies(response.data.items || [])
    } catch (error) {
      console.error('Failed to load movies for mood:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading && moods.length === 0) {
    return <Loader />
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold text-gray-100 mb-2">Discover by Mood</h1>
        <p className="text-gray-400">
          Find movies based on the mood or vibe you're looking for
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {moods.map((mood) => (
          <div
            key={mood.id}
            onClick={() => setSelectedMood(mood.name)}
            className="cursor-pointer"
          >
            <MoodCard mood={mood} />
          </div>
        ))}
      </div>

      {selectedMood && (
        <div>
          <h2 className="text-3xl font-bold text-gray-100 mb-6">
            {selectedMood} Movies
          </h2>
          {loading ? (
            <Loader />
          ) : (
            <MovieGrid movies={movies} />
          )}
        </div>
      )}
    </div>
  )
}