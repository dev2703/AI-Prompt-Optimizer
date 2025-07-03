import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { api } from '@/lib/api'

interface User {
  id: string
  email: string
  name: string
  subscription_tier: string
  created_at: string
}

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  loading: boolean
}

interface AuthActions {
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string, name: string) => Promise<void>
  logout: () => void
  checkAuth: () => Promise<void>
  setUser: (user: User) => void
  setToken: (token: string) => void
}

type AuthStore = AuthState & AuthActions

export const useAuthStore = create<AuthStore>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      loading: false,

      login: async (email: string, password: string) => {
        set({ loading: true })
        try {
          const response = await api.post('/auth/login', { email, password })
          const { access_token, user } = response.data
          
          set({
            user,
            token: access_token,
            isAuthenticated: true,
            loading: false,
          })
          
          // Set auth header for future requests
          api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
        } catch (error) {
          set({ loading: false })
          throw error
        }
      },

      register: async (email: string, password: string, name: string) => {
        set({ loading: true })
        try {
          const response = await api.post('/auth/register', { 
            email, 
            password, 
            name 
          })
          const { access_token, user } = response.data
          
          set({
            user,
            token: access_token,
            isAuthenticated: true,
            loading: false,
          })
          
          // Set auth header for future requests
          api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
        } catch (error) {
          set({ loading: false })
          throw error
        }
      },

      logout: () => {
        set({
          user: null,
          token: null,
          isAuthenticated: false,
        })
        
        // Remove auth header
        delete api.defaults.headers.common['Authorization']
      },

      checkAuth: async () => {
        const { token } = get()
        if (!token) {
          set({ isAuthenticated: false, loading: false })
          return
        }

        try {
          // Set auth header
          api.defaults.headers.common['Authorization'] = `Bearer ${token}`
          
          const response = await api.get('/auth/me')
          set({
            user: response.data,
            isAuthenticated: true,
            loading: false,
          })
        } catch (error) {
          set({
            user: null,
            token: null,
            isAuthenticated: false,
            loading: false,
          })
          delete api.defaults.headers.common['Authorization']
        }
      },

      setUser: (user: User) => {
        set({ user })
      },

      setToken: (token: string) => {
        set({ token, isAuthenticated: true })
        api.defaults.headers.common['Authorization'] = `Bearer ${token}`
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({ 
        user: state.user, 
        token: state.token,
        isAuthenticated: state.isAuthenticated 
      }),
    }
  )
) 