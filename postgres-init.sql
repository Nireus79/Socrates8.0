-- PostgreSQL initialization script for Socrates 8.0
-- This script runs automatically when the PostgreSQL container starts

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Set client encoding
SET client_encoding = 'UTF8';

-- Create schema
CREATE SCHEMA IF NOT EXISTS socrates;

-- Grant privileges
GRANT USAGE ON SCHEMA socrates TO socrates;
GRANT CREATE ON SCHEMA socrates TO socrates;

-- Alter session to use the socrates schema by default
ALTER USER socrates SET search_path TO socrates, public;
