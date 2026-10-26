import json
import os
from pathlib import Path
from datetime import datetime

import requests
import streamlit as st


# POISONGUARD_ANIMATION_PACK_V1
st.markdown("""
<style>
@keyframes pgFadeSlideIn {
  from { opacity: 0; transform: translateY(14px); }
  to { opacity: 1; transform: translateY(0); }
}
/* PG_WOW_ENHANCEMENT_V1 */
@keyframes pgSoftGlow {
  0%, 100% { box-shadow: 0 5px 12px rgba(50, 20, 25, 0.08); }
  50% { box-shadow: 0 12px 28px rgba(200, 164, 93, 0.22); }
}
@keyframes pgIconSpin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Entrance motion */
div[data-testid="stMetric"],
div[data-testid="stPlotlyChart"],
div[data-testid="stDataFrame"],
div[data-testid="stTable"] {
  animation: pgFadeSlideIn 0.7s cubic-bezier(0.2, 0.8, 0.2, 1) both;
}

/* Metric cards: stronger hover feedback, no color changes */
/* Metric cards: premium hover motion, existing colors preserved */
div[data-testid="stMetric"] {
    transition:
        transform 320ms cubic-bezier(0.2, 0.8, 0.2, 1),
        box-shadow 320ms cubic-bezier(0.2, 0.8, 0.2, 1) !important;
    transform: translateY(0);
    position: relative;
    z-index: 0;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-6px) scale(1.015) !important;
    box-shadow:
        0 5px 10px rgba(0, 0, 0, 0.06),
        0 14px 28px rgba(0, 0, 0, 0.13) !important;
    z-index: 2;
}

/* Gentle premium glow on metric-card hover */
div[data-testid="stMetric"]:hover {
  animation: pgSoftGlow 2.4s ease-in-out infinite;
}

/* Buttons */
div[data-testid="stButton"] button {
  transition: transform 0.2s ease, filter 0.2s ease !important;
}
div[data-testid="stButton"] button:hover {
  transform: translateY(-3px) !important;
  filter: drop-shadow(0 4px 5px rgba(0, 0, 0, 0.18));
}
div[data-testid="stButton"] button:active {
  transform: scale(0.97) !important;
}
div[data-testid="stButton"] button:hover svg {
  animation: pgIconSpin 0.8s ease-in-out;
}

/* Native Streamlit table hover */
div[data-testid="stTable"] tbody tr {
  transition: background-color 0.2s ease;
}

/* Expanders */
div[data-testid="stExpander"] {
  transition: filter 0.25s ease;
}
div[data-testid="stExpander"]:hover {
  filter: drop-shadow(0 5px 9px rgba(200, 164, 93, 0.20));
}

/* Alerts enter gently; preserve their existing colors */
div[data-testid="stAlert"] {
  animation: pgFadeSlideIn 0.5s ease-out both;
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation: none !important;
    transition: none !important;
  }
}


/* Premium 3D cards — existing theme preserved */
div[data-testid="stMetric"],
div[data-testid="stExpander"],
div[data-testid="stDataFrame"],
div[data-testid="stTable"] {
    border-radius: 16px !important;
    box-shadow:
        0 2px 5px rgba(50, 20, 25, 0.08),
        0 9px 22px rgba(50, 20, 25, 0.12),
        inset 0 1px 0 rgba(255, 255, 255, 0.55) !important;
    transition:
        transform 280ms cubic-bezier(0.2, 0.8, 0.2, 1),
        box-shadow 280ms ease !important;
}

div[data-testid="stMetric"]:hover,
div[data-testid="stExpander"]:hover {
    transform: translateY(-5px) !important;
    box-shadow:
        0 5px 10px rgba(50, 20, 25, 0.08),
        0 16px 30px rgba(50, 20, 25, 0.17),
        inset 0 1px 0 rgba(255, 255, 255, 0.65) !important;
}

div[data-testid="stButton"] button {
    border-radius: 12px !important;
    transition: transform 220ms ease, box-shadow 220ms ease !important;
}

div[data-testid="stButton"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 14px rgba(50, 20, 25, 0.16) !important;
}

@media (prefers-reduced-motion: reduce) {
    div[data-testid="stMetric"],
    div[data-testid="stExpander"],
    div[data-testid="stButton"] button {
        transition: none !important;
    }
}

/* Week 8: premium card content alignment */
div[data-testid="stMetric"] {
    box-sizing: border-box !important;
    padding: 14px 18px !important;
    border-radius: 18px !important;
}

div[data-testid="stMetricLabel"],
div[data-testid="stMetricValue"],
div[data-testid="stMetricDelta"] {
    text-align: left !important;
    width: 100%;
}

div[data-testid="stExpander"] details > summary {
    padding: 12px 18px !important;
    box-sizing: border-box !important;
}

div[data-testid="stExpander"] details > div {
    padding-left: 18px !important;
    padding-right: 18px !important;
    box-sizing: border-box !important;
}



/* POISONGUARD_WOW_ANIMATIONS_V1 */

/* Smooth entrance for dashboard cards and visualizations */
@keyframes pgWowEntrance {
    from {
        opacity: 0;
        transform: translateY(14px) scale(0.985);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

div[data-testid="stMetric"],
div[data-testid="stPlotlyChart"],
div[data-testid="stDataFrame"],
div[data-testid="stTable"] {
    animation: pgWowEntrance 650ms cubic-bezier(0.2, 0.75, 0.25, 1) both;
}

/* Staggered metric card entrance */
div[data-testid="stMetric"]:nth-of-type(2) {
    animation-delay: 70ms;
}
div[data-testid="stMetric"]:nth-of-type(3) {
    animation-delay: 140ms;
}
div[data-testid="stMetric"]:nth-of-type(4) {
    animation-delay: 210ms;
}

/* Refined 3D hover with existing theme colors */
div[data-testid="stMetric"] {
    border: 1px solid rgba(200, 164, 93, 0.45) !important;
    box-shadow:
        0 3px 6px rgba(45, 20, 24, 0.05),
        0 8px 18px rgba(45, 20, 24, 0.07) !important;
    transition:
        transform 280ms cubic-bezier(0.2, 0.8, 0.2, 1),
        box-shadow 280ms ease,
        border-color 280ms ease !important;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-5px) scale(1.008) !important;
    border-color: #C8A45D !important;
    box-shadow:
        0 7px 12px rgba(45, 20, 24, 0.08),
        0 16px 30px rgba(45, 20, 24, 0.12),
        0 0 0 1px rgba(200, 164, 93, 0.12) !important;
    z-index: 3;
}

/* Smooth, polished expanders and buttons */
div[data-testid="stExpander"] {
    transition: box-shadow 250ms ease, transform 250ms ease !important;
}
div[data-testid="stExpander"]:hover {
    box-shadow: 0 7px 18px rgba(45, 20, 24, 0.08) !important;
}
div[data-testid="stButton"] button {
    transition:
        transform 200ms ease,
        box-shadow 200ms ease,
        filter 200ms ease !important;
}
div[data-testid="stButton"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 5px 12px rgba(45, 20, 24, 0.12) !important;
}

/* Respect accessibility settings */
@media (prefers-reduced-motion: reduce) {
    div[data-testid="stMetric"],
    div[data-testid="stPlotlyChart"],
    div[data-testid="stDataFrame"],
    div[data-testid="stTable"],
    div[data-testid="stExpander"],
    div[data-testid="stButton"] button {
        animation: none !important;
        transition: none !important;
    }
}

</style>
""", unsafe_allow_html=True)

