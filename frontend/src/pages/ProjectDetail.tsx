import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { api } from '../services/api'
import { Project, Session } from '../types/models'
import './Pages.css'

export const ProjectDetail: React.FC = () => {
  const { projectId } = useParams<{ projectId: string }>()
  const navigate = useNavigate()
  const [project, setProject] = useState<Project | null>(null)
  const [sessions, setSessions] = useState<Session[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchProjectData = async () => {
      if (!projectId) {
        setError('Project not found')
        setLoading(false)
        return
      }

      try {
        const projectRes = await api.getProject(projectId)
        setProject(projectRes.data)

        // Fetch sessions for this project
        const sessionsRes = await api.getSessions()
        const projectSessions = sessionsRes.data?.filter(
          (s: Session) => s.project_id === projectId
        ) || []
        setSessions(projectSessions)
      } catch (err) {
        console.error('Failed to fetch project:', err)
        setError('Failed to load project')
      } finally {
        setLoading(false)
      }
    }

    fetchProjectData()
  }, [projectId])

  const handleSessionClick = (sessionId: string) => {
    navigate(`/sessions/${sessionId}`)
  }

  const handleNewSession = () => {
    // TODO: Show modal or navigate to create session page
    console.log('Create new session for project:', projectId)
  }

  if (loading) {
    return (
      <div className="page-container">
        <div className="loading">Loading project...</div>
      </div>
    )
  }

  if (error || !project) {
    return (
      <div className="page-container">
        <div className="error-message">{error || 'Project not found'}</div>
        <button className="btn btn-secondary" onClick={() => navigate('/projects')}>
          Back to Projects
        </button>
      </div>
    )
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <button className="back-btn" onClick={() => navigate('/projects')}>
          ← Back
        </button>
        <h2>{project.title || 'Untitled Project'}</h2>
        <p>{project.description || 'No description'}</p>
        <button className="btn btn-primary" onClick={handleNewSession}>
          + New Session
        </button>
      </div>

      <div className="project-content">
        <section className="project-info">
          <h3>Project Information</h3>
          <div className="info-grid">
            <div className="info-item">
              <label>Status</label>
              <span className={`status ${project.status}`}>{project.status}</span>
            </div>
            <div className="info-item">
              <label>Created</label>
              <span>{new Date(project.created_at).toLocaleDateString()}</span>
            </div>
            <div className="info-item">
              <label>Last Updated</label>
              <span>{new Date(project.updated_at).toLocaleDateString()}</span>
            </div>
          </div>
        </section>

        <section className="project-sessions">
          <h3>Sessions ({sessions.length})</h3>
          {sessions.length === 0 ? (
            <div className="empty-state">
              <p>No sessions yet. Create your first session to begin.</p>
              <button className="btn btn-primary" onClick={handleNewSession}>
                New Session
              </button>
            </div>
          ) : (
            <div className="sessions-list">
              {sessions.map((session) => (
                <div
                  key={session.id}
                  className="session-item"
                  onClick={() => handleSessionClick(session.id)}
                >
                  <h4>{session.title || 'Untitled Session'}</h4>
                  <p>{session.status}</p>
                </div>
              ))}
            </div>
          )}
        </section>
      </div>
    </div>
  )
}
