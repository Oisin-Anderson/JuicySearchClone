import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Header from './components/Header'
import HomePage from './pages/HomePage'
import SearchResults from './pages/SearchResults'
import './App.css'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
        <Header />
        <main>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/search" element={<SearchResults />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App 