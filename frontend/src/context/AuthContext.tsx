import React, { createContext, useState, useContext, useEffect } from 'react'
import { User } from '../types/models'
import { api } from '../services/api'

interface AuthContextType {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string, name: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  // Check if user is already logged in on mount
  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (token) {
      // Try to fetch user profile
      api.getProfile()
        .then((res) => {
          setUser(res.data.user || res.data)
        })
        .catch(() => {
          localStorage.removeItem('access_token')
        })
        .finally(() => {
          setIsLoading(false)
        })
    } else {
      setIsLoading(false)
    }
  }, [])

  const login = async (email: string, password: string) => {
    try {
      const response = await api.login(email, password)
      // Handle nested response structure: { success, data: { access_token, user_id, username, email, ... } }
      const loginData = response.data.data || response.data
      const { access_token } = loginData

      localStorage.setItem('access_token', access_token)

      // Create user object from login response
      const userData: User = {
        id: loginData.user_id || loginData.id || '',
        email: loginData.email,
        name: loginData.username || `${loginData.first_name || ''} ${loginData.last_name || ''}`.trim(),
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      }
      setUser(userData)
    } catch (error) {
      console.error('Login failed:', error)
      throw error
    }
  }

  const register = async (email: string, password: string, name: string) => {
    try {
      const response = await api.register(email, password, name)
      // Backend returns: { success, data: { id, username, email, first_name, last_name, created_at }, message }
      // Note: Registration doesn't return access_token, user needs to login after
      const userData = response.data.data || response.data

      // Auto-login after registration by calling login
      await login(email, password)
    } catch (error) {
      console.error('Registration failed:', error)
      throw error
    }
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    setUser(null)
    api.logout().catch(() => {
      // Ignore errors on logout
    })
  }

  const value: AuthContextType = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    register,
    logout,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
