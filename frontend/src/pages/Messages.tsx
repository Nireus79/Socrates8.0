import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../services/api'
import { Message } from '../types/models'
import './Pages.css'

export const Messages: React.FC = () => {
  const navigate = useNavigate()
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [filter, setFilter] = useState<'all' | 'unread' | 'archived'>('all')

  useEffect(() => {
    fetchMessages()
  }, [filter])

  const fetchMessages = async () => {
    try {
      setLoading(true)
      const response = await api.get('/messages', {
        params: { filter },
      })
      setMessages(response.data.data || response.data || [])
    } catch (err) {
      console.error('Failed to fetch messages:', err)
      setError('Failed to load messages')
    } finally {
      setLoading(false)
    }
  }

  const handleMessageClick = (message: Message) => {
    // Navigate to the session where this message belongs
    if (message.session_id) {
      navigate(`/sessions/${message.session_id}`)
    }
  }

  const handleArchive = async (messageId: string) => {
    try {
      await api.post(`/messages/${messageId}/archive`)
      setMessages(messages.filter(m => m.id !== messageId))
    } catch (err) {
      console.error('Failed to archive message:', err)
      setError('Failed to archive message')
    }
  }

  const handleDelete = async (messageId: string) => {
    if (window.confirm('Are you sure you want to delete this message?')) {
      try {
        await api.delete(`/messages/${messageId}`)
        setMessages(messages.filter(m => m.id !== messageId))
      } catch (err) {
        console.error('Failed to delete message:', err)
        setError('Failed to delete message')
      }
    }
  }

  if (loading) {
    return (
      <div className="page-container">
        <div className="loading">Loading messages...</div>
      </div>
    )
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h2>Messages & Activity</h2>
        <p>View your recent messages and notifications</p>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="messages-filters">
        <button
          className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
          onClick={() => setFilter('all')}
        >
          All Messages
        </button>
        <button
          className={`filter-btn ${filter === 'unread' ? 'active' : ''}`}
          onClick={() => setFilter('unread')}
        >
          Unread
        </button>
        <button
          className={`filter-btn ${filter === 'archived' ? 'active' : ''}`}
          onClick={() => setFilter('archived')}
        >
          Archived
        </button>
      </div>

      {messages.length === 0 ? (
        <div className="empty-state">
          <h3>No messages</h3>
          <p>
            {filter === 'all'
              ? 'You don\'t have any messages yet. Start a new session to begin!'
              : `No ${filter} messages found.`}
          </p>
        </div>
      ) : (
        <div className="messages-list">
          {messages.map((message) => (
            <div key={message.id} className="message-item">
              <div className="message-item-header">
                <div className="message-item-title">
                  <span className="message-sender">
                    {message.role === 'user' ? 'You' : 'AI Mentor'}
                  </span>
                  <p className="message-preview">{message.content?.substring(0, 100)}...</p>
                </div>
                <span className="message-date">
                  {new Date(message.created_at).toLocaleDateString()}
                </span>
              </div>
              <div className="message-item-actions">
                <button
                  className="action-btn"
                  onClick={() => handleMessageClick(message)}
                  title="View in session"
                >
                  View
                </button>
                <button
                  className="action-btn"
                  onClick={() => handleArchive(message.id)}
                  title="Archive"
                >
                  Archive
                </button>
                <button
                  className="action-btn delete-btn"
                  onClick={() => handleDelete(message.id)}
                  title="Delete"
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
