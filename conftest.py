"""
Pytest configuration: sets required environment variables for test runs.
"""
import os

# Set a deterministic test key for HMAC audit trail validation
os.environ.setdefault("AUDIT_SECRET_KEY", "test-audit-key-for-pytest-only-do-not-use-in-production")
