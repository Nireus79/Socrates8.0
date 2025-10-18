"""User service for user management."""

import re
from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from backend.src.models import User
from backend.src.repositories import UserRepository
from backend.src.services.base_service import BaseService

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class UserService(BaseService):
    """Service for user management."""

    def __init__(self, db: Session):
        """Initialize user service."""
        super().__init__(db)
        self.repo = UserRepository(db)

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password securely.

        Args:
            password: Plain password

        Returns:
            Hashed password
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain: str, hashed: str) -> bool:
        """Verify password.

        Args:
            plain: Plain password
            hashed: Hashed password

        Returns:
            True if passwords match
        """
        return pwd_context.verify(plain, hashed)

    @staticmethod
    def _validate_password(password: str) -> tuple[bool, str]:
        """Validate password strength.

        Args:
            password: Password to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters"

        if not re.search(r"[a-z]", password):
            return False, "Password must contain lowercase letters"

        if not re.search(r"[A-Z]", password):
            return False, "Password must contain uppercase letters"

        if not re.search(r"\d", password):
            return False, "Password must contain numbers"

        return True, ""

    @staticmethod
    def _validate_email(email: str) -> bool:
        """Validate email format.

        Args:
            email: Email to validate

        Returns:
            True if valid email format
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def register_user(
        self,
        username: str,
        email: str,
        password: str,
        first_name: str = None,
        last_name: str = None
    ) -> User:
        """Register new user.

        Args:
            username: Username
            email: Email address
            password: Plain password
            first_name: First name (optional)
            last_name: Last name (optional)

        Returns:
            Created user

        Raises:
            ValueError: If validation fails
        """
        # Validate inputs
        if not username or len(username.strip()) < 3:
            raise ValueError("Username must be at least 3 characters")

        if not self._validate_email(email):
            raise ValueError("Invalid email format")

        is_valid, error_msg = self._validate_password(password)
        if not is_valid:
            raise ValueError(error_msg)

        # Check if user already exists
        if self.repo.get_by_username(username):
            raise ValueError("Username already exists")

        if self.repo.get_by_email(email):
            raise ValueError("Email already exists")

        # Create user
        user = User(
            username=username,
            email=email,
            password_hash=self.hash_password(password),
            first_name=first_name,
            last_name=last_name,
            status="ACTIVE"
        )
        self.db.add(user)
        self.commit()

        self.logger.info(f"User created: {username}")
        return user

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate user.

        Args:
            username: Username
            password: Plain password

        Returns:
            User if authenticated, None otherwise
        """
        user = self.repo.get_by_username(username)

        if not user:
            self.logger.warning(f"Login attempt for non-existent user: {username}")
            return None

        if not self.verify_password(password, user.password_hash):
            self.logger.warning(f"Failed login attempt for user: {username}")
            return None

        self.logger.info(f"User authenticated: {username}")
        return user

    def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID.

        Args:
            user_id: User ID

        Returns:
            User or None
        """
        return self.repo.get_by_id(user_id)

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username.

        Args:
            username: Username

        Returns:
            User or None
        """
        return self.repo.get_by_username(username)

    def update_profile(
        self,
        user_id: UUID,
        first_name: str = None,
        last_name: str = None,
        bio: str = None,
        avatar_url: str = None
    ) -> User:
        """Update user profile.

        Args:
            user_id: User ID
            first_name: New first name
            last_name: New last name
            bio: New bio
            avatar_url: New avatar URL

        Returns:
            Updated user

        Raises:
            ValueError: If user not found
        """
        user = self.repo.get_by_id(user_id)

        if not user:
            raise ValueError("User not found")

        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if bio is not None:
            user.bio = bio
        if avatar_url is not None:
            user.avatar_url = avatar_url

        self.commit()
        self.logger.info(f"User profile updated: {user_id}")
        return user

    def change_password(
        self,
        user_id: UUID,
        current_password: str,
        new_password: str
    ) -> bool:
        """Change user password.

        Args:
            user_id: User ID
            current_password: Current password
            new_password: New password

        Returns:
            True if successful

        Raises:
            ValueError: If validation fails
        """
        user = self.repo.get_by_id(user_id)

        if not user:
            raise ValueError("User not found")

        # Verify current password
        if not self.verify_password(current_password, user.password_hash):
            raise ValueError("Current password is incorrect")

        # Validate new password
        is_valid, error_msg = self._validate_password(new_password)
        if not is_valid:
            raise ValueError(error_msg)

        # Update password
        user.password_hash = self.hash_password(new_password)
        self.commit()

        self.logger.info(f"Password changed for user: {user_id}")
        return True

    def deactivate_user(self, user_id: UUID) -> User:
        """Deactivate user account.

        Args:
            user_id: User ID

        Returns:
            Updated user

        Raises:
            ValueError: If user not found
        """
        user = self.repo.get_by_id(user_id)

        if not user:
            raise ValueError("User not found")

        user.status = "INACTIVE"
        self.commit()

        self.logger.info(f"User deactivated: {user_id}")
        return user

    def activate_user(self, user_id: UUID) -> User:
        """Activate user account.

        Args:
            user_id: User ID

        Returns:
            Updated user

        Raises:
            ValueError: If user not found
        """
        user = self.repo.get_by_id(user_id)

        if not user:
            raise ValueError("User not found")

        user.status = "ACTIVE"
        self.commit()

        self.logger.info(f"User activated: {user_id}")
        return user
