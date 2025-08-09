import re
import hashlib
import requests

COMMON_PATTERNS = [
    "1234", "password", "qwerty", "1111", "abc123", "letmein", "admin",
    "welcome", "monkey", "login", "dragon", "football"
]

def has_repeated_sequences(password, seq_length=3):
    for i in range(len(password) - seq_length * 2 + 1):
        seq = password[i:i+seq_length]
        if seq * 2 in password:
            return True
    return False

def contains_common_patterns(password):
    password_lower = password.lower()
    for pattern in COMMON_PATTERNS:
        if pattern in password_lower:
            return True
    return False

def check_strength(password):
    length = len(password)
    length_ok = length >= 8
    upper = bool(re.search(r'[A-Z]', password))
    lower = bool(re.search(r'[a-z]', password))
    digit = bool(re.search(r'\d', password))
    special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
    repeated_seq = has_repeated_sequences(password)
    common_pattern = contains_common_patterns(password)

    # Scoring system
    score = 0
    score += 1 if length >= 8 else 0
    score += 1 if upper else 0
    score += 1 if lower else 0
    score += 1 if digit else 0
    score += 1 if special else 0
    if repeated_seq:
        score -= 2
    if common_pattern:
        score -= 3

    score = max(0, min(score, 5))

    strength_details = {
        "Length ≥ 8": length_ok,
        "Contains Uppercase": upper,
        "Contains Lowercase": lower,
        "Contains Digit": digit,
        "Contains Special Character": special,
        "No Repeated Sequences": not repeated_seq,
        "No Common Patterns": not common_pattern
    }

    if score <= 2:
        strength_label = "Weak"
    elif score == 3:
        strength_label = "Moderate"
    elif score == 4:
        strength_label = "Strong"
    else:
        strength_label = "Very Strong"

    return score, strength_label, strength_details


def check_pwned(password):
    sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5, tail = sha1[:5], sha1[5:]

    url = f"https://api.pwnedpasswords.com/range/{first5}"
    try:
        res = requests.get(url)
        res.raise_for_status()
    except requests.RequestException:
        return False, -1  # API error indicator

    hashes = res.text.splitlines()
    for h in hashes:
        h_tail, count = h.split(":")
        if h_tail == tail:
            return True, int(count)
    return False, 0
