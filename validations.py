import re
import msvcrt
valid_roles = ["Backend", "Frontend", "Designer UX", "Designer UI"]

_EMAIL_PATTERN = re.compile(r"^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$")
_NAME_PATTERN = re.compile(r"^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s\-']+$")

def validate_email_format(email):
    return bool(_EMAIL_PATTERN.match(email))

def validate_unique_email(email, users, exclude_id=None):
    for u in users:
        if u["email"].lower() == email.lower() and u["id"] != exclude_id:
            return False
    return True

def validate_name(name):
    if not _NAME_PATTERN.match(name):
        return False
    if re.search(r"[\-']{3,}", name):
        return False
    letters_only = re.sub(r"[\s\-']", "", name)
    if len(letters_only) < 2:
        return False
    if len(set(letters_only.lower())) == 1:
        return False
    if re.search(r"([a-záéíóúüñ])\1{3,}", letters_only):
        return False
    return True

def validate_role_selection(option_str):
    if not option_str.isdigit():
        return False
    idx = int(option_str) - 1
    return 0 <= idx < len(valid_roles)

def get_role_by_index(option_str):
    idx = int(option_str) - 1
    return valid_roles[idx]

def read_single_key():
    try:
        char = msvcrt.getch().decode('utf-8', errors='ignore')
        return char.lower()
    except ImportError:
        pass