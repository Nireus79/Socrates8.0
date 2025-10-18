import React, { useEffect, useState } from 'react'
import { useAuth } from '../context/AuthContext'
import { api } from '../services/api'
import { CreateProjectModal } from '../components/CreateProjectModal'
import './Pages.css'

export const Dashboard: React.FC = () => {
  const { user } = useAuth()
  const [stats, setStats] = useState({
    projectCount: 0,
    sessionCount: 0,
    messageCount: 0,
  })
  const [loading, setLoading] = useState(true)
  const [showCreateProject, setShowCreateProject] = useState(false)

  useEffect(() => {
    // Fetch dashboard stats
    const fetchStats = async () => {
      try {
        // These would be actual API calls - for now using mock data
        setStats({
          projectCount: 0,
          sessionCount: 0,
          messageCount: 0,
        })
      } catch (error) {
        console.error('Failed to fetch stats:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchStats()
  }, [])

  return (
    <div className="page-container">
      <div className="page-header">
        <h2>Dashboard</h2>
        <p>Welcome back, {user?.name}!</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">📁</div>
          <div className="stat-content">
            <h3>Projects</h3>
            <p className="stat-value">{loading ? '-' : stats.projectCount}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">💬</div>
          <div className="stat-content">
            <h3>Sessions</h3>
            <p className="stat-value">{loading ? '-' : stats.sessionCount}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">✉️</div>
          <div className="stat-content">
            <h3>Messages</h3>
            <p className="stat-value">{loading ? '-' : stats.messageCount}</p>
          </div>
        </div>
      </div>

      <div className="dashboard-sections">
        <section className="dashboard-section">
          <h3>Recent Projects</h3>
          <div className="empty-state">
            <p>No projects yet. Create your first project to get started!</p>
            <button
              className="btn btn-primary"
              onClick={() => setShowCreateProject(true)}
            >
              New Project
            </button>
          </div>
        </section>

        <section className="dashboard-section">
          <h3>Recent Sessions</h3>
          <div className="empty-state">
            <p>No active sessions. Start a new session to begin learning!</p>
            <button className="btn btn-primary" onClick={() => setShowCreateProject(true)}>
              New Session
            </button>
          </div>
        </section>
      </div>

      <CreateProjectModal
        isOpen={showCreateProject}
        onClose={() => setShowCreateProject(false)}
        onSuccess={() => {
          // Refresh stats
          setLoading(true)
        }}
      />
    </div>
  )
}
