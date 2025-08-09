import streamlit as st
import json
from checker import check_strength, check_pwned

st.set_page_config(page_title="🔐 Password Strength Checker", layout="centered")

st.title("🔐Password Strength & Breach Checker🔐")
st.write("Enter a password to evaluate its strength and check if it's been exposed in data breaches.")

# Password input with visibility toggle
show_password = st.checkbox("Show password")
password = st.text_input("Enter Password", type="default" if show_password else "password")

def generate_report(password, score, strength_label, details, breached, count):
    report = {
        "Password Checked": password,
        "Strength Score": score,
        "Strength Label": strength_label,
        "Criteria": details,
        "Breach Status": "Breached" if breached else "Not Breached",
        "Breach Count": count if breached else 0
    }
    return report

if password:
    st.subheader("🔎Strength Analysis🔍")
    score, strength_label, details = check_strength(password)

    # Show criteria with checkmarks
    for criterion, passed in details.items():
        if passed:
            st.success(f"✅ {criterion}")
        else:
            st.error(f"❌ {criterion}")

    # Colored progress bar for strength score
    progress_pct = score / 5
    if score <= 2:
        bar_color = "#FF4B4B"  # red
    elif score == 3:
        bar_color = "#FFA500"  # orange
    elif score == 4:
        bar_color = "#FFD700"  # yellow
    else:
        bar_color = "#4CAF50"  # green

    st.markdown(f"**Password Strength:** {strength_label} ({score}/5)")
    st.progress(progress_pct)

    st.subheader("🛡️Breach Check (HaveIBeenPwned)🛡️")

    with st.spinner("Checking breaches..."):
        breached, count = check_pwned(password)

    if count == -1:
        st.warning("⚠️ Breach check failed due to network or API error. Please try again later.")
    elif breached:
        st.error(f"⚠️ This password has appeared in **{count}** known data breaches!")
    else:
        st.success("Great! This password has NOT appeared in known breaches.")

    # Toast notification with fallback
    try:
        if score >= 4 and count == 0:
            st.toast("👌 Strong & Safe Password!", icon="🔐")
        elif score < 4 or breached:
            st.toast("💡 Consider using a password manager to generate stronger, safer passwords.", icon="‼")
    except AttributeError:
        if score >= 4 and count == 0:
            st.success("👌 Strong & Safe Password! 🔐")
        else:
            st.warning("Tip: Consider using a password manager to generate stronger, safer passwords.")

    # Export report options
    report = generate_report(password, score, strength_label, details, breached, count)

    st.subheader("📤 Export Report")
    export_format = st.radio("Choose export format:", ("JSON", "Plain Text"))

    if export_format == "JSON":
        json_str = json.dumps(report, indent=4)
        st.download_button(
            label="Download JSON Report",
            data=json_str,
            file_name="password_report.json",
            mime="application/json"
        )
    else:  # Plain Text
        text_lines = [
            f"Password Checked: {report['Password Checked']}",
            f"Strength Score: {report['Strength Score']} ({report['Strength Label']})",
            "Criteria:"
        ]
        for crit, val in report["Criteria"].items():
            status = "Passed" if val else "Failed"
            text_lines.append(f" - {crit}: {status}")
        text_lines.append(f"Breach Status: {report['Breach Status']}")
        if breached:
            text_lines.append(f"Breach Count: {report['Breach Count']}")

        plain_text_report = "\n".join(text_lines)

        st.download_button(
            label="Download Plain Text Report",
            data=plain_text_report,
            file_name="password_report.txt",
            mime="text/plain"
        )
