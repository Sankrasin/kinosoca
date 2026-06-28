import axiosClient from './axiosClient'

export const searchApi = {
  search: (params) =>
    axiosClient.get('/search', { params }),

  semanticSearch: (query, limit = 12) =>
    axiosClient.post('/search/semantic', { query, limit }),
}