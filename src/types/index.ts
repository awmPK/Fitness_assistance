// User types
export interface User {
  user_id: string
  email: string
  name: string
  fitness_goal?: string
  experience_level?: 'beginner' | 'intermediate' | 'advanced'
  created_at?: string
  updated_at?: string
  last_login_at?: string
  avatar?: string
  fitnessLevel?: 'beginner' | 'intermediate' | 'advanced'
  height?: number
  weight?: number
  age?: number
}

// Message types
export interface Message {
  message_id: string
  conversation_id: string
  sender_type: 'user' | 'assistant'
  content: string
  timestamp: string
  metadata?: Record<string, any>
}

// Conversation types
export interface Conversation {
  conversation_id: string
  user_id: string
  title: string
  created_at: string
  updated_at: string
  messages?: Message[]
}

// Fitness Plan types
export interface FitnessPlan {
  id: string
  userId: string
  name: string
  description: string
  goal: string
  duration: number
  frequency: number
  startDate: string
  endDate: string
  status: 'active' | 'paused' | 'completed'
  workouts?: Workout[]
}

export interface CreatePlanRequest {
  name: string
  description: string
  goal: string
  duration: number
  frequency: number
  startDate: Date
  endDate: Date
  userId: string
}

export interface Workout {
  id: string
  date: string
  type: string
  duration: number
  calories?: number
  completed: boolean
}

export interface Activity {
  id: string
  type: string
  date: string
  duration: number
  calories: number
}

export interface Achievement {
  id: string
  name: string
  icon: string
  earned: boolean
}

// Progress Record types
export interface ProgressRecord {
  record_id: string
  user_id: string
  workout_date: string
  exercise_name: string
  sets_completed: number
  reps_completed: number
  weight_used: number
  duration_minutes: number
}

// API Response types
export interface ApiResponse<T> {
  success: boolean
  data: T
  message?: string
  error?: string
}

// Chat API types
export interface ChatRequest {
  user_id: string
  message: string
  context?: {
    fitness_goal?: string
    experience_level?: string
    conversation_id?: string
    [key: string]: any
  }
}

export interface ChatResponse {
  reply: string
  memory_used: boolean
  related_memories: Memory[]
  conversation_id: string
}

// Memory types for MemOS integration
export interface Memory {
  id: string
  content: string
  timestamp: string
  relevance?: number
}

export interface MemoryQuery {
  query: string
  limit?: number
  threshold?: number
  filters?: Record<string, any>
  userId: string
}

export interface CreateMemoryRequest {
  content: string
  metadata?: Record<string, any>
  type: 'text' | 'json' | 'event'
  timestamp: string
}

export interface UpdateMemoryRequest {
  content: string
  metadata?: Record<string, any>
  timestamp: string
}
