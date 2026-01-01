# global_state.py
import threading
from typing import Any, Dict, Optional

class GlobalState:
    """
    A thread-safe singleton class for storing global state across all modules
    """
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(GlobalState, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._storage = {}
            self._lock = threading.RLock()  # Re-entrant lock for nested calls
            self._initialized = True
    
    def set(self, key: str, value: Any) -> None:
        """Set a value in global storage"""
        with self._lock:
            self._storage[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from global storage"""
        with self._lock:
            return self._storage.get(key, default)
    
    def delete(self, key: str) -> bool:
        """Delete a key from global storage"""
        with self._lock:
            if key in self._storage:
                del self._storage[key]
                return True
            return False
    
    def exists(self, key: str) -> bool:
        """Check if a key exists"""
        with self._lock:
            return key in self._storage
    
    def clear(self) -> None:
        """Clear all stored data"""
        with self._lock:
            self._storage.clear()
    
    def keys(self) -> list:
        """Get all keys in storage"""
        with self._lock:
            return list(self._storage.keys())
    
    # Token-specific methods
    def set_token(self, token: str) -> None:
        """Store authentication token"""
        self.set('auth_token', token)
    
    def get_token(self) -> Optional[str]:
        """Get authentication token"""
        return self.get('auth_token')
    
    def delete_token(self) -> None:
        """Delete authentication token"""
        self.delete('auth_token')
    
    def has_token(self) -> bool:
        """Check if token exists"""
        return self.exists('auth_token')
    
    # User-specific methods
    def set_current_user(self, user_data: Dict[str, Any]) -> None:
        """Store current user data"""
        self.set('current_user', user_data)
    
    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Get current user data"""
        return self.get('current_user')
    
    def delete_current_user(self) -> None:
        """Delete current user data"""
        self.delete('current_user')
    
    # Property-style access for common attributes
    @property
    def token(self) -> Optional[str]:
        return self.get_token()
    
    @token.setter
    def token(self, value: str):
        self.set_token(value)
    
    @property
    def current_user(self) -> Optional[Dict[str, Any]]:
        return self.get_current_user()
    
    @current_user.setter
    def current_user(self, value: Dict[str, Any]):
        self.set_current_user(value)

# Create the global instance
global_state = GlobalState()