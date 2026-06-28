import axiosClient from './axiosClient'

export const authApi = {
  register: (email, username, password) =>
    axiosClient.post('/auth/register', { email, username, password }),

  login: (email, password) =>
    axiosClient.post('/auth/login', { email, password }),

  refresh: (refreshToken) =>
    axiosClient.post('/auth/refresh', { refresh_token: refreshToken }),

  getCurrentUser: () =>
    axiosClient.get('/auth/me'),
}