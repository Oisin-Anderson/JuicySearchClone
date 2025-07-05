import React from 'react'
import { Link } from 'react-router-dom'
import { Search, Heart, MapPin, Filter, Image as ImageIcon } from 'lucide-react'

const Header: React.FC = () => {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-r from-primary-500 to-primary-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">J</span>
            </div>
            <span className="text-xl font-bold text-gray-900">JuicySearch</span>
          </Link>

          {/* Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            <Link to="/" className="text-gray-600 hover:text-primary-600 transition-colors">
              Search
            </Link>
            <Link to="/search" className="text-gray-600 hover:text-primary-600 transition-colors flex items-center space-x-1">
              <ImageIcon size={16} />
              <span>Image Search</span>
            </Link>
            <Link to="/search" className="text-gray-600 hover:text-primary-600 transition-colors flex items-center space-x-1">
              <Filter size={16} />
              <span>Filters</span>
            </Link>
            <Link to="/search" className="text-gray-600 hover:text-primary-600 transition-colors flex items-center space-x-1">
              <MapPin size={16} />
              <span>Near Me</span>
            </Link>
            <Link to="/search" className="text-gray-600 hover:text-primary-600 transition-colors flex items-center space-x-1">
              <Heart size={16} />
              <span>Wishlist</span>
            </Link>
          </nav>

          {/* Mobile menu button */}
          <button className="md:hidden p-2 rounded-md text-gray-600 hover:text-primary-600 hover:bg-gray-100">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>
      </div>
    </header>
  )
}

export default Header 