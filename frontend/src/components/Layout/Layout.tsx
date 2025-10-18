import React, { useState } from 'react'
import { useAuth } from '../../context/AuthContext'
import { useNavigate } from 'react-router-dom'
import './Layout.css'

interface LayoutProps {
  children: React.ReactNode
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [sidebarOpen, setSidebarOpen] = useState(true)

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="layout">
      {/* Sidebar */}
      <aside className={`sidebar ${sidebarOpen ? 'open' : 'closed'}`}>
        <div className="sidebar-header">
          <h2>Socrates</h2>
          <button
            className="toggle-btn"
            onClick={() => setSidebarOpen(!sidebarOpen)}
            title={sidebarOpen ? 'Close sidebar' : 'Open sidebar'}
          >
            {sidebarOpen ? '‹' : '›'}
          </button>
        </div>

        <nav className="sidebar-nav">
          <ul>
            <li>
              <a
                href="#"
                onClick={(e) => {
                  e.preventDefault()
                  navigate('/dashboard')
                }}
                className="nav-link"
              >
                <span className="icon">📊</span>
                {sidebarOpen && <span>Dashboard</span>}
              </a>
            </li>
            <li>
              <a
                href="#"
                onClick={(e) => {
                  e.preventDefault()
                  navigate('/projects')
                }}
                className="nav-link"
              >
                <span className="icon">📁</span>
                {sidebarOpen && <span>Projects</span>}
              </a>
            </li>
            <li>
              <a
                href="#"
                onClick={(e) => {
                  e.preventDefault()
                }}
                className="nav-link"
              >
                <span className="icon">💬</span>
                {sidebarOpen && <span>Messages</span>}
              </a>
            </li>
            <li>
              <a
                href="#"
                onClick={(e) => {
                  e.preventDefault()
                }}
                className="nav-link"
              >
                <span className="icon">⚙️</span>
                {sidebarOpen && <span>Settings</span>}
              </a>
            </li>
          </ul>
        </nav>

        <div className="sidebar-footer">
          <button
            className="logout-btn"
            onClick={handleLogout}
            title="Logout"
          >
            <span className="icon">🚪</span>
            {sidebarOpen && <span>Logout</span>}
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <div className="layout-content">
        {/* Header */}
        <header className="header">
          <div className="header-left">
            <button
              className="mobile-toggle-btn"
              onClick={() => setSidebarOpen(!sidebarOpen)}
              title={sidebarOpen ? 'Close sidebar' : 'Open sidebar'}
            >
              ☰
            </button>
          </div>

          <div className="header-center">
            <h1>Socrates 8.0</h1>
          </div>

          <div className="header-right">
            <div className="user-info">
              <span className="user-name">{user?.name || 'User'}</span>
              <div className="user-avatar">
                {user?.name?.charAt(0).toUpperCase() || 'U'}
              </div>
            </div>
          </div>
        </header>

        {/* Content Area */}
        <main className="main-content">
          {children}
        </main>

        {/* Footer */}
        <footer className="footer">
          <p>&copy; 2025 Socrates 8.0. All rights reserved.</p>
          <div className="footer-links">
            <a href="#about">About</a>
            <a href="#privacy">Privacy</a>
            <a href="#terms">Terms</a>
          </div>
        </footer>
      </div>
    </div>
  )
}
