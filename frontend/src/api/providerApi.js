import axiosClient from './axiosClient'

export const providerApi = {
  getProviders: (country = 'IN') =>
    axiosClient.get('/providers', { params: { country } }),
}