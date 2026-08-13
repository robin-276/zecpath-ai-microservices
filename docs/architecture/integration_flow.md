# Zecpath ATS: API Integration & Async Flow

## 1. Asynchronous Job Handling Strategy

AI models (`sentence-transformers`, regex parsers) are computationally heavy. To prevent HTTP timeouts:

1. **Client Request:** The frontend uploads the resume to `/api/v1/ats/process-resume`.
2. **API Response:** The server immediately returns a `202 Accepted` status along with a `task_id`.
3. **Background Queue:** A background worker (e.g., Celery, Redis Queue) picks up the task, executes the Day 1 - Day 15 Python modules, and saves the final JSON to the database.
4. **Client Polling/Webhook:** The frontend polls a status endpoint using the `task_id` or listens for a WebSocket/Webhook event to know when the candidate is ready for review.

## 2. Standard Error Contracts

All API errors must return standard HTTP status codes and a consistent JSON structure to prevent frontend crashes.

**Format:**

```json
{
  "success": false,
  "error": {
    "code": "ERR_INVALID_FILE",
    "message": "The uploaded file exceeds the 5MB size limit."
  }
}
```

git add .
git commit -m "docs: add API specs, async integration flow, and bias reduction logic (Days 15 & 16)"
git push origin main
