# Data Model: AI/Spec-Driven Book with Integrated RAG Chatbot

## Overview
This document defines the data models for the AI-driven technical book with integrated RAG chatbot system. All models align with the functional requirements and support the constitutional principles of the project.

## Core Entities

### Book Content
- **Entity**: BookContent
- **Purpose**: Represents the technical book content in the system
- **Fields**:
  - `id`: UUID (Primary Key)
  - `title`: String (Content title)
  - `content`: Text (Markdown content)
  - `section`: String (Book section/chapter)
  - `page_path`: String (URL path for navigation)
  - `created_at`: DateTime
  - `updated_at`: DateTime
  - `version`: Integer (For tracking updates)
- **Validation**:
  - Title and content must not be empty
  - page_path must be unique
  - Content must be valid Markdown format
- **Relationships**: None

### Query
- **Entity**: Query
- **Purpose**: Represents user queries to the RAG system
- **Fields**:
  - `id`: UUID (Primary Key)
  - `query_text`: Text (User's question)
  - `user_id`: UUID (Optional, for tracking)
  - `scope`: String (enum: "full_book", "section", "page")
  - `section_id`: UUID (Optional, if scope is "section")
  - `created_at`: DateTime
- **Validation**:
  - query_text must not be empty
  - scope must be one of allowed values
- **Relationships**: One-to-many with QueryResponse

### Retrieved Context
- **Entity**: RetrievedContext
- **Purpose**: Represents the context retrieved from book content for a query
- **Fields**:
  - `id`: UUID (Primary Key)
  - `query_id`: UUID (Foreign Key to Query)
  - `content_id`: UUID (Foreign Key to BookContent)
  - `content_snippet`: Text (Relevant text snippet)
  - `similarity_score`: Float (0.0 to 1.0)
  - `page_path`: String (Source location)
  - `position`: Integer (Position in original content)
- **Validation**:
  - similarity_score must be between 0.0 and 1.0
  - content_snippet must not be empty
- **Relationships**: Many-to-one with Query and BookContent

### Query Response
- **Entity**: QueryResponse
- **Purpose**: Represents the AI's response to a user query
- **Fields**:
  - `id`: UUID (Primary Key)
  - `query_id`: UUID (Foreign Key to Query)
  - `response_text`: Text (AI-generated response)
  - `citations`: JSON (List of source citations)
  - `status`: String (enum: "success", "not_found", "error")
  - `created_at`: DateTime
  - `processing_time_ms`: Integer
- **Validation**:
  - response_text must not be empty when status is "success"
  - citations must be valid JSON when status is "success"
- **Relationships**: One-to-one with Query, One-to-many with ResponseCitation

### Response Citation
- **Entity**: ResponseCitation
- **Purpose**: Represents individual citations in a response
- **Fields**:
  - `id`: UUID (Primary Key)
  - `response_id`: UUID (Foreign Key to QueryResponse)
  - `content_id`: UUID (Foreign Key to BookContent)
  - `page_path`: String (Source location)
  - `content_snippet`: Text (Cited content)
  - `position`: Integer (Position in original content)
- **Validation**:
  - page_path must match the original content location
- **Relationships**: Many-to-one with QueryResponse and BookContent

## API Data Contracts

### Query Request
- **Purpose**: Request to query the RAG system
- **Structure**:
  ```json
  {
    "query": "string (required)",
    "scope": "enum (optional, default: 'full_book')",
    "section": "string (optional)"
  }
  ```
- **Validation**:
  - query: Required, minimum 3 characters
  - scope: One of ["full_book", "section", "page"]
  - section: Required only if scope is "section" or "page"

### Query Response
- **Purpose**: Response from the RAG system
- **Structure**:
  ```json
  {
    "response": "string",
    "status": "enum ('success', 'not_found', 'error')",
    "citations": [
      {
        "page_path": "string",
        "content_snippet": "string",
        "position": "integer"
      }
    ],
    "processing_time_ms": "integer"
  }
  ```
- **Validation**:
  - response: Always present
  - status: Always one of allowed values
  - citations: Present only when status is "success"
  - processing_time_ms: Always present

### Book Content Response
- **Purpose**: Response for book content operations
- **Structure**:
  ```json
  {
    "id": "uuid",
    "title": "string",
    "content": "string",
    "section": "string",
    "page_path": "string"
  }
  ```
- **Validation**:
  - All fields required

## State Transitions

### Query Processing Flow
1. **Query Received** → Query entity created with status "processing"
2. **Context Retrieved** → RetrievedContext entities created for relevant content
3. **Response Generated** → QueryResponse entity created with final status
4. **Completed** → Query entity updated with completion timestamp

### Content Lifecycle
1. **Content Added** → BookContent created with version 1
2. **Content Updated** → BookContent version incremented
3. **Content Indexed** → Content vectors updated in Qdrant
4. **Content Removed** → BookContent marked as deleted, vectors removed from Qdrant

## Constraints and Business Rules

### RAG Integrity Constraints
- All responses must be based only on retrieved context
- Citations must reference actual book content
- "Not found" responses must be returned when no relevant context exists
- Zero hallucination rate must be maintained

### Performance Constraints
- Query processing time must be under 3 seconds for 95% of requests
- Content indexing must complete within 10 seconds for normal-sized updates
- Vector search must return results within 500ms

### Data Integrity Constraints
- Book content must maintain referential integrity with citations
- Query history must be preserved for analytics
- Content versioning must be maintained for rollback capabilities