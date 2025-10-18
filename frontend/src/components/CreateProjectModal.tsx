import React, { useState } from 'react'
import { Modal } from './Modal'
import { api } from '../services/api'

interface CreateProjectModalProps {
  isOpen: boolean
  onClose: () => void
  onSuccess: () => void
}

export const CreateProjectModal: React.FC<CreateProjectModalProps> = ({
  isOpen,
  onClose,
  onSuccess,
}) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    technology_stack: '',
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await api.createProject({
        title: formData.title,
        description: formData.description,
        technology_stack: formData.technology_stack.split(',').map(s => s.trim()),
      })

      setFormData({ title: '', description: '', technology_stack: '' })
      onSuccess()
      onClose()
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Failed to create project'
      setError(errorMessage)
    } finally {
      setLoading(false)
    }
  }

  const handleClose = () => {
    setFormData({ title: '', description: '', technology_stack: '' })
    setError('')
    onClose()
  }

  return (
    <Modal
      isOpen={isOpen}
      title="Create New Project"
      onClose={handleClose}
      size="medium"
    >
      <form onSubmit={handleSubmit} className="form">
        {error && <div className="form-error">{error}</div>}

        <div className="form-group">
          <label htmlFor="title">Project Name *</label>
          <input
            id="title"
            type="text"
            name="title"
            placeholder="e.g., Web Development Course"
            value={formData.title}
            onChange={handleChange}
            required
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="description">Description</label>
          <textarea
            id="description"
            name="description"
            placeholder="Describe your project..."
            value={formData.description}
            onChange={handleChange}
            disabled={loading}
            rows={4}
          />
        </div>

        <div className="form-group">
          <label htmlFor="technology_stack">Technology Stack</label>
          <input
            id="technology_stack"
            type="text"
            name="technology_stack"
            placeholder="e.g., React, TypeScript, Node.js (comma separated)"
            value={formData.technology_stack}
            onChange={handleChange}
            disabled={loading}
          />
        </div>

        <div className="form-actions">
          <button
            type="button"
            className="btn btn-secondary"
            onClick={handleClose}
            disabled={loading}
          >
            Cancel
          </button>
          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading}
          >
            {loading ? 'Creating...' : 'Create Project'}
          </button>
        </div>
      </form>
    </Modal>
  )
}
