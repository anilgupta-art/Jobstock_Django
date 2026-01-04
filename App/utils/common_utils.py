import base64
import os
import re
import hashlib
import secrets
import string
from typing import Any, List, Dict, Optional, Union
import json
from types import SimpleNamespace

from utils.json_read import dict_to_namespace

class CommonUtils:
    
    # ========== VALIDATION METHODS ==========
    
    @staticmethod
    def is_empty(value: Any) -> bool:
        """Check if a value is None, empty string, or empty collection"""
        if value is None:
            return True
        if isinstance(value, str):
            return value.strip() == ""
        if hasattr(value, '__len__'):
            return len(value) == 0
        return False
    
    @staticmethod
    def is_not_empty(value: Any) -> bool:
        """Check if a value is not None and not empty"""
        return not CommonUtils.is_empty(value)
    
    @staticmethod
    def generate_simple_password(length=12):
        """Simple password generator in one line."""
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(secrets.choice(characters) for _ in range(length))
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Validate email format"""
        if CommonUtils.is_empty(email):
            return False
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_regex, email))
    
    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        """Validate phone number (basic validation)"""
        if CommonUtils.is_empty(phone):
            return False
        # Remove spaces, dashes, parentheses
        cleaned = re.sub(r'[\s\-\(\)]', '', phone)
        return bool(re.match(r'^\d{10,15}$', cleaned))
    
    @staticmethod
    def is_numeric(value: str) -> bool:
        """Check if string contains only digits"""
        if CommonUtils.is_empty(value):
            return False
        return value.isdigit()
    
    @staticmethod
    def is_alpha(value: str) -> bool:
        """Check if string contains only letters and spaces"""
        if CommonUtils.is_empty(value):
            return False
        return bool(re.match(r'^[a-zA-Z\s]+$', value))
    
    @staticmethod
    def is_alpha_numeric(value: str) -> bool:
        """Check if string contains only alphanumeric characters"""
        if CommonUtils.is_empty(value):
            return False
        return bool(re.match(r'^[a-zA-Z0-9\s]+$', value))
    
    # ========== ENCODING/DECODING METHODS ==========
    
    @staticmethod
    def base64_encode(text: str) -> Optional[str]:
        """Base64 encode a string"""
        if text is None:
            return None
        encoded_bytes = base64.b64encode(text.encode('utf-8'))
        return encoded_bytes.decode('utf-8')
    
    @staticmethod
    def base64_decode(encoded_text: str) -> Optional[str]:
        """Base64 decode a string"""
        if encoded_text is None:
            return None
        try:
            decoded_bytes = base64.b64decode(encoded_text)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None
    
    @staticmethod
    def url_encode(text: str) -> Optional[str]:
        """URL encode (basic implementation)"""
        if text is None:
            return None
        import urllib.parse
        return urllib.parse.quote(text)
    
    @staticmethod
    def md5(text: str) -> Optional[str]:
        """Generate MD5 hash"""
        if text is None:
            return None
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    
    @staticmethod
    def sha256(text: str) -> Optional[str]:
        """Generate SHA-256 hash"""
        if text is None:
            return None
        return hashlib.sha256(text.encode('utf-8')).hexdigest()
    
    @staticmethod
    def sha1(text: str) -> Optional[str]:
        """Generate SHA-1 hash"""
        if text is None:
            return None
        return hashlib.sha1(text.encode('utf-8')).hexdigest()
    
    # ========== STRING MANIPULATION METHODS ==========
    
    @staticmethod
    def capitalize(text: str) -> str:
        """Capitalize first letter of a string"""
        if CommonUtils.is_empty(text):
            return text
        return text[0].upper() + text[1:].lower()
    
    @staticmethod
    def to_title_case(text: str) -> str:
        """Convert string to title case"""
        if CommonUtils.is_empty(text):
            return text
        return ' '.join(word.capitalize() for word in text.split())
    
    @staticmethod
    def truncate(text: str, max_length: int, suffix: str = "...") -> str:
        """Truncate string to specified length"""
        if text is None or max_length <= 0:
            return text
        if len(text) <= max_length:
            return text
        return text[:max_length] + suffix
    
    @staticmethod
    def remove_whitespace(text: str) -> Optional[str]:
        """Remove all whitespace from string"""
        if text is None:
            return None
        return re.sub(r'\s+', '', text)
    
    @staticmethod
    def strip_all(text: str) -> Optional[str]:
        """Strip whitespace from both ends and normalize internal spaces"""
        if text is None:
            return None
        return ' '.join(text.split())
    
    # ========== NULL SAFETY METHODS ==========
    
    @staticmethod
    def default_if_none(value: Any, default_value: Any) -> Any:
        """Return default value if object is None"""
        return value if value is not None else default_value
    
    @staticmethod
    def empty_if_none(value: Optional[str]) -> str:
        """Return empty string if None"""
        return value if value is not None else ""
    
    @staticmethod
    def zero_if_none(value: Optional[Union[int, float]]) -> Union[int, float]:
        """Return zero if None (for numbers)"""
        return value if value is not None else 0
    
    # ========== FORMATTING METHODS ==========
    
    @staticmethod
    def format_file_size(bytes_size: int) -> str:
        """Format file size in human readable format"""
        if bytes_size == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
        i = 0
        while bytes_size >= 1024 and i < len(size_names) - 1:
            bytes_size /= 1024.0
            i += 1
        
        return f"{bytes_size:.2f} {size_names[i]}".rstrip('0').rstrip('.')
    
    @staticmethod
    def mask_sensitive(data: str, visible_start: int, visible_end: int, mask_char: str = "*") -> str:
        """Mask sensitive data (like credit cards, emails)"""
        if CommonUtils.is_empty(data) or len(data) <= visible_start + visible_end:
            return data
        
        start = data[:visible_start]
        end = data[-visible_end:] if visible_end > 0 else ""
        mask_length = len(data) - visible_start - visible_end
        middle = mask_char * mask_length
        
        return start + middle + end
    
    @staticmethod
    def mask_email(email: str) -> str:
        """Mask email address"""
        if not CommonUtils.is_valid_email(email):
            return email
        
        username, domain = email.split('@')
        
        if len(username) <= 2:
            return f"{username}@{domain}"
        
        masked_username = username[0] + "***" + username[-1] if len(username) > 2 else username
        return f"{masked_username}@{domain}"
    
    @staticmethod
    def mask_phone(phone: str) -> str:
        """Mask phone number"""
        if CommonUtils.is_empty(phone):
            return phone
        
        cleaned = re.sub(r'[\s\-\(\)]', '', phone)
        if len(cleaned) < 6:
            return phone
        
        return CommonUtils.mask_sensitive(cleaned, 3, 2)
    
    # ========== LIST/DICT UTILITIES ==========
    
    @staticmethod
    def safe_list_get(lst: List[Any], index: int, default: Any = None) -> Any:
        """Safely get item from list by index"""
        try:
            return lst[index]
        except (IndexError, TypeError):
            return default
    
    @staticmethod
    def safe_dict_get(dct: Dict[Any, Any], key: Any, default: Any = None) -> Any:
        """Safely get value from dictionary by key"""
        try:
            return dct.get(key, default)
        except (AttributeError, TypeError):
            return default
    
    @staticmethod
    def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
        """Split list into chunks of specified size"""
        if CommonUtils.is_empty(lst) or chunk_size <= 0:
            return []
        return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]
    
    # ========== TYPE CONVERSION METHODS ==========
    
    @staticmethod
    def to_int(value: Any, default: int = 0) -> int:
        """Safely convert value to integer"""
        try:
            return int(value)
        except (ValueError, TypeError):
            return default
    
    @staticmethod
    def to_float(value: Any, default: float = 0.0) -> float:
        """Safely convert value to float"""
        try:
            return float(value)
        except (ValueError, TypeError):
            return default
    
    @staticmethod
    def to_bool(value: Any, default: bool = False) -> bool:
        """Safely convert value to boolean"""
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return bool(value)
        if isinstance(value, str):
            return value.lower() in ('true', '1', 'yes', 'on', 't')
        return default
    

 
    @staticmethod
    def dict_to_namespace(file_path):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, file_path)
        # Load and convert
        with open(config_path, 'r') as file:
            config_dict = json.load(file)
            """Convert dictionary to object with dot notation access"""
            if isinstance(config_dict, dict):
                return SimpleNamespace(**{k: dict_to_namespace(v) for k, v in config_dict.items()})
            elif isinstance(config_dict, list):
                return [dict_to_namespace(i) for i in config_dict]
            else:
                return config_dict
                # print(f"Data file: {config.UserImport.FileUpload.data_file}")
                # print(f"Mapping file: {config.UserImport.FileUpload.mapping_file}")
                # print(f"Default role: {config.UserImport.default_values.role_id}")
                # print(f"Case sensitive: {config.UserImport.case_sensitive}")
    
# # Import the utility class
# from common_utils import CommonUtils

# def example_usage():
#     print("=== VALIDATION EXAMPLES ===")
#     print(f"Is empty: {CommonUtils.is_empty('')}")  # True
#     print(f"Is not empty: {CommonUtils.is_not_empty('hello')}")  # True
#     print(f"Valid email: {CommonUtils.is_valid_email('test@example.com')}")  # True
#     print(f"Valid phone: {CommonUtils.is_valid_phone('123-456-7890')}")  # True
#     print(f"Is numeric: {CommonUtils.is_numeric('12345')}")  # True
#     print(f"Is alpha: {CommonUtils.is_alpha('hello world')}")  # True
    
#     print("\n=== ENCODING/DECODING EXAMPLES ===")
#     original = "Hello World!"
#     encoded = CommonUtils.base64_encode(original)
#     decoded = CommonUtils.base64_decode(encoded)
#     print(f"Original: {original}")
#     print(f"Encoded: {encoded}")
#     print(f"Decoded: {decoded}")
    
#     print(f"MD5: {CommonUtils.md5('password')}")
#     print(f"SHA256: {CommonUtils.sha256('password')}")
#     print(f"URL Encoded: {CommonUtils.url_encode('hello world & test')}")
    
#     print("\n=== STRING MANIPULATION EXAMPLES ===")
#     print(f"Capitalize: {CommonUtils.capitalize('hello')}")  # Hello
#     print(f"Title case: {CommonUtils.to_title_case('hello world')}")  # Hello World
#     print(f"Truncate: {CommonUtils.truncate('This is a long text', 10)}")  # This is a...
#     print(f"Remove whitespace: {CommonUtils.remove_whitespace(' hello  world ')}")  # helloworld
#     print(f"Strip all: {CommonUtils.strip_all('  hello    world  ')}")  # hello world
    
#     print("\n=== NULL SAFETY EXAMPLES ===")
#     null_string = None
#     print(f"Default if None: {CommonUtils.default_if_none(null_string, 'default')}")  # default
#     print(f"Empty if None: '{CommonUtils.empty_if_none(null_string)}'")  # ''
#     print(f"Zero if None: {CommonUtils.zero_if_none(None)}")  # 0
    
#     print("\n=== FORMATTING EXAMPLES ===")
#     print(f"File size: {CommonUtils.format_file_size(1024 * 1024)}")  # 1.00 MB
#     print(f"Masked email: {CommonUtils.mask_email('john.doe@example.com')}")  # j***e@example.com
#     print(f"Masked phone: {CommonUtils.mask_phone('123-456-7890')}")  # 123******90
#     print(f"Masked sensitive: {CommonUtils.mask_sensitive('1234567890123456', 4, 4)}")  # 1234************3456
    
#     print("\n=== LIST/DICT UTILITIES ===")
#     my_list = [1, 2, 3, 4, 5]
#     my_dict = {'name': 'John', 'age': 30}
    
#     print(f"Safe list get: {CommonUtils.safe_list_get(my_list, 10, 'not found')}")  # not found
#     print(f"Safe dict get: {CommonUtils.safe_dict_get(my_dict, 'email', 'not found')}")  # not found
#     print(f"Chunk list: {CommonUtils.chunk_list(my_list, 2)}")  # [[1, 2], [3, 4], [5]]
    
#     print("\n=== TYPE CONVERSION EXAMPLES ===")
#     print(f"To int: {CommonUtils.to_int('123')}")  # 123
#     print(f"To int (default): {CommonUtils.to_int('abc', 999)}")  # 999
#     print(f"To float: {CommonUtils.to_float('3.14')}")  # 3.14
#     print(f"To bool: {CommonUtils.to_bool('true')}")  # True
#     print(f"To bool: {CommonUtils.to_bool('yes')}")  # True

# # Real-world usage examples
# def practical_examples():
#     print("\n=== PRACTICAL EXAMPLES ===")
    
#     # User input validation
#     user_email = "user@example.com"
#     user_phone = "1234567890"
    
#     if CommonUtils.is_valid_email(user_email) and CommonUtils.is_valid_phone(user_phone):
#         print("Valid user data")
#         masked_email = CommonUtils.mask_email(user_email)
#         print(f"Masked email for logging: {masked_email}")
    
#     # Password hashing
#     password = "my_secure_password"
#     hashed_password = CommonUtils.sha256(password)
#     print(f"Hashed password: {hashed_password}")
    
#     # Data processing
#     dirty_string = "  Hello    World  "
#     clean_string = CommonUtils.strip_all(dirty_string)
#     print(f"Cleaned string: '{clean_string}'")
    
#     # Safe data access
#     user_data = {'name': 'Alice', 'age': '25'}
#     user_age = CommonUtils.to_int(CommonUtils.safe_dict_get(user_data, 'age', '0'))
#     user_email = CommonUtils.safe_dict_get(user_data, 'email', 'N/A')
#     print(f"User age: {user_age}, Email: {user_email}")

# if __name__ == "__main__":
#     example_usage()
#     practical_examples()