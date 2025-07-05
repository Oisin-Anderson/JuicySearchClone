import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Search, Filter, MapPin, Image as ImageIcon } from 'lucide-react'

interface SearchBarProps {
  onSearch: (query: string) => void
  placeholder?: string
  className?: string
}

const SearchBar: React.FC<SearchBarProps> = ({ 
  onSearch, 
  placeholder = "Search OnlyFans creators by name...", 
  className = "" 
}) => {
  const [searchQuery, setSearchQuery] = useState('')
  const navigate = useNavigate()

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (searchQuery.trim()) {
      onSearch(searchQuery.trim())
      navigate(`/search?q=${encodeURIComponent(searchQuery.trim())}`)
    }
  }

  return (
    <div className={`w-full max-w-4xl mx-auto ${className}`}>
      <form onSubmit={handleSubmit} className="relative">
        <div className="relative">
          <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder={placeholder}
            className="search-input pl-12 pr-4"
            autoFocus={window.location.pathname === '/search'}
          />
          <button
            type="submit"
            className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-primary-600 hover:bg-primary-700 text-white p-2 rounded-md transition-colors"
          >
            <Search className="w-5 h-5" />
          </button>
        </div>
      </form>

      {/* Quick filters */}
      <div className="flex flex-wrap gap-2 mt-4 justify-center">
        <button className="flex items-center space-x-1 px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded-full text-sm text-gray-700 transition-colors">
          <MapPin size={14} />
          <span>Near me</span>
        </button>
        <button className="flex items-center space-x-1 px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded-full text-sm text-gray-700 transition-colors">
          <span>🆓</span>
          <span>Free</span>
        </button>
        <button className="flex items-center space-x-1 px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded-full text-sm text-gray-700 transition-colors">
          <span>🌟</span>
          <span>New</span>
        </button>
        <button className="flex items-center space-x-1 px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded-full text-sm text-gray-700 transition-colors">
          <span>👩</span>
          <span>Female</span>
        </button>
        <button className="flex items-center space-x-1 px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded-full text-sm text-gray-700 transition-colors">
          <span>⚧️</span>
          <span>Trans</span>
        </button>
        <button className="flex items-center space-x-1 px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded-full text-sm text-gray-700 transition-colors">
          <span>🤩</span>
          <span>Celebrity Lookalikes</span>
        </button>
      </div>
    </div>
  )
}

export default SearchBar 