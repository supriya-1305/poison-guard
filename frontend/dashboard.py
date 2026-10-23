
import os
from datetime import datetime

import requests
import streamlit as st


st.set_page_config(
    page_title="PoisonGuard Security Dashboard",
    page_icon="🛡️",
    layout="wide",
)

DEFAULT_API_URL = os.getenv(
    "POISONGUARD_API_URL",
    "http://127.0.0.1:8000",
)


def fetch_api(path):
    """Fetch live data from the PoisonGuard FastAPI backend."""
    try:
        response = requests.get(
            f"{api_url.rstrip('/')}{path}",
            timeout=5,
        )
        response.raise_for_status()
        return response.json(), None
    except requests.RequestException as exc:
        return None, str(exc)
    except ValueError:
        return None, "The API returned an invalid JSON response."


st.markdown(
    """
    <style>
    .stApp {
        background-color: #0b1120;
    }
    [data-testid="stMetric"] {
        background: #151f32;
        border: 1px solid #283650;
        padding: 16px;
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.title("🛡️ PoisonGuard")
    st.caption("ML Security Operations Center")
    api_url = st.text_input(
        "FastAPI base URL",
        value=DEFAULT_API_URL,
    )
    st.caption("Default: http://127.0.0.1:8000")
    refresh = st.button("Refresh dashboard", use_container_width=True)
    st.divider()
    st.info(
        "Monitoring only. This dashboard does not automatically "
        "retrain, promote, activate, or roll back models."
    )

st.title("PoisonGuard Security Dashboard")
st.caption(
    f"Live backend monitoring · Last page load: "
    f"{datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')}"
)

if refresh:
    st.rerun()

health, health_error = fetch_api("/health")
model_status, model_error = fetch_api("/model/status")
security, security_error = fetch_api("/security-score")
incidents_data, incidents_error = fetch_api("/week7/incidents")
registry_data, registry_error = fetch_api("/registry/versions")
audit_data, audit_error = fetch_api("/week7/audit")

# API and model status
st.subheader("System status")
col1, col2, col3 = st.columns(3)

with col1:
    if health_error:
        st.metric("API health", "Unavailable")
    else:
        st.metric("API health", "Online")

with col2:
    if model_error:
        st.metric("Model status", "Unavailable")
    elif model_status.get("model_loaded"):
        st.metric("Model status", "Loaded")
    else:
        st.metric("Model status", "Not loaded")

with col3:
    if model_status:
        st.metric(
            "Active model version",
            str(model_status.get("model_version", "Unknown")),
        )
    else:
        st.metric("Active model version", "Unknown")

with st.expander("Backend response details"):
    st.write("Health endpoint")
    if health_error:
        st.warning(health_error)
    else:
        st.json(health)

    st.write("Model status endpoint")
    if model_error:
        st.warning(model_error)
    else:
        st.json(model_status)

# Security score
st.divider()
st.subheader("Security overview")

if security_error:
    st.warning(f"Security score unavailable: {security_error}")
else:
    st.json(security)

# Incident management
st.divider()
st.subheader("Runtime incidents")

if incidents_error:
    st.warning(f"Incident data unavailable: {incidents_error}")
else:
    incidents = incidents_data.get("incidents", [])
    st.metric("Recorded incidents", incidents_data.get("count", len(incidents)))

    if incidents:
        st.dataframe(incidents, use_container_width=True)
    else:
        st.success("No incidents are currently recorded.")

# Model registry
st.divider()
st.subheader("Model registry")

if registry_error:
    st.warning(f"Registry data unavailable: {registry_error}")
else:
    versions = registry_data.get("versions", [])
    st.caption(
        f"Registry: {registry_data.get('model_name', 'PoisonGuard-ResNet18')}"
    )
    st.metric("Registered versions", registry_data.get("count", len(versions)))

    if versions:
        st.dataframe(versions, use_container_width=True)
    else:
        st.info("No registered versions were returned by the backend.")

# Audit trail
st.divider()
st.subheader("Incident response audit trail")

if audit_error:
    st.warning(f"Audit data unavailable: {audit_error}")
else:
    events = audit_data.get("events", [])
    st.metric("Audit events", len(events))

    if events:
        st.dataframe(events, use_container_width=True)
    else:
        st.info("No audit events are currently recorded.")

# Validation report
st.divider()
st.subheader("Sanitized candidate validation")

report_path = (
    "experiments/week7/results/promotion_validation.json"
)

try:
    import json
    from pathlib import Path

    report_file = Path(__file__).resolve().parents[1] / report_path

    if report_file.is_file():
        report = json.loads(report_file.read_text(encoding="utf-8"))
        status = report.get("validation_status", "Unknown")
        promotion = report.get("promotion_status", "Unknown")
        metrics = report.get("observed_metrics", {})

        left, middle, right = st.columns(3)
        left.metric(
            "Candidate clean accuracy",
            f"{metrics.get('candidate_clean_accuracy', 0) * 100:.2f}%"
            if "candidate_clean_accuracy" in metrics
            else "Unavailable",
        )
        middle.metric(
            "Candidate attack success rate",
            f"{metrics.get('candidate_attack_success_rate', 0) * 100:.2f}%"
            if "candidate_attack_success_rate" in metrics
            else "Unavailable",
        )
        right.metric("Promotion status", str(promotion))

        st.write("Validation status:", status)
        st.json(report)
        st.info(
            "A passing evaluation is limited to the configured test "
            "data and trigger. This dashboard does not approve or "
            "activate the candidate."
        )
    else:
        st.warning("The Week 7 promotion validation report was not found.")
except (OSError, ValueError) as exc:
    st.error(f"Could not read the validation report: {exc}")

st.divider()
st.caption(
    "PoisonGuard prototype · Displayed API data is fetched live. "
    "Candidate validation is read from the local report file."
)

