# Architecture — Smart Expense Categorization System

## Service Components
1. **Ingestion API**
   - Validates and stores incoming transactions.
   - Enforces idempotency and schema rules.

2. **Normalization & Enrichment Service**
   - Merchant normalization (name cleanup, alias mapping).
   - Optional enrichments (MCC mapping, geolocation).

3. **Rules Engine**
   - Priority-ordered rules for deterministic categories.
   - Configurable per tenant.

4. **ML Classification Service**
   - Produces category predictions with confidence scores.
   - Exposes versioned models and explainability metadata.

5. **Human Review Service**
   - Queue for low-confidence or flagged items.
   - Captures corrected labels and feedback.

6. **Reporting Service**
   - Aggregations and exports.
   - Cached summaries for faster dashboard queries.

## Data Model (Core)
- **transactions**
  - `id`, `external_id`, `amount`, `currency`, `timestamp`, `merchant_raw`, `merchant_normalized`, `mcc`, `category_id`, `confidence`, `status`
- **categories**
  - `id`, `name`, `parent_id`, `taxonomy_version`
- **rules**
  - `id`, `tenant_id`, `priority`, `match_type`, `pattern`, `category_id`
- **review_queue**
  - `transaction_id`, `reason`, `assigned_to`, `status`
- **model_versions**
  - `id`, `name`, `trained_at`, `metrics`, `artifact_uri`

## API Surface (Draft)
### POST /v1/transactions
- Request: `{ external_id, amount, currency, timestamp, merchant_raw, metadata }`
- Response: `{ transaction_id, status }`

### POST /v1/transactions/{id}/categorize
- Response: `{ category_id, confidence, explanation }`

### GET /v1/review-queue
- Response: `[{ transaction_id, reason, suggested_category }]`

### POST /v1/review-queue/{id}/resolve
- Request: `{ category_id, notes }`

## ML Lifecycle
- Feature extraction: text features, MCC, amount buckets, time-of-day.
- Training data: labeled transactions from human review and overrides.
- Monitoring: drift detection and category distribution shifts.

## Deployment
- Containerized services (Docker).
- Orchestrated with Kubernetes (HPA for autoscaling).
- CI/CD pipeline for tests, linting, and security scans.
