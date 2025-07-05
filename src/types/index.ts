export interface Creator {
  id: string
  name: string
  username: string
  avatar: string
  price: number
  location: string
  followers: number
  posts: number
  isFree: boolean
  isNew: boolean
  description: string
}

export interface SearchFilters {
  location?: string
  priceRange?: {
    min: number
    max: number
  }
  isFree?: boolean
  isNew?: boolean
  gender?: string
  contentType?: string[]
} 