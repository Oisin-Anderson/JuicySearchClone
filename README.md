# JuicySearch Clone

A modern OnlyFans search engine clone built with React, TypeScript, and Tailwind CSS. This project replicates the core functionality of JuicySearch, allowing users to search through OnlyFans creators by name with a beautiful, responsive interface.

## Features

- 🔍 **Smart Search**: Search OnlyFans creators by name, username, or description
- 🎯 **Advanced Filtering**: Filter by location, price, content type, and more
- 💖 **Wishlist**: Save your favorite creators for later
- 📱 **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- ⚡ **Fast Performance**: Built with Vite for lightning-fast development and builds
- 🎨 **Modern UI**: Beautiful design with smooth animations and transitions

## Tech Stack

- **Frontend**: React 18 + TypeScript
- **Styling**: Tailwind CSS
- **Build Tool**: Vite
- **Icons**: Lucide React
- **Animations**: Framer Motion
- **Routing**: React Router DOM

## Getting Started

### Prerequisites

- Node.js (version 16 or higher)
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/JuicySearchClone.git
cd JuicySearchClone
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open your browser and navigate to `http://localhost:3000`

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run lint:fix` - Fix ESLint errors

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Header.tsx      # Navigation header
│   ├── SearchBar.tsx   # Search input component
│   └── CreatorCard.tsx # Creator profile card
├── pages/              # Page components
│   ├── HomePage.tsx    # Landing page
│   └── SearchResults.tsx # Search results page
├── types/              # TypeScript type definitions
│   └── index.ts        # Main type definitions
├── App.tsx             # Main app component
├── main.tsx            # App entry point
└── index.css           # Global styles
```

## Features in Detail

### Search Functionality
- Real-time search through creator names, usernames, and descriptions
- URL-based search state management
- Responsive search interface with quick filters

### Creator Cards
- Beautiful card layout with hover effects
- Creator information display (name, username, price, location, followers, posts)
- Favorite/wishlist functionality
- Price badges (Free/Paid)
- New creator indicators

### Responsive Design
- Mobile-first approach
- Grid and list view modes
- Adaptive layouts for different screen sizes
- Touch-friendly interface

## Customization

### Styling
The project uses Tailwind CSS for styling. You can customize the design by modifying:
- `tailwind.config.js` - Tailwind configuration
- `src/index.css` - Global styles and custom components
- Component-specific classes in each component

### Adding New Features
1. Create new components in the `src/components/` directory
2. Add new pages in the `src/pages/` directory
3. Update routing in `src/App.tsx`
4. Add new types in `src/types/index.ts`

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This project is a clone/educational demonstration and is not affiliated with OnlyFans or JuicySearch. It uses mock data for demonstration purposes only.

## Support

If you have any questions or need help, please open an issue on GitHub.
