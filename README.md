# X-Ray: Decision Observability for Multi-Step Systems
# Introduction:
Modern software systems don’t fail loudly — they fail silently and logically.

In many real-world pipelines (LLMs, heuristics, ranking logic), systems technically work while producing the wrong outcome. A recommendation feels off. A competitor match looks irrelevant. A filter removes something it shouldn’t have.

Traditional logs tell us what executed, but not why a specific decision was made.

When a final result is wrong, engineers are forced to reverse-engineer intent from scattered logs, rerun pipelines, or manually inspect intermediate data. This slows iteration, increases cognitive load, and makes non-deterministic systems hard to trust.

X-Ray is designed to solve this gap.

Instead of treating decision logic as opaque, X-Ray makes decision-making itself observable — capturing not just inputs and outputs, but the reasoning, filters, eliminations, and selections at every step.

# What This System Does

X-Ray provides end-to-end visibility into multi-step decision pipelines by:

Capturing structured decision data at each step

Preserving context, reasoning, and failure explanations

Storing execution trails in a queryable JSON format

Visualizing the full decision flow in a developer-friendly dashboard

# The demo simulates a competitor product selection system, but the architecture is intentionally general-purpose and reusable for:

Recommendation engines

Lead scoring systems

Content ranking pipelines

LLM-based evaluations

Any multi-step, non-deterministic decision process

# Architecture Overview

# The system is split into three cleanly separated layers:

1. X-Ray SDK (Instrumentation Layer)

A lightweight wrapper integrated into application logic that records step-level decision data:

Inputs and outputs

Candidate evaluations

Filters applied

Reasoning and explanations

Emits structured JSON logs for each execution.

2. Execution Log (Data Layer)

A single JSON file represents a full decision trace

Each step is self-contained and reconstructable

Designed to be human-readable and machine-queryable

3. Dashboard (Visualization Layer)

Reads X-Ray logs and renders them visually, allowing engineers to:

Inspect each step independently

Compare passed vs failed candidates

Identify where and why decisions diverged

Optimized for debugging, not presentation.

# Application Logic
      ↓
# X-Ray SDK (Decision Capture)
      ↓
# Structured JSON Execution Log
      ↓
# Streamlit Dashboard (Decision Visualization)

# Tech Stack

Language: Python (readability, fast prototyping)

SDK: Custom lightweight Python module

Data Format: JSON (transparent, portable, extensible)

Dashboard: Streamlit (fast internal tooling)

Charts: Plotly (interactive summaries)

Data Handling: Pandas (clean transformations)

The stack is intentionally chosen to optimize clarity and debuggability, not over-engineering.

# Key Design Decisions:

# JSON instead of a database
Enables fast iteration and easy inspection without premature persistence complexity.

# Streamlit for UI
Keeps focus on decision observability rather than frontend plumbing.

# Mock data instead of real integrations
Keeps the demo focused on system design, not API reliability.

# Simple SDK abstraction
Encourages reuse across domains without tight coupling.

System Components
Decision Pipeline

# A simulated multi-step pipeline mirroring real AI-driven systems:

Keyword generation (intent extraction)

Candidate search

Relevance evaluation (mock LLM-style logic)

Filtering and ranking via business constraints

Each step produces structured input, output, and reasoning.

X-Ray SDK

# Core responsibilities:

Record decision steps

Persist structured logs

Attach optional candidate-level evaluations

# Design choices:

Schema-flexible JSON logging

No dependency on LLMs, databases, or frameworks

Dashboard

Built for inspection, not vanity metrics.

# Capabilities:

Chronological step expanders

Side-by-side input/output views

Candidate tables with pass/fail status

Interactive filtering

Visual summaries for quick diagnosis

Data Model (Simplified)
# Decision Step

Step name

Timestamp

Input payload

Output payload

Reasoning text

Optional candidate evaluations

Candidate Evaluation

Unique identifier (asin)

Title

Metrics (price, rating, reviews, relevance)

Qualified status (true / false)

Failure reasons (if any)

# Visual encoding:

Green → qualified

Red → failed

Gold → final selection

# Setup & Usage
# Prerequisites:

Python 3.9+

pip

Installation
pip install streamlit pandas plotly

# Step 1: Run the Decision Pipeline
python demo_pipeline.py


Generates xray_log.json with the full execution trace.

# Step 2: Launch the Dashboard
streamlit run dashboard.py

Typical Debugging Flow

Start at the final selected output

Walk backward through earlier steps

Inspect eliminations and failure reasons

Identify whether issues came from:

Keyword generation

Candidate retrieval

Filtering thresholds

Ranking logic

# Known Limitations & Future Improvements

This implementation is intentionally lightweight. Planned improvements include:

Persistent storage backends (S3, MongoDB, ClickHouse)

Execution IDs for multi-run comparison

Diff views between pipeline executions

Asynchronous event streaming for high-volume pipelines

Sampling strategies for large candidate sets

Alerting on abnormal decision patterns

API-backed dashboard with saved views

Authentication & access control

LLM-native reasoning capture (token-level or prompt traces)

# Why This Matters

# Early-stage systems fail subtly:

Logic drifts

Heuristics accumulate

LLM behavior changes silently

# X-Ray provides:

Faster feedback loops

Confidence in automated decisions

A shared debugging language across engineering, product, and data teams

# Conclusion

This prototype demonstrates decision observability using a competitor selection workflow, but the architecture is intentionally general-purpose.

X-Ray helps engineers see not just what a system decided, but why — enabling trust, faster iteration, and prevention of silent failures before they compound.

This is tooling built for engineers: lightweight, extensible, and focused on clarity over vanity.
