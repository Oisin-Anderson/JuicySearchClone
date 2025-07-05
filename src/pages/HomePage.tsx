import React from 'react'
import SearchBar from '../components/SearchBar'
import { motion } from 'framer-motion'

const HomePage: React.FC = () => {
  const handleSearch = (query: string) => {
    console.log('Searching for:', query)
    // This will be handled by the SearchBar component navigation
  }

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative py-20 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
              Juicy Search: The Ultimate{' '}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary-600 to-primary-800">
                OnlyFans Finder
              </span>
            </h1>
            
            <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
              Stop scrolling. Start finding OnlyFans creators you actually want to subscribe to with Smart Filters & Precise Results.
            </p>

            {/* Main Search */}
            <div className="mb-12">
              <SearchBar 
                onSearch={handleSearch} 
                placeholder="Search OnlyFans creators by name..."
              />
            </div>

            {/* Search Tips */}
            <div className="text-sm text-gray-500 mb-8">
              <p>💡 <strong>Search Tips:</strong> Try searching by creator names like "Sophia", "Emma", "Lily", "Chloe", "Zoe", "Grace", "Scarlett", or "Victoria"</p>
            </div>
          </motion.div>

          {/* Features Grid */}
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mt-16"
          >
            {/* Feature 1 */}
            <div className="card p-6 text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🔍</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Name Search</h3>
              <p className="text-gray-600">
                Find creators instantly by searching their real names or usernames with our advanced search algorithm.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="card p-6 text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🎯</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Precise Filters</h3>
              <p className="text-gray-600">
                Filter by location, price, content type, and more to find exactly what you're looking for.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="card p-6 text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">💖</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Wishlist</h3>
              <p className="text-gray-600">
                Save your favorite creators to your wishlist and never lose track of them again.
              </p>
            </div>
          </motion.div>
        </div>
      </section>

      {/* How it works section */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              How It Works
            </h2>
            <p className="text-lg text-gray-600">
              Find your perfect OnlyFans creators in three simple steps
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-12 h-12 bg-primary-600 text-white rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                1
              </div>
              <h3 className="text-xl font-semibold mb-2">Search by Name</h3>
              <p className="text-gray-600">
                Enter a creator's name in the search bar above. Our system will find matches instantly.
              </p>
            </div>

            <div className="text-center">
              <div className="w-12 h-12 bg-primary-600 text-white rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                2
              </div>
              <h3 className="text-xl font-semibold mb-2">Browse Results</h3>
              <p className="text-gray-600">
                Explore detailed profiles with photos, pricing, and content information.
              </p>
            </div>

            <div className="text-center">
              <div className="w-12 h-12 bg-primary-600 text-white rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                3
              </div>
              <h3 className="text-xl font-semibold mb-2">Connect</h3>
              <p className="text-gray-600">
                Visit their OnlyFans profile and start your subscription journey.
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}

export default HomePage 