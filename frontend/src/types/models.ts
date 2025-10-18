// User types
export interface User {
  id: string
  email: string
  name: string
  created_at: string
  updated_at: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user: User
}

// Project types
export interface Project {
  id: string
  name: string
  description: string
  owner_id: string
  created_at: string
  updated_at: string
}

export interface CreateProjectRequest {
  name: string
  description: string
}

// Session types
export interface Session {
  id: string
  project_id: string
  user_id: string
  title: string
  description: string
  status: 'active' | 'completed' | 'archived'
  created_at: string
  updated_at: string
}

export interface CreateSessionRequest {
  project_id: string
  title: string
  description: string
}

// Message types
export interface Message {
  id: string
  session_id: string
  user_id: string
  content: string
  type: 'user' | 'ai' | 'system'
  created_at: string
}

export interface CreateMessageRequest {
  content: string
}

// Error response
export interface ErrorResponse {
  detail: string | string[]
}

// API Response wrapper
export interface ApiResponse<T> {
  data: T
  status: number
}
