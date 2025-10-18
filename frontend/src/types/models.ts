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
  title?: string
  name?: string
  description: string
  owner_id: string
  status?: 'PLANNING' | 'ACTIVE' | 'COMPLETED'
  technology_stack?: string[]
  created_at: string
  updated_at: string
}

export interface CreateProjectRequest {
  title?: string
  name?: string
  description: string
  technology_stack?: string[]
}

// Session types
export interface Session {
  id: string
  project_id: string
  user_id: string
  title: string
  status: 'ACTIVE' | 'COMPLETED' | 'ARCHIVED' | 'active' | 'completed' | 'archived'
  mode?: 'chat' | 'question' | 'teaching' | 'review'
  role_description?: string
  created_at: string
  updated_at: string
  archived_at?: string
}

export interface CreateSessionRequest {
  project_id: string
  title: string
  mode?: 'chat' | 'question' | 'teaching' | 'review'
  role_description?: string
}

// Message types
export interface Message {
  id: string
  session_id: string
  user_id: string
  content: string
  type?: 'user' | 'ai' | 'system' | 'assistant'
  role?: 'user' | 'assistant' | 'system'
  message_type?: string
  meta?: Record<string, any>
  created_at: string
  updated_at?: string
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
