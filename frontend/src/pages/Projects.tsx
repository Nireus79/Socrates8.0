import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../services/api'
import { Project } from '../types/models'
import './Pages.css'

export const Projects: React.FC = () => {
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const response = await api.getProjects()
        setProjects(response.data || [])
      } catch (err) {
        console.error('Failed to fetch projects:', err)
        setError('Failed to load projects')
      } finally {
        setLoading(false)
      }
    }

    fetchProjects()
  }, [])

  const handleProjectClick = (projectId: string) => {
    navigate(`/projects/${projectId}`)
  }

  const handleNewProject = () => {
    // TODO: Show modal or navigate to create project page
    console.log('Create new project')
  }

  if (loading) {
    return (
      <div className="page-container">
        <div className="loading">Loading projects...</div>
      </div>
    )
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h2>Projects</h2>
        <p>Manage your learning projects</p>
        <button className="btn btn-primary" onClick={handleNewProject}>
          + New Project
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {projects.length === 0 ? (
        <div className="empty-state">
          <h3>No projects yet</h3>
          <p>Create your first project to organize your learning journey.</p>
          <button className="btn btn-primary" onClick={handleNewProject}>
            Create Project
          </button>
        </div>
      ) : (
        <div className="projects-grid">
          {projects.map((project) => (
            <div
              key={project.id}
              className="project-card"
              onClick={() => handleProjectClick(project.id)}
            >
              <h3>{project.title || 'Untitled Project'}</h3>
              <p>{project.description || 'No description'}</p>
              <div className="project-meta">
                <span className={`status ${project.status}`}>
                  {project.status}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
