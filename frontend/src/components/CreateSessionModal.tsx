import React, { useState } from 'react'
import { Modal } from './Modal'
import { api } from '../services/api'

interface CreateSessionModalProps {
  isOpen: boolean
  projectId: string
  onClose: () => void
  onSuccess: () => void
}

export const CreateSessionModal: React.FC<CreateSessionModalProps> = ({
  isOpen,
  projectId,
  onClose,
  onSuccess,
}) => {
  const [formData, setFormData] = useState({
    title: '',
    mode: 'chat' as 'chat' | 'question' | 'teaching' | 'review',
    role_description: '',
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const modes = [
    { value: 'chat', label: 'Chat', description: 'Free-form conversation' },
    { value: 'question', label: 'Q&A', description: 'Answer specific questions' },
    { value: 'teaching', label: 'Teaching', description: 'AI teaches you' },
    { value: 'review', label: 'Review', description: 'Review and feedback' },
  ]

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
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
      await api.createSession({
        project_id: projectId,
        title: formData.title,
        mode: formData.mode,
        role_description: formData.role_description,
      })

      setFormData({ title: '', mode: 'chat', role_description: '' })
      onSuccess()
      onClose()
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Failed to create session'
      setError(errorMessage)
    } finally {
      setLoading(false)
    }
  }

  const handleClose = () => {
    setFormData({ title: '', mode: 'chat', role_description: '' })
    setError('')
    onClose()
  }

  return (
    <Modal
      isOpen={isOpen}
      title="Create New Session"
      onClose={handleClose}
      size="medium"
    >
      <form onSubmit={handleSubmit} className="form">
        {error && <div className="form-error">{error}</div>}

        <div className="form-group">
          <label htmlFor="title">Session Name *</label>
          <input
            id="title"
            type="text"
            name="title"
            placeholder="e.g., React Hooks Tutorial"
            value={formData.title}
            onChange={handleChange}
            required
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="mode">Session Mode *</label>
          <select
            id="mode"
            name="mode"
            value={formData.mode}
            onChange={handleChange}
            disabled={loading}
          >
            {modes.map((m) => (
              <option key={m.value} value={m.value}>
                {m.label} - {m.description}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="role_description">AI Role Description</label>
          <textarea
            id="role_description"
            name="role_description"
            placeholder="Describe how the AI should behave. E.g., 'Act as a friendly Python tutor, explain concepts with examples'"
            value={formData.role_description}
            onChange={handleChange}
            disabled={loading}
            rows={4}
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
            {loading ? 'Creating...' : 'Create Session'}
          </button>
        </div>
      </form>
    </Modal>
  )
}
