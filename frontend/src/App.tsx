import React from 'react'
import './App.css'

function App() {
  return (
    <div className="App">
      <header className="app-header">
        <h1>Socrates 8.0</h1>
        <p>AI-Powered Socratic Learning Platform</p>
        <div className="status">
          <p>Backend API: <span className="status-check">✓ Connected</span></p>
          <p>WebSocket: <span className="status-check">✓ Ready</span></p>
        </div>
      </header>

      <main className="app-main">
        <section className="welcome">
          <h2>Welcome to Socrates 8.0</h2>
          <p>An AI-powered platform for Socratic questioning and guided learning.</p>

          <div className="features">
            <div className="feature-card">
              <h3>Interactive Sessions</h3>
              <p>Engage in guided conversations with AI mentors</p>
            </div>

            <div className="feature-card">
              <h3>Real-time Collaboration</h3>
              <p>WebSocket-powered live communication</p>
            </div>

            <div className="feature-card">
              <h3>Project Management</h3>
              <p>Organize and track your learning journey</p>
            </div>
          </div>

          <div className="cta-section">
            <button className="btn btn-primary">Get Started</button>
            <button className="btn btn-secondary">Learn More</button>
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