DEFAULT_API_URL = os.getenv("POISONGUARD_API_URL", "http://127.0.0.1:2222")



# PoisonGuard chart helper: supported Altair API and consistent accessible colors.
def _pg_bar_chart(data, title, x_title, y_title):
    import pandas as pd
    import altair as alt
    palette = ["#581824", "#6D2433", "#7C303F", "#8B3A49", "#A8B85A"]
    if not isinstance(data, dict) or not data:
        st.info("No chart data available yet.")
        return
    labels, values = [], []
    for key, value in data.items():
        if isinstance(value, (list, tuple)):
            value = value[0] if value else 0
        labels.append(str(key))
        values.append(value)
    frame = pd.DataFrame({"label": labels, "count": values})
    chart = (
        alt.Chart(frame)
        .mark_bar(stroke="#6F5830", strokeWidth=1)
        .encode(
            x=alt.X("label:N", title=x_title,
                    axis=alt.Axis(labelColor="#4A3434", titleColor="#5D1A27",
                                  labelAngle=-25)),
            y=alt.Y("count:Q", title=y_title,
                    axis=alt.Axis(labelColor="#4A3434", titleColor="#5D1A27",
                                  gridColor="#E4D8C5"),
                    scale=alt.Scale(domainMin=0)),
            color=alt.Color(
                "label:N",
                scale=alt.Scale(domain=labels, range=palette[:len(labels)]),
                legend=None
            ),
            tooltip=[
                alt.Tooltip("label:N", title=x_title),
                alt.Tooltip("count:Q", title=y_title)
            ]
        )
        .properties(
            title=alt.Title(title, color="#5D1A27"),
            height=300,
            background="#F7F1E7"
        )
        .configure_view(stroke=None)
        .configure_axis(domainColor="#8B3A49")
    )
    st.altair_chart(chart, use_container_width=True)


