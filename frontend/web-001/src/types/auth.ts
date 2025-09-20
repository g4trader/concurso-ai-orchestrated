export interface User {
  id: string
  email: string
  name: string
  avatar?: string
  createdAt: string
  lastLogin?: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface LoginResponse {
  user: User
  token: string
  expiresIn: number
}
