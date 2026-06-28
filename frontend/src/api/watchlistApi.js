import axiosClient from './axiosClient'

export const watchlistApi = {
  getWatchlist: () =>
    axiosClient.get('/watchlist'),

  addToWatchlist: (movieId) =>
    axiosClient.post('/watchlist', { movie_id: movieId }),

  updateWatchlistStatus: (movieId, status) =>
    axiosClient.patch(`/watchlist/${movieId}`, { status }),

  removeFromWatchlist: (movieId) =>
    axiosClient.delete(`/watchlist/${movieId}`),
}