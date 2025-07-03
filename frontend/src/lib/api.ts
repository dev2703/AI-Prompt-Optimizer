import axios from 'axios'
import { toast } from 'sonner'

// Create axios instance
export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('auth-storage')
    if (token) {
      try {
        const authData = JSON.parse(token)
        if (authData.state?.token) {
          config.headers.Authorization = `Bearer ${authData.state.token}`
        }
      } catch (error) {
        console.error('Error parsing auth storage:', error)
      }
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    const { response } = error
    
    if (response) {
      const { status, data } = response
      
      switch (status) {
        case 401:
          // Unauthorized - clear auth and redirect to login
          localStorage.removeItem('auth-storage')
          window.location.href = '/login'
          break
        case 403:
          toast.error('Access denied. You don\'t have permission to perform this action.')
          break
        case 404:
          toast.error('Resource not found.')
          break
        case 422:
          // Validation error
          if (data.detail && Array.isArray(data.detail)) {
            const errors = data.detail.map((err: any) => err.msg).join(', ')
            toast.error(errors)
          } else {
            toast.error('Validation error. Please check your input.')
          }
          break
        case 429:
          toast.error('Too many requests. Please try again later.')
          break
        case 500:
          toast.error('Server error. Please try again later.')
          break
        default:
          toast.error(data?.detail || 'An unexpected error occurred.')
      }
    } else {
      // Network error
      toast.error('Network error. Please check your connection.')
    }
    
    return Promise.reject(error)
  }
)

// API endpoints
export const endpoints = {
  auth: {
    login: '/auth/login',
    register: '/auth/register',
    me: '/auth/me',
    refresh: '/auth/refresh',
  },
  prompts: {
    list: '/prompts',
    create: '/prompts',
    get: (id: string) => `/prompts/${id}`,
    update: (id: string) => `/prompts/${id}`,
    delete: (id: string) => `/prompts/${id}`,
  },
  optimizations: {
    list: '/optimizations',
    create: '/optimizations',
    get: (id: string) => `/optimizations/${id}`,
    update: (id: string) => `/optimizations/${id}`,
    delete: (id: string) => `/optimizations/${id}`,
  },
  templates: {
    list: '/templates',
    create: '/templates',
    get: (id: string) => `/templates/${id}`,
    update: (id: string) => `/templates/${id}`,
    delete: (id: string) => `/templates/${id}`,
  },
  analytics: {
    dashboard: '/analytics/dashboard',
    usage: '/analytics/usage',
    performance: '/analytics/performance',
  },
  users: {
    profile: '/users/profile',
    update: '/users/profile',
  },
} 