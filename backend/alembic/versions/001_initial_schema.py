"""Initial schema creation with all 7 tables.

Revision ID: 001_initial_schema
Revises:
Create Date: 2025-10-17 18:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.String(32), nullable=False),
        sa.Column('username', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('first_name', sa.String(255), nullable=True),
        sa.Column('last_name', sa.String(255), nullable=True),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('avatar_url', sa.String(500), nullable=True),
        sa.Column('status', sa.String(50), nullable=False, server_default='ACTIVE'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )
    op.create_index('idx_users_email', 'users', ['email'])
    op.create_index('idx_users_status', 'users', ['status'])
    op.create_index('idx_users_username', 'users', ['username'])

    # Create projects table
    op.create_table(
        'projects',
        sa.Column('id', sa.String(32), nullable=False),
        sa.Column('owner_id', sa.String(32), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(50), nullable=False, server_default='PLANNING'),
        sa.Column('technology_stack', sa.JSON(), nullable=False, server_default='[]'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_projects_created', 'projects', ['created_at'])
    op.create_index('idx_projects_owner', 'projects', ['owner_id'])
    op.create_index('idx_projects_status', 'projects', ['status'])

    # Create sessions table
    op.create_table(
        'sessions',
        sa.Column('id', sa.String(32), nullable=False),
        sa.Column('owner_id', sa.String(32), nullable=False),
        sa.Column('project_id', sa.String(32), nullable=True),
        sa.Column('name', sa.String(255), nullable=True),
        sa.Column('status', sa.String(50), nullable=False, server_default='ACTIVE'),
        sa.Column('mode', sa.String(50), nullable=False, server_default='chat'),
        sa.Column('role', sa.String(100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('archived_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_sessions_created', 'sessions', ['created_at'])
    op.create_index('idx_sessions_owner', 'sessions', ['owner_id'])
    op.create_index('idx_sessions_project', 'sessions', ['project_id'])
    op.create_index('idx_sessions_status', 'sessions', ['status'])

    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', sa.String(32), nullable=False),
        sa.Column('session_id', sa.String(32), nullable=False),
        sa.Column('user_id', sa.String(32), nullable=False),
        sa.Column('role', sa.String(50), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('message_type', sa.String(50), nullable=False, server_default='text'),
        sa.Column('meta', sa.JSON(), nullable=False, server_default='{}'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['session_id'], ['sessions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_messages_created', 'messages', ['created_at'])
    op.create_index('idx_messages_role', 'messages', ['role'])
    op.create_index('idx_messages_session', 'messages', ['session_id'])
    op.create_index('idx_messages_user', 'messages', ['user_id'])

    # Create user_preferences table
    op.create_table(
        'user_preferences',
        sa.Column('id', sa.String(32), nullable=False),
        sa.Column('user_id', sa.String(32), nullable=False),
        sa.Column('theme', sa.String(50), nullable=False, server_default='dark'),
        sa.Column('llm_model', sa.String(255), nullable=False, server_default='claude-3-sonnet'),
        sa.Column('llm_temperature', sa.Float(), nullable=False, server_default='0.7'),
        sa.Column('llm_max_tokens', sa.Integer(), nullable=False, server_default='2000'),
        sa.Column('ide_type', sa.String(50), nullable=True),
        sa.Column('auto_sync', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('notifications_enabled', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index('idx_preferences_user', 'user_preferences', ['user_id'])

    # Create documents table
    op.create_table(
        'documents',
        sa.Column('id', sa.String(32), nullable=False),
        sa.Column('owner_id', sa.String(32), nullable=False),
        sa.Column('project_id', sa.String(32), nullable=True),
        sa.Column('filename', sa.String(500), nullable=False),
        sa.Column('file_path', sa.String(500), nullable=False),
        sa.Column('file_type', sa.String(50), nullable=True),
        sa.Column('content_summary', sa.Text(), nullable=True),
        sa.Column('vector_id', sa.String(500), nullable=True),
        sa.Column('status', sa.String(50), nullable=False, server_default='PROCESSED'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_documents_owner', 'documents', ['owner_id'])
    op.create_index('idx_documents_project', 'documents', ['project_id'])
    op.create_index('idx_documents_status', 'documents', ['status'])

    # Create audit_log table
    op.create_table(
        'audit_log',
        sa.Column('id', sa.String(32), nullable=False),
        sa.Column('user_id', sa.String(32), nullable=True),
        sa.Column('entity_type', sa.String(100), nullable=True),
        sa.Column('entity_id', sa.String(32), nullable=True),
        sa.Column('action', sa.String(50), nullable=True),
        sa.Column('old_value', sa.JSON(), nullable=True),
        sa.Column('new_value', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_audit_action', 'audit_log', ['action'])
    op.create_index('idx_audit_created', 'audit_log', ['created_at'])
    op.create_index('idx_audit_entity', 'audit_log', ['entity_type', 'entity_id'])
    op.create_index('idx_audit_user', 'audit_log', ['user_id'])


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_index('idx_audit_user', table_name='audit_log')
    op.drop_index('idx_audit_entity', table_name='audit_log')
    op.drop_index('idx_audit_created', table_name='audit_log')
    op.drop_index('idx_audit_action', table_name='audit_log')
    op.drop_table('audit_log')

    op.drop_index('idx_documents_status', table_name='documents')
    op.drop_index('idx_documents_project', table_name='documents')
    op.drop_index('idx_documents_owner', table_name='documents')
    op.drop_table('documents')

    op.drop_index('idx_preferences_user', table_name='user_preferences')
    op.drop_table('user_preferences')

    op.drop_index('idx_messages_user', table_name='messages')
    op.drop_index('idx_messages_session', table_name='messages')
    op.drop_index('idx_messages_role', table_name='messages')
    op.drop_index('idx_messages_created', table_name='messages')
    op.drop_table('messages')

    op.drop_index('idx_sessions_status', table_name='sessions')
    op.drop_index('idx_sessions_project', table_name='sessions')
    op.drop_index('idx_sessions_owner', table_name='sessions')
    op.drop_index('idx_sessions_created', table_name='sessions')
    op.drop_table('sessions')

    op.drop_index('idx_projects_status', table_name='projects')
    op.drop_index('idx_projects_owner', table_name='projects')
    op.drop_index('idx_projects_created', table_name='projects')
    op.drop_table('projects')

    op.drop_index('idx_users_username', table_name='users')
    op.drop_index('idx_users_status', table_name='users')
    op.drop_index('idx_users_email', table_name='users')
    op.drop_table('users')
