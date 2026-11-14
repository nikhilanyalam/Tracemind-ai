# TraceMind AI

TraceMind AI is a lightweight observability and incident-investigation MVP designed to simulate distributed system telemetry, highlight latency anomalies, and surface likely root-cause events across a microservice flow.

The project combines synthetic trace generation, a SQLite-backed telemetry store, and a Streamlit dashboard to create an enterprise-style monitoring experience for demos, learning, and prototyping AI-driven root cause analysis.

## Overview

Modern systems often fail in cascading ways: one database issue can cause downstream queue delays, API timeouts, and user-facing 5xx errors. TraceMind AI focuses on this exact problem by modeling a small distributed system and emphasizing how observability data can be used to identify the primary failure node.

In this MVP, the application:

- generates synthetic telemetry for a multi-service system
- stores traces in SQLite
- visualizes service latency and anomaly patterns
- highlights critical incidents in a dashboard
- presents a simple root-cause narrative for a simulated failure

## Key Features

- Synthetic telemetry generation for API Gateway, Order Service, and Database layers
- Database-backed trace storage using SQLite
- Streamlit dashboard for monitoring and incident review
- Latency trend analysis across services
- Critical anomaly identification based on high-latency failures
- Incident evidence panel showing the cascade path from root cause to symptom
- Raw telemetry table for deep inspection

## Architecture

TraceMind AI is structured as a small observability demo with three major components:

- Data generator: creates telemetry records and injects an anomaly cascade
- Telemetry store: SQLite database (`tracemind.db`)
- Dashboard: Streamlit frontend for system health and incident analysis

The architecture is intentionally simple so it remains easy to understand and extend.

## Project Structure

```text
Tracemind-ai/
├── dashboard/
│   └── app.py
├── simulator/
│   ├── gateway_service.py
│   └── order_service.py
├── generate_data.py
├── requirements.txt
├── tracemind.db
├── .gitignore
└── README.md
```

## Tech Stack

- Python
- FastAPI
- Streamlit
- Plotly
- Pandas
- NumPy
- SQLite
- scikit-learn (prepared for future ML-based anomaly detection)
- OpenTelemetry ready dependencies for observability instrumentation

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/nikhilanyalam/Tracemind-ai.git
cd Tracemind-ai
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # On macOS/Linux
# .venv\Scripts\activate    # On Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Generate telemetry data

```bash
python generate_data.py
```

This creates a SQLite database named `tracemind.db` and populates it with both normal traffic and a simulated critical incident.

### 5. Launch the dashboard

```bash
streamlit run dashboard/app.py
```

Then open the URL shown in the terminal, typically:

```text
http://localhost:8501
```

## Example Workflow

1. Run the telemetry generator to populate the database.
2. Open the dashboard and inspect service latency trends.
3. Review the anomaly panel for a critical incident.
4. Use the raw data view to trace the failure path.
5. Extend the project with real ML or LLM-based root cause analysis.

## Simulated Incident Scenario

The project includes a sample cascade scenario designed to mimic a real distributed system failure:

- Database latency spikes to 5000ms and returns HTTP 503
- Order service fails shortly after due to downstream dependency issues
- API Gateway reports a bad gateway response to the caller

This makes the repository useful for demonstrating how observability teams can investigate root causes across service dependencies.

## Data Model

The telemetry table stores the following fields:

| Column | Description |
| --- | --- |
| timestamp | Event timestamp |
| trace_id | Unique request trace identifier |
| service_name | Service generating the request |
| endpoint | Endpoint or operation name |
| latency_ms | Latency in milliseconds |
| status_code | HTTP-like status result |

## Why This Project Matters

TraceMind AI demonstrates how observability data can be transformed into actionable system insight. It is especially helpful for:

- learning distributed tracing and telemetry concepts
- prototyping dashboards for cloud-native application monitoring
- exploring AI/ML techniques for root cause detection
- building a demo for incident response and on-call workflows

## Roadmap

Future enhancements could include:

- real anomaly detection using Isolation Forest or other ML models
- dependency graph analysis across services
- AI-generated incident summaries
- integration with OpenTelemetry collectors
- support for multi-tenant, multi-region monitoring
- alerting and Slack/email notifications

## License

This project is currently shared as an open demo/prototype for learning and experimentation.

## Contributing

Contributions are welcome. You can help by:

- improving the telemetry simulation
- adding real anomaly detection models
- enhancing the dashboard UX
- documenting the architecture and workflows

## Project Status

Status: MVP / demo prototype

This repository is intentionally simple and focused on demonstrating observability, trace analysis, and root-cause investigation in a way that can be expanded into a production-ready platform.

---

Built for exploring how AI can support modern observability workflows and incident analysis.
