import axiosClient from './axiosClient'

export const recommendationApi = {
  getSimilar: (movieId, limit = 12) =>
    axiosClient.get(`/recommendations/similar/${movieId}`, { params: { limit } }),

  getPersonalized: (limit = 12) =>
    axiosClient.get('/recommendations/personalized', { params: { limit } }),

  getMoods: () =>
    axiosClient.get('/moods'),

  getMoviesForMood: (moodName, limit = 20) =>
    axiosClient.get(`/moods/${moodName}/movies`, { params: { limit } }),
}