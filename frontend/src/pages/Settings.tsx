import React, { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import { api } from '../services/api'
import './Pages.css'

export const Settings: React.FC = () => {
  const { user } = useAuth()
  const [theme, setTheme] = useState('light')
  const [llmModel, setLlmModel] = useState('claude-3-sonnet')
  const [temperature, setTemperature] = useState(0.7)
  const [maxTokens, setMaxTokens] = useState(2000)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [message, setMessage] = useState('')

  useEffect(() => {
    fetchSettings()
  }, [])

  const fetchSettings = async () => {
    try {
      const response = await api.get('/profile/settings')
      const settings = response.data.data || response.data
      setTheme(settings.theme || 'light')
      setLlmModel(settings.llm_model || 'claude-3-sonnet')
      setTemperature(settings.temperature || 0.7)
      setMaxTokens(settings.max_tokens || 2000)
    } catch (err) {
      console.error('Failed to fetch settings:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleSave = async () => {
    setSaving(true)
    try {
      await api.put('/profile/settings', {
        theme,
        llm_model: llmModel,
        temperature,
        max_tokens: maxTokens,
      })
      setMessage('Settings saved successfully!')
      setTimeout(() => setMessage(''), 3000)
    } catch (err) {
      console.error('Failed to save settings:', err)
      setMessage('Failed to save settings')
      setTimeout(() => setMessage(''), 3000)
    } finally {
      setSaving(false)
    }
  }

  if (loading) {
    return (
      <div className="page-container">
        <div className="loading">Loading settings...</div>
      </div>
    )
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h2>Settings</h2>
        <p>Configure your preferences and AI settings</p>
      </div>

      {message && (
        <div className={`message-banner ${message.includes('Failed') ? 'error' : 'success'}`}>
          {message}
        </div>
      )}

      <div className="settings-content">
        <div className="settings-section">
          <h3>Appearance</h3>
          <div className="form-group">
            <label htmlFor="theme">Theme</label>
            <select
              id="theme"
              value={theme}
              onChange={(e) => setTheme(e.target.value)}
            >
              <option value="light">Light</option>
              <option value="dark">Dark</option>
              <option value="auto">Auto</option>
            </select>
          </div>
        </div>

        <div className="settings-section">
          <h3>AI Model Settings</h3>
          <div className="form-group">
            <label htmlFor="llmModel">LLM Model</label>
            <select
              id="llmModel"
              value={llmModel}
              onChange={(e) => setLlmModel(e.target.value)}
            >
              <option value="claude-3-sonnet">Claude 3 Sonnet</option>
              <option value="claude-3-opus">Claude 3 Opus</option>
              <option value="claude-3-haiku">Claude 3 Haiku</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="temperature">
              Temperature: <span className="value">{temperature.toFixed(2)}</span>
            </label>
            <input
              id="temperature"
              type="range"
              min="0"
              max="1"
              step="0.1"
              value={temperature}
              onChange={(e) => setTemperature(parseFloat(e.target.value))}
            />
            <p className="help-text">
              Lower values (0-0.5) for focused responses, higher values (0.7-1.0) for creative responses
            </p>
          </div>

          <div className="form-group">
            <label htmlFor="maxTokens">
              Max Tokens: <span className="value">{maxTokens}</span>
            </label>
            <input
              id="maxTokens"
              type="range"
              min="100"
              max="4000"
              step="100"
              value={maxTokens}
              onChange={(e) => setMaxTokens(parseInt(e.target.value))}
            />
            <p className="help-text">Maximum length of AI responses</p>
          </div>
        </div>

        <div className="settings-section">
          <h3>Account Information</h3>
          <div className="info-item">
            <label>Email</label>
            <p>{user?.email}</p>
          </div>
          <div className="info-item">
            <label>Name</label>
            <p>{user?.name}</p>
          </div>
          <div className="info-item">
            <label>Member Since</label>
            <p>{user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}</p>
          </div>
        </div>

        <div className="settings-actions">
          <button
            className="btn btn-primary"
            onClick={handleSave}
            disabled={saving}
          >
            {saving ? 'Saving...' : 'Save Settings'}
          </button>
        </div>
      </div>
    </div>
  )
}
