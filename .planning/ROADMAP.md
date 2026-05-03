# ROADMAP

## Project: Local RAG using Ollama - Refactor and GUI Migration

### Goal
Transform the CLI-based RAG system into a modular, secure, and user-friendly Streamlit GUI application while maintaining all functionality.

### Requirements
- REQ-SEC-01: Remove hardcoded secrets and implement secure configuration management
- REQ-MOD-01: Refactor monolithic code into modular services
- REQ-ERR-01: Implement comprehensive error handling and logging
- REQ-GUI-01: Migrate CLI functionality to Streamlit GUI

### Phases

#### Phase 01: Security and Configuration
**Goal:** Fix critical security issues and implement proper configuration management.

**Requirements:** REQ-SEC-01

**Plans:** 2 plans

- [x] 01-01-PLAN.md — Implement secure config management
- [x] 01-02-PLAN.md — Remove hardcoded secrets and add input validation

#### Phase 02: Modular Architecture Refactor
**Goal:** Break down monolithic code into modular, maintainable services.

**Requirements:** REQ-MOD-01

**Plans:** 3 plans

- [x] 02-01-PLAN.md — Extract core services into modules
- [x] 02-02-PLAN.md — Implement dependency injection
- [x] 02-03-PLAN.md — Update main scripts to use modules

#### Phase 03: Error Handling and Logging
**Goal:** Add robust error handling, logging, and monitoring.

**Requirements:** REQ-ERR-01

**Plans:** 2 plans

- [x] 03-01-PLAN.md — Implement logging system
- [x] 03-02-PLAN.md — Add comprehensive error handling

#### Phase 04: Streamlit GUI Migration
**Goal:** Migrate all CLI functionality to a Streamlit web interface.

**Requirements:** REQ-GUI-01

**Plans:** 3 plans

- [x] 04-01-PLAN.md — Create Streamlit app structure
- [x] 04-02-PLAN.md — Implement document ingestion UI
- [x] 04-03-PLAN.md — Implement chat interface UI

### Success Criteria
- All functionality from CLI available in Streamlit GUI
- Code is modular, secure, and well-logged
- No hardcoded secrets
- Comprehensive error handling
- User can upload documents and chat via web interface
