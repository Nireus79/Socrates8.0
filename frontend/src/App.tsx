import React, { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [backendStatus, setBackendStatus] = useState('Connecting...')
  const [showAlert, setShowAlert] = useState('')

  useEffect(() => {
    // Check backend connection
    fetch('http://localhost:8000/health')
      .then(res => res.json())
      .then(data => setBackendStatus('✓ Connected'))
      .catch(() => setBackendStatus('✗ Disconnected'))
  }, [])

  const handleGetStarted = () => {
    setShowAlert('Get Started clicked! Navigation to session creation would go here.')
    setTimeout(() => setShowAlert(''), 3000)
  }

  const handleLearnMore = () => {
    setShowAlert('Learn More clicked! Documentation would open here.')
    setTimeout(() => setShowAlert(''), 3000)
  }

  const handleFeatureClick = (feature: string) => {
    setShowAlert(`${feature} feature clicked!`)
    setTimeout(() => setShowAlert(''), 3000)
  }

  return (
    <div className="App">
      {showAlert && (
        <div className="alert">
          {showAlert}
        </div>
      )}

      <header className="app-header">
        <h1>Socrates 8.0</h1>
        <p>AI-Powered Socratic Learning Platform</p>
        <div className="status">
          <p>Backend API: <span className="status-check">{backendStatus}</span></p>
          <p>WebSocket: <span className="status-check">✓ Ready</span></p>
        </div>
      </header>

      <main className="app-main">
        <section className="welcome">
          <h2>Welcome to Socrates 8.0</h2>
          <p>An AI-powered platform for Socratic questioning and guided learning.</p>

          <div className="features">
            <div
              className="feature-card"
              onClick={() => handleFeatureClick('Interactive Sessions')}
              style={{ cursor: 'pointer' }}
            >
              <h3>Interactive Sessions</h3>
              <p>Engage in guided conversations with AI mentors</p>
            </div>

            <div
              className="feature-card"
              onClick={() => handleFeatureClick('Real-time Collaboration')}
              style={{ cursor: 'pointer' }}
            >
              <h3>Real-time Collaboration</h3>
              <p>WebSocket-powered live communication</p>
            </div>

            <div
              className="feature-card"
              onClick={() => handleFeatureClick('Project Management')}
              style={{ cursor: 'pointer' }}
            >
              <h3>Project Management</h3>
              <p>Organize and track your learning journey</p>
            </div>
          </div>

          <div className="cta-section">
            <button className="btn btn-primary" onClick={handleGetStarted}>
              Get Started
            </button>
            <button className="btn btn-secondary" onClick={handleLearnMore}>
              Learn More
            </button>
          </div>
        </section>

        <section className="tech-stack">
          <h3>Technology Stack</h3>
          <ul>
            <li><strong>Backend:</strong> FastAPI (Python 3.12)</li>
            <li><strong>Frontend:</strong> React 18 + TypeScript + Vite</li>
            <li><strong>Real-time:</strong> WebSockets + Socket.io</li>
            <li><strong>Database:</strong> PostgreSQL + SQLAlchemy ORM</li>
            <li><strong>Styling:</strong> Tailwind CSS</li>
          </ul>
        </section>
      </main>

      <footer className="app-footer">
        <p>&copy; 2025 Socrates 8.0. All rights reserved.</p>
      </footer>
    </div>
  )
}

export default App
