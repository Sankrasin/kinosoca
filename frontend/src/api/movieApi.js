import axiosClient from './axiosClient'

export const movieApi = {
  getTrending: (page = 1, pageSize = 20) =>
    axiosClient.get('/movies/trending', { params: { page, page_size: pageSize } }),

  getPopular: (page = 1, pageSize = 20) =>
    axiosClient.get('/movies/popular', { params: { page, page_size: pageSize } }),

  getTopRated: (page = 1, pageSize = 20) =>
    axiosClient.get('/movies/top-rated', { params: { page, page_size: pageSize } }),

  getMovieDetail: (movieId, country = 'IN') =>
    axiosClient.get(`/movies/${movieId}`, { params: { country } }),

  getMovieProviders: (movieId, country = 'IN') =>
    axiosClient.get(`/movies/${movieId}/providers`, { params: { country } }),
}