st.set_page_config(
    page_title="PoisonGuard | Security Operations",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)





# PoisonGuard five-color theme
st.markdown("""<style>

/* PoisonGuard unified five-color theme */
:root {
  --burgundy: #5A1825;
  --pistachio: #A8B85A;
  --cream: #F7F0E5;
  --muted-gold: #C8A45D;
  --dark-plum: #5A1825;
}
html, body, .stApp, [data-testid="stAppViewContainer"],
[data-testid="stMain"], [data-testid="stMainBlockContainer"] {
  background: #A8B85A !important;
  color: #5A1825 !important;
}
[data-testid="stSidebar"], [data-testid="stSidebar"] > div {
  background: #5A1825 !important;
  color: #F7F1E7 !important;
}
h1, h2, h3, h4, p, label, [data-testid="stMarkdownContainer"],
[data-testid="stMetricLabel"], [data-testid="stMetricValue"] {
  color: #5A1825 !important;
}
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3, [data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
[data-testid="stSidebar"] [data-testid="stWidgetLabel"],
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
  color: #A8B85A !important;
}
input, textarea, [data-testid="stTextInput"] input {
  background: #F7F1E7 !important;
  color: #5A1825 !important;
  border: 1px solid #C8A45D !important;
}
button, [data-testid="stBaseButton-primary"],
[data-testid="stSidebar"] button {
  background: #F7F0E5 !important;
  color: #5A1825 !important;
  border: 1px solid #C8A45D !important;
}
[data-testid="stMetric"], [data-testid="stExpander"],
[data-testid="stDataFrame"], [data-testid="stTable"] {
  background: #F7F1E7 !important;
  color: #5A1825 !important;
  border-color: #C8A45D !important;
}
[data-testid="stAlert"] {
  background: #F7F1E7 !important;
  color: #5A1825 !important;
  border: 1px solid #C8A45D !important;
}
hr { border-color: #C8A45D !important; }
/* Streamlit chart SVG text and grid labels */
[data-testid="stVegaLiteChart"] text,
[data-testid="stVegaLiteChart"] .role-axis-label,
[data-testid="stVegaLiteChart"] .role-axis-title {
  fill: #211719 !important;
  color: #5A1825 !important;
}

</style>""", unsafe_allow_html=True)

# Week 8 premium encryption theme

with st.sidebar:
    st.title("🛡️ PoisonGuard")
    st.caption("ML SECURITY OPERATIONS")
    api_url = st.text_input(
        "Backend API URL", value=DEFAULT_API_URL
    )
    if st.button("↻ Refresh dashboard", width="stretch"):
        st.rerun()
    st.divider()
    st.markdown("### Navigation")
    st.markdown(
        "- Overview\n"
        "- Dataset Security\n"
        "- Model Security\n"
        "- Runtime Monitoring\n"
        "- Incidents\n"
        "- Model Registry\n"
        "- Audit Trail"
    )
    st.divider()
    st.caption(
        "Read-only monitoring. Model promotion, activation, "
        "rollback and retraining are not triggered by this dashboard."
    )

def fetch_api(api_url, path):
    """Fetch JSON data from the PoisonGuard backend."""
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
        return None, "The API returned invalid JSON."


health, health_error = fetch_api(api_url, "/health")
model, model_error = fetch_api(api_url, "/model/status")
security, security_error = fetch_api(api_url, "/security-score")
incidents_data, incidents_error = fetch_api(
    api_url, "/week7/incidents"
)
registry_data, registry_error = fetch_api(
    api_url, "/registry/versions"
)
audit_data, audit_error = fetch_api(api_url, "/week7/audit")
dataset_history_data, dataset_history_error = fetch_api(
    api_url, "/scan/dataset/history"
)

