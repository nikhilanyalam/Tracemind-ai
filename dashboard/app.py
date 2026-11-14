import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(page_title="TraceMind AI", page_icon="🧠", layout="wide")

# Custom CSS to make it look like an enterprise dashboard
st.markdown("""
    <style>
    .main {background-color: #0e1117;}
    h1, h2, h3 {color: #fafafa;}
    .stAlert {border-radius: 4px;}
    </style>
""", unsafe_allow_html=True)

# 2. Sidebar for Navigation & Filters
with st.sidebar:
    st.title("🧠 TraceMind AI")
    st.caption("AI-Powered Root Cause Analysis Platform")
    st.markdown("---")
    st.info("**Environment:** Local MVP\n\n**ML Engine:** Pending\n\n**Storage:** SQLite")
    st.markdown("---")
    refresh = st.button("🔄 Refresh Telemetry")

# 3. Data Loading
@st.cache_data
def load_data():
    try:
        conn = sqlite3.connect("tracemind.db")
        df = pd.read_sql_query("SELECT * FROM telemetry", conn)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        conn.close()
        return df
    except Exception as e:
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.error("No telemetry data found. Please run `python generate_data.py` first.")
else:
    # 4. Main Header
    st.title("System Observability Command Center")
    st.markdown("Real-time distributed tracing and AI-driven anomaly detection.")

    # 5. Top KPI Metrics
    total_traces = df['trace_id'].nunique()
    total_events = len(df)
    # Simple hardcoded anomaly threshold for the UI before we add Isolation Forest
    anomalies = df[df['latency_ms'] > 1000]
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Traces", total_traces)
    col2.metric("Telemetry Events", total_events)
    col3.metric("Detected Anomalies", len(anomalies), delta="Critical", delta_color="inverse")
    col4.metric("System Health", "Degraded" if len(anomalies) > 0 else "Healthy")

    st.markdown("---")

    # 6. Tabbed Interface
    tab1, tab2, tab3 = st.tabs(["📊 Telemetry Overview", "🔍 AI Root Cause Analysis", "🗄️ Raw Data"])

    with tab1:
        st.subheader("Service Latency Distribution")
        # Polished Plotly Chart
        fig = px.scatter(
            df, x="timestamp", y="latency_ms", color="service_name",
            size_max=10, opacity=0.8,
            title="End-to-End Latency vs Time",
            labels={"latency_ms": "Latency (ms)", "timestamp": "Time", "service_name": "Microservice"},
            color_discrete_sequence=px.colors.qualitative.Set1
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(showgrid=True, gridcolor='#333'),
            yaxis=dict(showgrid=True, gridcolor='#333')
        )
        # Highlight the anomaly zone if it exists
        if not anomalies.empty:
            fig.add_hline(y=1000, line_dash="dash", line_color="red", annotation_text="Anomaly Threshold")
        
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Automated Incident Investigation")
        if not anomalies.empty:
            st.error("🚨 **Critical Incident Detected:** Cascading latency failure across multiple services.")
            
            with st.expander("🧠 View AI Root Cause Evidence", expanded=True):
                st.markdown("""
                **Sequence of Events (Trace ID: `trace_ANOMALY_CRITICAL`):**
                1. **Database Service:** Reported HTTP 503 with 5000ms latency.
                2. **Order Service:** Failed 1 second later (HTTP 500) due to downstream timeout.
                3. **API Gateway:** Failed 2 seconds later (HTTP 502) reporting bad gateway to client.
                
                **Verdict:** The **Database Service** is the origin node of the failure graph.
                """)
                
                st.button("Generate LLM Incident Report (Coming Soon)")
        else:
            st.success("No anomalies detected in the current time window.")

    with tab3:
        st.subheader("Raw Telemetry Feed")
        # Display as an interactive dataframe
        st.dataframe(
            df.sort_values("timestamp", ascending=False).style.highlight_max(subset=['latency_ms'], color='#5c1616'),
            use_container_width=True,
            height=400
        )