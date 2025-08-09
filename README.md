# PASSWORD-STRENGTH-AND-BREACH-CHECKER
# 🔐 Password Strength & Breach Checker

A **Streamlit-based** web application that helps users:
- **Check password strength** based on multiple security criteria.
- **Detect common patterns** and repeated sequences in passwords.
- **Verify if a password has been exposed** in known data breaches via the **HaveIBeenPwned API**.
- Export results for offline analysis.

## 🚀 Project Features
- ✅ **Password Strength Analysis**
  - Checks length, uppercase, lowercase, digits, special characters.
  - Detects common patterns (`1234`, `password`, `qwerty`, etc.).
  - Flags repeated sequences.
- 📊 **Scoring System**
  - Strength calculated on a scale, not just pass/fail.
  - Visual strength meter with color coding.
- 🌐 **Breach Check**
  - Uses [HaveIBeenPwned API](https://haveibeenpwned.com/API/v3) to see if the password was exposed.
  - Secure k-Anonymity method (first 5 characters of SHA1 hash sent to API).
- 🛡 **Error Handling**
  - Network/API error handling with user-friendly messages.
- 👁 **Password Visibility Toggle**
  - Show/hide password while typing.
- ⏳ **Loading Spinner**
  - Displays a spinner during breach checks.
- 📤 **Export Report**
  - Save results as **plain text** or **JSON**.
    
## 🛠 Technologies & Tools Used
- **Python 3.8+**
- **Streamlit** (Frontend/UI)
- **Requests** (API calls)
- **Hashlib** (SHA-1 hashing for breach checking)
- **JSON** (Report export)
- **HaveIBeenPwned API** (Breach data source)
