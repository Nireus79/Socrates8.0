import axios, { AxiosInstance, AxiosError } from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

class APIClient {
  private client: AxiosInstance

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Add request interceptor to include token
    this.client.interceptors.request.use((config) => {
      const token = localStorage.getItem('access_token')
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    })

    // Add response interceptor to handle errors
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('access_token')
          window.location.href = '/login'
        }
        return Promise.reject(error)
      }
    )
  }

  // Auth endpoints
  async register(email: string, password: string, name: string) {
    return this.client.post('/register', { email, password, name })
  }

  async login(email: string, password: string) {
    return this.client.post('/login', { email, password })
  }

  async logout() {
    return this.client.post('/logout')
  }

  async getProfile() {
    return this.client.get('/profile')
  }

  async updateProfile(data: any) {
    return this.client.put('/profile', data)
  }

  // Project endpoints
  async getProjects() {
    return this.client.get('/projects')
  }

  async getProject(id: string) {
    return this.client.get(`/projects/${id}`)
  }

  async createProject(data: any) {
    return this.client.post('/projects', data)
  }

  async updateProject(id: string, data: any) {
    return this.client.put(`/projects/${id}`, data)
  }

  async deleteProject(id: string) {
    return this.client.delete(`/projects/${id}`)
  }

  // Session endpoints
  async getSessions() {
    return this.client.get('/sessions')
  }

  async getSession(id: string) {
    return this.client.get(`/sessions/${id}`)
  }

  async createSession(data: any) {
    return this.client.post('/sessions', data)
  }

  async updateSession(id: string, data: any) {
    return this.client.put(`/sessions/${id}`, data)
  }

  async deleteSession(id: string) {
    return this.client.delete(`/sessions/${id}`)
  }

  // Message endpoints
  async getMessages(sessionId: string) {
    return this.client.get(`/sessions/${sessionId}/messages`)
  }

  async sendMessage(sessionId: string, content: string) {
    return this.client.post(`/sessions/${sessionId}/messages`, { content })
  }

  // Health check
  async healthCheck() {
    return axios.get('http://localhost:8000/health')
  }
}

export const api = new APIClient()
