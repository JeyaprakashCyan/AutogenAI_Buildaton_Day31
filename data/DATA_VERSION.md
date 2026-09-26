# Mock knowledge-base versioning

Documents are versioned by filename/metadata in the ingestion manifest. Increment `version` when a policy changes and rebuild the affected department index. The vector store metadata retains `source`, `version`, `page`, and `chunk_id` so answers can cite the document and page.

Example:
- employee_handbook.pdf -> version 1.0
- appraisal_and_growth_policy.pdf -> version 1.0
