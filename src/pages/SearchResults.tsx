import React, { useState, useEffect } from 'react'
import { useSearchParams } from 'react-router-dom'
import SearchBar from '../components/SearchBar'
import CreatorCard from '../components/CreatorCard'
import { Filter, Grid, List, Search } from 'lucide-react'

// Enhanced mock data with more realistic OnlyFans creators
const mockCreators = [
  {
    id: '1',
    name: 'Sophia Rose',
    username: 'sophiarose',
    avatar: 'https://via.placeholder.com/300x400/ec4899/ffffff?text=Sophia',
    price: 9.99,
    location: 'Los Angeles, CA',
    followers: 125000,
    posts: 450,
    isFree: false,
    isNew: false,
    description: 'Fitness enthusiast and lifestyle content creator. Sharing my journey and exclusive content with my amazing fans!'
  },
  {
    id: '2',
    name: 'Emma Johnson',
    username: 'emmaj',
    avatar: 'https://via.placeholder.com/300x400/8b5cf6/ffffff?text=Emma',
    price: 0,
    location: 'New York, NY',
    followers: 89000,
    posts: 320,
    isFree: true,
    isNew: true,
    description: 'Free content creator sharing daily life, fashion, and lifestyle tips. New to the platform!'
  },
  {
    id: '3',
    name: 'Isabella Smith',
    username: 'bella_smith',
    avatar: 'https://via.placeholder.com/300x400/06b6d4/ffffff?text=Isabella',
    price: 14.99,
    location: 'Miami, FL',
    followers: 210000,
    posts: 780,
    isFree: false,
    isNew: false,
    description: 'Professional model and content creator. Exclusive photoshoots and behind-the-scenes content available.'
  },
  {
    id: '4',
    name: 'Olivia Davis',
    username: 'oliviadavis',
    avatar: 'https://via.placeholder.com/300x400/10b981/ffffff?text=Olivia',
    price: 7.99,
    location: 'Chicago, IL',
    followers: 67000,
    posts: 290,
    isFree: false,
    isNew: false,
    description: 'Art student sharing creative content and lifestyle. Let\'s explore art and life together!'
  },
  {
    id: '5',
    name: 'Ava Wilson',
    username: 'avawilson',
    avatar: 'https://via.placeholder.com/300x400/f59e0b/ffffff?text=Ava',
    price: 0,
    location: 'Seattle, WA',
    followers: 45000,
    posts: 180,
    isFree: true,
    isNew: true,
    description: 'Tech enthusiast and gamer girl. Sharing gaming content and tech reviews. Free content available!'
  },
  {
    id: '6',
    name: 'Mia Brown',
    username: 'miabrown',
    avatar: 'https://via.placeholder.com/300x400/ef4444/ffffff?text=Mia',
    price: 12.99,
    location: 'Austin, TX',
    followers: 156000,
    posts: 520,
    isFree: false,
    isNew: false,
    description: 'Musician and performer. Exclusive music content and behind-the-scenes of my performances.'
  },
  {
    id: '7',
    name: 'Lily Anderson',
    username: 'lilyanderson',
    avatar: 'https://via.placeholder.com/300x400/8b5cf6/ffffff?text=Lily',
    price: 5.99,
    location: 'Portland, OR',
    followers: 78000,
    posts: 340,
    isFree: false,
    isNew: false,
    description: 'Yoga instructor and wellness advocate. Mind, body, and soul content for your daily inspiration.'
  },
  {
    id: '8',
    name: 'Chloe Martinez',
    username: 'chloemartinez',
    avatar: 'https://via.placeholder.com/300x400/06b6d4/ffffff?text=Chloe',
    price: 0,
    location: 'Denver, CO',
    followers: 32000,
    posts: 120,
    isFree: true,
    isNew: true,
    description: 'Adventure seeker and travel blogger. Exploring the world and sharing amazing experiences!'
  },
  {
    id: '9',
    name: 'Zoe Taylor',
    username: 'zoetaylor',
    avatar: 'https://via.placeholder.com/300x400/10b981/ffffff?text=Zoe',
    price: 11.99,
    location: 'Nashville, TN',
    followers: 189000,
    posts: 650,
    isFree: false,
    isNew: false,
    description: 'Country music singer and songwriter. Behind-the-scenes studio sessions and exclusive performances.'
  },
  {
    id: '10',
    name: 'Grace Lee',
    username: 'gracelee',
    avatar: 'https://via.placeholder.com/300x400/f59e0b/ffffff?text=Grace',
    price: 8.99,
    location: 'San Francisco, CA',
    followers: 95000,
    posts: 420,
    isFree: false,
    isNew: false,
    description: 'Tech entrepreneur and lifestyle influencer. Balancing work, fitness, and personal growth.'
  },
  {
    id: '11',
    name: 'Scarlett Williams',
    username: 'scarlettw',
    avatar: 'https://via.placeholder.com/300x400/ef4444/ffffff?text=Scarlett',
    price: 0,
    location: 'Las Vegas, NV',
    followers: 28000,
    posts: 95,
    isFree: true,
    isNew: true,
    description: 'Dancer and performer. Show-stopping routines and behind-the-scenes of the entertainment world.'
  },
  {
    id: '12',
    name: 'Victoria Garcia',
    username: 'victoriagarcia',
    avatar: 'https://via.placeholder.com/300x400/ec4899/ffffff?text=Victoria',
    price: 15.99,
    location: 'Phoenix, AZ',
    followers: 245000,
    posts: 890,
    isFree: false,
    isNew: false,
    description: 'Fashion model and style consultant. High-end fashion shoots and exclusive styling tips.'
  }
]