incidents = (
    incidents_data.get("incidents", [])
    if incidents_data else []
)
versions = (
    registry_data.get("versions", [])
    if registry_data else []
)
events = (
    audit_data.get("events", [])
    if audit_data else []
)

api_online = bool(health and not health_error)
model_loaded = bool(
    model and model.get("model_loaded") and not model_error
)
model_version = (
    model.get("model_version", "Unknown") if model else "Unknown"
)
prediction_count = (
    security.get("predictions_logged", 0) if security else 0
)
incident_count = (
    incidents_data.get("count", len(incidents))
    if incidents_data else len(incidents)
)

st.markdown(f"""
<div class="hero">
    <h1>PoisonGuard Security Dashboard</h1>
    <p>Machine learning security monitoring · Backend-connected overview</p>
    <p>Last refreshed: {datetime.now().astimezone().strftime('%d %b %Y, %H:%M:%S %Z')}</p>
</div>
""", unsafe_allow_html=True)

st.subheader("Overview")
c1, c2, c3, c4 = st.columns(4)
c1.metric("API Health", "Online" if api_online else "Unavailable")
c2.metric("Model Status", "Loaded" if model_loaded else "Unavailable")
c3.metric("Predictions Logged", prediction_count)
c4.metric("Open/Recorded Incidents", incident_count)

with st.expander("Backend connection details"):
    st.write("Health")
    st.error(f"Health endpoint unavailable: {health_error}")
    if health:
        st.json(health)
    st.write("Model status")
    st.error(f"Model status unavailable: {model_error}")
    if model:
        st.json(model)

st.divider()
st.header("Dataset Security")

if dataset_history_error:
    st.warning(f"Dataset scan history unavailable: {dataset_history_error}")
elif dataset_history_data is not None:
    saved_scans = dataset_history_data.get("scans", [])
    total_scans = dataset_history_data.get("count", len(saved_scans))
    total_images = sum(
        scan.get("scanned_count", 0) for scan in saved_scans
    )
    total_errors = sum(
        scan.get("error_count", 0) for scan in saved_scans
    )

    metric1, metric2, metric3 = st.columns(3)
    metric1.metric("Saved Scans", total_scans)
    metric2.metric("Images Scanned", total_images)
    metric3.metric("Image Errors", total_errors)

    if not saved_scans:
        st.info(
            "No dataset scans have been saved yet. "
            "Submit images to POST /scan/dataset to create the first record."
        )
    else:
        st.caption("Showing saved dataset scans, newest first.")
        for scan in reversed(saved_scans):
            scan_id = scan.get("scan_id", "Unknown")
            timestamp = scan.get("timestamp", "Timestamp unavailable")
            with st.expander(f"Scan {scan_id} — {timestamp}"):
                st.write(f"Images scanned: {scan.get('scanned_count', 0)}")
                st.write(f"Image errors: {scan.get('error_count', 0)}")
                results = scan.get("results", [])
                if results:
                    st.dataframe(results, use_container_width=True)
                else:
                    st.caption("This scan contains no individual results.")
else:
    st.info("Dataset scan history is not available yet.")

st.divider()
st.header("Model Security")
left, right = st.columns(2)

with left:
    st.markdown("#### Active model")
    st.metric("Model version", str(model_version))
    if model:
        st.caption(f"Checkpoint: {model.get('checkpoint', 'Unknown')}")
        st.caption(f"Device: {model.get('device', 'Unknown')}")
        if model.get("error"):
            st.warning(str(model["error"]))
    else:
        st.error(f"Model details unavailable: {model_error}")

with right:
    st.markdown("#### Runtime security score")
    if security_error:
        st.error(f"Security score unavailable: {security_error}")
    elif security:
        score = security.get("security_score")
        st.metric(
            "Preliminary rule-based score",
            score if score is not None else "Unavailable",
        )
        st.caption(security.get("interpretation", "No interpretation supplied"))
        st.caption(
            security.get(
                "scoring_note",
                "The score may not represent a validated security rating.",
            )
        )
        st.metric(
            "Incidents in score calculation",
            security.get("incidents_recorded", "Unavailable"),
        )

st.divider()
st.header("Runtime Monitoring")
st.metric("Predictions logged", prediction_count)

