import React from 'react'
import { Heart, MapPin, DollarSign } from 'lucide-react'

interface Creator {
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

interface CreatorCardProps {
  creator: Creator
  onFavorite: (creatorId: string) => void
  isFavorited: boolean
}

const CreatorCard: React.FC<CreatorCardProps> = ({ creator, onFavorite, isFavorited }) => {
  return (
    <div className="card overflow-hidden group">
      {/* Image */}
      <div className="relative aspect-[3/4] overflow-hidden">
        <img
          src={creator.avatar}
          alt={creator.name}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          onError={(e) => {
            const target = e.target as HTMLImageElement
            target.src = 'https://via.placeholder.com/300x400/ec4899/ffffff?text=Creator'
          }}
        />
        
        {/* Overlay with actions */}
        <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-all duration-300">
          <div className="absolute top-3 right-3">
            <button
              onClick={() => onFavorite(creator.id)}
              className={`p-2 rounded-full transition-all duration-200 ${
                isFavorited 
                  ? 'bg-red-500 text-white' 
                  : 'bg-white/80 text-gray-700 hover:bg-red-500 hover:text-white'
              }`}
            >
              <Heart size={16} fill={isFavorited ? 'currentColor' : 'none'} />
            </button>
          </div>
          
          {/* Price badge */}
          <div className="absolute bottom-3 left-3">
            <div className={`px-3 py-1 rounded-full text-sm font-medium ${
              creator.isFree 
                ? 'bg-green-500 text-white' 
                : 'bg-primary-600 text-white'
            }`}>
              {creator.isFree ? 'FREE' : `$${creator.price}`}
            </div>
          </div>
          
          {/* New badge */}
          {creator.isNew && (
            <div className="absolute top-3 left-3">
              <div className="px-2 py-1 bg-yellow-500 text-white text-xs font-medium rounded-full">
                NEW
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Content */}
      <div className="p-4">
        <div className="flex items-start justify-between mb-2">
          <div>
            <h3 className="font-semibold text-gray-900 truncate">{creator.name}</h3>
            <p className="text-sm text-gray-500">@{creator.username}</p>
          </div>
        </div>

        <p className="text-sm text-gray-600 mb-3 line-clamp-2">{creator.description}</p>

        {/* Stats */}
        <div className="flex items-center justify-between text-sm text-gray-500">
          <div className="flex items-center space-x-1">
            <MapPin size={14} />
            <span>{creator.location}</span>
          </div>
          <div className="flex items-center space-x-3">
            <span>{creator.followers.toLocaleString()} followers</span>
            <span>{creator.posts} posts</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default CreatorCard 