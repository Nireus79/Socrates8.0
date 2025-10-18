import React, { useEffect, useState, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { api } from '../services/api'
import { Session as SessionType, Message } from '../types/models'
import './Pages.css'

export const Session: React.FC = () => {
  const { sessionId } = useParams<{ sessionId: string }>()
  const navigate = useNavigate()
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const [session, setSession] = useState<SessionType | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [messageInput, setMessageInput] = useState('')
  const [sending, setSending] = useState(false)

  useEffect(() => {
    const fetchSessionData = async () => {
      if (!sessionId) {
        setError('Session not found')
        setLoading(false)
        return
      }

      try {
        const sessionRes = await api.getSession(sessionId)
        setSession(sessionRes.data)

        const messagesRes = await api.getMessages(sessionId)
        setMessages(messagesRes.data || [])
      } catch (err) {
        console.error('Failed to fetch session:', err)
        setError('Failed to load session')
      } finally {
        setLoading(false)
      }
    }

    fetchSessionData()
  }, [sessionId])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!messageInput.trim() || !sessionId) return

    setSending(true)
    try {
      const response = await api.sendMessage(sessionId, messageInput, 'user')
      setMessages([...messages, response.data])
      setMessageInput('')

      // TODO: Implement AI response handling via WebSocket or polling
    } catch (err) {
      console.error('Failed to send message:', err)
      setError('Failed to send message')
    } finally {
      setSending(false)
    }
  }

  if (loading) {
    return (
      <div className="page-container">
        <div className="loading">Loading session...</div>
      </div>
    )
  }

  if (error || !session) {
    return (
      <div className="page-container">
        <div className="error-message">{error || 'Session not found'}</div>
        <button className="btn btn-secondary" onClick={() => navigate('/projects')}>
          Back to Projects
        </button>
      </div>
    )
  }

  return (
    <div className="page-container session-container">
      <div className="session-header">
        <button className="back-btn" onClick={() => navigate('/projects')}>
          ← Back
        </button>
        <h2>{session.title || 'Untitled Session'}</h2>
        <span className={`status ${session.status}`}>{session.status}</span>
      </div>

      <div className="session-content">
        <div className="messages-container">
          {messages.length === 0 ? (
            <div className="empty-messages">
              <p>No messages yet. Start the conversation!</p>
            </div>
          ) : (
            <>
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`message ${message.type}`}
                >
                  <div className="message-avatar">
                    {message.type === 'user' ? '👤' : '🤖'}
                  </div>
                  <div className="message-content">
                    <span className="message-type">
                      {message.type === 'user' ? 'You' : 'AI'}
                    </span>
                    <p>{message.content}</p>
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </>
          )}
        </div>

        <form className="message-form" onSubmit={handleSendMessage}>
          <input
            type="text"
            placeholder="Type your message..."
            value={messageInput}
            onChange={(e) => setMessageInput(e.target.value)}
            disabled={sending}
            className="message-input"
          />
          <button
            type="submit"
            disabled={sending || !messageInput.trim()}
            className="btn btn-primary send-btn"
          >
            {sending ? 'Sending...' : 'Send'}
          </button>
        </form>
      </div>
    </div>
  )
}