if security and isinstance(prediction_count, (int, float)):
    _pg_bar_chart({"Recorded predictions": [prediction_count]}, title="Runtime Monitoring", x_title="Metric", y_title="Count")
    st.caption(
        "This chart displays the backend's current aggregate count, "
        "not a time-series history."
    )
else:
    st.info("Prediction activity data is unavailable.")

st.divider()
st.header("Incidents")
if incidents_error:
    st.error(f"Incident endpoint unavailable: {incidents_error}")

if incidents_data:
    st.metric("Incidents returned by incident endpoint", incident_count)
    if incidents:
        incident_rows = [
            item for item in incidents if isinstance(item, dict)
        ]
        if incident_rows:
            st.dataframe(incident_rows, width="stretch", hide_index=True)

            severity_counts = {}
            for item in incident_rows:
                severity = str(item.get("severity", "Unknown"))
                severity_counts[severity] = severity_counts.get(severity, 0) + 1

            st.markdown("#### Incidents by severity")
            _pg_bar_chart(severity_counts, title='Incidents by severity', x_title='Category', y_title='Count')
        else:
            st.info("Incident records were returned in an unexpected format.")
    else:
        st.success("The incident endpoint returned no incidents.")
else:
    st.info("Incident information is currently unavailable.")

st.divider()
st.header("Model Registry")
if registry_error:
    st.error(f"Registry endpoint unavailable: {registry_error}")

if registry_data:
    st.metric("Registered model versions", registry_data.get("count", len(versions)))
    if versions:
        registry_rows = [
            item for item in versions if isinstance(item, dict)
        ]
        if registry_rows:
            st.dataframe(registry_rows, width="stretch", hide_index=True)
            st.markdown("#### Registered versions by validation status")
            validation_counts = {}
            for item in registry_rows:
                status = str(item.get("validation_status", "Unknown"))
                validation_counts[status] = validation_counts.get(status, 0) + 1
            _pg_bar_chart(validation_counts, title='Registered versions by validation status', x_title='Category', y_title='Count')
        else:
            st.info("Registry records were returned in an unexpected format.")
    else:
        st.info("The registry currently returns no model versions.")

st.divider()
st.header("Audit Trail")
if audit_error:
    st.error(f"Audit endpoint unavailable: {audit_error}")

if audit_data:
    st.metric("Audit events returned", len(events))
    if events:
        event_rows = [
            item for item in events if isinstance(item, dict)
        ]
        if event_rows:
            st.dataframe(event_rows, width="stretch", hide_index=True)
            st.markdown("#### Events by action")
            action_counts = {}
            for item in event_rows:
                action = str(item.get("action", "Unknown"))
                action_counts[action] = action_counts.get(action, 0) + 1
            _pg_bar_chart(action_counts, title='Events by action', x_title='Category', y_title='Count')
        else:
            st.info("Audit events were returned in an unexpected format.")
    else:
        st.info("No audit events were returned.")
else:
    st.info("Audit trail information is currently unavailable.")

st.divider()
st.header("Sanitized Candidate Validation")

report_path = (
    Path(__file__).resolve().parents[1]
    / "experiments/week7/results/promotion_validation.json"
)

if report_path.is_file():
    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
        metrics = report.get("observed_metrics", {})
        a, b, c = st.columns(3)
        accuracy = metrics.get("candidate_clean_accuracy")
        asr = metrics.get("candidate_attack_success_rate")
        a.metric(
            "Candidate clean accuracy",
            f"{accuracy * 100:.2f}%" if isinstance(accuracy, (int, float)) else "Unavailable",
        )
        b.metric(
            "Candidate attack success rate",
            f"{asr * 100:.2f}%" if isinstance(asr, (int, float)) else "Unavailable",
        )
        c.metric(
            "Promotion status",
            str(report.get("promotion_status", "Unknown")),
        )
        st.write(
            "Validation status:",
            report.get("validation_status", "Unknown"),
        )
        st.info(
            "Validation results do not constitute approval to activate a model. "
            "Manual authorization and candidate-specific checks remain required."
        )
        with st.expander("View validation report"):
            st.json(report)
    except (OSError, ValueError) as exc:
        st.error(f"Could not read validation report: {exc}")
else:
    st.info("The standard Week 7 validation report was not found.")

st.caption(
    "PoisonGuard prototype · Live API data is separated from local validation reports. "
    "Charts show returned aggregates, not fabricated historical data."
)
