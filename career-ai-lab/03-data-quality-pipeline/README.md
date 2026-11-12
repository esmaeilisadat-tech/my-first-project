# 03 — Traceable Event Data Quality Pipeline

**Inspired by:** DB Systel Data Engineer (data integration, ETL, quality checks, metadata and provenance).

## Current MVP
A tiny batch ETL on **synthetic transit events**. It validates IDs, day, station and passenger counts, rejects invalid/duplicate events with explicit reasons, aggregates accepted data by day and station, and creates a minimal lineage summary.

Run: python career-ai-lab/03-data-quality-pipeline/pipeline.py

## Next milestones
1. CSV/JSON input adapters with explicit data contracts and batch IDs.
2. PostgreSQL/DuckDB storage with replay-safe upserts and SQL checks.
3. Incremental processing, partitioning, retries and structured logs.
4. Document chunking and permission-aware retrieval for RAG workloads.
5. CI, cost/latency monitoring and operational dashboard.

No actual Deutsche Bahn data or internal systems are used.