const SearchResults: React.FC = () => {
  const [searchParams] = useSearchParams()
  const [searchQuery, setSearchQuery] = useState('')
  const [filteredCreators, setFilteredCreators] = useState(mockCreators)
  const [favorites, setFavorites] = useState<string[]>([])
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid')

  useEffect(() => {
    const query = searchParams.get('q') || ''
    setSearchQuery(query)
    
    if (query) {
      // Enhanced search focusing on names but also checking username and description
      const filtered = mockCreators.filter(creator => {
        const searchTerm = query.toLowerCase().trim()
        const nameMatch = creator.name.toLowerCase().includes(searchTerm)
        const usernameMatch = creator.username.toLowerCase().includes(searchTerm)
        const descriptionMatch = creator.description.toLowerCase().includes(searchTerm)
        
        // Prioritize name matches, then username, then description
        return nameMatch || usernameMatch || descriptionMatch
      })
      setFilteredCreators(filtered)
    } else {
      setFilteredCreators(mockCreators)
    }
  }, [searchParams])

  const handleSearch = (query: string) => {
    setSearchQuery(query)
    if (query.trim()) {
      // Enhanced search focusing on names but also checking username and description
      const filtered = mockCreators.filter(creator => {
        const searchTerm = query.toLowerCase().trim()
        const nameMatch = creator.name.toLowerCase().includes(searchTerm)
        const usernameMatch = creator.username.toLowerCase().includes(searchTerm)
        const descriptionMatch = creator.description.toLowerCase().includes(searchTerm)
        
        // Prioritize name matches, then username, then description
        return nameMatch || usernameMatch || descriptionMatch
      })
      setFilteredCreators(filtered)
    } else {
      setFilteredCreators(mockCreators)
    }
  }

  const handleFavorite = (creatorId: string) => {
    setFavorites(prev => 
      prev.includes(creatorId) 
        ? prev.filter(id => id !== creatorId)
        : [...prev, creatorId]
    )
  }

  return (
    <div className="min-h-screen py-8">
      <div className="max-w-7xl mx-auto px-4">
        {/* Search Bar */}
        <div className="mb-8">
          <SearchBar onSearch={handleSearch} placeholder="Search creators by name..." />
        </div>

        {/* Results Header */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              {searchQuery ? `Search results for "${searchQuery}"` : 'All Creators'}
            </h1>
            <p className="text-gray-600 mt-1">
              {filteredCreators.length} creator{filteredCreators.length !== 1 ? 's' : ''} found
            </p>
          </div>

          {/* View Controls */}
          <div className="flex items-center space-x-4 mt-4 sm:mt-0">
            <div className="flex items-center space-x-2 bg-white rounded-lg border border-gray-200 p-1">
              <button
                onClick={() => setViewMode('grid')}
                className={`p-2 rounded-md transition-colors ${
                  viewMode === 'grid' 
                    ? 'bg-primary-100 text-primary-600' 
                    : 'text-gray-600 hover:text-primary-600'
                }`}
              >
                <Grid size={20} />
              </button>
              <button
                onClick={() => setViewMode('list')}
                className={`p-2 rounded-md transition-colors ${
                  viewMode === 'list' 
                    ? 'bg-primary-100 text-primary-600' 
                    : 'text-gray-600 hover:text-primary-600'
                }`}
              >
                <List size={20} />
              </button>
            </div>

            <button className="flex items-center space-x-2 px-4 py-2 bg-white border border-gray-200 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors">
              <Filter size={16} />
              <span>Filters</span>
            </button>
          </div>
        </div>

        {/* Results Grid */}
        {filteredCreators.length > 0 ? (
          <div className={`grid gap-6 ${
            viewMode === 'grid' 
              ? 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4' 
              : 'grid-cols-1'
          }`}>
            {filteredCreators.map(creator => (
              <CreatorCard
                key={creator.id}
                creator={creator}
                onFavorite={handleFavorite}
                isFavorited={favorites.includes(creator.id)}
              />
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <div className="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Search className="w-12 h-12 text-gray-400" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">No creators found</h3>
            <p className="text-gray-600">
              Try adjusting your search terms or filters to find what you're looking for.
            </p>
          </div>
        )}
      </div>
    </div>
  )
}

export default SearchResults 