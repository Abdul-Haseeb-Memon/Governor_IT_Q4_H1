# API Contract: RAG System Validation

## Overview
This document specifies the API contracts for the RAG system validation endpoints.

## Validation Endpoints

### GET /validation/status
**Purpose**: Check the current status of the validation system

**Request**:
- Method: GET
- Path: /validation/status
- Headers: None required
- Query Parameters: None

**Response**:
- Status Code: 200 OK
- Content-Type: application/json
- Body:
```json
{
  "status": "running|completed|failed",
  "timestamp": "ISO 8601 timestamp",
  "components": {
    "006-ingestion": "not_started|running|passed|failed",
    "007-retrieval": "not_started|running|passed|failed",
    "008-generation": "not_started|running|passed|failed",
    "009-frontend": "not_started|running|passed|failed"
  }
}
```

### POST /validation/run
**Purpose**: Execute the complete RAG system validation

**Request**:
- Method: POST
- Path: /validation/run
- Headers:
  - Content-Type: application/json
- Body:
```json
{
  "components": ["006", "007", "008", "009"],
  "apply_corrections": true
}
```

**Response**:
- Status Code: 200 OK
- Content-Type: application/json
- Body:
```json
{
  "validation_id": "unique validation identifier",
  "status": "running|completed|failed",
  "results": [
    {
      "component_id": "006|007|008|009",
      "name": "ingestion|retrieval|generation|frontend",
      "status": "passed|failed|error",
      "message": "descriptive message about the result",
      "error_details": "details if failed, null otherwise",
      "corrective_action_applied": "description of action if applicable"
    }
  ],
  "overall_status": "passed|failed",
  "timestamp": "ISO 8601 timestamp"
}
```

### GET /validation/results/{validation_id}
**Purpose**: Retrieve the results of a specific validation run

**Request**:
- Method: GET
- Path: /validation/results/{validation_id}
- Headers: None required
- Path Parameters:
  - validation_id: ID of the validation run to retrieve

**Response**:
- Status Code: 200 OK
- Content-Type: application/json
- Body:
```json
{
  "validation_id": "unique validation identifier",
  "status": "completed|failed",
  "results": [
    {
      "component_id": "006|007|008|009",
      "name": "ingestion|retrieval|generation|frontend",
      "status": "passed|failed|error",
      "message": "descriptive message about the result",
      "error_details": "details if failed, null otherwise",
      "corrective_action_applied": "description of action if applicable"
    }
  ],
  "overall_status": "passed|failed",
  "start_time": "ISO 8601 timestamp",
  "end_time": "ISO 8601 timestamp",
  "duration_seconds": 123
}
```

## Component-Specific Endpoints

### POST /validation/run-component
**Purpose**: Execute validation for a specific component

**Request**:
- Method: POST
- Path: /validation/run-component
- Headers:
  - Content-Type: application/json
- Body:
```json
{
  "component_id": "006|007|008|009",
  "apply_corrections": true
}
```

**Response**:
- Status Code: 200 OK
- Content-Type: application/json
- Body:
```json
{
  "component_id": "006|007|008|009",
  "name": "ingestion|retrieval|generation|frontend",
  "status": "passed|failed|error",
  "message": "descriptive message about the result",
  "error_details": "details if failed, null otherwise",
  "corrective_action_applied": "description of action if applicable",
  "timestamp": "ISO 8601 timestamp"
}
```

## Error Responses
All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "error": "bad_request",
  "message": "descriptive error message",
  "details": "additional details about the error"
}
```

### 500 Internal Server Error
```json
{
  "error": "internal_server_error",
  "message": "an unexpected error occurred",
  "details": "additional details about the error"
}
```

## Security Considerations
- All validation endpoints should be secured with appropriate authentication in production
- API keys should be validated before allowing validation runs
- Rate limiting should be applied to prevent abuse