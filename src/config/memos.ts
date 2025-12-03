export interface MemOSConfig {
  apiKey: string
  baseURL: string
  timeout?: number
  enabled?: boolean
}

export const memosConfig: MemOSConfig = {
  apiKey: import.meta.env.VITE_MEMOS_API_KEY || '',
  baseURL: import.meta.env.VITE_MEMOS_BASE_URL || 'http://localhost:8000',
  timeout: 30000,
  enabled: import.meta.env.VITE_MEMOS_ENABLED === 'true' || false
}

export const getMemosConfig = (): MemOSConfig => {
  return {
    ...memosConfig,
    apiKey: import.meta.env.VITE_MEMOS_API_KEY || memosConfig.apiKey,
    baseURL: import.meta.env.VITE_MEMOS_BASE_URL || memosConfig.baseURL,
    enabled: import.meta.env.VITE_MEMOS_ENABLED === 'true' || memosConfig.enabled
  }
}

export const isMemOSEnabled = (): boolean => {
  const config = getMemosConfig()
  return config.enabled && config.apiKey.length > 0
}