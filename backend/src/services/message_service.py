"""Message service for conversation handling."""

from typing import List, Tuple, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from anthropic import Anthropic

from backend.src.models import Message
from backend.src.repositories import MessageRepository, SessionRepository
from backend.src.services.base_service import BaseService


class MessageService(BaseService):
    """Service for message handling and AI responses."""

    def __init__(self, db: Session, anthropic_api_key: str):
        """Initialize message service.

        Args:
            db: SQLAlchemy session
            anthropic_api_key: Anthropic API key
        """
        super().__init__(db)
        self.repo = MessageRepository(db)
        self.session_repo = SessionRepository(db)
        self.client = Anthropic(api_key=anthropic_api_key)

    def send_message(
        self,
        session_id: UUID,
        user_id: UUID,
        content: str,
        message_type: str = "text"
    ) -> Tuple[Message, Message]:
        """Send user message and generate assistant response.

        Args:
            session_id: Session ID
            user_id: User ID
            content: Message content
            message_type: Message type (text, code, question)

        Returns:
            Tuple of (user_message, assistant_message)

        Raises:
            ValueError: If validation fails
        """
        # Validate input
        if not content or len(content.strip()) == 0:
            raise ValueError("Message content cannot be empty")

        if len(content) > 10000:
            raise ValueError("Message content too long (max 10000 characters)")

        # Verify session exists
        session = self.session_repo.get_by_id(session_id)
        if not session:
            raise ValueError("Session not found")

        if session.owner_id != user_id:
            raise ValueError("Not authorized for this session")

        # Save user message
        user_message = Message(
            session_id=session_id,
            user_id=user_id,
            role="user",
            content=content,
            message_type=message_type
        )
        self.db.add(user_message)
        self.flush()

        # Generate assistant response
        try:
            response_text = self._generate_response(session_id, content)
        except Exception as e:
            self.logger.error(f"Response generation failed: {e}")
            raise ValueError("Failed to generate AI response")

        # Save assistant message
        assistant_message = Message(
            session_id=session_id,
            user_id=user_id,
            role="assistant",
            content=response_text,
            message_type="text"
        )
        self.db.add(assistant_message)
        self.commit()

        self.logger.info(f"Message sent in session: {session_id}")
        return user_message, assistant_message

    def _generate_response(self, session_id: UUID, user_input: str) -> str:
        """Generate response using Claude API.

        Args:
            session_id: Session ID for context
            user_input: User input

        Returns:
            AI-generated response

        Raises:
            Exception: If API call fails
        """
        # Get session for mode and role information
        session = self.session_repo.get_by_id(session_id)

        # Get message history for context (last 10 messages)
        messages_history = self.repo.get_by_session_sorted(
            session_id,
            limit=10,
            sort_order="asc"
        )

        # Build message list for API
        messages = []
        for msg in messages_history:
            messages.append({
                "role": msg.role,
                "content": msg.content
            })

        # Add current message
        messages.append({
            "role": "user",
            "content": user_input
        })

        # Get system prompt based on session mode
        system_prompt = self._get_system_prompt(session)

        # Call Claude API with system prompt
        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                system=system_prompt,
                messages=messages
            )
            return response.content[0].text
        except Exception as e:
            self.logger.error(f"Claude API call failed: {e}")
            # Return a fallback message
            return "I apologize, but I'm experiencing technical difficulties. Please try again in a moment."

    def _get_system_prompt(self, session) -> str:
        """Get system prompt based on session mode and role.

        Args:
            session: Session object

        Returns:
            System prompt string
        """
        mode = session.mode if session else "chat"
        role = session.role if session and session.role else "AI Assistant"

        base_prompt = f"You are {role}. Be helpful, respectful, and educational. "

        mode_prompts = {
            "chat": "Engage in friendly conversation and help the user with their questions. Be conversational and approachable.",
            "question": "Help the user answer specific questions. Provide clear, concise explanations. Ask clarifying questions if needed.",
            "teaching": "Act as a teacher/mentor. Explain concepts clearly, provide examples, and help the user understand the material. Encourage learning and ask probing questions.",
            "review": "Review the user's work constructively. Point out strengths, areas for improvement, and provide specific suggestions. Be encouraging but honest."
        }

        system_prompt = base_prompt + mode_prompts.get(mode, mode_prompts["chat"])
        return system_prompt

    def get_session_messages(
        self,
        session_id: UUID,
        user_id: UUID,
        skip: int = 0,
        limit: int = 50
    ) -> List[Message]:
        """Get messages for session.

        Args:
            session_id: Session ID
            user_id: User ID (for authorization)
            skip: Number to skip
            limit: Limit

        Returns:
            List of messages

        Raises:
            ValueError: If not authorized
        """
        session = self.session_repo.get_by_id(session_id)

        if not session:
            raise ValueError("Session not found")

        if session.owner_id != user_id:
            raise ValueError("Not authorized for this session")

        return self.repo.get_by_session(session_id, skip=skip, limit=limit)

    def delete_message(self, message_id: UUID, user_id: UUID) -> bool:
        """Delete message.

        Args:
            message_id: Message ID
            user_id: User ID (for authorization)

        Returns:
            True if deleted

        Raises:
            ValueError: If authorization fails
        """
        message = self.repo.get_by_id(message_id)

        if not message:
            raise ValueError("Message not found")

        if message.user_id != user_id:
            raise ValueError("Not authorized to delete this message")

        self.db.delete(message)
        self.commit()

        self.logger.info(f"Message deleted: {message_id}")
        return True

    def get_message_count_for_session(self, session_id: UUID) -> int:
        """Get message count for session.

        Args:
            session_id: Session ID

        Returns:
            Message count
        """
        return self.repo.get_by_session_count(session_id)

    def count_messages(self, session_id: UUID = None) -> int:
        """Count messages for session.

        Args:
            session_id: Session ID

        Returns:
            Count of messages
        """
        from sqlalchemy import func
        query = self.db.query(func.count(Message.id))

        if session_id:
            query = query.filter(Message.session_id == session_id)

        return query.scalar()

    def get_messages_paginated(
        self,
        session_id: UUID,
        page: int = 1,
        limit: int = 50
    ) -> List[Message]:
        """Get paginated messages for session.

        Args:
            session_id: Session ID
            page: Page number (1-indexed)
            limit: Items per page

        Returns:
            List of messages
        """
        query = self.db.query(Message).filter(Message.session_id == session_id)

        # Sort by created_at ascending (oldest first)
        query = query.order_by(Message.created_at.asc())

        # Apply pagination
        skip = (page - 1) * limit
        return query.offset(skip).limit(limit).all()
