# Sprint Backlog

**Generated**: 2026-02-27
**Source**: user_stories.md
**Team Calibration**: 1 SP = 1 day (adjust in config.yml)
**Status**: 🟡 Ready for Sprint Planning

---

## 🏗️ Architecture & Non-Functional Stories

### Story A1: Setup Core Cloud Infrastructure
#### Description:
As a DevOps engineer, I want to provision the foundational cloud infrastructure (VPC, subnets, basic compute, database service, object storage), so that development teams have a secure and scalable environment to deploy the application.
**Details**:
-   **Tech Stack**: AWS CloudFormation (or Terraform for IaC), AWS VPC, AWS ECS Fargate (for containerized services), AWS RDS for PostgreSQL, AWS S3 for object storage.
-   **Infrastructure**:
    -   A dedicated VPC with public and private subnets across at least two Availability Zones.
    -   NAT Gateways for private subnet outbound internet access.
    -   Internet Gateway for public subnet internet access.
    -   Security Groups configured for least privilege access between components (e.g., web servers to DB, DB to itself).
    -   ECS Cluster with Fargate launch type for backend and potentially frontend static asset hosting.
    -   RDS PostgreSQL instance (db.t3.medium or similar for dev/test).
    -   S3 bucket for raw file uploads and processed data.
    -   Basic IAM roles and policies for services to interact securely.
-   **Performance Targets**: Initial setup focused on correctness and security, not specific performance targets beyond basic responsiveness.
-   **Security Requirements**: Adherence to AWS best practices for networking and IAM.
-   **Scalability**: Initial setup supports horizontal scaling for ECS Fargate and RDS read replicas (future).
-   **Constraints**: Must use AWS services. Infrastructure as Code (IaC) is mandatory.

#### Acceptance Criteria
- [x] A dedicated AWS VPC is provisioned with public and private subnets across at least two Availability Zones.
- [x] NAT Gateways are configured in public subnets to allow private subnet instances outbound internet access.
- [x] Security Groups are defined and applied to restrict traffic between components (e.g., only backend ECS tasks can connect to RDS).
- [x] An AWS RDS PostgreSQL instance (e.g., `db.t3.medium`) is provisioned within a private subnet.
- [x] An AWS S3 bucket is created for application data storage (e.g., `audit-sampling-gl-data-[env]`).
- [x] An AWS ECS Cluster is provisioned with Fargate launch type.
- [x] Core IAM roles (e.g., ECS Task Execution Role, RDS Access Role) with least privilege are created.
- [x] All infrastructure is defined and deployable via CloudFormation/Terraform.
- [x] Basic documentation for the core infrastructure setup is provided.

#### Effort Estimate: **4 SP**
**Complexity**: Medium

**Breakdown**:
- DevOps: 100% (4 days)

**Reasoning**:
```
Day 1:
- Research and select IaC tool (e.g., CloudFormation vs Terraform - assume CloudFormation for native AWS). (2 hours)
- Define VPC, subnets, Internet Gateway, NAT Gateways in CloudFormation. (6 hours)

Day 2:
- Define Security Groups for various layers (web, app, db). (4 hours)
- Define RDS PostgreSQL instance and associated security. (4 hours)

Day 3:
- Define S3 bucket with appropriate policies. (3 hours)
- Define ECS Cluster and basic Task Execution/Role definitions. (5 hours)

Day 4:
- Review and refine CloudFormation templates. (4 hours)
- Initial deployment to a dev environment and verification. (4 hours)
```

**Risk Factors**:
- ⚠️ **Complexity of AWS Networking**: Incorrect subnet or routing table configuration could lead to connectivity issues. Mitigation: Thorough review of CloudFormation templates, use of AWS best practices, and small, iterative deployments.
- ⚠️ **IAM Permissions**: Overly permissive or restrictive IAM policies could cause security vulnerabilities or deployment failures. Mitigation: Start with minimal permissions and iterate, use IAM Access Analyzer.

**Dependencies**: None

**Build Order**: #1

---

### Story A2: Establish Core Database & User Schema
#### Description:
As a backend engineer, I want to set up the PostgreSQL database instance and define the initial schema for user authentication and authorization, so that user accounts and roles can be securely stored and managed.
**Details**:
-   **Tech Stack**: PostgreSQL (on AWS RDS), SQLAlchemy (Python ORM), Alembic (database migrations).
-   **Data Model**:
    -   `users` table: `id` (UUID, PK), `email` (VARCHAR, UNIQUE), `password_hash` (VARCHAR), `first_name` (VARCHAR), `last_name` (VARCHAR), `is_active` (BOOLEAN, DEFAULT TRUE), `created_at` (TIMESTAMP), `updated_at` (TIMESTAMP).
    -   `roles` table: `id` (UUID, PK), `name` (VARCHAR, UNIQUE, e.g., 'Auditor', 'Manager').
    -   `user_roles` join table: `user_id` (FK to users.id), `role_id` (FK to roles.id), composite PK.
-   **Constraints**: Passwords must be hashed using a strong algorithm (e.g., bcrypt). Email must be unique.

#### Acceptance Criteria
- [x] PostgreSQL database instance is accessible from the application layer (via A1).
- [x] `users` table is created with `id`, `email`, `password_hash`, `first_name`, `last_name`, `is_active`, `created_at`, `updated_at` fields.
- [x] `email` field in `users` table has a unique constraint.
- [x] `roles` table is created with `id` and `name` fields, `name` having a unique constraint.
- [x] `user_roles` join table is created with foreign keys linking to `users` and `roles` tables.
- [x] Initial roles ('Auditor', 'Manager') are seeded into the `roles` table.
- [x] Database migrations are managed using Alembic (or similar tool).
- [x] Connection string and credentials are securely managed (e.g., AWS Secrets Manager or environment variables).

#### Effort Estimate: **2 SP**
**Complexity**: High

**Breakdown**:
- Backend: 75% (1.5 days)
- DevOps: 25% (0.5 days)

**Reasoning**:
```
Day 1:
- Design database schema for users, roles, and user_roles. (3 hours)
- Set up Alembic for migrations. (3 hours)
- Write initial migration script for user and role tables. (2 hours)

Day 2:
- Implement initial seeding script for 'Auditor' and 'Manager' roles. (2 hours)
- Test database connection from a sample application/script. (3 hours)
- Document schema and migration process. (3 hours)
```

**Risk Factors**:
- ⚠️ **Schema Changes**: Future changes to the core user schema might be complex if not designed carefully. Mitigation: Use a robust migration tool (Alembic) and plan for extensibility.
- ⚠️ **Security of Credentials**: Database credentials must be handled with extreme care. Mitigation: Use AWS Secrets Manager or environment variables, not hardcoded values.

**Dependencies**: A1 (Database instance provisioned)

**Build Order**: #2

---

### Story A3: Implement CI/CD Pipeline for Backend & Frontend
#### Description:
As a DevOps engineer, I want to establish automated Continuous Integration and Continuous Deployment pipelines for both backend and frontend services, so that code changes can be efficiently tested, built, and deployed to development environments.
**Details**:
-   **Tech Stack**: GitHub Actions (for CI/CD orchestration), Docker (for containerization), AWS ECR (for Docker image storage), AWS ECS Fargate (for backend deployment), AWS S3 + CloudFront (for frontend static site hosting).
-   **Infrastructure**:
    -   GitHub repository configured with GitHub Actions workflows.
    -   AWS ECR repositories for backend and frontend Docker images.
    -   S3 bucket for frontend static assets, optionally with CloudFront for CDN.
    -   ECS Service definitions for backend (pointing to ECR images).
-   **Performance Targets**: CI build time < 10 minutes, CD deployment time < 5 minutes.
-   **Security Requirements**: IAM roles for GitHub Actions to interact with AWS, secure credential management.
-   **Constraints**: Must support both Python/FastAPI backend and React/TypeScript frontend.

#### Acceptance Criteria
- [x] GitHub Actions workflow is configured for the backend service.
- [x] Backend CI pipeline automatically triggers on push to `develop` branch.
- [x] Backend CI pipeline runs tests, builds a Docker image, and pushes it to AWS ECR.
- [x] Backend CD pipeline automatically deploys the latest image from ECR to a development ECS Fargate service.
- [x] GitHub Actions workflow is configured for the frontend service.
- [x] Frontend CI pipeline automatically triggers on push to `develop` branch.
- [x] Frontend CI pipeline runs tests, builds static assets.
- [x] Frontend CD pipeline automatically deploys static assets to an S3 bucket (and invalidates CloudFront cache if used).
- [x] Deployment status and logs are easily viewable in GitHub Actions.
- [x] IAM roles for GitHub Actions have minimal necessary permissions to interact with AWS.

#### Effort Estimate: **5 SP**
**Complexity**: Medium

**Breakdown**:
- DevOps: 100% (5 days)

**Reasoning**:
```
Day 1:
- Research GitHub Actions AWS integration. (2 hours)
- Set up AWS ECR repositories for backend and frontend. (2 hours)
- Create basic Dockerfiles for backend (FastAPI) and frontend (React). (4 hours)

Day 2:
- Implement backend CI workflow: checkout, setup Python, install dependencies, run tests, build Docker image. (5 hours)
- Configure push to ECR in backend CI workflow. (3 hours)

Day 3:
- Implement backend CD workflow: pull image from ECR, update ECS service definition. (6 hours)
- Test backend CI/CD pipeline end-to-end. (2 hours)

Day 4:
- Implement frontend CI workflow: checkout, setup Node.js, install dependencies, run tests, build static assets. (5 hours)
- Configure S3 bucket for static hosting and optionally CloudFront. (3 hours)

Day 5:
- Implement frontend CD workflow: sync static assets to S3, invalidate CloudFront cache. (5 hours)
- Test frontend CI/CD pipeline end-to-end. (3 hours)
```

**Risk Factors**:
- ⚠️ **Cross-Account/Cross-Service Permissions**: Getting IAM roles and permissions correct for GitHub Actions to interact with AWS services can be tricky. Mitigation: Start with a clear IAM policy, use `aws-actions/configure-aws-credentials` and `aws-actions/amazon-ecs-deploy` actions.
- ⚠️ **Deployment Rollbacks**: Initial pipeline might not have robust rollback mechanisms. Mitigation: Plan for manual rollbacks initially, then automate with ECS deployment strategies (e.g., blue/green) in a later story.

**Dependencies**: A1 (ECS Cluster, S3 bucket, ECR repositories), A5 (API Gateway for backend endpoint)

**Build Order**: #3

---

### Story A4: Configure Basic Application Monitoring & Alerting
#### Description:
As a DevOps engineer, I want to set up basic application performance monitoring (APM) and error alerting, so that we can proactively identify and respond to system health issues and errors.
**Details**:
-   **Tech Stack**: AWS CloudWatch Logs, CloudWatch Metrics, CloudWatch Alarms, AWS SNS (for notifications).
-   **Infrastructure**:
    -   ECS Fargate tasks configured to send logs to CloudWatch Logs.
    -   CloudWatch Metric Filters for key log patterns (e.g., "ERROR", "5xx").
    -   CloudWatch Alarms based on CPU/Memory utilization of ECS tasks, and custom metrics from log filters.
    -   SNS Topic for sending alerts (e.g., to email or Slack).
-   **Performance Targets**: Alerts triggered within 5 minutes of an incident.
-   **Security Requirements**: IAM roles for ECS tasks to write logs, SNS topic access control.

#### Acceptance Criteria
- [x] Backend ECS Fargate tasks are configured to send application logs to AWS CloudWatch Logs.
- [x] Frontend application (if server-side rendered) or CDN logs are configured to send logs to CloudWatch Logs.
- [x] CloudWatch Metric Filters are created to extract key metrics from logs (e.g., count of "ERROR" messages, count of 5xx HTTP responses).
- [x] CloudWatch Alarms are configured for:
    -   ECS Service CPU Utilization > 80% for 5 minutes.
    -   ECS Service Memory Utilization > 80% for 5 minutes.
    -   Count of "ERROR" log messages > 0 for 1 minute.
    -   Count of 5xx HTTP responses > 0 for 1 minute.
- [x] An SNS Topic is created and configured to send notifications (e.g., email) when an alarm state is reached.
- [x] A basic CloudWatch Dashboard is created to visualize key application metrics (CPU, Memory, Error counts).
- [x] Documentation on how to access logs, metrics, and alerts is provided.

#### Effort Estimate: **2 SP**
**Complexity**: Medium

**Breakdown**:
- DevOps: 100% (2 days)

**Reasoning**:
```
Day 1:
- Configure ECS task definitions to send logs to CloudWatch Logs. (4 hours)
- Create CloudWatch Log Groups and ensure logs are flowing. (2 hours)
- Define CloudWatch Metric Filters for common error patterns (e.g., "ERROR", "Exception"). (2 hours)

Day 2:
- Create CloudWatch Alarms for CPU, Memory, and custom error metrics. (4 hours)
- Set up an SNS Topic and subscription for notifications. (2 hours)
- Create a basic CloudWatch Dashboard. (2 hours)
```

**Risk Factors**:
- ⚠️ **Alert Fatigue**: Too many non-critical alerts can lead to engineers ignoring them. Mitigation: Start with critical alerts and refine thresholds based on observed behavior.
- ⚠️ **Log Volume/Cost**: High log volume can incur significant costs. Mitigation: Implement log retention policies and filter out verbose debug logs in production.

**Dependencies**: A1 (ECS Fargate, CloudWatch Logs), A3 (CI/CD to deploy logging config)

**Build Order**: #4

---

### Story A5: Secure Backend API Gateway & TLS
#### Description:
As a security engineer, I want to configure an API Gateway with TLS 1.2+ encryption for all backend endpoints, so that all data in transit between the frontend and backend is secured against eavesdropping.
**Details**:
-   **Tech Stack**: AWS API Gateway, AWS Certificate Manager (ACM), Route 53 (for custom domain).
-   **Infrastructure**:
    -   API Gateway REST API (or HTTP API) configured as a proxy for the backend ECS service.
    -   Custom domain name (e.g., `api.auditsampling.com`) associated with the API Gateway.
    -   TLS 1.2+ enforced using an ACM-managed certificate.
    -   Basic AWS WAF integration for common web exploits (optional, but good practice).
-   **Performance Targets**: API Gateway latency < 50ms (p95).
-   **Security Requirements**: TLS 1.2+ enforcement, secure certificate management, WAF rules.
-   **Constraints**: Must use a custom domain.

#### Acceptance Criteria
- [x] An AWS API Gateway (REST or HTTP) is provisioned and configured to proxy requests to the backend ECS service.
- [x] A custom domain name (e.g., `api.auditsampling.com`) is configured for the API Gateway.
- [x] An SSL/TLS certificate is provisioned via AWS Certificate Manager (ACM) for the custom domain.
- [x] The API Gateway is configured to enforce TLS 1.2 or higher for all connections.
- [x] DNS records (e.g., A record or CNAME) in Route 53 are updated to point the custom domain to the API Gateway.
- [x] All backend API endpoints are accessible only through the API Gateway.
- [x] A basic AWS WAF Web ACL is associated with the API Gateway (e.g., AWSManagedRulesCommonRuleSet).
- [x] Documentation on API Gateway setup and TLS configuration is provided.

#### Effort Estimate: **3 SP**
**Complexity**: Medium

**Breakdown**:
- DevOps: 100% (3 days)

**Reasoning**:
```
Day 1:
- Research API Gateway options (REST vs HTTP API) and integration with ECS. (3 hours)
- Provision API Gateway and configure basic proxy integration with ECS service. (5 hours)

Day 2:
- Request/import SSL/TLS certificate via ACM for the custom domain. (4 hours)
- Configure custom domain name in API Gateway and associate the ACM certificate. (4 hours)

Day 3:
- Update Route 53 DNS records to point to API Gateway. (3 hours)
- Test TLS enforcement and API accessibility through the custom domain. (3 hours)
- Configure basic AWS WAF Web ACL and associate with API Gateway. (2 hours)
```

**Risk Factors**:
- ⚠️ **DNS Propagation Delays**: Changes to DNS records can take time to propagate, impacting testing. Mitigation: Plan for propagation time, use DNS checkers.
- ⚠️ **Certificate Management**: Ensuring certificates are renewed automatically and correctly. Mitigation: ACM handles renewals automatically, but verify setup.

**Dependencies**: A1 (VPC, ECS service), A3 (CI/CD to deploy backend service behind API Gateway), External: Domain name registration.

**Build Order**: #5

---

### Story A6: Design & Implement GL Data Storage Schema
#### Description:
As a backend engineer, I want to design and implement the database schema for storing uploaded GL data and associated metadata, so that large datasets can be efficiently stored, queried, and linked to sampling activities.
**Details**:
-   **Tech Stack**: PostgreSQL (on AWS RDS), SQLAlchemy (Python ORM), Alembic (database migrations).
-   **Data Model**:
    -   `engagements` table: `id` (UUID, PK), `name` (VARCHAR), `client_name` (VARCHAR), `start_date` (DATE), `end_date` (DATE), `user_id` (FK to users.id), `created_at`, `updated_at`.
    -   `gl_datasets` table: `id` (UUID, PK), `engagement_id` (FK to engagements.id), `original_filename` (VARCHAR), `upload_date` (TIMESTAMP), `status` (ENUM: 'uploaded', 'parsing', 'validated', 'error'), `total_records` (INT), `total_value` (NUMERIC), `currency` (VARCHAR), `uploaded_by_user_id` (FK to users.id).
    -   `gl_transactions` table: `id` (UUID, PK), `dataset_id` (FK to gl_datasets.id), `transaction_id` (VARCHAR), `account_id` (VARCHAR), `transaction_date` (DATE), `amount` (NUMERIC), `description` (TEXT), `source_system` (VARCHAR), `other_mapped_field_1` (TEXT), `other_mapped_field_2` (TEXT), `risk_score` (NUMERIC, NULLABLE), `is_selected_for_sample` (BOOLEAN, DEFAULT FALSE), `selected_sample_id` (FK to samples.id, NULLABLE), `created_at`, `updated_at`.
-   **Indexing**: `gl_transactions.dataset_id`, `gl_transactions.transaction_date`, `gl_transactions.amount`, `gl_transactions.risk_score`.
-   **Constraints**: `transaction_id` + `dataset_id` should be unique. `amount` should be non-negative.

#### Acceptance Criteria
- [x] `engagements` table is created with `id`, `name`, `client_name`, `start_date`, `end_date`, `user_id`, `created_at`, `updated_at` fields.
- [x] `gl_datasets` table is created with `id`, `engagement_id`, `original_filename`, `upload_date`, `status`, `total_records`, `total_value`, `currency`, `uploaded_by_user_id` fields.
- [x] `gl_transactions` table is created with `id`, `dataset_id`, `transaction_id`, `account_id`, `transaction_date`, `amount`, `description`, `source_system`, `other_mapped_field_X` (at least 2 generic fields), `risk_score`, `is_selected_for_sample`, `selected_sample_id` fields.
- [x] Foreign key constraints are correctly defined between `engagements`, `gl_datasets`, and `gl_transactions` tables.
- [x] Unique constraint on `(transaction_id, dataset_id)` in `gl_transactions` table.
- [x] Appropriate indexes are created on `gl_transactions.dataset_id`, `gl_transactions.transaction_date`, `gl_transactions.amount`, and `gl_transactions.risk_score` for efficient querying.
- [x] Database migrations are created using Alembic to apply the new schema.
- [x] Documentation for the GL data schema is updated.

#### Effort Estimate: **3 SP**
**Complexity**: High

**Breakdown**:
- Backend: 100% (3 days)

**Reasoning**:
```
Day 1:
- Design detailed schema for engagements, datasets, and transactions, considering future needs (e.g., generic fields for mapping). (4 hours)
- Identify necessary indexes for performance. (2 hours)
- Define relationships and constraints. (2 hours)

Day 2:
- Write Alembic migration script to create all new tables and indexes. (6 hours)
- Review migration script for correctness and potential issues. (2 hours)

Day 3:
- Test schema creation and basic data insertion/retrieval. (4 hours)
- Update ORM models (SQLAlchemy) to reflect the new schema. (4 hours)
```

**Risk Factors**:
- ⚠️ **Schema Evolution**: Changes to the core GL data schema after initial deployment can be complex and require data migration. Mitigation: Design for flexibility with generic fields and consider future requirements carefully.
- ⚠️ **Performance with Large Datasets**: Inefficient indexing or schema design could lead to slow queries for large GL datasets. Mitigation: Proactive indexing, consider partitioning for very large tables (future optimization).

**Dependencies**: A2 (Core DB setup), B5 (GL Data Storage Service will use this schema)

**Build Order**: #6

---

### Story A7: Design & Implement Audit Trail Database Schema
#### Description:
As a backend engineer, I want to design and implement an immutable database schema for the audit trail, including user actions, system decisions, and parameter changes, so that all significant activities are securely logged and traceable (FR5).
**Details**:
-   **Tech Stack**: PostgreSQL (on AWS RDS), SQLAlchemy (Python ORM), Alembic (database migrations).
-   **Data Model**:
    -   `audit_logs` table: `id` (UUID, PK), `timestamp` (TIMESTAMP, DEFAULT NOW()), `user_id` (FK to users.id, NULLABLE for system actions), `engagement_id` (FK to engagements.id, NULLABLE for global actions), `action_type` (VARCHAR, e.g., 'GL_UPLOAD', 'SAMPLE_CALC', 'SAMPLE_OVERRIDE'), `description` (TEXT), `details` (JSONB for structured data, e.g., old_value, new_value, parameters), `ip_address` (VARCHAR, NULLABLE).
-   **Immutability**: No UPDATE or DELETE operations allowed on this table.
-   **Indexing**: `audit_logs.timestamp`, `audit_logs.user_id`, `audit_logs.engagement_id`, `audit_logs.action_type`.

#### Acceptance Criteria
- [x] `audit_logs` table is created with `id`, `timestamp`, `user_id`, `engagement_id`, `action_type`, `description`, `details` (JSONB), `ip_address` fields.
- [x] `timestamp` field defaults to the current time and is not nullable.
- [x] Foreign key constraints are correctly defined for `user_id` (to users.id) and `engagement_id` (to engagements.id).
- [x] Appropriate indexes are created on `timestamp`, `user_id`, `engagement_id`, and `action_type` for efficient querying.
- [x] Database migrations are created using Alembic to apply the new schema.
- [x] Database-level constraints or triggers are considered (if necessary) to enforce immutability (e.g., no UPDATE/DELETE).
- [x] Documentation for the audit trail schema is provided.

#### Effort Estimate: **2 SP**
**Complexity**: Medium

**Breakdown**:
- Backend: 100% (2 days)

**Reasoning**:
```
Day 1:
- Design detailed schema for audit logs, focusing on immutability and comprehensive logging. (4 hours)
- Define `action_type` enumeration and `details` JSONB structure. (2 hours)
- Write Alembic migration script to create the `audit_logs` table and indexes. (2 hours)

Day 2:
- Review migration script and schema for immutability and completeness. (3 hours)
- Test schema creation and basic data insertion. (3 hours)
- Update ORM models (SQLAlchemy) for the new schema. (2 hours)
```

**Risk Factors**:
- ⚠️ **Data Volume**: Audit trails can grow very large. Mitigation: Ensure efficient indexing, consider partitioning or archiving strategies for long-term storage (future optimization).
- ⚠️ **Immutability Enforcement**: Relying solely on application logic for immutability can be risky. Mitigation: Consider database-level policies or triggers to prevent updates/deletes (e.g., row-level security, `BEFORE UPDATE/DELETE` triggers).

**Dependencies**: A2 (Core DB setup), A6 (Engagements table for FK), B10 (Audit Trail Logging API will use this schema)

**Build Order**: #7

---

### Story A8: Implement Data Encryption at Rest for GL Data
#### Description:
As a security engineer, I want to configure encryption at rest for all GL data stored in the database and object storage, so that sensitive financial information is protected in compliance with NFR2.1.
**Details**:
-   **Tech Stack**: AWS RDS Encryption (KMS), AWS S3 Server-Side Encryption (SSE-KMS).
-   **Infrastructure**:
    -   AWS Key Management Service (KMS) Customer Master Key (CMK) for encryption.
    -   RDS PostgreSQL instance configured with KMS encryption.
    -   S3 bucket for GL data configured with default SSE-KMS encryption.
-   **Security Requirements**: Use AWS KMS for key management, encryption of all sensitive data at rest.
-   **Compliance**: NFR2.1 (Data Protection).
-   **Constraints**: Must use AWS native encryption services.

#### Acceptance Criteria
- [x] An AWS KMS Customer Master Key (CMK) is created and configured for data encryption.
- [x] The AWS RDS PostgreSQL instance storing GL data is configured to use the KMS CMK for encryption at rest.
- [x] The AWS S3 bucket storing raw GL data files is configured with default server-side encryption using SSE-KMS and the created CMK.
- [x] Verification steps are documented to confirm that both RDS and S3 data are encrypted at rest.
- [x] IAM policies are updated to ensure services (e.g., ECS tasks) have permission to use the KMS key for encryption/decryption.
- [x] Documentation on encryption configuration and key management is provided.

#### Effort Estimate: **2 SP**
**Complexity**: Medium

**Breakdown**:
- DevOps: 100% (2 days)

**Reasoning**:
```
Day 1:
- Create a new KMS Customer Master Key (CMK). (3 hours)
- Configure RDS instance to use the KMS CMK for encryption (requires recreating if not done at creation). (5 hours)

Day 2:
- Configure S3 bucket default encryption to use SSE-KMS with the CMK. (4 hours)
- Update IAM roles for services (e.g., ECS tasks) to grant KMS decrypt permissions. (2 hours)
- Verify encryption status for both RDS and S3. (2 hours)
```

**Risk Factors**:
- ⚠️ **Data Loss/Corruption**: Incorrectly configuring encryption or key management can lead to data inaccessibility. Mitigation: Thorough testing in non-production environments, careful management of KMS key access.
- ⚠️ **Performance Impact**: While usually minimal, encryption/decryption can add overhead. Mitigation: Monitor performance after implementation, especially for high-volume operations.

**Dependencies**: A1 (RDS, S3), A6 (GL Data Storage Schema)

**Build Order**: #8

---

### Story A9: Setup Performance Testing Framework
#### Description:
As a QA engineer, I want to set up a performance testing framework, so that we can systematically test the application's performance against NFR1 (e.g., data upload, calculation, export speeds) with large datasets.
**Details**:
-   **Tech Stack**: k6 (or JMeter) for load generation, Grafana/Prometheus (or CloudWatch) for monitoring, Docker for test runner.
-   **Infrastructure**:
    -   Dedicated EC2 instance or containerized environment for running k6/JMeter tests.
    -   Integration with existing monitoring (CloudWatch) or new setup (Prometheus/Grafana).
-   **Performance Targets**: Framework capable of simulating 100 concurrent users for 30 minutes.
-   **Constraints**: Must be scriptable and integrate with CI/CD (future).

#### Acceptance Criteria
- [x] A performance testing tool (e.g., k6) is selected and installed in a dedicated environment (e.g., Docker container, EC2 instance).
- [x] A basic k6 script is created to simulate a simple user flow (e.g., login, upload a small file).
- [x] The framework can execute the script and generate basic performance metrics (e.g., response times, throughput, error rates).
- [x] Test results can be stored and visualized (e.g., local HTML report, integration with CloudWatch/Grafana).
- [x] The performance testing environment is documented, including setup instructions and how to run tests.
- [x] The framework is capable of simulating at least 10 concurrent users.

#### Effort Estimate: **3 SP**
**Complexity**: Medium

**Breakdown**:
- DevOps: 50% (1.5 days)
- QA: 50% (1.5 days)

**Reasoning**:
```
Day 1:
- Research and select a performance testing tool (e.g., k6 for modern JS scripting). (3 hours)
- Set up a dedicated environment (e.g., Docker image for k6 runner). (5 hours)

Day 2:
- Write a basic k6 script for a simple API call (e.g., login endpoint). (4 hours)
- Configure k6 to run and output basic metrics. (4 hours)

Day 3:
- Integrate k6 with a reporting mechanism (e.g., local HTML report, or push to CloudWatch/Grafana). (4 hours)
- Document setup and basic usage. (4 hours)
```

**Risk Factors**:
- ⚠️ **Tool Complexity**: Learning a new performance testing tool can have a steep curve. Mitigation: Start with simple scripts, leverage community resources.
- ⚠️ **Environment Setup**: Ensuring the test runner environment is stable and isolated. Mitigation: Use Docker for consistent environments.

**Dependencies**: A1 (Cloud infrastructure), A4 (Monitoring for target system), B1 (Login API for initial test script)

**Build Order**: #9

---

### Story A10: Scalability Testing for Data Ingestion
#### Description:
As a QA engineer, I want to conduct initial scalability tests for GL data upload and parsing, so that we can ensure the system can handle large datasets and concurrent uploads without degradation, as per NFR3.
**Details**:
-   **Tech Stack**: k6 (or JMeter), pre-generated large CSV/Excel files (e.g., 100k-1M rows), CloudWatch/Grafana for monitoring.
-   **Infrastructure**: Utilize the framework from A9.
-   **Performance Targets**:
    -   Upload of a 100,000-row GL data file completes within 5 minutes.
    -   Parsing of a 100,000-row GL data file completes within 10 minutes.
    -   System maintains < 200ms API response time (p95) under 5 concurrent uploads.
-   **Constraints**: Must use realistic data volumes.

#### Acceptance Criteria
- [x] A k6 (or JMeter) script is developed to simulate GL data file uploads (using B3).
- [x] Test data (large CSV/Excel files, e.g., 100k rows) is generated or acquired.
- [x] Scalability tests are executed with at least 5 concurrent users uploading large GL data files.
- [x] System performance metrics (CPU, Memory, Network I/O, API response times) are monitored during the tests.
- [x] The upload of a 100,000-row GL data file completes within 5 minutes (from client perspective).
- [x] The parsing and initial storage of a 100,000-row GL data file completes within 10 minutes (backend processing).
- [x] A report summarizing test results, identified bottlenecks, and compliance with NFR3 is generated.
- [x] Any performance bottlenecks identified are documented.

#### Effort Estimate: **3 SP**
**Complexity**: Medium

**Breakdown**:
- DevOps: 50% (1.5 days)
- QA: 50% (1.5 days)

**Reasoning**:
```
Day 1:
- Generate realistic large test data (e.g., 100k-1M rows CSV/Excel). (4 hours)
- Adapt k6 script from A9 to simulate GL data upload (B3 endpoint). (4 hours)

Day 2:
- Configure k6 to run tests with 5 concurrent users uploading large files. (4 hours)
- Execute initial test runs and monitor system metrics via CloudWatch. (4 hours)

Day 3:
- Analyze test results, identify potential bottlenecks (e.g., DB writes, parsing speed). (4 hours)
- Generate a summary report and document findings. (4 hours)
```

**Risk Factors**:
- ⚠️ **Realistic Test Data**: Generating truly representative large datasets can be challenging. Mitigation: Collaborate with domain experts, use synthetic data generators.
- ⚠️ **Bottleneck Identification**: Pinpointing the exact cause of performance issues can be time-consuming. Mitigation: Leverage detailed monitoring (A4) and profiling tools.

**Dependencies**: A9 (Performance Testing Framework), B3 (GL Data Upload API), B4 (GL Data Parsing Service), B5 (GL Data Storage Service)

**Build Order**: #10

---

## 💻 Frontend Stories

### Story F1: User Login & Registration UI
#### Description:
As an auditor, I want to be able to register for an account and log in securely, so that I can access the Audit Sampling Tool.
**Details**:
-   **Components**: `LoginForm`, `RegistrationForm`, `AuthLayout`.
-   **UX Flow**:
    1.  User lands on `/login` or `/register`.
    2.  Fills out form (email, password, confirm password, first name, last name for registration).
    3.  Submits form.
    4.  On success: Redirects to `/dashboard`.
    5.  On error: Displays error message (e.g., "Invalid credentials", "Email already exists").
-   **State Management**: Local component state for form inputs, global state (e.g., React Context or Redux) for authentication status and user token.
-   **API Calls**: `POST /api/v1/auth/register`, `POST /api/v1/auth/login` (from B1).
-   **Responsive Design**: Mobile-first, adapts to tablet and desktop.
-   **Edge Cases**: Empty fields, invalid email format, password mismatch, API errors (401, 409).

#### Acceptance Criteria
- [x] A login form is displayed at `/login` with fields for email and password.
- [x] A registration form is displayed at `/register` with fields for first name, last name, email, password, and confirm password.
- [x] Users can successfully register for a new account by submitting valid details.
- [x] Users can successfully log in with valid credentials.
- [x] Upon successful login/registration, a JWT token is securely stored (e.g., in `localStorage` or `sessionStorage`).
- [x] Upon successful login/registration, the user is redirected to the `/dashboard` route.
- [x] Error messages are displayed clearly to the user for:
    -   Invalid login credentials.
    -   Email already registered during registration.
    -   Password mismatch during registration.
    -   Empty required fields.
    -   Invalid email format.
- [x] Password fields mask input.
- [x] The UI is responsive and usable on mobile, tablet, and desktop devices.
- [x] Unit tests are written for form validation and component rendering.

#### Effort Estimate: **3 SP**
**Complexity**: Medium

**Breakdown**:
- Frontend: 100% (3 days)

**Reasoning**:
```
Day 1:
- Set up project structure for authentication module. (2 hours)
- Create `AuthLayout` component. (2 hours)
- Develop `LoginForm` component with basic input fields and submit button. (4 hours)

Day 2:
- Implement form validation for `LoginForm` (empty fields, email format). (3 hours)
- Integrate with B1 login API, handle success (token storage, redirect) and error states. (5 hours)

Day 3:
- Develop `RegistrationForm` component with additional fields. (4 hours)
- Implement form validation for `RegistrationForm` (password mismatch, email uniqueness). (2 hours)
- Integrate with B1 registration API, handle success and error states. (2 hours)
```

**Risk Factors**:
- ⚠️ **Security of Token Storage**: Incorrect JWT storage can lead to XSS/CSRF vulnerabilities. Mitigation: Use `localStorage` for convenience, but acknowledge risks and consider `httpOnly` cookies for higher security (requires backend changes).
- ⚠️ **Complex Form Validation**: Extensive client-side validation can be time-consuming. Mitigation: Use a form library (e.g., React Hook Form, Formik) to streamline validation.

**Dependencies**: B1 (User Authentication & Authorization API)

**Build Order**: #11

---

### Story F2: Role-Based Dashboard & Navigation
#### Description:
As a user, I want to see a dashboard and navigation tailored to my role (Auditor/Manager), so that I can easily access the features relevant to my responsibilities.
**Details**:
-   **Components**: `DashboardLayout`, `SidebarNavigation`, `RoleBasedRouteGuard`.
-   **UX Flow**:
    1.  After login, user is redirected to `/dashboard`.
    2.  Based on the user's role (obtained from JWT or user profile API), display specific navigation items and dashboard widgets.
    3.  Auditor sees "GL Data Upload", "Sampling", "Engagements".
    4.  Manager sees "Audit Trail", "User Management" (future), "Engagements".
    5.  Unauthorized access to a route redirects to `/dashboard` or `/unauthorized`.
-   **State Management**: Global state for user object (including roles).
-   **API Calls**: `GET /api/v1/users/me` (to retrieve user profile and roles, part of B1/B2).
-   **Responsive Design**: Collapsible sidebar on mobile, always visible on desktop.
-   **Edge Cases**: User has no role, multiple roles.

#### Acceptance Criteria
- [x] A main `DashboardLayout` component is created with a header and a sidebar navigation.
- [x] The sidebar navigation dynamically displays links based on the logged-in user's role.
- [x] Auditors see navigation links for "GL Data Upload", "Sampling", and "Engagements".
- [x] Managers see navigation links for "Audit Trail" and "Engagements" (and potentially "User Management" if implemented).
- [x] A `RoleBasedRouteGuard` (or similar mechanism) is implemented to protect routes based on user roles.
- [x] Users attempting to access unauthorized routes are redirected to a default page (e.g., `/dashboard`) or an "Unauthorized" page.
- [x] The user's role information is retrieved from the backend (e.g., via a `GET /api/v1/users/me` endpoint or decoded from JWT).
- [x] The navigation sidebar is responsive, collapsing on smaller screens and expanding on larger screens.
- [x] Unit tests are written for role-based rendering logic and route guards.

#### Effort Estimate: **3 SP**
**Complexity**: Medium

**Breakdown**:
- Frontend: 100% (3 days)

**Reasoning**:
```
Day 1:
- Design `DashboardLayout` with header and placeholder sidebar. (3 hours)
- Implement basic routing for dashboard and protected routes. (3 hours)
- Fetch user profile/roles from API (B1/B2) and store in global state. (2 hours)

Day 2:
- Develop `SidebarNavigation` component. (4 hours)
- Implement conditional rendering logic for navigation items based on user role. (4 hours)

Day 3:
- Implement `RoleBasedRouteGuard` to protect routes. (4 hours)
- Test different user roles and unauthorized access scenarios. (4 hours)
```

**Risk Factors**:
- ⚠️ **Inconsistent Role Data**: Mismatch between frontend and backend understanding of roles. Mitigation: Clear API contract for user roles, robust error handling.
- ⚠️ **Security Bypass**: Frontend role-based rendering is not a security measure; backend must enforce RBAC. Mitigation: Emphasize that this is a UX feature, not security.

**Dependencies**: F1 (User Login), B2 (Role-Based Access Control API)

**Build Order**: #12

---

### Story F3: GL Data Upload UI
#### Description:
As an auditor, I want to upload GL data files (CSV, Excel) through a user-friendly interface with a progress indicator, so that I can easily import my data for sampling.
**Details**:
-   **Components**: `FileUploadCard`, `ProgressBar`, `EngagementSelector`.
-   **UX Flow**:
    1.  User navigates to "GL Data Upload" page.
    2.  Selects an existing engagement or creates a new one (future story).
    3.  Drag-and-drop area or file input button for selecting CSV/Excel files.
    4.  Upon file selection, displays file name and size.
    5.  Upon upload initiation, displays a progress bar.
    6.  On success: Displays success message and redirects to F4 (Column Mapping).
    7.  On error: Displays error message (e.g., "File too large", "Invalid file type", "Upload failed").
-   **State Management**: Local component state for file selection, upload progress.
-   **API Calls**: `POST /api/v1/gl-data/upload` (from B3).
-   **Responsive Design**: Mobile-friendly drag-and-drop area.
-   **Edge Cases**: Large files, network interruptions, invalid file types.

#### Acceptance Criteria
- [x] A dedicated "GL Data Upload" page is accessible via navigation (F2).
- [x] A file input component (or drag-and-drop area) is present, allowing selection of `.csv`, `.xls`, and `.xlsx` files.
- [x] Users can select an existing engagement from a dropdown (or create a new one, if that feature is ready).
- [x] Upon file selection, the file name and size are displayed.
- [x] A visual progress indicator (e.g., progress bar) is displayed during the file upload process.
- [x] Upon successful upload, a success message is displayed, and the user is redirected to the Column Mapping UI (F4).
- [x] Clear error messages are displayed for:
    -   Unsupported file types.
    -   Files exceeding a predefined size limit (e.g., 500MB).
    -   Network errors during upload.
    -   Backend API errors.
- [x] The UI is responsive and provides a good experience on various screen sizes.
- [x] Unit tests are written for file selection and progress display.

#### Effort Estimate: **3 SP**
**Complexity**: Medium

**Breakdown**:
- Frontend: 100% (3 days)

**Reasoning**:
```
Day 1:
- Create "GL Data Upload" page component. (3 hours)
- Implement file input component with drag-and-drop functionality. (5 hours)

Day 2:
- Implement file type and size validation. (3 hours)
- Develop and integrate a progress bar component. (5 hours)

Day 3:
- Integrate with B3 upload API, handling `multipart/form-data` and progress events. (5 hours)
- Handle success (redirect to F4) and various error states. (3 hours)
```

**Risk Factors**:
- ⚠️ **Large File Uploads**: Handling large files efficiently and reliably, especially over unstable networks. Mitigation: Use chunked uploads (if backend supports, not in B3 yet), provide clear feedback.
- ⚠️ **Browser Compatibility**: File API and drag-and-drop might have subtle differences across browsers. Mitigation: Test across major browsers.

**Dependencies**: F2 (Navigation), B3 (GL Data Upload API Endpoint)

**Build Order**: #13

---

### Story F4: GL Data Column Mapping UI
#### Description:
As an auditor, I want to map uploaded file columns to predefined GL data fields (e.g., Transaction ID, Amount) using an interactive interface, so that the tool correctly interprets my data.
**Details**:
-   **Components**: `ColumnMappingTable`, `DropdownSelector`.
-   **UX Flow**:
    1.  User is redirected from F3 to the Column Mapping page.
    2.  Displays a table with two columns: "Uploaded File Column" (read-only, showing headers from the uploaded file) and "Map to GL Field" (dropdown).
    3.  "Map to GL Field" dropdown contains predefined GL fields (e.g., Transaction ID, Amount, Date, Description, Account ID, Source System, etc.).
    4.  User selects the appropriate GL field for each uploaded column.
    5.  A "Save Mapping" button.
    6.  On success: Displays success message and redirects to F5 (Validation Display).
    7.  On error: Displays error message (e.g., "Mapping failed", "Required fields not mapped").
-   **State Management**: Local component state for selected mappings.
-   **API Calls**: `GET /api/v1/gl-data/{dataset_id}/headers` (to get uploaded headers), `GET /api/v1/gl-data/fields` (to get predefined GL fields), `POST /api/v1/gl-data/{dataset_id}/map-columns` (from B6).
-   **Responsive Design**: Scrollable table on smaller screens.
-   **Edge Cases**: No headers in file, duplicate uploaded headers, required fields not mapped.

#### Acceptance Criteria
- [x] The Column Mapping page is accessible after a successful GL data upload (from F3).
- [x] A table is displayed showing the headers extracted from the uploaded file.
- [x] For each uploaded column, a dropdown is provided to select a corresponding predefined GL data field (e.g., "Transaction ID", "Amount", "Transaction Date", "Description", "Account ID", "Source System", "Other Field 1", "Other Field 2").
- [x] Predefined GL data fields are fetched from the backend.
- [x] Users can select a mapping for each column.
- [x] A "Save Mapping" button is available to persist the selections.
- [x] Upon successful mapping, a success message is displayed, and the user is redirected to the GL Data Validation Display UI (F5).
- [x] Error messages are displayed for:
    -   Required GL fields (e.g., Transaction ID, Amount) not being mapped.
    -   Mapping conflicts (e.g., two uploaded columns mapped to the same GL field).
    -   Backend API errors during mapping save.
- [x] The UI is responsive, allowing horizontal scrolling for many columns on smaller screens.
- [x] Unit tests are written for mapping logic and component rendering.

#### Effort Estimate: **4 SP**
**Complexity**: Medium

**Breakdown**:
- Frontend: 100% (4 days)

**Reasoning**:
```
Day 1:
- Create "Column Mapping" page component. (3 hours)
- Fetch uploaded file headers (from B6) and predefined GL fields (from B6). (5 hours)

Day 2:
- Develop `ColumnMappingTable` component to display headers and dropdowns. (6 hours)
- Implement state management for selected mappings. (2 hours)

Day 3:
- Implement validation logic for mappings (e.g., required fields, no duplicates). (5 hours)
- Develop "Save Mapping" button and integrate with B6 API. (3 hours)

Day 4:
- Handle success (redirect to F5) and various error states. (4 hours)
- Ensure responsive design for the table. (4 hours)
```

**Risk Factors**:
- ⚠️ **Complex Mapping Logic**: Handling various mapping scenarios (e.g., optional fields, default values) can be complex. Mitigation: Start with core required fields, add advanced features later.
- ⚠️ **User Experience for Many Columns**: A file with many columns can make the UI cluttered. Mitigation: Implement search/filter for columns, sticky headers.

**Dependencies**: F3 (GL Data Upload UI), B6 (GL Data Column Mapping API)

**Build Order**: #14

---

### Story F5: GL Data Validation Display & User Correction UI
#### Description:
As an auditor, I want to review flagged data issues (missing fields, non-numeric values, duplicates) and have options to correct them or proceed with the valid subset, so that I can ensure the integrity of my GL data before sampling.
**Details**:
-   **Components**: `ValidationResultsTable`, `ErrorFilter`, `CorrectionModal`, `ActionButtons`.
-   **UX Flow**:
    1.  User is redirected from F4 to the Validation Display page.
    2.  Displays a table of GL transactions, highlighting rows/cells with validation errors.
    3.  Filters/tabs to view specific error types (e.g., "Missing Fields", "Non-numeric Amounts", "Duplicates").
    4.  Option to "Correct" an individual error (e.g., inline edit or modal).
    5.  Option to "Discard Invalid Rows" or "Proceed with Valid Data".
    6.  On "Proceed": Redirects to F6 (GL Data Summary).
    7.  On "Discard": Confirms action, then redirects to F6.
-   **State Management**: Local component state for filters, selected rows, edited values.
-   **API Calls**: `GET /api/v1/gl-data/{dataset_id}/validation-errors` (from B7/B8), `PATCH /api/v1/gl-data/{dataset_id}/transactions/{transaction_id}` (for corrections), `POST /api/v1/gl-data/{dataset_id}/finalize-validation` (to discard/proceed).
-   **Responsive Design**: Scrollable data table.
-   **Edge Cases**: No errors, all errors, user corrects some but not all.

#### Acceptance Criteria
- [x] The GL Data Validation Display page is accessible after successful column mapping (from F4).
- [x] A data table displays GL transactions, visually highlighting rows or cells containing validation errors.
- [x] Filters or tabs are available to view transactions by specific error types (e.g., "Missing Required Fields", "Non-numeric Amounts", "Duplicate Transaction IDs").
- [x] Users can view detailed error messages for each flagged issue.
- [x] Users have the option to correct individual data points (e.g., via an inline editor or a modal dialog).
- [x] Corrected data is sent to the backend for update (via `PATCH` API call).
- [x] Users have the option to "Discard Invalid Rows" (removing all transactions with errors).
- [x] Users have the option to "Proceed with Valid Data" (keeping only valid transactions, or all if no errors).
- [x] Upon "Proceed" or "Discard", the user is redirected to the GL Data Summary Display UI (F6).
- [x] Error messages are displayed for failed corrections or backend validation issues.
- [x] The UI is responsive, providing a usable experience for large tables.
- [x] Unit tests are written for error display, filtering, and correction logic.

#### Effort Estimate: **5 SP**
**Complexity**: High

**Breakdown**:
- Frontend: 100% (5 days)

**Reasoning**:
```
Day 1:
- Create "Validation Display" page component. (3 hours)
- Fetch validation errors and GL data from B7/B8. (5 hours)

Day 2:
- Develop `ValidationResultsTable` to display data and highlight errors. (6 hours)
- Implement filtering/tabbing for different error types. (2 hours)

Day 3:
- Implement inline editing or modal for correcting individual data points. (6 hours)
- Integrate correction updates with backend PATCH API. (2 hours)

Day 4:
- Develop "Discard Invalid Rows" and "Proceed with Valid Data" buttons. (5 hours)
- Integrate these actions with backend API (e.g., `finalize-validation`). (3 hours)

Day 5:
- Handle success (redirect to F6) and various error states. (4 hours)
- Ensure responsive design and performance for large datasets. (4 hours)
```

**Risk Factors**:
- ⚠️ **Complex Data Grid**: Building a feature-rich data grid with inline editing and error highlighting is complex. Mitigation: Use a robust data grid library (e.g., AG Grid, TanStack Table) to accelerate development.
- ⚠️ **Performance with Many Errors**: Displaying and managing corrections for thousands of errors can be slow. Mitigation: Implement pagination, virtualized lists, and optimize rendering.

**Dependencies**: F4 (Column Mapping UI), B7 (Missing/Non-numeric Validation API), B8 (Duplicate Transaction IDs Validation API)

**Build Order**: #15

---

### Story F6: GL Data Summary Display UI
#### Description:
As an auditor, I want to view a summary of the uploaded GL data (e.g., total entries, total value, date range), so that I can quickly confirm the dataset I'm working with.
**Details**:
-   **Components**: `SummaryCard`, `DatasetInfo`.
-   **UX Flow**:
    1.  User is redirected from F5 to the GL Data Summary page.
    2.  Displays key statistics: total number of transactions, total monetary value, earliest transaction date, latest transaction date, currency.
    3.  A "Continue to Sampling" button.
    4.  On "Continue": Redirects to F7 (Sample Size Calculation).
-   **State Management**: Global state for current dataset ID.
-   **API Calls**: `GET /api/v1/gl-data/{dataset_id}/summary` (from B9).
-   **Responsive Design**: Simple layout, adapts well.
-   **Edge Cases**: Empty dataset (after discarding all invalid rows).

#### Acceptance Criteria
- [x] The GL Data Summary Display page is accessible after data validation (from F5).
- [x] Key summary statistics are displayed:
    -   Total number of transactions.
    -   Total monetary value of all transactions.
    -   Earliest transaction date.
    -   Latest transaction date.
    -   Currency of the transactions.
- [x] Data is fetched from the backend using the GL Data Summary API (B9).
- [x] A "Continue to Sampling" button is present, which redirects the user to the Sample Size Calculation Parameters UI (F7).
- [x] The UI handles an empty dataset gracefully (e.g., displays "No data available").
- [x] The UI is clean, concise, and responsive.
- [x] Unit tests are written for component rendering and data display.

#### Effort Estimate: **2 SP**
**Complexity**: Low

**Breakdown**:
- Frontend: 100% (2 days)

**Reasoning**:
```
Day 1:
- Create "GL Data Summary" page component. (3 hours)
- Fetch summary data from B9 API. (5 hours)

Day 2:
- Display summary statistics in a clear, readable format. (4 hours)
- Implement "Continue to Sampling" button and redirect to F7. (4 hours)
```

**Risk Factors**:
- ⚠️ **Data Consistency**: Ensuring the summary reflects the *validated* data, not the raw uploaded data. Mitigation: Backend (B9) must operate on the validated dataset.

**Dependencies**: F5 (GL Data Validation Display), B9 (GL Data Summary API)

**Build Order**: #16

---

### Story F7: Sample Size Calculation Parameters UI
#### Description:
As an auditor, I want to input and select configurable parameters (Confidence Level, Tolerable Misstatement, Expected Misstatement) for sample size calculation, so that I can determine a statistically valid sample size.
**Details**:
-   **Components**: `SampleParametersForm`, `Dropdown`, `NumberInput`.
-   **UX Flow**:
    1.  User is redirected from F6 to the Sample Size Calculation page.
    2.  Displays input fields for:
        -   Confidence Level (dropdown: 90%, 95%, 99%).
        -   Tolerable Misstatement (percentage input, e.g., 1-10%).
        -   Expected Misstatement (percentage input, e.g., 0-5%).
    3.  A "Calculate Sample Size" button.
    4.  On success: Displays calculated sample size (F8).
    5.  On error: Displays validation errors or API errors.
-   **State Management**: Local component state for form inputs.
-   **API Calls**: `POST /api/v1/sampling/{dataset_id}/calculate-sample-size` (from B11).
-   **Responsive Design**: Form layout adapts to screen size.
-   **Edge Cases**: Invalid input values (e.g., negative percentages), Expected Misstatement > Tolerable Misstatement.

#### Acceptance Criteria
- [x] The Sample Size Calculation Parameters page is accessible after viewing the GL Data Summary (from F6).
- [x] Input fields are provided for:
    -   Confidence Level (dropdown with options like 90%, 95%, 99%).
    -   Tolerable Misstatement (percentage input, e.g., 1.00% to 10.00%).
    -   Expected Misstatement (percentage input, e.g., 0.00% to 5.00%).
- [x] Input fields have appropriate client-side validation (e.g., numeric, range checks).
- [x] A "Calculate Sample Size" button is present.
- [x] Upon clicking "Calculate Sample Size", the parameters are sent to the backend (B11).
- [x] Upon successful calculation, the user is redirected to the Calculated Sample Size Display UI (F8).
- [x] Clear error messages are displayed for:
    -   Invalid input values (e.g., non-numeric, out of range).
    -   Logical errors (e.g., Expected Misstatement > Tolerable Misstatement).
    -   Backend API errors.
- [x] The UI is responsive and user-friendly.
- [x] Unit tests are written for form validation and component rendering.

#### Effort Estimate: **3 SP**
**Complexity**: Medium

**Breakdown**:
- Frontend: 100% (3 days)

**Reasoning**:
```
Day 1:
- Create "Sample Size Calculation" page component. (3 hours)
- Develop input fields for Confidence Level (dropdown), Tolerable Misstatement, Expected Misstatement (number inputs). (5 hours)

Day 2:
- Implement client-side validation for input parameters (e.g., ranges, numeric). (4 hours)
- Develop "Calculate Sample Size" button. (2 hours)
- Integrate with B11 API to send parameters. (2 hours)

Day 3:
- Handle success (redirect to F8) and various error states from API and client-side validation. (4 hours)
- Ensure responsive form layout. (4 hours)
```

**Risk Factors**:
- ⚠️ **Complex Validation Rules**: Statistical parameters often have interdependencies (e.g., expected cannot exceed tolerable). Mitigation: Implement clear validation messages and disable/enable fields as appropriate.

**Dependencies**: F6 (GL Data Summary), B11 (Sample Size Calculation API)

**Build Order**: #17

---

### Story F8: Calculated Sample Size Display & Override UI
#### Description:
As an auditor, I want to see the calculated sample size and have the option to override it with a manual input, providing a justification, so that I can adjust the sample size if audit judgment requires it.
**Details**:
-   **Components**: `CalculatedSampleSizeDisplay`, `OverrideForm`, `JustificationInput`.
-   **UX Flow**:
    1.  User is redirected from F7 to this page.
    2.  Displays the calculated sample size prominently.
    3.  An "Override Sample Size" button/toggle.
    4.  If overridden: Input field for manual sample size, text area for justification (required).
    5.  A "Confirm Sample Size" button.
    6.  On success: Redirects to F9 (Sampling Method Selection).
    7.  On error: Displays validation errors or API errors.
-   **State Management**: Local component state for override status, manual input, justification.
-   **API Calls**: `POST /api/v1/sampling/{dataset_id}/override-sample-size` (from B12).
-   **Responsive Design**: Adapts form layout.
-   **Edge Cases**: Invalid manual input (e.g., non-numeric, negative, too large), missing justification.

#### Acceptance Criteria
- [x] The Calculated Sample Size Display page is accessible after sample size calculation (from F7).
- [x] The calculated sample size (from B11) is displayed prominently.
- [x] An option (e.g., checkbox, toggle, or button) is provided to "Override Sample Size".
- [x] When "Override Sample Size" is activated:
    -   An input field appears for the user to enter a manual sample size.
    -   A text area appears for the user to provide a mandatory justification for the override.
- [x] Client-side validation is implemented for the manual sample size (e.g., numeric, positive, not exceeding population size) and justification (e.g., not empty).
- [x] A "Confirm Sample Size" button is present.
- [x] Upon clicking "Confirm Sample Size", the chosen sample size (calculated or overridden) and justification (if applicable) are sent to the backend (B12).
- [x] Upon successful confirmation, the user is redirected to the Sampling Method Selection UI (F9).
- [x] Clear error messages are displayed for:
    -   Invalid manual sample size input.
    -   Missing justification when override is active.
    -   Backend API errors.
- [x] Unit tests are written for override logic and form validation.

#### Effort Estimate: **3 SP**
**Complexity**: Medium

**Breakdown**:
- Frontend: 100% (3 days)

**Reasoning**:
```
Day 1:
- Create "Calculated Sample Size" page component. (3 hours)
- Display the calculated sample size. (2 hours)
- Implement "Override Sample Size" toggle/button. (3 hours)

Day 2:
- Conditionally render manual input and justification text area based on override state. (5 hours)
- Implement client-side validation for manual input and justification. (3 hours)

Day 3:
- Develop "Confirm Sample Size" button. (2 hours)
- Integrate with B12 API to send chosen sample size and justification. (4 hours)
- Handle success (redirect to F9) and error states. (2 hours)
```

**Risk Factors**:
- ⚠️ **Justification Enforcement**: Ensuring the justification is meaningful and not just boilerplate. Mitigation: This is a policy/process issue, but UI can enforce minimum length.
- ⚠️ **State Management Complexity**: Managing conditional rendering and form state for override. Mitigation: Use a form library and clear state variables.

**Dependencies**: F7 (Sample Size Calculation), B12 (Sample Size Override API)

**Build Order**: #18

---

### Story F9: Sampling Method Selection UI
#### Description:
As an auditor, I want to select from various sampling methods (Random, Systematic, MUS) and configure their specific parameters, so that I can apply the appropriate methodology for my audit.
**Details**:
-   **Components**: `SamplingMethodSelector`, `MethodParametersForm` (conditional).
-   **UX Flow**:
    1.  User is redirected from F8 to the Sampling Method Selection page.
    2.  Radio buttons or tabs for "Simple Random Sampling", "Systematic Sampling", "Monetary Unit Sampling (MUS)".
    3.  When a method is selected, display relevant configuration parameters:
        -   **Random**: No additional parameters.
        -   **Systematic**: "Starting Point" (optional, random if not provided).
        -   **MUS**: "Tainting Factor" (optional, default 1.0).
    4.  A "Generate Sample" button.
    5.  On success: Displays selected samples (F11).
    6.  On error: Displays validation errors or API errors.
-   **State Management**: Local component state for selected method and parameters.
-   **API Calls**: `POST /api/v1/sampling/{dataset_id}/random`, `POST /api/v1/sampling/{dataset_id}/systematic`, `POST /api/v1/sampling/{dataset_id}/mus` (from B14, B15, B16).
-   **Responsive Design**: Adapts form layout.
-   **Edge Cases**: Invalid parameters for a method.

#### Acceptance Criteria
- [x] The Sampling Method Selection page is accessible after confirming sample size (from F8).
- [x] Options are presented to select a sampling method: "Simple Random Sampling", "Systematic Sampling", "Monetary Unit Sampling (MUS)".
- [x] When "Simple Random Sampling" is selected, no additional parameters are required.
- [x] When "Systematic Sampling" is selected, an optional "Starting Point" input field is displayed.
- [x] When "Monetary Unit Sampling (MUS)" is selected, an optional "Tainting Factor" input field is displayed (defaulting to 1.0).
- [x] Client-side validation is implemented for method-specific parameters (e.g., numeric, positive).
- [x] A "Generate Sample" button is present.
- [x] Upon clicking "Generate Sample", the selected method and its parameters are sent to the appropriate backend API (B14, B15, or B16).
- [x] Upon successful sample generation, the user is redirected to the Selected Samples Display UI (F11).
- [x] Clear error messages are displayed for:
    -   Invalid method-specific parameters.
    -   Backend API errors during sample generation.
- [x] The UI is responsive and easy to navigate.
- [x] Unit tests are written for method selection and parameter display.

#### Effort Estimate: **4 SP**
**Complexity**: Medium

**Breakdown**:
- Frontend: 100% (4 days)

**Reasoning**:
```
Day 1:
- Create "Sampling Method Selection" page component. (3 hours)
- Implement radio buttons/tabs for method selection. (5 hours)

Day 2:
- Conditionally render parameter input forms based on selected method. (6 hours)
- Develop input fields for Systematic (Starting Point) and MUS (Tainting Factor). (2 hours)

Day 3:
- Implement client-side validation for method-specific parameters. (4 hours)
- Develop "Generate Sample" button. (2 hours)
- Integrate with B14, B15, B16 APIs based on selected method. (2 hours)

Day 4:
- Handle success (redirect to F11) and various error states. (4 hours)
- Ensure responsive layout. (4 hours)
```

**Risk Factors**:
- ⚠️ **Conditional UI Complexity**: Managing the display of different forms based on selection can become complex. Mitigation: Use a clear component structure and state management.
- ⚠️ **Parameter Validation**: Ensuring all method-specific parameters are correctly validated. Mitigation: Centralize validation logic.

**Dependencies**: F8 (Calculated Sample Size), B14 (Random Sampling API), B15 (Systematic Sampling API), B16 (MUS Sampling API)

**Build Order**: #19

---

### Story F10: GL Data Filtering UI
#### Description:
As an auditor, I want to filter the GL data based on criteria like date range, account type, or amount range before sample selection, so that I can focus my sampling on a specific subset of transactions.
**Details**:
-   **Components**: `FilterPanel`, `DateRangePicker`, `TextInput`, `NumberRangeInput`.
-   **UX Flow**:
    1.  User accesses the filtering options (e.g., on the Sampling Method Selection page or a dedicated "Filter Data" step).
    2.  Input fields for:
        -   Date Range (start date, end date).
        -   Account Type (text input, potentially multi-select dropdown).
        -   Amount Range (min amount, max amount).
    3.  "Apply Filters" and "Clear Filters" buttons.
    4.  The filtered data count is updated dynamically (if possible) or after applying filters.
-   **State Management**: Local component state for filter criteria.
-   **API Calls**: `POST /api/v1/gl-data/{dataset_id}/filter` (from B13). This API call should be made *before* sample generation.
-   **Responsive Design**: Filter panel should be collapsible on mobile.
-   **Edge Cases**: Invalid date ranges, non-numeric amount ranges, no matching data.

#### Acceptance Criteria
- [x] A filter panel or section is available (e.g., on the Sampling Method Selection page or a preceding step).
- [x] Filter options are provided for:
    -   Date Range (start and end date pickers).
    -   Account Type (text input or multi-select dropdown).
    -   Amount Range (min and max numeric inputs).
- [x] Client-side validation is implemented for filter inputs (e.g., valid dates, numeric amounts, start date <= end date).
- [x] "Apply Filters" and "Clear Filters" buttons are present.
- [x] Upon clicking "Apply Filters", the selected criteria are sent to the backend (B13) to filter the GL data *before* sample generation.
- [x] The UI provides feedback on the number of transactions remaining after applying filters.
- [x] Upon clicking "Clear Filters", all filter criteria are reset.
- [x] Clear error messages are displayed for invalid filter inputs.
- [x] The filter UI is responsive, potentially collapsing on smaller screens.
- [x] Unit tests are written for filter input validation and state management.

#### Effort Estimate: **4 SP**
**Complexity**: Medium

**Breakdown**:
- Frontend: 100% (4 days)

**Reasoning**:
```
Day 1:
- Create `FilterPanel` component. (3 hours)
- Implement Date Range Picker component. (5 hours)

Day 2:
- Implement Account Type text input/dropdown. (4 hours)
- Implement Amount Range min/max number inputs. (4 hours)

Day 3:
- Implement client-side validation for all filter inputs. (4 hours)
- Develop "Apply Filters" and "Clear Filters" buttons. (2 hours)
- Integrate with B13 API to send filter criteria. (2 hours)

Day 4:
- Display feedback on filtered data count. (3 hours)
- Ensure responsive design for the filter panel. (3 hours)
- Test various filter combinations and edge cases. (2 hours)
```

**Risk Factors**:
- ⚠️ **Performance with Complex Filters**: Applying multiple filters on large datasets can be slow if not optimized on the backend. Mitigation: Ensure B13 is efficient, consider debouncing filter applications.
- ⚠️ **Filter State Management**: Maintaining filter state across different views or steps. Mitigation: Use global state management for filters if they persist.

**Dependencies**: F9 (Sampling Method Selection, as filtering happens before sampling), B13 (GL Data Filtering API)

**Build Order**: #20

---

### Story F11: Selected Samples Display UI
#### Description:
As an auditor, I want to view the selected samples in a clear tabular format, including all original GL data fields, so that I can review the results of the sampling process.
**Details**:
-   **Components**: `SampleDataTable`, `Pagination`, `ColumnVisibilityToggle`.
-   **UX Flow**:
    1.  User is redirected from F9 (or F14) to the Selected Samples Display page.
    2.  Displays a data table with all selected GL transactions.
    3.  Includes all original GL data fields (Transaction ID, Amount, Date, Description, etc.).
    4.  Pagination for large sample sets.
    5.  Option to sort by columns.
    6.  A "Export Samples" button (F12).
-   **State Management**: Local component state for pagination, sorting.
-   **API Calls**: `GET /api/v1/sampling/{dataset_id}/samples` (from B17).
-   **Responsive Design**: Scrollable table, potentially hiding less critical columns on mobile.
-   **Edge Cases**: Empty sample set, very large sample set.

#### Acceptance Criteria
- [x] The Selected Samples Display page is accessible after sample generation (from F9 or F14).
- [x] A data table displays all transactions selected as part of the sample.
- [x] The table includes all original GL data fields (e.g., Transaction ID, Amount, Transaction Date, Description, Account ID, Source System, etc.).
- [x] Pagination is implemented for efficient browsing of large sample sets.
- [x] Users can sort the table by any column.
- [x] A "Export Samples" button is present, which triggers the export functionality (F12).
- [x] The UI handles an empty sample set gracefully (e.g., "No samples selected").
- [x] The UI is responsive, allowing horizontal scrolling for many columns and potentially hiding/showing columns based on screen size.
- [x] Unit tests are written for table rendering, pagination, and sorting logic.

#### Effort Estimate: **3 SP**
**Complexity**: Medium

**Breakdown**:
- Frontend: 100% (3 days)

**Reasoning**:
```
Day 1:
- Create "Selected Samples Display" page component. (3 hours)
- Fetch selected samples from B17 API. (5 hours)

Day 2:
- Develop `SampleDataTable` component to display all GL fields. (6 hours)
- Implement basic pagination for the table. (2 hours)

Day 3:
- Implement column sorting functionality. (4 hours)
- Add "Export Samples" button (linking to F12). (2 hours)
- Ensure responsive design for the table. (2 hours)
```

**Risk Factors**:
- ⚠️ **Performance with Many Columns/Rows**: Displaying a large table with many columns can impact performance. Mitigation: Use a virtualized table component, optimize data fetching.
- ⚠️ **Data Integrity**: Ensuring the displayed sample data is exactly what was selected and stored. Mitigation: Backend (B17) must be robust.

**Dependencies**: F9 (Sampling Method Selection), F14 (Risk-Stratified Sampling), B17 (Selected Samples Persistence & Retrieval API)

**Build Order**: #21

---

### Story F12: Sample Export Trigger UI
#### Description:
As an auditor, I want to trigger the export of selected samples to CSV or Excel format, so that I can use the sample list in my audit workpapers.
**Details**:
-   **Components**: `ExportButton`, `ExportFormatSelector` (dropdown).
-   **UX Flow**:
    1.  User clicks "Export Samples" button (from F11).
    2.  A small modal or dropdown appears, allowing selection of "CSV" or "Excel (XLSX)".
    3.  User clicks "Download".
    4.  The browser initiates a file download.
    5.  Displays loading indicator during export generation.
    6.  On error: Displays error message.
-   **State Management**: Local component state for selected export format.
-   **API Calls**: `GET /api/v1/sampling/{dataset_id}/samples/export?format={csv|xlsx}` (from B18).
-   **Responsive Design**: Simple button/modal.
-   **Edge Cases**: Empty sample set, large export file generation time, network issues during download.

#### Acceptance Criteria
- [x] An "Export Samples" button is available on the Selected Samples Display UI (F11).
- [x] Upon clicking "Export Samples", a modal or dropdown appears, allowing the user to choose between "CSV" and "Excel (XLSX)" formats.
- [x] A "Download" button is present within the export selection.
- [x] Upon clicking "Download", a request is sent to the backend (B18) with the selected format.
- [x] The browser automatically initiates the download of the generated file (CSV or XLSX).
- [x] A loading indicator is displayed while the export file is being generated by the backend.
- [x] Clear error messages are displayed if the export fails (e.g., backend error, no samples to export).
- [x] The UI is simple and intuitive for triggering exports.
- [x] Unit tests are written for export format selection and button click handling.

#### Effort Estimate: **2 SP**
**Complexity**: Low

**Breakdown**:
- Frontend: 100% (2 days)

**Reasoning**:
```
Day 1:
- Implement "Export Samples" button (from F11). (2 hours)
- Create a modal/dropdown for selecting export format (CSV, XLSX). (4 hours)
- Implement "Download" button within the modal. (2 hours)

Day 2:
- Integrate with B18 API to trigger file download. (4 hours)
- Handle loading states and error messages. (2 hours)
- Test file download across different browsers. (2 hours)
```

**Risk Factors**:
- ⚠️ **Large File Downloads**: Very large exports might take a long time to generate or download, potentially timing out. Mitigation: Backend (B18) should handle large file generation efficiently, potentially using async jobs for extremely large files (future).
- ⚠️ **Browser Download Behavior**: Different browsers handle file downloads slightly differently. Mitigation: Test thoroughly.

**Dependencies**: F11 (Selected Samples Display UI), B18 (Sample Export API)

**Build Order**: #22

---

### Story F13: Audit Trail Viewing UI
#### Description:
As an audit manager, I want to view a chronological log of all significant user actions and system decisions for an engagement, so that I can review and understand the sampling process and decisions made.
**Details**:
-   **Components**: `AuditLogTable`, `FilterPanel` (date, user, action type), `Pagination`.
-   **UX Flow**:
    1.  Manager navigates to "Audit Trail" page (via F2).
    2.  Displays a table of audit log entries, ordered chronologically (newest first).
    3.  Each entry shows: Timestamp, User, Action Type, Description, and a "Details" button/modal for JSONB data.
    4.  Filters for Date Range, User, and Action Type.
    5.  Pagination for large log sets.
-   **State Management**: Local component state for filters, pagination.
-   **API Calls**: `GET /api/v1/audit-trail/{engagement_id}` (from B19).
-   **Responsive Design**: Scrollable table, filter panel collapsible.
-   **Edge Cases**: No audit logs for an engagement, very large number of logs.

#### Acceptance Criteria
- [x] The "Audit Trail" page is accessible via navigation for users with the "Manager" role (F2).
- [x] A data table displays audit log entries for a selected engagement, ordered chronologically (newest first).
- [x] Each table row displays: Timestamp, User (name/email), Action Type, and a concise Description.
- [x] A mechanism (e.g., expandable row, modal) is provided to view the full `details` (JSONB) of an audit log entry.
- [x] Filters are available for:
    -   Date Range (start and end date pickers).
    -   User (dropdown or text input).
    -   Action Type (dropdown with predefined types like 'GL_UPLOAD', 'SAMPLE_CALC', 'SAMPLE_OVERRIDE').
- [x] Pagination is implemented for efficient browsing of large audit log sets.
- [x] Data is fetched from the backend using the Audit Trail Retrieval API (B19).
- [x] The UI handles an empty audit log gracefully.
- [x] The UI is responsive, allowing horizontal scrolling for the table and collapsible filters.
- [x] Unit tests are written for table rendering, filtering, and pagination logic.

#### Effort Estimate: **3 SP**
**Complexity**: Medium

**Breakdown**:
- Frontend: 100% (3 days)

**Reasoning**:
```
Day 1:
- Create "Audit Trail" page component. (3 hours)
- Fetch audit logs from B19 API for a given engagement. (5 hours)

Day 2:
- Develop `AuditLogTable` component to display log entries. (6 hours)
- Implement basic pagination and sorting by timestamp. (2 hours)

Day 3:
- Implement filter panel for Date Range, User, and Action Type. (4 hours)
- Add functionality to view `details` JSONB (e.g., modal). (2 hours)
- Ensure responsive design. (2 hours)
```

**Risk Factors**:
- ⚠️ **Performance with Many Logs**: Displaying and filtering a very large audit trail can be slow. Mitigation: Backend (B19) must be optimized for filtering and pagination.
- ⚠️ **JSONB Display**: Presenting complex JSONB data in a user-friendly way. Mitigation: Use a JSON viewer component or format it clearly.

**Dependencies**: F2 (Role-Based Dashboard), B19 (Audit Trail Retrieval API)

**Build Order**: #23

---

### Story F14: Risk-Stratified Sampling Configuration UI
#### Description:
As an auditor, I want to configure a percentage of my sample to be directed towards high-risk transactions identified by the ML model, so that I can focus audit effort on areas of higher potential misstatement.
**Details**:
-   **Components**: `RiskStratifiedConfigForm`, `SliderInput`, `NumberInput`.
-   **UX Flow**:
    1.  User accesses this configuration (e.g., as an option within F9, or a separate step before sample generation).
    2.  Input field/slider for "Percentage of Sample from High-Risk Transactions" (e.g., 0-100%).
    3.  A "Apply Risk Stratification" button.
    4.  This configuration is then used when generating the sample (F9).
-   **State Management**: Local component state for the percentage.
-   **API Calls**: This configuration is passed as a parameter to the sampling APIs (B14, B15, B16, specifically B21).
-   **Responsive Design**: Simple form layout.
-   **Edge Cases**: Invalid percentage (non-numeric, out of range).

#### Acceptance Criteria
- [x] A configuration option for "Risk-Stratified Sampling" is available (e.g., as part of F9 or a preceding step).
- [x] An input field or slider allows the user to specify the "Percentage of Sample from High-Risk Transactions" (e.g., from 0% to 100%).
- [x] Client-side validation is implemented for the percentage input (numeric, between 0 and 100).
- [x] This percentage is passed as a parameter to the backend sampling APIs (B21) when "Generate Sample" is clicked.
- [x] The UI provides clear feedback on how this setting will influence the sample.
- [x] Clear error messages are displayed for invalid percentage input.
- [x] The UI is responsive and intuitive.
- [x] Unit tests are written for input validation and state management.

#### Effort Estimate: **3 SP**
**Complexity**: Medium

**Breakdown**:
- Frontend: 100% (3 days)

**Reasoning**:
```
Day 1:
- Integrate risk-stratified option into the sampling workflow (e.g., F9). (4 hours)
- Develop input field/slider for "Percentage of Sample from High-Risk Transactions". (4 hours)

Day 2:
- Implement client-side validation for the percentage input. (4 hours)
- Ensure the percentage is stored in component state. (2 hours)
- Update the "Generate Sample" button logic to include this parameter in API calls to B21. (2 hours)

Day 3:
- Test integration with sampling APIs and ensure the parameter is passed correctly. (4 hours)
- Refine UI/UX for clarity. (4 hours)
```

**Risk Factors**:
- ⚠️ **Integration with Existing Sampling Flow**: Seamlessly adding this option to the existing F9 flow without making it overly complex. Mitigation: Design for modularity, use conditional rendering.
- ⚠️ **User Understanding**: Ensuring auditors understand the implications of this setting. Mitigation: Provide clear labels and tooltips.

**Dependencies**: F9 (Sampling Method Selection UI), B21 (Risk-Stratified Sampling Logic API), M5 (ML Explainability, for context)

**Build Order**: #24

---

### Story F15: ML Explainability Display UI
#### Description:
As an auditor, I want to see an explainability summary for each risk-scored transaction (e.g., "round-number amount, posted 2 AM"), so that I can understand and assess the model's risk prioritization.
**Details**:
-   **Components**: `ExplainabilityTooltip`, `RiskScoreBadge`.
-   **UX Flow**:
    1.  On the Selected Samples Display UI (F11), for transactions that were risk-scored.
    2.  A visual indicator (e.g., a small icon, or the risk score itself) next to each transaction.
    3.  Hovering over or clicking this indicator/score reveals a tooltip or modal with the explainability summary.
    4.  The summary is concise, human-readable text (e.g., "Flagged: round-number amount, posted 2 AM").
-   **State Management**: Local component state for tooltip visibility.
-   **API Calls**: The explainability data should be available as part of the transaction data retrieved from B17 (which integrates with B20/M5). No separate API call from frontend for this.
-   **Responsive Design**: Tooltip/modal adapts to screen size.
-   **Edge Cases**: Transaction not risk-scored, no explanation available.

#### Acceptance Criteria
- [x] On the Selected Samples Display UI (F11), for transactions that have a risk score, a visual indicator (e.g., a badge, icon, or the risk score itself) is displayed.
- [x] Hovering over or clicking this indicator/score reveals a tooltip or modal containing the ML explainability summary for that specific transaction.
- [x] The explainability summary is displayed as concise, human-readable text (e.g., "Flagged: round-number amount, posted 2 AM", "Reason: High amount, unusual time").
- [x] The explainability data is retrieved as part of the transaction details from the backend (B17, which integrates M5).
- [x] The UI gracefully handles cases where a transaction does not have a risk score or an explanation.
- [x] The tooltip/modal is responsive and does not obstruct other UI elements.
- [x] Unit tests are written for the display logic of the explainability summary.

#### Effort Estimate: **3 SP**
**Complexity**: Medium

**Breakdown**:
- Frontend: 100% (3 days)

**Reasoning**:
```
Day 1:
- Modify `SampleDataTable` (F11) to display a visual indicator for risk-scored transactions. (4 hours)
- Design `ExplainabilityTooltip` or modal component. (4 hours)

Day 2:
- Implement logic to show/hide the tooltip/modal on hover/click. (5 hours)
- Integrate explainability text (from B17 data) into the tooltip/modal. (3 hours)

Day 3:
- Ensure clear and readable formatting of the explanation text. (4 hours)
- Handle edge cases (no risk score, no explanation). (2 hours)
- Ensure responsive behavior and accessibility. (2 hours)
```

**Risk Factors**:
- ⚠️ **Clarity of Explanations**: Ensuring the explanations are truly helpful and not confusing to auditors. Mitigation: Collaborate with ML team (M5) and domain experts on wording.
- ⚠️ **Performance of Tooltips**: Many tooltips on a large table could impact performance. Mitigation: Optimize tooltip rendering, lazy load content if complex.

**Dependencies**: F11 (Selected Samples Display UI), M5 (Explainability Feature Generation), B17 (Selected Samples Persistence & Retrieval API, which will include explainability data)

**Build Order**: #25

---

## ⚙️ Backend Stories

### Story B1: User Authentication & Authorization API
#### Description:
As a backend engineer, I want to implement RESTful API endpoints for user registration, login, and JWT token generation/validation, so that users can securely authenticate with the system.
**Details**:
-   **Tech Stack**: Python (FastAPI), PostgreSQL (A2), `passlib` (for password hashing, e.g., bcrypt), `PyJWT` (for JWT handling).
-   **Endpoints**:
    -   `POST /api/v1/auth/register`:
        -   Request: `{ "email": "...", "password": "...", "first_name": "...", "last_name": "..." }`
        -   Response: `{ "message": "User registered successfully" }` (201 Created) or `{ "detail": "Email already registered" }` (409 Conflict).
    -   `POST /api/v1/auth/login`:
        -   Request: `{ "email": "...", "password": "..." }`
        -   Response: `{ "access_token": "...", "token_type": "bearer" }` (200 OK) or `{ "detail": "Invalid credentials" }` (401 Unauthorized).
    -   `GET /api/v1/auth/me` (protected):
        -   Request: `Authorization: Bearer <token>`
        -   Response: `{ "id": "...", "email": "...", "first_name": "...", "last_name": "...", "roles": ["Auditor"] }` (200 OK) or `{ "detail": "Unauthorized" }` (401 Unauthorized).
-   **Data Model**: Uses `users` table from A2.
-   **Business Rules**: Passwords hashed with bcrypt. JWTs expire after a configurable time (e.g., 1 hour).
-   **Error Handling**: Specific HTTP status codes (400, 401, 409) and clear error messages.

#### Acceptance Criteria
- [x] `POST /api/v1/auth/register` endpoint is implemented.
- [x] Registration endpoint hashes user passwords using bcrypt (or similar strong algorithm) before storing in the database.
- [x] Registration endpoint validates input (email format, password strength, required fields).
- [x] Registration endpoint returns 409 Conflict if email already exists.
- [x] `POST /api/v1/auth/login` endpoint is implemented.
- [x] Login endpoint validates user credentials against stored hashes.
- [x] Upon successful login, a JWT access token is generated with a configurable expiration time (e.g., 1 hour) and returned.
- [x] Login endpoint returns 401 Unauthorized for invalid credentials.
- [x] A mechanism for JWT token validation is implemented (e.g., FastAPI dependency).
- [x] `GET /api/v1/auth/me` endpoint is implemented and protected by JWT authentication.
- [x] `GET /api/v1/auth/me` returns the authenticated user's details (id, email, first_name, last_name, roles).
- [x] All endpoints handle common HTTP errors (e.g., 400 Bad Request for invalid input).
- [x] Unit and integration tests are written for all authentication endpoints.

#### Effort Estimate: **4 SP**
**Complexity**: Medium

**Breakdown**:
- Backend: 100% (4 days)

**Reasoning**:
```
Day 1:
- Set up FastAPI project structure and database connection (SQLAlchemy). (4 hours)
- Implement user model and basic CRUD operations for `users` table. (4 hours)

Day 2:
- Implement password hashing (bcrypt) and verification logic. (4 hours)
- Develop `POST /api/v1/auth/register` endpoint with input validation and error handling. (4 hours)

Day 3:
- Implement JWT token generation and encoding logic. (4 hours)
- Develop `POST /api/v1/auth/login` endpoint with credential verification and token return. (4 hours)

Day 4:
- Implement JWT token decoding and validation middleware/dependency. (4 hours)
- Develop `GET /api/v1/auth/me` endpoint, protected by JWT. (2 hours)
- Write unit and integration tests for all auth endpoints. (2 hours)
```

**Risk Factors**:
- ⚠️ **Security Vulnerabilities**: Incorrect implementation of password hashing, JWT handling, or input validation can lead to security flaws. Mitigation: Use well-vetted libraries, follow security best practices, conduct code reviews.
- ⚠️ **JWT Expiration/Refresh**: Initial implementation might not include refresh tokens, leading to frequent re-logins. Mitigation: Plan for refresh tokens in a future story if needed, or set a reasonable expiration.

**Dependencies**: A2 (Core Database & User Schema), A5 (API Gateway & TLS)

**Build Order**: #10

---

### Story B2: Role-Based Access Control (RBAC) API
#### Description:
As a backend engineer, I want to implement API logic to enforce role-based access control (Auditor, Manager/Reviewer) for different features and data, so that users only access authorized functionalities.
**Details**:
-   **Tech Stack**: Python (FastAPI), PostgreSQL (A2), FastAPI dependencies for RBAC.
-   **Endpoints**: Apply RBAC to existing and future endpoints.
    -   Example: `GET /api/v1/admin/users` (Manager only), `POST /api/v1/gl-data/upload` (Auditor only).
-   **Data Model**: Uses `roles` and `user_roles` tables from A2.
-   **Business Rules**:
    -   Users with 'Auditor' role can perform data upload, mapping, validation, sampling.
    -   Users with 'Manager' role can view audit trails, manage users (future).
    -   Some actions might be accessible to both.
-   **Error Handling**: Return 403 Forbidden for unauthorized access.

#### Acceptance Criteria
- [x] A FastAPI dependency or decorator is implemented to check user roles based on the authenticated user's JWT.
- [x] The RBAC mechanism can enforce access based on a single required role (e.g., `@requires_role("Manager")`).
- [x] The RBAC mechanism can enforce access based on multiple possible roles (e.g., `@requires_any_role(["Auditor", "Manager"])`).
- [x] Attempting to access a protected endpoint without the required role returns a 403 Forbidden response.
- [x] At least one endpoint is protected for 'Auditor' role (e.g., `POST /api/v1/gl-data/upload` - future story).
- [x] At least one endpoint is protected for 'Manager' role (e.g., `GET /api/v1/audit-trail` - future story).
- [x] The `GET /api/v1/auth/me` endpoint (from B1) correctly returns the roles associated with the authenticated user.
- [x] Unit and integration tests are written for the RBAC middleware/dependencies.

#### Effort Estimate: **3 SP**
**Complexity**: Medium

**Breakdown**:
- Backend: 100% (3 days)

**Reasoning**:
```
Day 1:
- Design RBAC strategy using FastAPI dependencies. (4 hours)
- Implement a dependency to extract user roles from the JWT payload (from B1). (4 hours)

Day 2:
- Develop a decorator/dependency `@requires_role` to check for a single required role. (5 hours)
- Develop a decorator/dependency `@requires_any_role` to check for multiple possible roles. (3 hours)

Day 3:
- Apply RBAC to `GET /api/v1/auth/me` to ensure roles are returned. (2 hours)
- Write unit and integration tests for RBAC enforcement. (4 hours)
- Document RBAC usage for future endpoint development. (2 hours)
```

**Risk Factors**:
- ⚠️ **Granularity of Control**: Initial RBAC might be too coarse-grained. Mitigation: Design for future expansion to more granular permissions if needed.
- ⚠️ **Performance Overhead**: RBAC checks on every request could add overhead. Mitigation: Optimize role retrieval (e.g., cache roles in JWT).

**Dependencies**: B1 (User Authentication & Authorization API), A2 (Core Database & User Schema)

**Build Order**: #11

---

### Story B3: GL Data Upload API Endpoint
#### Description:
As a backend engineer, I want to create an API endpoint to receive uploaded CSV/Excel files and store them temporarily in object storage, so that the files are ready for parsing.
**Details**:
-   **Tech Stack**: Python (FastAPI), AWS S3 (A1), `boto3` (AWS SDK for Python).
-   **Endpoints**:
    -   `POST /api/v1/gl-data/upload`:
        -   Request: `multipart/form-data` with `file` (CSV/Excel) and `engagement_id` (UUID).
        -   Response: `{ "dataset_id": "...", "filename": "...", "status": "uploaded" }` (202 Accepted) or `{ "detail": "..." }` (400 Bad Request, 413 Payload Too Large).
-   **Data Model**: Stores `original_filename` in `gl_datasets` table (A6).
-   **Business Rules**:
    -   Accepts `.csv`, `.xls`, `.xlsx` file extensions.
    -   File size limit (e.g., 500MB).
    -   Stores files in a dedicated S3 bucket (A1) with a unique key (e.g., `engagement_id/dataset_id/original_filename`).
-   **Error Handling**: File type validation, size limit, S3 upload errors.

#### Acceptance Criteria
- [x] `POST /api/v1/gl-data/upload` endpoint is implemented, accepting `multipart/form-data`.
- [x] Endpoint validates that the uploaded file has a `.csv`, `.xls`, or `.xlsx` extension.
- [x] Endpoint enforces a maximum file size limit (e.g., 500MB).
- [x] The uploaded file is securely stored in the designated AWS S3 bucket (from A1).
- [x] A new entry is created in the `gl_datasets` table (from A6) with `original_filename`, `upload_date`, `status='uploaded'`, and `uploaded_by_user_id` (from authenticated user).
- [x] The endpoint returns a 202 Accepted response with the `dataset_id` and `filename` upon successful upload.
- [x] Error responses are returned for:
    -   Invalid file type (400 Bad Request).
    -   File exceeding size limit (413 Payload Too Large).
    -   Missing `engagement_id` or `file`.
    -   S3 upload failures.
- [x] The endpoint is protected by RBAC, requiring the 'Auditor' role (from B2).
- [x] Unit and integration tests are written for the upload endpoint.

#### Effort Estimate: **3 SP**
**Complexity**: Medium

**Breakdown**:
- Backend: 100% (3 days)

**Reasoning**:
```
Day 1:
- Define `POST /api/v1/gl-data/upload` endpoint in FastAPI. (3 hours)
- Implement file type and size validation. (3 hours)
- Integrate with `boto3` to upload file to S3. (2 hours)

Day 2:
- Create a new `gl_datasets` entry in the database (A6) after successful S3 upload. (4 hours)
- Return appropriate success (202) or error responses. (2 hours)
- Apply RBAC protection (Auditor role) using B2. (2 hours)

Day 3:
- Write unit and integration tests for file upload, validation, and S3 interaction. (6 hours)
- Document API endpoint. (2 hours)
```

**Risk Factors**:
- ⚠️ **Large File Handling**: FastAPI's default handling of large `multipart/form-data` can consume significant memory. Mitigation: Stream file directly to S3 if possible, or increase server memory.
- ⚠️ **S3 Permissions**: Incorrect IAM permissions for S3 bucket access. Mitigation: Ensure least privilege IAM policy for the backend service.

**Dependencies**: A1 (S3 bucket), A5 (API Gateway), A6 (GL Data Storage Schema), B2 (RBAC API)

**Build Order**: #12

---

### Story B4: GL Data Parsing Service
#### Description:
As a backend engineer, I want to develop a service to parse uploaded CSV and Excel (XLSX, XLS) files into a structured format, so that the data can be processed and validated.
**Details**:
-   **Tech Stack**: Python (FastAPI, Pandas, `openpyxl`, `xlrd`), Celery/RQ (for asynchronous task processing), Redis (for Celery/RQ broker), AWS S3 (A1).
-   **Service Logic**:
    -   Triggered asynchronously after a successful upload (B3).
    -   Retrieves file from S3 using `dataset_id`.
    -   Uses Pandas to read CSV/Excel files.
    -   Extracts headers and a sample of rows for column mapping (B6).
    -   Parses all rows into a standardized intermediate format.
    -   Updates `gl_datasets.status` (e.g., 'parsing', 'parsed').
-   **Business Rules**:
    -   Handles various CSV delimiters (comma, semicolon, tab).
    -   Detects headers automatically or assumes first row.
    -   Handles common Excel sheet formats (first sheet, named sheet).
-   **Error Handling**: File corruption, parsing errors, invalid file format.

#### Acceptance Criteria
- [x] An asynchronous task (e.g., Celery/RQ task) is created for GL data parsing.
- [x] The parsing task is triggered automatically after a successful file upload (B3).
- [x] The task retrieves the uploaded file from S3 using the `dataset_id`.
- [x] The service can successfully parse `.csv` files, handling common delimiters (comma, semicolon, tab).
- [x] The service can successfully parse `.xls` and `.xlsx` Excel files.
- [x] The service extracts column headers from the file.
- [x] The service parses all rows into a standardized intermediate format (e.g., list of dictionaries).
- [x] The `gl_datasets.status` field is updated to 'parsing' at the start and 'parsed' (or 'error') upon completion.
- [x] Parsing errors (e.g., malformed rows, unsupported format) are logged, and the `gl_datasets.status` is set to 'error'.
- [x] Unit and integration tests are written for the parsing logic with various file types and edge cases.

#### Effort Estimate: **4 SP**
**Complexity**: High

**Breakdown**:
- Backend: 100% (4 days)

**Reasoning**:
```
Day 1:
- Research and set up asynchronous task queue (e.g., Celery with Redis broker). (4 hours)
- Implement basic task to retrieve file from S3. (4 hours)

Day 2:
- Develop CSV parsing logic using Pandas, handling delimiters. (5 hours)
- Develop Excel parsing logic using Pandas (`openpyxl`, `xlrd`). (3 hours)

Day 3:
- Implement logic to extract headers and standardize row format. (5 hours)
- Update `gl_datasets.status` during parsing lifecycle. (3 hours)

Day 4:
- Implement robust error handling for parsing failures. (4 hours)
- Write unit and integration tests with various test files (valid, invalid, different formats). (4 hours)
```

**Risk Factors**:
- ⚠️ **File Format Variations**: CSV/Excel files can have many subtle variations (encodings, malformed rows, merged cells). Mitigation: Use robust libraries (Pandas), implement comprehensive error handling, provide user feedback.
- ⚠️ **Asynchronous Task Management**: Setting up and monitoring Celery/RQ can be complex. Mitigation: Start with a simple setup, ensure proper logging and error reporting.

**Dependencies**: B3 (GL Data Upload API), A1 (S3), A6 (GL Data Storage Schema for status updates)

**Build Order**: #13

---

### Story B5: GL Data Storage Service
#### Description:
As a backend engineer, I want to implement a service to persist the parsed GL data into the database, linking it to the user and engagement, so that it can be efficiently retrieved for subsequent steps.
**Details**:
-   **Tech Stack**: Python (FastAPI, SQLAlchemy), PostgreSQL (A6).
-   **Service Logic**:
    -   Triggered after successful parsing (B4).
    -   Receives standardized GL data from the parsing service.
    -   Performs bulk insertion into the `gl_transactions` table (A6).
    -   Links transactions to the `gl_datasets` and `engagements` tables.
    -   Updates `gl_datasets.status` to 'stored'.
-   **Business Rules**:
    -   Efficient bulk insertion for large datasets.
    -   Ensures data integrity (foreign keys, constraints).
-   **Error Handling**: Database connection issues, constraint violations.

#### Acceptance Criteria
- [x] A service function is implemented to persist standardized GL data into the database.
- [x] The service is triggered after successful parsing by B4.
- [x] Data is inserted into the `gl_transactions` table (A6) using efficient bulk insertion methods (e.g., `COPY` command or SQLAlchemy bulk insert).
- [x] Each transaction is correctly linked to its `dataset_id` and implicitly to `engagement_id`.
- [x] The `gl_datasets.status` field is updated to 'stored' upon successful persistence.
- [x] Database constraints (e.g., unique `(transaction_id, dataset_id)`) are respected, and errors are handled gracefully.
- [x] Error handling is implemented for database connection issues or insertion failures.
- [x] Unit and integration tests are written for the data storage logic, including bulk inserts and error cases.

#### Effort Estimate: **3 SP**
**Complexity**: Medium

**Breakdown**:
- Backend: 100% (3 days)

**Reasoning**:
```
Day 1:
- Design data flow from parsing service to storage service. (3 hours)
- Implement SQLAlchemy ORM models for `gl_transactions` table (A6). (5 hours)

Day 2:
- Develop bulk insertion logic using SQLAlchemy's `bulk_insert_mappings` or similar. (6 hours)
- Implement logic to update `gl_datasets.status` to 'stored'. (2 hours)

Day 3:
- Implement error handling for database operations. (4 hours)
- Write unit and integration tests for data persistence, including large datasets. (4 hours)
```

**Risk Factors**:
- ⚠️ **Performance of Bulk Inserts**: Very large datasets can still be slow to insert. Mitigation: Optimize database configuration, use native `COPY` command if SQLAlchemy is too slow.
- ⚠️ **Data Integrity**: Ensuring all foreign key relationships and constraints are correctly handled during bulk inserts. Mitigation: Thorough testing with various data scenarios.

**Dependencies**: B4 (GL Data Parsing Service), A6 (GL Data Storage Schema)

**Build Order**: #14

---

### Story B6: GL Data Column Mapping API
#### Description:
As a backend engineer, I want to implement API endpoints to allow users to map uploaded file columns to predefined GL data fields, so that the system correctly understands the data structure.
**Details**:
-   **Tech Stack**: Python (FastAPI), PostgreSQL (A6), SQLAlchemy.
-   **Endpoints**:
    -   `GET /api/v1/gl-data/{dataset_id}/headers`:
        -   Response: `{ "uploaded_headers": ["Column A", "Column B", ...], "sample_data": [["val1", "val2"], ...] }` (200 OK).
    -   `GET /api/v1/gl-data/fields`:
        -   Response: `{ "predefined_fields": ["transaction_id", "amount", "transaction_date", ...] }` (200 OK).
    -   `POST /api/v1/gl-data/{dataset_id}/map-columns`:
        -   Request: `{ "mapping": { "Uploaded Column A": "transaction_id", "Uploaded Column B": "amount", ... } }`
        -   Response: `{ "message": "Mapping saved successfully" }` (200 OK) or `{ "detail": "..." }` (400 Bad Request).
-   **Data Model**: Stores mapping in `gl_datasets` metadata (e.g., JSONB field) or a new `column_mappings` table. For simplicity, let's assume a JSONB field in `gl_datasets`.
-   **Business Rules**:
    -   Requires `dataset_id` to be in 'parsed' or 'stored' status.
    -   Validates that all required GL fields are mapped.
    -   Validates against duplicate mappings.
-   **Error Handling**: Invalid `dataset_id`, missing required mappings, duplicate mappings.

#### Acceptance Criteria
- [x] `GET /api/v1/gl-data/{dataset_id}/headers` endpoint is implemented to retrieve column headers and a sample of rows from the parsed GL data (from B4/B5).
- [x] `GET /api/v1/gl-data/fields` endpoint is implemented to return a list of predefined GL data fields (e.g., `transaction_id`, `amount`, `transaction_date`, `description`, `account_id`, `source_system`, `other_mapped_field_1`, `other_mapped_field_2`).
- [x] `POST /api/v1/gl-data/{dataset_id}/map-columns` endpoint is implemented to receive and store the user's column mappings.
- [x] The mapping is stored in the `gl_datasets` table (e.g., in a JSONB field).
- [x] The mapping endpoint validates that all mandatory GL fields (e.g., `transaction_id`, `amount`, `transaction_date`) are included in the provided mapping.
- [x] The mapping endpoint validates against duplicate mappings (i.e., one GL field mapped to multiple uploaded columns).
- [x] The `gl_datasets.status` is updated to 'mapped' upon successful mapping.
- [x] All endpoints are protected by RBAC, requiring the 'Auditor' role (from B2).
- [x] Unit and integration tests are written for all mapping endpoints.

#### Effort Estimate: **3 SP**
**Complexity**: Medium

**Breakdown**:
- Backend: 100% (3 days)

**Reasoning**:
```
Day 1:
- Define `GET /api/v1/gl-data/{dataset_id}/headers` endpoint. (4 hours)
- Implement logic to retrieve headers and sample data from S3/DB. (4 hours)

Day 2:
- Define `GET /api/v1/gl-data/fields` endpoint. (2 hours)
- Define `POST /api/v1/gl-data/{dataset_id}/map-columns` endpoint. (4 hours)
- Implement logic to store mapping in `gl_datasets` JSONB field. (2 hours)

Day 3:
- Implement validation for required fields and duplicate mappings. (4 hours)
- Update `gl_datasets.status` to 'mapped'. (2 hours)
- Apply RBAC (Auditor role) to all endpoints. (1 hour)
- Write unit and integration tests. (1 hour)
```

**Risk Factors**:
- ⚠️ **Schema Flexibility**: If predefined GL fields change frequently, this mapping process needs to be robust. Mitigation: Keep predefined fields stable, or build a more dynamic system (future).
- ⚠️ **Performance of Header Extraction**: For very large files, extracting headers and sample data might be slow. Mitigation: B4 should pre-extract and store headers/sample.

**Dependencies**: B5 (GL Data Storage Service), A6 (GL Data Storage Schema), B2 (RBAC API)

**Build Order**: #15

---

### Story B7: GL Data Validation API - Missing/Non-numeric Fields
#### Description:
As a backend engineer, I want to implement API logic to identify and flag missing required fields and non-numeric values in amount fields, so that data quality issues are detected early.
**Details**:
-   **Tech Stack**: Python (FastAPI, Pandas), PostgreSQL (A6).
-   **Endpoints**:
    -   `GET /api/v1/gl-data/{dataset_id}/validation-errors`:
        -   Response: `{ "errors": [ { "row_index": 1, "column": "amount", "error_type": "non_numeric", "message": "..." }, ... ], "valid_transactions_count": 123 }` (200 OK).
-   **Service Logic**:
    -   Reads GL data from `gl_transactions` table (A6).
    -   Applies validation rules based on the stored column mapping (B6).
    -   Identifies missing values for required fields (e.g., `transaction_id`, `amount`, `transaction_date`).
    -   Identifies non-numeric values in `amount` fields.
    -   Returns a list of errors and a count of valid transactions.
-   **Business Rules**:
    -   Required fields are defined in the system (e.g., `transaction_id`, `amount`, `transaction_date`).
    -   `amount` field must be numeric and positive.
-   **Error Handling**: Invalid `dataset_id`, data retrieval errors.

#### Acceptance Criteria
- [x] `GET /api/v1/gl-data/{dataset_id}/validation-errors` endpoint is implemented.
- [x] The endpoint retrieves GL data from the `gl_transactions` table (A6) for the given `dataset_id`.
- [x] The endpoint identifies and flags transactions with missing values in required GL fields (e.g., `transaction_id`, `amount`, `transaction_date`).
- [x] The endpoint identifies and flags transactions where the `amount` field is non-numeric or negative.
- [x] The endpoint returns a structured list of validation errors, including `row_index`, `column`, `error_type`, and `message`.
- [x] The endpoint also returns the count of transactions that are currently considered valid (i.e., without any flagged errors).
- [x] The endpoint is protected by RBAC, requiring the 'Auditor' role (from B2).
- [x] Unit and integration tests are written for the validation logic with various data scenarios.

#### Effort Estimate: **4 SP**
**Complexity**: High

**Breakdown**:
- Backend: 100% (4 days)

**Reasoning**:
```
Day 1:
- Define `GET /api/v1/gl-data/{dataset_id}/validation-errors` endpoint. (3 hours)
- Implement logic to retrieve GL data and stored column mapping. (5 hours)

Day 2:
- Develop validation logic for missing required fields based on mapping. (6 hours)
- Develop validation logic for non-numeric/negative amount fields. (2 hours)

Day 3:
- Structure error responses to include row index, column, type, message. (5 hours)
- Calculate and return the count of valid transactions. (3 hours)

Day 4:
- Apply RBAC (Auditor role). (1 hour)
- Write comprehensive unit and integration tests for various error types and valid data. (7 hours)
```

**Risk Factors**:
- ⚠️ **Performance on Large Datasets**: Iterating through millions of rows for validation can be slow. Mitigation: Optimize database queries, use Pandas for vectorized operations, consider batch processing.
- ⚠️ **Complex Validation Rules**: As more validation rules are added, the logic can become complex. Mitigation: Modularize validation functions, use a clear rule engine.

**Dependencies**: B5 (GL Data Storage Service), B6 (GL Data Column Mapping API), A6 (GL Data Storage Schema), B2 (RBAC API)

**Build Order**: #16

---

### Story B8: GL Data Validation API - Duplicate Transaction IDs
#### Description:
As a backend engineer, I want to implement API logic to identify and flag duplicate transaction IDs within an uploaded dataset, so that data integrity is maintained.
**Details**:
-   **Tech Stack**: Python (FastAPI), PostgreSQL (A6).
-   **Endpoints**:
    -   `GET /api/v1/gl-data/{dataset_id}/validation-errors` (extends B7):
        -   Response: `{ "errors": [ { "row_index": 1, "column": "transaction_id", "error_type": "duplicate", "message": "..." }, ... ], "valid_transactions_count": 123 }` (200 OK).
-   **Service Logic**:
    -   Reads GL data from `gl_transactions` table (A6).
    -   Identifies duplicate `transaction_id` values within the same `dataset_id`.
    -   Adds these to the list of errors returned by the validation endpoint.
-   **Business Rules**: `transaction_id` must be unique within a `dataset_id`.
-   **Error Handling**: Invalid `dataset_id`, data retrieval errors.

#### Acceptance Criteria
- [x] The `GET /api/v1/gl-data/{dataset_id}/validation-errors` endpoint (from B7) is extended to include duplicate transaction ID detection.
- [x] The endpoint identifies and flags transactions where the `transaction_id` is duplicated within the same `dataset_id`.
- [x] Duplicate transaction ID errors are returned in the structured error list, including `row_index`, `column` (transaction_id), `error_type` ('duplicate'), and `message`.
- [x] The `valid_transactions_count` correctly excludes transactions flagged as duplicates.
- [x] The endpoint is protected by RBAC, requiring the 'Auditor' role (from B2).
- [x] Unit and integration tests are written for duplicate transaction ID detection with various data scenarios.

#### Effort Estimate: **3 SP**
**Complexity**: Medium

**Breakdown**:
- Backend: 100% (3 days)

**Reasoning**:
```
Day 1:
- Integrate duplicate detection logic into the existing B7 validation endpoint. (4 hours)
- Implement efficient database query to find duplicate `transaction_id` within a `dataset_id`. (4 hours)

Day 2:
- Format duplicate errors to match the existing error structure. (4 hours)
- Ensure `valid_transactions_count` correctly accounts for duplicates. (4 hours)

Day 3:
- Apply RBAC (Auditor role). (1 hour)
- Write unit and integration tests specifically for duplicate transaction IDs. (7 hours)
```

**Risk Factors**:
- ⚠️ **Performance on Large Datasets**: Querying for duplicates on very large tables can be resource-intensive. Mitigation: Use database indexing, optimize SQL queries (e.g., `GROUP BY` with `HAVING COUNT > 1`).
- ⚠️ **False Positives/Negatives**: Ensuring the duplicate detection logic is accurate. Mitigation: Thorough testing with edge cases (e.g., case sensitivity, leading/trailing spaces).

**Dependencies**: B7 (GL Data Validation API - Missing/Non-numeric Fields), A6 (GL Data Storage Schema), B2 (RBAC API)

**Build Order**: #17

---

### Story B9: GL Data Summary API
#### Description:
As a backend engineer, I want to create an API endpoint to provide a summary of the uploaded GL data (e.g., total entries, total population value, date range), so that users can quickly review their dataset.
**Details**:
-   **Tech Stack**: Python (FastAPI), PostgreSQL (A6), SQLAlchemy.
-   **Endpoints**:
    -   `GET /api/v1/gl-data/{dataset_id}/summary`:
        -   Response: `{ "total_transactions": 10000, "total_value": 1234567.89, "earliest_date": "2022-01-01", "latest_date": "2022-12-31", "currency": "USD" }` (200 OK).
-   **Service Logic**:
    -   Queries the `gl_transactions` table (A6) for the given `dataset_id`.
    -   Calculates total count, sum of `amount`, min/max `transaction_date`.
    -   Retrieves `currency` from `gl_datasets` table (A6).
    -   **Important**: This summary should reflect the *validated* data, not necessarily the raw uploaded data if invalid rows were discarded.
-   **Business Rules**: Only valid transactions (after B7/B8) should be included in the summary.
-   **Error Handling**: Invalid `dataset_id`, no data found.

#### Acceptance Criteria
- [x] `GET /api/v1/gl-data/{dataset_id}/summary` endpoint is implemented.
- [x] The endpoint retrieves summary statistics from the `gl_transactions` table (A6) for the given `dataset_id`.
- [x] The summary includes:
    -   `total_transactions`: Count of all *valid* transactions.
    -   `total_value`: Sum of `amount` for all *valid* transactions.
    -   `earliest_date`: Minimum `transaction_date` among *valid* transactions.
    -   `latest_date`: Maximum `transaction_date` among *valid* transactions.
    -   `currency`: Retrieved from the `gl_datasets` table.
- [x] The summary calculations only include transactions that have passed validation (i.e., not flagged with errors from B7/B8).
- [x] The endpoint returns a 200 OK response with the summary data.
- [x] Error responses are returned for:
    -   Invalid `dataset_id`.
    -   No valid transactions found for the `dataset_id`.
- [x] The endpoint is protected by RBAC, requiring the 'Auditor' role (from B2).
- [x] Unit and integration tests are written for the summary endpoint.

#### Effort Estimate: **2 SP**
**Complexity**: Low

**Breakdown**:
- Backend: 100% (2 days)

**Reasoning**:
```
Day 1:
- Define `GET /api/v1/gl-data/{dataset_id}/summary` endpoint. (3 hours)
- Implement database queries to calculate total count, sum, min/max date for valid transactions. (5 hours)

Day 2:
- Retrieve currency from `gl_datasets` table. (2 hours)
- Format and return the summary data. (2 hours)
- Apply RBAC (Auditor role). (1 hour)
- Write unit and integration tests. (3 hours)
```

**Risk Factors**:
- ⚠️ **Performance on Large Datasets**: Aggregation queries on very large tables can be slow. Mitigation: Ensure appropriate indexing (A6), consider materialized views for frequently accessed summaries (future).
- ⚠️ **Consistency with Validation**: Ensuring the summary reflects the *current* state of validated data. Mitigation: The logic must explicitly filter for valid transactions.

**Dependencies**: B5 (GL Data Storage Service), B7/B8 (GL Data Validation APIs, to determine 'valid' transactions), A6 (GL Data Storage Schema), B2 (RBAC API)

**Build Order**: #18

---

### Story B10: Audit Trail Logging API
#### Description:
As a backend engineer, I want to implement a robust API for logging all significant user actions and system decisions (e.g., uploads, parameter changes, overrides, sample generation) to the immutable audit trail, so that all activities are traceable (FR5).
**Details**:
-   **Tech Stack**: Python (FastAPI), PostgreSQL (A7), SQLAlchemy.
-   **Service Logic**:
    -   A dedicated internal service/function `log_audit_event` that other backend services call.
    -   Takes `user_id`, `engagement_id`, `action_type`, `description`, `details` (JSONB), `ip_address`.
    -   Inserts a new record into the `audit_logs` table (A7).
    -   Ensures immutability (no updates/deletes).
-   **Business Rules**:
    -   Log all user-initiated actions (upload, map, validate, calculate, override, filter, sample, export).
    -   Log all significant system decisions (e.g., automatic sample size calculation, ML risk scoring applied).
    -   `details` field should capture relevant parameters (e.g., old value, new value, parameters used).
-   **Error Handling**: Database insertion failures.

#### Acceptance Criteria
- [x] An internal service function `log_audit_event` is implemented to record audit trail entries.
- [x] `log_audit_event` accepts parameters: `user_id` (nullable), `engagement_id` (nullable), `action_type` (string), `description` (string), `details` (JSONB), `ip_address` (nullable).
- [x] `log_audit_event` inserts a new record into the `audit_logs` table (A7) with a timestamp.
- [x] The `audit_logs` table is configured to be immutable (no updates or deletes allowed via application logic).
- [x] The `user_id` is automatically extracted from the authenticated user's context when available.
- [x] The `ip_address` of the request is captured and stored.
- [x] Error handling is implemented for database insertion failures (e.g., log the error internally, but don't block the main operation).
- [x] Documentation is provided on how to use `log_audit_event` from other backend services.
- [x] Unit tests are written for the `log_audit_event` function.

#### Effort Estimate: **3 SP**
**Complexity**: Medium

**Breakdown**:
- Backend: 100% (3 days)

**Reasoning**:
```
Day 1:
- Design `log_audit_event` internal function signature. (3 hours)
- Implement SQLAlchemy ORM model for `audit_logs` table (A7). (5 hours)

Day 2:
- Implement logic to insert new records into `audit_logs`. (6 hours)
- Implement logic to capture `user_id` and `ip_address`. (2 hours)

Day 3:
- Implement error handling for database writes. (3 hours)
- Write unit tests for `log_audit_event`. (3 hours)
- Document integration points for other services. (2 hours)
```

**Risk Factors**:
- ⚠️ **Performance Impact**: Frequent logging could impact performance. Mitigation: Ensure database inserts are efficient, consider asynchronous logging for non-critical events (future).
- ⚠️ **Completeness of Logs**: Ensuring all critical actions are logged. Mitigation: Establish clear guidelines for what constitutes a "significant" action and integrate logging into all relevant stories.

**Dependencies**: A7 (Audit Trail Database Schema), B1 (User Authentication for `user_id`)

**Build Order**: #19

---

### Story B11: Sample Size Calculation API
#### Description:
As a backend engineer, I want to implement an API that calculates the statistically valid sample size based on user-configurable parameters (Confidence Level, Tolerable Misstatement, Expected Misstatement, Population Size), so that auditors get a recommended sample size.
**Details**:
-   **Tech Stack**: Python (FastAPI, `scipy.stats` or custom statistical functions), PostgreSQL (A6).
-   **Endpoints**:
    -   `POST /api/v1/sampling/{dataset_id}/calculate-sample-size`:
        -   Request: `{ "confidence_level": 0.95, "tolerable_misstatement_percent": 0.05, "expected_misstatement_percent": 0.01 }`
        -   Response: `{ "calculated_sample_size": 123, "population_size": 10000, "population_value": 1234567.89 }` (200 OK).
-   **Service Logic**:
    -   Retrieves `population_size` (total valid transactions) and `population_value` (total valid monetary value) from B9.
    -   Applies statistical formulas (e.g., based on attributes sampling or variables sampling, depending on context. For simplicity, let's assume attributes sampling for now, or a simplified formula for monetary value sampling if MUS is implied). Let's use a simplified formula for monetary unit sampling (MUS) for consistency with B16, which often starts with sample size calculation.
    -   Formula: `Sample Size = (Confidence Factor / Tolerable Misstatement Rate)^2 * (1 - Expected Misstatement Rate)` (simplified for illustration, actual MUS formulas are more complex). Or, for attributes: `n = (Z^2 * p * (1-p)) / E^2`. Given the parameters, it's likely a variation of MUS sample size calculation.
-   **Business Rules**:
    -   Confidence Level: 90%, 95%, 99%.
    -   Tolerable Misstatement: Percentage of population value.
    -   Expected Misstatement: Percentage of population value.
    -   Expected Misstatement must be less than Tolerable Misstatement.
-   **Error Handling**: Invalid input parameters, statistical calculation errors.

#### Acceptance Criteria
- [x] `POST /api/v1/sampling/{dataset_id}/calculate-sample-size` endpoint is implemented.
- [x] The endpoint accepts `confidence_level` (e.g., 0.90, 0.95, 0.99), `tolerable_misstatement_percent`, and `expected_misstatement_percent`.
- [x] The endpoint retrieves the `population_size` and `population_value` from the GL data summary (B9).
- [x] The endpoint implements a statistically valid formula to calculate the sample size based on the provided parameters and population data.
- [x] The endpoint validates input parameters (e.g., percentages are within valid range, expected < tolerable).
- [x] The endpoint returns the `calculated_sample_size`, `population_size`, and `population_value`.
- [x] Error responses are returned for:
    -   Invalid input parameters (400 Bad Request).
    -   Logical inconsistencies (e.g., expected misstatement >= tolerable misstatement).
    -   Calculation failures.
- [x] The endpoint is protected by RBAC, requiring the 'Auditor' role (from B2).
- [x] Unit tests are written for the sample size calculation logic with various parameter sets.

#### Effort Estimate: **4 SP**
**Complexity**: High

**Breakdown**:
- Backend: 100% (4 days)

**Reasoning**:
```
Day 1:
- Define `POST /api/v1/sampling/{dataset_id}/calculate-sample-size` endpoint. (3 hours)
- Research and select appropriate statistical formula for sample size calculation (e.g., for MUS or attributes sampling). (5 hours)

Day 2:
- Implement input validation for `confidence_level`, `tolerable_misstatement_percent`, `expected_misstatement_percent`. (4 hours)
- Retrieve `population_size` and `population_value` from B9. (4 hours)

Day 3:
- Implement the core sample size calculation logic. (6 hours)
- Handle edge cases in calculation (e.g., zero expected misstatement). (2 hours)

Day 4:
- Return calculated sample size and population details. (2 hours)
- Apply RBAC (Auditor role). (1 hour)
- Write comprehensive unit tests for the calculation logic. (5 hours)
```

**Risk Factors**:
- ⚠️ **Statistical Correctness**: Ensuring the formula used is statistically sound and appropriate for audit sampling. Mitigation: Consult with domain experts/auditors, double-check formulas.
- ⚠️ **Edge Cases**: Formulas can behave unexpectedly with extreme input values. Mitigation: Thorough unit testing with boundary conditions.

**Dependencies**: B9 (GL Data Summary API), B2 (RBAC API)

**Build Order**: #20

---

### Story B12: Sample Size Override API
#### Description:
As a backend engineer, I want to implement an API to allow users to override the calculated sample size, requiring and storing a justification, so that audit judgment can be applied while maintaining traceability.
**Details**:
-   **Tech Stack**: Python (FastAPI), PostgreSQL (A6, A7), SQLAlchemy.
-   **Endpoints**:
    -   `POST /api/v1/sampling/{dataset_id}/override-sample-size`:
        -   Request: `{ "manual_sample_size": 150, "justification": "Increased sample due to high inherent risk." }`
        -   Response: `{ "message": "Sample size overridden successfully" }` (200 OK).
-   **Service Logic**:
    -   Validates `manual_sample_size` (numeric, positive, not exceeding population size).
    -   Validates `justification` (non-empty).
    -   Stores the chosen sample size (calculated or overridden) and justification in the `gl_datasets` table (e.g., new fields `final_sample_size`, `sample_size_justification`).
    -   Logs this action to the audit trail (B10).
-   **Business Rules**: Justification is mandatory for overrides.
-   **Error Handling**: Invalid input, missing justification.

#### Acceptance Criteria
- [x] `POST /api/v1/sampling/{dataset_id}/override-sample-size` endpoint is implemented.
- [x] The endpoint accepts `manual_sample_size` and `justification`.
- [x] The endpoint validates that `manual_sample_size` is a positive integer and does not exceed the `population_size` (from B9).
- [x] The endpoint validates that `justification` is provided and is not empty.
- [x] The chosen sample size (either the calculated one from B11 or the `manual_sample_size`) is stored in the `gl_datasets` table (e.g., in a new `final_sample_size` field).
- [x] The `justification` for the override is stored in the `gl_datasets` table (e.g., in a new `sample_size_justification` field).
- [x] An audit log entry is created using B10 for the sample size override, including the old calculated size, new manual size, and justification in the `details` JSONB.
- [x] The endpoint returns a 200 OK response upon successful override.
- [x] Error responses are returned for invalid input or missing justification.
- [x] The endpoint is protected by RBAC, requiring the 'Auditor' role (from B2).
- [x] Unit and integration tests are written for the override logic and audit logging.

#### Effort Estimate: **2 SP**
**Complexity**: Low

**Breakdown**:
- Backend: 100% (2 days)

**Reasoning**:
```
Day 1:
- Define `POST /api/v1/sampling/{dataset_id}/override-sample-size` endpoint. (3 hours)
- Implement input validation for `manual_sample_size` and `justification`. (5 hours)

Day 2:
- Update `gl_datasets` table with `final_sample_size` and `sample_size_justification`. (4 hours)
- Integrate with B10 to log the override action. (2 hours)
- Apply RBAC (Auditor role) and write tests. (2 hours)
```

**Risk Factors**:
- ⚠️ **Data Consistency**: Ensuring the `final_sample_size` is always correctly set, whether calculated or overridden. Mitigation: Clear logic for setting this field.
- ⚠️ **Audit Trail Completeness**: Forgetting to log all relevant details of the override. Mitigation: Review audit log requirements carefully.

**Dependencies**: B11 (Sample Size Calculation API), B10 (Audit Trail Logging API), A6 (GL Data Storage Schema), B2 (RBAC API)

**Build Order**: #21

---

### Story B13: GL Data Filtering API
#### Description:
As a backend engineer, I want to implement API endpoints to filter the GL data based on user-specified criteria (e.g., date range, account type, amount range), so that samples can be drawn from specific subsets.
**Details**:
-   **Tech Stack**: Python (FastAPI), PostgreSQL (A6), SQLAlchemy.
-   **Endpoints**:
    -   `POST /api/v1/gl-data/{dataset_id}/filter`:
        -   Request: `{ "date_range": { "start_date": "2022-01-01", "end_date": "2022-12-31" }, "account_type": "Expense", "amount_range": { "min_amount": 1000, "max_amount": 5000 } }`
        -   Response: `{ "filtered_transaction_count": 5000, "filtered_value": 500000.00 }` (200 OK).
-   **Service Logic**:
    -   Receives filter criteria.
    -   Constructs dynamic SQL queries to filter `gl_transactions` for the given `dataset_id`.
    -   Stores the active filter criteria for the `dataset_id` (e.g., in `gl_datasets` JSONB field or a new `filters` table).
    -   Returns the count and total value of the filtered subset.
-   **Business Rules**: Filters apply to the *validated* GL data.
-   **Error Handling**: Invalid filter parameters, no data matching filters.

#### Acceptance Criteria
- [x] `POST /api/v1/gl-data/{dataset_id}/filter` endpoint is implemented.
- [x] The endpoint accepts filter criteria for `date_range` (start/end date), `account_type` (string), and `amount_range` (min/max numeric amount).
- [x] The endpoint constructs and executes dynamic SQL queries to filter the `gl_transactions` table (A6) based on the provided criteria.
- [x] The filtering is applied to the *validated* GL data (i.e., excluding transactions flagged with errors from B7/B8).
- [x] The active filter criteria are stored for the `dataset_id` (e.g., in a JSONB field in `gl_datasets`).
- [x] The endpoint returns the `filtered_transaction_count` and `filtered_value` of the subset.
- [x] Error responses are returned for:
    -   Invalid filter parameters (e.g., malformed dates, non-numeric amounts).
    -   `dataset_id` not found.
- [x] The endpoint is protected by RBAC, requiring the 'Auditor' role (from B2).
- [x] Unit and integration tests are written for the filtering logic with various filter combinations.

#### Effort Estimate: **3 SP**
**Complexity**: Medium

**Breakdown**:
- Backend: 100% (3 days)

**Reasoning**:
```
Day 1:
- Define `POST /api/v1/gl-data/{dataset_id}/filter` endpoint. (3 hours)
- Implement input validation for filter parameters. (5 hours)

Day 2:
- Develop logic to dynamically construct SQL `WHERE` clauses based on filter criteria. (6 hours)
- Implement logic to store active filters in `gl_datasets` (JSONB). (2 hours)

Day 3:
- Execute filtered query and return count/value. (3 hours)
- Apply RBAC (Auditor role) and write tests for various filter combinations. (5 hours)
```

**Risk Factors**:
- ⚠️ **SQL Injection**: Dynamically constructed queries are vulnerable if not handled carefully. Mitigation: Use parameterized queries or ORM features that prevent SQL injection.
- ⚠️ **Performance on Large Datasets**: Complex filters on large tables can be slow. Mitigation: Ensure appropriate indexing (A6), optimize query patterns.

**Dependencies**: B5 (GL Data Storage Service), B7/B8 (GL Data Validation APIs), A6 (GL Data Storage Schema), B2 (RBAC API)

**Build Order**: #22

---

### Story B14: Random Sampling Algorithm API
#### Description:
As a backend engineer, I want to implement an API that performs simple random sampling from the filtered GL data, so that auditors can select samples using this method.
**Details**:
-   **Tech Stack**: Python (FastAPI), PostgreSQL (A6), SQLAlchemy.
-   **Endpoints**:
    -   `POST /api/v1/sampling/{dataset_id}/random`:
        -   Request: `{ "sample_size": 100 }` (from B12)
        -   Response: `{ "selected_sample_ids": ["uuid1", "uuid2", ...], "sample_size": 100 }` (200 OK).
-   **Service Logic**:
    -   Retrieves the `final_sample_size` from `gl_datasets` (B12).
    -   Retrieves the currently filtered GL data (from B13).
    -   Selects `sample_size` random transactions from the filtered data.
    -   Stores the selected sample (B17).
    -   Logs the sampling action to the audit trail (B10).
-   **Business Rules**:
    -   Sample size must be positive and not exceed the filtered population size.
    -   Selection must be truly random.
-   **Error Handling**: Invalid sample size, insufficient population.

#### Acceptance Criteria
- [x] `POST /api/v1/sampling/{dataset_id}/random` endpoint is implemented.
- [x] The endpoint retrieves the `final_sample_size` from the `gl_datasets` table (B12).
- [x] The endpoint retrieves the GL transactions based on the currently active filters (from B13).
- [x] The endpoint implements a simple random sampling algorithm to select the specified `sample_size` transactions from the filtered population.
- [x] The selected sample transactions are stored using the B17 API.
- [x] An audit log entry is created using B10 for the random sampling action, including the sample size and method.
- [x] The endpoint returns a 200 OK response with the IDs of the selected sample transactions and the final sample size.
- [x] Error responses are returned for:
    -   Invalid `sample_size` (e.g., negative, zero, or exceeding filtered population).
    -   Insufficient filtered population to draw the sample.
- [x] The endpoint is protected by RBAC, requiring the 'Auditor' role (from B2).
- [x] Unit and integration tests are written for the random sampling logic.

#### Effort Estimate: **3 SP**
**Complexity**: Medium

**Breakdown**:
- Backend: 100% (3 days)

**Reasoning**:
```
Day 1:
- Define `POST /api/v1/sampling/{dataset_id}/random` endpoint. (3 hours)
- Implement logic to retrieve `final_sample_size` (B12) and filtered GL data (B13). (5 hours)

Day 2:
- Develop random sampling algorithm (e.g., `ORDER BY RANDOM() LIMIT N` in SQL). (6 hours)
- Implement validation for sample size against population. (2 hours)

Day 3:
- Integrate with B17 to store selected samples. (3 hours)
- Integrate with B10 to log the sampling action. (2 hours)
- Apply RBAC (Auditor role) and write tests. (3 hours)
```

**Risk Factors**:
- ⚠️ **True Randomness**: Ensuring the random selection is statistically sound and not biased. Mitigation: Use database's native random functions or a cryptographically secure random number generator if higher assurance is needed.
- ⚠️ **Performance on Large Populations**: `ORDER BY RANDOM()` can be slow on very large tables. Mitigation: Consider alternative sampling techniques for large datasets (e.g., reservoir sampling if data is streamed, or pre-generating random numbers).

**Dependencies**: B12 (Sample Size Override API), B13 (GL Data Filtering API), B17 (Selected Samples Persistence API), B10 (Audit Trail Logging API), A6 (GL Data Storage Schema), B2 (RBAC API)

**Build Order**: #23

---

### Story B15: Systematic Sampling Algorithm API
#### Description:
As a backend engineer, I want to implement an API that performs systematic sampling (every Nth item after a random start) from the filtered GL data, so that auditors can select samples using this method.
**Details**:
-   **Tech Stack**: Python (FastAPI), PostgreSQL (A6), SQLAlchemy.
-   **Endpoints**:
    -   `POST /api/v1/sampling/{dataset_id}/systematic`:
        -   Request: `{ "sample_size": 100, "starting_point": 5 }` (from B12, F9)
        -   Response: `{ "selected_sample_ids": ["uuid1", "uuid2", ...], "sample_size": 100 }` (200 OK).
-   **Service Logic**:
    -   Retrieves `final_sample_size` (B12) and filtered GL data (B13).
    -   Calculates sampling interval `k = Population Size / Sample Size`.
    -   Selects a random `starting_point` (if not provided by user) within the first interval `1` to `k`.
    -   Selects every `k`th transaction from the ordered filtered data, starting from `starting_point`.
    -   Stores the selected sample (B17).
    -   Logs the sampling action to the audit trail (B10).
-   **Business Rules**:
    -   Data must be ordered (e.g., by `transaction_date` or `id`) for systematic sampling.
    -   Sample size must be positive and not exceed the filtered population size.
-   **Error Handling**: Invalid sample size, insufficient population, invalid starting point.

#### Acceptance Criteria
- [x] `POST /api/v1/sampling/{dataset_id}/systematic` endpoint is implemented.
- [x] The endpoint retrieves the `final_sample_size` from the `gl_datasets` table (B12).
- [x] The endpoint retrieves the GL transactions based on the currently active filters (from B13), ordered by a consistent field (e.g., `transaction_date` then `id`).
- [x] The endpoint calculates the sampling interval `k` (population size / sample size).
- [x] The endpoint selects a random `starting_point` within the first interval `1` to `k` if not provided by the user.
- [x] The endpoint implements a systematic sampling algorithm to select every `k`th transaction from the ordered filtered data, starting from the `starting_point`.
- [x] The selected sample transactions are stored using the B17 API.
- [x] An audit log entry is created using B10 for the systematic sampling action, including the sample size, method, interval, and starting point.
- [x] The endpoint returns a 200 OK response with the IDs of the selected sample transactions and the final sample size.
- [x] Error responses are returned for:
    -   Invalid `sample_size` or `starting_point`.
    -   Insufficient filtered population.
- [x] The endpoint is protected by RBAC, requiring the 'Auditor' role (from B2).
- [x] Unit and integration tests are written for the systematic sampling logic.

#### Effort Estimate: **3 SP**
**Complexity**: Medium

**Breakdown**:
- Backend: 100% (3 days)

**Reasoning**:
```
Day 1:
- Define `POST /api/v1/sampling/{dataset_id}/systematic` endpoint. (3 hours)
- Implement logic to retrieve `final_sample_size` (B12) and filtered GL data (B13), ensuring consistent ordering. (5 hours)

Day 2:
- Develop logic to calculate sampling interval `k`. (3 hours)
- Implement logic to select a random `starting_point` or use user-provided. (3 hours)
- Develop systematic selection logic (e.g., using `ROW_NUMBER()` and modulo in SQL). (2 hours)

Day 3:
- Integrate with B17 to store selected samples. (3 hours)
- Integrate with B10 to log the sampling action. (2 hours)
- Apply RBAC (Auditor role) and write tests for various scenarios. (3 hours)
```

**Risk Factors**:
- ⚠️ **Ordering Bias**: If the underlying data has a hidden order that correlates with the sampling interval, bias can be introduced. Mitigation: Document the ordering criteria used, ensure it's not related to the audit objective.
- ⚠️ **Performance**: Ordering large datasets can be slow. Mitigation: Ensure appropriate indexing, optimize SQL queries.

**Dependencies**: B12 (Sample Size Override API), B13 (GL Data Filtering API), B17 (Selected Samples Persistence API), B10 (Audit Trail Logging API), A6 (GL Data Storage Schema), B2 (RBAC API)

**Build Order**: #24

---

### Story B16: Monetary Unit Sampling (MUS) Algorithm API
#### Description:
As a backend engineer, I want to implement an API that performs Monetary Unit Sampling (MUS) / PPS sampling, so that auditors can select samples proportional to their monetary value.
**Details**:
-   **Tech Stack**: Python (FastAPI), PostgreSQL (A6), SQLAlchemy.
-   **Endpoints**:
    -   `POST /api/v1/sampling/{dataset_id}/mus`:
        -   Request: `{ "sample_size": 100, "tainting_factor": 1.0 }` (from B12, F9)
        -   Response: `{ "selected_sample_ids": ["uuid1", "uuid2", ...], "sample_size": 100 }` (200 OK).
-   **Service Logic**:
    -   Retrieves `final_sample_size` (B12) and filtered GL data (B13).
    -   Calculates sampling interval `k = Population Value / Sample Size`.
    -   Generates `sample_size` random monetary units.
    -   Selects transactions corresponding to these monetary units (e.g., using cumulative sum of amounts).
    -   Handles negative amounts (e.g., treat as positive for selection, or exclude).
    -   Stores the selected sample (B17).
    -   Logs the sampling action to the audit trail (B10).
-   **Business Rules**:
    -   Sample size must be positive and not exceed the filtered population size.
    -   Tainting factor (for projecting misstatement) can be provided.
-   **Error Handling**: Invalid sample size, insufficient population, negative amounts if not handled.

#### Acceptance Criteria
- [x] `POST /api/v1/sampling/{dataset_id}/mus` endpoint is implemented.
- [x] The endpoint retrieves the `final_sample_size` from the `gl_datasets` table (B12).
- [x] The endpoint retrieves the GL transactions based on the currently active filters (from B13), ordered by a consistent field (e.g., `id`).
- [x] The endpoint calculates the sampling interval (monetary units per sample item).
- [x] The endpoint implements the Monetary Unit Sampling (MUS) algorithm to select transactions proportional to their monetary value.
- [x] The algorithm correctly handles positive and negative transaction amounts (e.g., negative amounts are typically excluded or treated specially in MUS).
- [x] The selected sample transactions are stored using the B17 API.
- [x] An audit log entry is created using B10 for the MUS sampling action, including the sample size, method, and interval.
- [x] The endpoint returns a 200 OK response with the IDs of the selected sample transactions and the final sample size.
- [x] Error responses are returned for:
    -   Invalid `sample_size`.
    -   Insufficient filtered population value.
- [x] The endpoint is protected by RBAC, requiring the 'Auditor' role (from B2).
- [x] Unit and integration tests are written for the MUS sampling logic with various data scenarios.

#### Effort Estimate: **5 SP**
**Complexity**: High

**Breakdown**:
- Backend: 100% (5 days)

**Reasoning**:
```
Day 1:
- Define `POST /api/v1/sampling/{dataset_id}/mus` endpoint. (3 hours)
- Implement logic to retrieve `final_sample_size` (B12) and filtered GL data (B13). (5 hours)

Day 2:
- Research and understand the MUS algorithm in detail, including handling of negative/zero amounts. (6 hours)
- Develop logic to calculate monetary sampling interval. (2 hours)

Day 3:
- Implement core MUS selection logic (e.g., using cumulative sums and random monetary units). (8 hours)

Day 4:
- Handle edge cases for MUS (e.g., very large transactions, zero population value). (4 hours)
- Implement validation for sample size against population value. (4 hours)

Day 5:
- Integrate with B17 to store selected samples. (3 hours)
- Integrate with B10 to log the sampling action. (2 hours)
- Apply RBAC (Auditor role) and write comprehensive tests. (3 hours)
```

**Risk Factors**:
- ⚠️ **Algorithm Complexity**: MUS is more complex than simple random or systematic sampling, requiring careful implementation to ensure statistical correctness. Mitigation: Thorough research, peer review of the algorithm, extensive unit testing with known examples.
- ⚠️ **Performance on Large Datasets**: Calculating cumulative sums and selecting transactions can be resource-intensive. Mitigation: Optimize database queries, consider pre-calculating cumulative sums if feasible.

**Dependencies**: B12 (Sample Size Override API), B13 (GL Data Filtering API), B17 (Selected Samples Persistence API), B10 (Audit Trail Logging API), A6 (GL Data Storage Schema), B2 (RBAC API)

**Build Order**: #25

---

### Story B17: Selected Samples Persistence & Retrieval API
#### Description:
As a backend engineer, I want to implement an API to store the selected samples and retrieve them efficiently, so that users can review and export their results.
**Details**:
-   **Tech Stack**: Python (FastAPI), PostgreSQL (A6), SQLAlchemy.
-   **Data Model**:
    -   `samples` table: `id` (UUID, PK), `dataset_id` (FK to gl_datasets.id), `sample_size` (INT), `sampling_method` (VARCHAR), `sampling_parameters` (JSONB), `generated_at` (TIMESTAMP), `generated_by_user_id` (FK to users.id).
    -   `gl_transactions` table (A6): `is_selected_for_sample` (BOOLEAN), `selected_sample_id` (FK to samples.id).
-   **Endpoints**:
    -   `POST /api/v1/sampling/{dataset_id}/samples/store`: (Internal, called by B14, B15, B16, B21)
        -   Request: `{ "transaction_ids": ["uuid1", "uuid2", ...], "sample_size": 100, "method": "random", "parameters": {} }`
        -   Response: `{ "sample_id": "..." }` (201 Created).
    -   `GET /api/v1/sampling/{dataset_id}/samples`:
        -   Response: `{ "sample_id": "...", "method": "...", "transactions": [ { "id": "...", "transaction_id": "...", "amount": "...", ... }, ... ] }` (200 OK).
-   **Service Logic**:
    -   Creates a new `samples` record.
    -   Updates `is_selected_for_sample` and `selected_sample_id` in `gl_transactions` for selected items.
    -   Retrieval endpoint joins `samples` and `gl_transactions` to get full data.
-   **Business Rules**: A dataset can have only one active sample at a time (or multiple, but only one is 'current'). For simplicity, assume one current sample.
-   **Error Handling**: Invalid `dataset_id`, database errors.

#### Acceptance Criteria
- [x] A `samples` table is created with `id`, `dataset_id`, `sample_size`, `sampling_method`, `sampling_parameters` (JSONB), `generated_at`, `generated_by_user_id` fields.
- [x] The `gl_transactions` table (A6) is updated with `is_selected_for_sample` (BOOLEAN) and `selected_sample_id` (FK to samples.id) fields.
- [x] An internal service function `store_selected_sample` is implemented to:
    -   Create a new record in the `samples` table.
    -   Update the `is_selected_for_sample` and `selected_sample_id` fields for the chosen transactions in `gl_transactions`.
- [x] `GET /api/v1/sampling/{dataset_id}/samples` endpoint is implemented to retrieve the currently selected sample.
- [x] The retrieval endpoint returns the full details of the selected GL transactions, including all original GL data fields.
- [x] The retrieval endpoint supports pagination for large sample sets.
- [x] All endpoints are protected by RBAC, requiring the 'Auditor' role (from B2).
- [x] Unit and integration tests are written for sample persistence and retrieval.

#### Effort Estimate: **3 SP**
**Complexity**: Medium

**Breakdown**:
- Backend: 100% (3 days)

**Reasoning**:
```
Day 1:
- Design `samples` table schema and update `gl_transactions` schema (A6). (4 hours)
- Write Alembic migration for new table and fields. (2 hours)
- Implement SQLAlchemy ORM models. (2 hours)

Day 2:
- Implement internal `store_selected_sample` function to create `samples` record and update `gl_transactions`. (6 hours)
- Define `GET /api/v1/sampling/{dataset_id}/samples` endpoint. (2 hours)

Day 3:
- Implement retrieval logic, joining `samples` and `gl_transactions`. (4 hours)
- Add pagination support to retrieval. (2 hours)
- Apply RBAC (Auditor role) and write tests. (2 hours)
```

**Risk Factors**:
- ⚠️ **Data Consistency**: Ensuring `gl_transactions` accurately reflects the selected sample. Mitigation: Use database transactions for updates.
- ⚠️ **Performance of Retrieval**: Retrieving full details for a large sample can be slow. Mitigation: Optimize SQL queries, ensure proper indexing.

**Dependencies**: B14, B15, B16, B21 (Sampling Algorithms), A6 (GL Data Storage Schema), B2 (RBAC API)

**Build Order**: #26

---

### Story B18: Sample Export API
#### Description:
As a backend engineer, I want to implement an API to generate and export the selected samples to CSV and XLSX formats, including a header with key sampling parameters, so that auditors can use the data externally.
**Details**:
-   **Tech Stack**: Python (FastAPI, Pandas, `openpyxl`), PostgreSQL (A6, B17).
-   **Endpoints**:
    -   `GET /api/v1/sampling/{dataset_id}/samples/export?format={csv|xlsx}`:
        -   Response: File download (CSV or XLSX) (200 OK).
-   **Service Logic**:
    -   Retrieves the selected sample transactions (from B17).
    -   Retrieves key sampling parameters (method, sample size, justification) from the `samples` table (B17).
    -   Generates a CSV or XLSX file.
    -   Includes a header section in the file with sampling parameters.
    -   Streams the generated file as a response.
-   **Business Rules**:
    -   Export includes all GL data fields.
    -   Header section should be clearly distinguishable.
-   **Error Handling**: No sample found, file generation errors.

#### Acceptance Criteria
- [x] `GET /api/v1/sampling/{dataset_id}/samples/export?format={csv|xlsx}` endpoint is implemented.
- [x] The endpoint accepts a `format` query parameter ('csv' or 'xlsx').
- [x] The endpoint retrieves the selected sample transactions and their full GL data fields (from B17).
- [x] The endpoint retrieves key sampling parameters (method, sample size, override justification, etc.) from the `samples` table (B17).
- [x] For CSV export:
    -   A CSV file is generated with a header row containing column names.
    -   A preceding section (e.g., commented lines or a separate sheet in Excel) includes key sampling parameters.
- [x] For XLSX export:
    -   An Excel file is generated with a sheet for the sample data.
    -   A separate sheet or a header section in the first sheet includes key sampling parameters.
- [x] The generated file is streamed as a download response with the correct `Content-Type` and `Content-Disposition` headers.
- [x] An audit log entry is created using B10 for the sample export action, including the format.
- [x] Error responses are returned for:
    -   Invalid `dataset_id` or no sample found.
    -   Unsupported export format.
    -   File generation failures.
- [x] The endpoint is protected by RBAC, requiring the 'Auditor' role (from B2).
- [x] Unit and integration tests are written for the export logic.

#### Effort Estimate: **4 SP**
**Complexity**: Medium

**Breakdown**:
- Backend: 100% (4 days)

**Reasoning**:
```
Day 1:
- Define `GET /api/v1/sampling/{dataset_id}/samples/export` endpoint. (3 hours)
- Implement logic to retrieve selected sample transactions (B17) and sampling parameters (B17). (5 hours)

Day 2:
- Develop CSV generation logic using Pandas, including custom header. (8 hours)

Day 3:
- Develop XLSX generation logic using Pandas/Openpyxl, including custom header/sheet. (8 hours)

Day 4:
- Implement file streaming as FastAPI response. (4 hours)
- Integrate with B10 to log export action. (1 hour)
- Apply RBAC (Auditor role) and write tests for both formats. (3 hours)
```

**Risk Factors**:
- ⚠️ **Large File Generation**: Generating very large CSV/XLSX files can be memory-intensive and slow. Mitigation: Use streaming writers, optimize Pandas usage, consider asynchronous generation for extremely large files (future).
- ⚠️ **Header Formatting**: Ensuring the custom header with sampling parameters is clear and readable in both formats. Mitigation: Test with various spreadsheet software.

**Dependencies**: B17 (Selected Samples Persistence & Retrieval API), B10 (Audit Trail Logging API), B2 (RBAC API)

**Build Order**: #27

---

### Story B19: Audit Trail Retrieval API
#### Description:
As a backend engineer, I want to implement an API to retrieve and display the immutable audit trail for specific engagements, so that authorized users can review all logged activities.
**Details**:
-   **Tech Stack**: Python (FastAPI), PostgreSQL (A7), SQLAlchemy.
-   **Endpoints**:
    -   `GET /api/v1/audit-trail/{engagement_id}`:
        -   Query Params: `start_date`, `end_date`, `user_id`, `action_type`, `page`, `page_size`.
        -   Response: `{ "total_records": 100, "page": 1, "page_size": 10, "logs": [ { "id": "...", "timestamp": "...", "user_email": "...", "action_type": "...", "description": "...", "details": {} }, ... ] }` (200 OK).
-   **Service Logic**:
    -   Queries the `audit_logs` table (A7).
    -   Supports filtering by `engagement_id`, date range, `user_id`, `action_type`.
    -   Implements pagination and sorting (by `timestamp` descending).
    -   Joins with `users` table (A2) to get user email/name.
-   **Business Rules**: Only 'Manager' role can access the audit trail.
-   **Error Handling**: Invalid `engagement_id`, invalid filter parameters.

#### Acceptance Criteria
- [x] `GET /api/v1/audit-trail/{engagement_id}` endpoint is implemented.
- [x] The endpoint retrieves audit log entries from the `audit_logs` table (A7) for the specified `engagement_id`.
- [x] The endpoint supports filtering by:
    -   `start_date` and `end_date` (for `timestamp`).
    -   `user_id` (linking to `users` table).
    -   `action_type`.
- [x] The endpoint supports pagination (`page`, `page_size`) and returns `total_records`.
- [x] Audit logs are returned sorted by `timestamp` in descending order.
- [x] The response includes `id`, `timestamp`, `user_email` (or name), `action_type`, `description`, and `details` (JSONB).
- [x] Error responses are returned for:
    -   Invalid `engagement_id`.
    -   Invalid filter parameters.
- [x] The endpoint is protected by RBAC, requiring the 'Manager' role (from B2).
- [x] Unit and integration tests are written for audit trail retrieval and filtering.

#### Effort Estimate: **3 SP**
**Complexity**: Medium

**Breakdown**:
- Backend: 100% (3 days)

**Reasoning**:
```
Day 1:
- Define `GET /api/v1/audit-trail/{engagement_id}` endpoint. (3 hours)
- Implement logic to query `audit_logs` table (A7) for `engagement_id`. (5 hours)

Day 2:
- Implement dynamic filtering logic for date range, user_id, action_type. (6 hours)
- Implement pagination and sorting by timestamp. (2 hours)

Day 3:
- Join with `users` table (A2) to retrieve user details. (3 hours)
- Apply RBAC (Manager role) and write tests for filtering and pagination. (5 hours)
```

**Risk Factors**:
- ⚠️ **Performance on Large Audit Trails**: Filtering and paginating through millions of audit logs can be slow. Mitigation: Ensure proper indexing (A7), optimize queries, consider dedicated search/analytics engine for very large logs (future).
- ⚠️ **Data Exposure**: Ensuring only authorized users can view audit logs. Mitigation: Robust RBAC enforcement.

**Dependencies**: B10 (Audit Trail Logging API), A7 (Audit Trail Database Schema), B2 (RBAC API)

**Build Order**: #28

---

### Story B20: ML Risk Scoring Integration API
#### Description:
As a backend engineer, I want to integrate with the ML inference service to receive transaction risk scores and store them alongside GL data, so that these scores can be used for risk-stratified sampling.
**Details**:
-   **Tech Stack**: Python (FastAPI), `httpx` (HTTP client), PostgreSQL (A6).
-   **Endpoints**:
    -   `POST /api/v1/gl-data/{dataset_id}/score-risk`: (Internal/Triggered)
        -   Request: `{ "transaction_ids": ["uuid1", "uuid2", ...] }` (or triggered after B5)
        -   Response: `{ "message": "Risk scoring initiated" }` (202 Accepted).
-   **Service Logic**:
    -   Triggered after GL data is stored (B5) or explicitly by an admin.
    -   Retrieves GL transaction data for the `dataset_id` (or a batch of transactions).
    -   Makes an HTTP request to the ML inference service (M4) with transaction features.
    -   Receives risk scores (e.g., 0-1) for each transaction.
    -   Updates the `risk_score` field in the `gl_transactions` table (A6) for each transaction.
    -   Logs the risk scoring action to the audit trail (B10).
-   **Business Rules**:
    -   Risk scoring should be an asynchronous process.
    -   Handles potential latency or errors from the ML service.
-   **Error Handling**: ML service unavailability, invalid response from ML service, database update failures.

#### Acceptance Criteria
- [x] An internal service function `trigger_risk_scoring` is implemented.
- [x] `trigger_risk_scoring` retrieves GL transaction data (features) for a given `dataset_id` (or a batch).
- [x] `trigger_risk_scoring` makes an HTTP POST request to the ML inference service endpoint (M4) with the transaction features.
- [x] `trigger_risk_scoring` parses the response from the ML service to extract risk scores for each transaction.
- [x] The `risk_score` field in the `gl_transactions` table (A6) is updated with the received scores.
- [x] An audit log entry is created using B10 for the risk scoring action, including the `dataset_id`.
- [x] Error handling is implemented for:
    -   ML inference service unavailability or timeout.
    -   Invalid or unexpected response from the ML service.
    -   Database update failures.
- [x] The `POST /api/v1/gl-data/{dataset_id}/score-risk` endpoint is implemented to trigger this internal service (can be protected for admin/manager initially).
- [x] Unit and integration tests are written for the ML integration logic.

#### Effort Estimate: **3 SP**
**Complexity**: Medium

**Breakdown**:
- Backend: 100% (3 days)

**Reasoning**:
```
Day 1:
- Design internal `trigger_risk_scoring` function. (3 hours)
- Implement HTTP client (`httpx`) to call ML inference service (M4). (5 hours)

Day 2:
- Implement logic to retrieve GL transaction data and format for ML service. (5 hours)
- Implement logic to parse ML service response and update `risk_score` in `gl_transactions`. (3 hours)

Day 3:
- Implement robust error handling for ML service calls and DB updates. (4 hours)
- Integrate with B10 for audit logging. (1 hour)
- Write unit and integration tests (mocking ML service). (3 hours)
```

**Risk Factors**:
- ⚠️ **ML Service Latency/Reliability**: The ML service might be slow or unstable. Mitigation: Implement timeouts, retries, circuit breakers, and asynchronous processing.
- ⚠️ **Data Format Mismatch**: Ensuring the data sent to and received from the ML service matches expectations. Mitigation: Clear API contract with ML team, robust serialization/deserialization.

**Dependencies**: B5 (GL Data Storage Service), M4 (Model Inference Service Deployment), B10 (Audit Trail Logging API), A6 (GL Data Storage Schema)

**Build Order**: #29

---

### Story B21: Risk-Stratified Sampling Logic API
#### Description:
As a backend engineer, I want to implement sampling logic that allows a configurable percentage of the sample to be drawn from the highest-risk transactions identified by the ML model, so that auditors can prioritize high-risk items.
**Details**:
-   **Tech Stack**: Python (FastAPI), PostgreSQL (A6), SQLAlchemy.
-   **Endpoints**:
    -   `POST /api/v1/sampling/{dataset_id}/risk-stratified`:
        -   Request: `{ "sample_size": 100, "high_risk_percentage": 30, "base_sampling_method": "random" }` (from B12, F14)
        -   Response: `{ "selected_sample_ids": ["uuid1", "uuid2", ...], "sample_size": 100 }` (200 OK).
-   **Service Logic**:
    -   Retrieves `final_sample_size` (B12) and `high_risk_percentage` (from request).
    -   Calculates number of high-risk samples (`N_high`) and remaining samples (`N_base`).
    -   Selects `N_high` transactions from the highest-risk transactions (based on `risk_score` from B20).
    -   Selects `N_base` transactions from the remaining population using a `base_sampling_method` (e.g., random).
    -   Combines the two sets of samples.
    -   Stores the selected sample (B17).
    -   Logs the sampling action to the audit trail (B10).
-   **Business Rules**:
    -   `risk_score` must be present for transactions.
    -   `high_risk_percentage` must be between 0 and 100.
-   **Error Handling**: Invalid parameters, insufficient high-risk population.

#### Acceptance Criteria
- [x] `POST /api/v1/sampling/{dataset_id}/risk-stratified` endpoint is implemented.
- [x] The endpoint accepts `sample_size`, `high_risk_percentage` (0-100), and an optional `base_sampling_method` (e.g., 'random', 'systematic').
- [x] The endpoint retrieves the `final_sample_size` (B12) and filtered GL data (B13), including `risk_score` (B20).
- [x] The endpoint calculates the number of samples to be drawn from high-risk transactions (`N_high`) and the remaining samples (`N_base`).
- [x] `N_high` transactions are selected from the highest-risk transactions (e.g., top `N_high` by `risk_score`).
- [x] `N_base` transactions are selected from the *remaining* population (excluding already selected high-risk) using the specified `base_sampling_method` (e.g., random sampling).
- [x] The combined set of `sample_size` transactions is stored using the B17 API.
- [x] An audit log entry is created using B10 for the risk-stratified sampling action, including parameters and selected sample IDs.
- [x] The endpoint returns a 200 OK response with the IDs of the selected sample transactions and the final sample size.
- [x] Error responses are returned for:
    -   Invalid `high_risk_percentage` or `sample_size`.
    -   Insufficient high-risk or base population.
    -   Missing `risk_score` for transactions.
- [x] The endpoint is protected by RBAC, requiring the 'Auditor' role (from B2).
- [x] Unit and integration tests are written for the risk-stratified sampling logic.

#### Effort Estimate: **4 SP**
**Complexity**: High

**Breakdown**:
- Backend: 100% (4 days)

**Reasoning**:
```
Day 1:
- Define `POST /api/v1/sampling/{dataset_id}/risk-stratified` endpoint. (3 hours)
- Implement input validation for `sample_size` and `high_risk_percentage`. (5 hours)

Day 2:
- Implement logic to retrieve `final_sample_size` (B12), filtered GL data (B13), and `risk_score` (B20). (6 hours)
- Calculate `N_high` and `N_base`. (2 hours)

Day 3:
- Develop logic to select `N_high` transactions from top risk scores. (5 hours)
- Develop logic to select `N_base` transactions from the remaining population using a base method (e.g., random). (3 hours)

Day 4:
- Combine samples, integrate with B17 to store. (3 hours)
- Integrate with B10 for audit logging. (1 hour)
- Apply RBAC (Auditor role) and write comprehensive tests. (4 hours)
```

**Risk Factors**:
- ⚠️ **Algorithm Complexity**: Combining two sampling methods and ensuring no duplicates or biases. Mitigation: Careful algorithm design, clear separation of concerns, extensive testing.
- ⚠️ **Performance**: Multiple database queries and selections on large datasets. Mitigation: Optimize queries, consider database-level set operations.

**Dependencies**: B12 (Sample Size Override API), B13 (GL Data Filtering API), B17 (Selected Samples Persistence API), B20 (ML Risk Scoring Integration API), B10 (Audit Trail Logging API), B14 (Random Sampling, for base method), A6 (GL Data Storage Schema), B2 (RBAC API)

**Build Order**: #30

---

## 🤖 ML Stories

### Story M1: GL Data Feature Engineering Pipeline for Risk Scoring
#### Description:
As an ML engineer, I want to develop a data pipeline to extract and engineer features from raw GL data (e.g., transaction amount, time of day, account combinations, round numbers) suitable for risk scoring, so that the ML model has relevant inputs.
**Details**:
-   **Tech Stack**: Python (Pandas, NumPy, Scikit-learn preprocessors), AWS S3 (A1), AWS Batch/ECS (for processing large datasets).
-   **Pipeline Logic**:
    1.  Input: Raw GL transaction data (from B5, stored in PostgreSQL).
    2.  Extract features:
        -   `amount`: numerical value.
        -   `transaction_date`: extract day of week, month, quarter, hour of day.
        -   `account_id`: one-hot encode or embed.
        -   `description`: text features (e.g., length, presence of keywords, TF-IDF - start simple).
        -   `round_number_flag`: boolean, true if amount is a round number (e.g., ends in .00, .50, or multiple of 100).
        -   `weekend_flag`: boolean, true if transaction date is a weekend.
        -   `unusual_hour_flag`: boolean, true if transaction hour is outside business hours (e.g., 10 PM - 6 AM).
    3.  Handle missing values (imputation or flag).
    4.  Scale/normalize numerical features.
    5.  Output: Feature matrix (e.g., Pandas DataFrame or Parquet file) stored in S3, linked to `dataset_id`.
-   **Training Data**: Uses the `gl_transactions` table (A6) as source.
-   **Inference Requirements**: Features must be extractable in real-time or near real-time for inference.
-   **Constraints**: Pipeline should be reproducible and versioned.

#### Acceptance Criteria
- [x] A Python-based feature engineering script/pipeline is developed.
- [x] The pipeline can read GL transaction data from the `gl_transactions` table (A6).
- [x] The pipeline extracts at least 5 relevant features from the raw GL data, including:
    -   Numerical `amount`.
    -   Time-based features (e.g., `day_of_week`, `hour_of_day`).
    -   Categorical features (e.g., `account_id` - one-hot encoded).
    -   Derived features (e.g., `round_number_flag`, `weekend_flag`, `unusual_hour_flag`).
- [x] The pipeline handles missing values (e.g., imputation, flagging).
- [x] Numerical features are scaled/normalized.
- [x] The output is a structured feature matrix (e.g., Pandas DataFrame) that can be stored (e.g., as Parquet in S3).
- [x] The pipeline is containerized (e.g., Docker) for execution in AWS Batch/ECS.
- [x] The pipeline is reproducible, meaning running it with the same input data yields the same features.
- [x] Documentation for the feature engineering process, including feature definitions, is provided.
- [x] Unit tests are written for individual feature extraction functions.

#### Effort Estimate: **5 SP**
**Complexity**: High

**Breakdown**:
- ML: 100% (5 days)

**Reasoning**:
```
Day 1:
- Research relevant features for GL transaction risk scoring. (4 hours)
- Set up Python environment with Pandas, NumPy, Scikit-learn. (4 hours)

Day 2:
- Implement initial data loading from PostgreSQL (A6) into Pandas DataFrame. (4 hours)
- Develop feature extraction for `amount` and basic `transaction_date` components (day, hour). (4 hours)

Day 3:
- Develop feature extraction for `account_id` (one-hot encoding). (4 hours)
- Implement derived features: `round_number_flag`, `weekend_flag`, `unusual_hour_flag`. (4 hours)

Day 4:
- Implement missing value handling and numerical feature scaling. (5 hours)
- Containerize the pipeline (Dockerfile). (3 hours)

Day 5:
- Write unit tests for feature functions. (4 hours)
- Document features and pipeline. (4 hours)
```

**Risk Factors**:
- ⚠️ **Feature Leakage**: Accidentally including features that are not available at inference time or directly encode the target variable. Mitigation: Careful feature selection, peer review.
- ⚠️ **Performance on Large Datasets**: Processing millions of transactions for feature engineering can be slow. Mitigation: Use vectorized Pandas operations, consider distributed processing (AWS Batch/Spark).
- ⚠️ **Data Drift**: Features might change over time, requiring pipeline updates. Mitigation: Monitor data quality, version control pipeline.

**Dependencies**: A1 (S3 for storage), B5 (GL Data Storage Service for raw data), A6 (GL Data Storage Schema)

**Build Order**: #15

---

### Story M2: Initial Risk Scoring Model Development
#### Description:
As an ML engineer, I want to develop an initial ML model (e.g., anomaly detection, classification) to score and rank GL transactions by risk level, considering features like unusual amounts and posting patterns, so that high-risk transactions can be identified.
**Details**:
-   **Tech Stack**: Python (Scikit-learn, XGBoost, Pandas), Jupyter notebooks.
-   **Model Type**: Supervised classification (if labeled data is available) or unsupervised anomaly detection (if not). Let's assume unsupervised anomaly detection (e.g., Isolation Forest, One-Class SVM) for initial development, as labeled fraud data is often scarce.
-   **Training Data**: Features generated by M1.
-   **Output**: A risk score (e.g., 0-1) for each transaction, where higher scores indicate higher risk.
-   **Evaluation Metrics**: For anomaly detection, focus on interpretability and ability to surface unusual transactions. If some labeled data exists, use Precision@K, Recall@K.
-   **Retraining Strategy**: Initial model is static; retraining will be manual.
-   **Constraints**: Model must be explainable (M5).

#### Acceptance Criteria
- [x] An initial ML model is developed using Python (e.g., Scikit-learn's Isolation Forest or One-Class SVM).
- [x] The model is trained using the features generated by the M1 pipeline.
- [x] The model outputs a numerical risk score (e.g., 0-1) for each transaction, indicating its anomaly/risk level.
- [x] The model is evaluated on a held-out test set, demonstrating its ability to identify unusual patterns.
- [x] The model artifacts (e.g., `.pkl` file for Scikit-learn model) are serialized and stored.
- [x] A Jupyter notebook or script documents the model development process, including data loading, training, and evaluation.
- [x] The model's performance is assessed qualitatively (e.g., by reviewing top-scored transactions) and quantitatively (e.g., using anomaly detection metrics if applicable).
- [x] Documentation for the chosen model, its parameters, and its expected behavior is provided.
- [x] Unit tests are written for model loading and prediction functions.

#### Effort Estimate: **6 SP**
**Complexity**: High

**Breakdown**:
- ML: 100% (6 days)

**Reasoning**:
```
Day 1:
- Research suitable ML model types for anomaly detection in financial data (e.g., Isolation Forest, One-Class SVM). (4 hours)
- Set up Jupyter notebook for experimentation. (4 hours)

Day 2:
- Load features from M1 pipeline. (3 hours)
- Preprocess data for model (e.g., handle categorical features, scaling). (5 hours)

Day 3:
- Train initial Isolation Forest model. (6 hours)
- Experiment with hyperparameters. (2 hours)

Day 4:
- Evaluate model performance using appropriate metrics (e.g., anomaly scores distribution, qualitative review of top anomalies). (6 hours)
- Refine model based on evaluation. (2 hours)

Day 5:
- Serialize the trained model (e.g., using `joblib` or `pickle`). (4 hours)
- Document model choice, training process, and evaluation results. (4 hours)

Day 6:
- Write unit tests for model loading and prediction. (4 hours)
- Prepare model for deployment (e.g., create a simple prediction function). (4 hours)
```

**Risk Factors**:
- ⚠️ **Lack of Labeled Data**: Without labeled fraud data, model evaluation is challenging. Mitigation: Focus on anomaly detection, use domain expertise for qualitative evaluation, plan for data labeling efforts.
- ⚠️ **Model Interpretability**: Complex models can be black boxes. Mitigation: Choose models known for some interpretability (e.g., tree-based models), or plan for post-hoc explainability (M5).
- ⚠️ **False Positives/Negatives**: Anomaly detection models can generate many false positives. Mitigation: Tune thresholds, iterate with auditors on feedback.

**Dependencies**: M1 (GL Data Feature Engineering Pipeline)

**Build Order**: #27

---

### Story M3: Model Training & Evaluation Automation
#### Description:
As an ML engineer, I want to set up an automated pipeline for training, evaluating, and versioning the risk scoring model, so that the model can be regularly updated and its performance tracked.
**Details**:
-   **Tech Stack**: MLflow (for experiment tracking, model registry, versioning), GitHub Actions (for orchestration), AWS S3 (for artifact storage), AWS Batch/ECS (for compute).
-   **Pipeline Logic**:
    1.  Trigger: Manual or scheduled (future).
    2.  Fetch data: Use M1 pipeline to generate features from latest GL data.
    3.  Train model: Execute M2 training script.
    4.  Evaluate model: Run evaluation script, log metrics (Precision@K, Recall@K, AUC if labeled data available).
    5.  Register model: Store model artifact and metadata in MLflow Model Registry.
    6.  Version model: Assign a new version number.
-   **Evaluation Metrics**: Log metrics from M2.
-   **Retraining Strategy**: Initial manual trigger.
-   **Constraints**: Must integrate with existing CI/CD (A3).

#### Acceptance Criteria
- [x] An automated pipeline is set up to trigger model training and evaluation.
- [x] The pipeline uses MLflow (or similar tool) for experiment tracking, logging parameters, metrics, and artifacts.
- [x] The pipeline fetches the latest features using the M1 pipeline.
- [x] The pipeline executes the M2 model training script.
- [x] The pipeline executes a model evaluation script, logging relevant metrics (e.g., Precision@K, Recall@K, F1-score if labeled data is used).
- [x] The trained model artifact is registered in MLflow Model Registry with versioning.
- [x] The pipeline is integrated with GitHub Actions (A3) for execution (e.g., a dedicated workflow).
- [x] Model training and evaluation runs are reproducible.
- [x] Documentation for the automated pipeline, including how to trigger it and interpret results, is provided.
- [x] Unit tests are written for the pipeline orchestration logic.

#### Effort Estimate: **5 SP**
**Complexity**: High

**Breakdown**:
- ML: 70% (3.5 days)
- DevOps: 30% (1.5 days)

**Reasoning**:
```
Day 1:
- Research MLOps tools (MLflow, DVC, SageMaker). Select MLflow for tracking/registry. (4 hours)
- Set up MLflow server (e.g., on EC2 or using managed service). (4 hours)

Day 2:
- Integrate M1 feature engineering and M2 model training scripts with MLflow tracking. (6 hours)
- Define evaluation metrics and log them to MLflow. (2 hours)

Day 3:
- Implement MLflow Model Registry for versioning and storing model artifacts. (6 hours)
- Create a Python script to orchestrate the training, evaluation, and registration steps. (2 hours)

Day 4:
- Integrate the orchestration script into a GitHub Actions workflow (A3). (5 hours)
- Configure AWS Batch/ECS for running the training job. (3 hours)

Day 5:
- Test the end-to-end pipeline, verify logging and model registration. (5 hours)
- Document the MLOps pipeline. (3 hours)
```

**Risk Factors**:
- ⚠️ **MLOps Tool Complexity**: Setting up and integrating MLOps tools can be complex. Mitigation: Start with core features of MLflow, iterate on advanced features.
- ⚠️ **Reproducibility Issues**: Ensuring the entire pipeline (data, code, environment) is reproducible. Mitigation: Use Docker, version control all scripts and dependencies.
- ⚠️ **Cost Management**: Running training jobs on cloud compute can be expensive. Mitigation: Optimize resource usage, use spot instances if appropriate.

**Dependencies**: M1 (Feature Engineering), M2 (Model Development), A3 (CI/CD Pipeline), A1 (S3 for artifacts)

**Build Order**: #28

---

### Story M4: Model Inference Service Deployment
#### Description:
As an ML engineer, I want to deploy the risk scoring model as a scalable inference service, so that the backend can request real-time risk scores for uploaded GL data.
**Details**:
-   **Tech Stack**: Python (FastAPI), Docker, AWS ECS Fargate (A1), AWS ECR (A3).
-   **Service Logic**:
    1.  Loads the latest/specified version of the trained model (from M3).
    2.  Exposes a REST API endpoint for inference.
    3.  Input: Raw GL transaction features (from B20).
    4.  Output: Risk scores (e.g., JSON array of scores).
-   **Inference Requirements**:
    -   Latency: < 200ms (p95) for a batch of 100 transactions.
    -   Scalability: Auto-scaling based on request load.
-   **Constraints**: Must be containerized and deployable via CI/CD (A3).

#### Acceptance Criteria
- [x] A Python FastAPI application is developed to serve the ML model for inference.
- [x] The application loads the latest (or specified) version of the trained ML model (from M3).
- [x] A `POST /predict` endpoint is exposed, accepting a batch of GL transaction features.
- [x] The endpoint returns a list of risk scores (e.g., 0-1) for the input transactions.
- [x] The application is containerized using Docker.
- [x] The Docker image is pushed to AWS ECR (A3) via the CI/CD pipeline.
- [x] The inference service is deployed to AWS ECS Fargate (A1) as a scalable service.
- [x] The service demonstrates a p95 latency of < 200ms for a batch of 100 transactions.
- [x] Basic auto-scaling is configured for the ECS service based on CPU utilization.
- [x] Error handling is implemented for invalid input, model loading failures, and prediction errors.
- [x] Documentation for the inference API and deployment is provided.
- [x] Unit and integration tests are written for the inference endpoint.

#### Effort Estimate: **4 SP**
**Complexity**: Medium

**Breakdown**:
- ML: 50% (2 days)
- DevOps: 50% (2 days)

**Reasoning**:
```
Day 1:
- Develop FastAPI application for inference. (4 hours)
- Implement model loading logic (from M3 artifact). (4 hours)

Day 2:
- Define `POST /predict` endpoint, accepting transaction features. (5 hours)
- Implement prediction logic and return risk scores. (3 hours)

Day 3:
- Create Dockerfile for the inference service. (4 hours)
- Integrate deployment into GitHub Actions CI/CD (A3) to ECS Fargate (A1). (4 hours)

Day 4:
- Configure ECS service for auto-scaling and monitoring (A4). (4 hours)
- Conduct performance testing to verify latency targets. (4 hours)
```

**Risk Factors**:
- ⚠️ **Latency Requirements**: Meeting strict latency targets can be challenging, especially with complex models or large batches. Mitigation: Optimize model for inference, use efficient serialization, consider GPU instances if needed (future).
- ⚠️ **Model Versioning**: Ensuring the correct model version is deployed and used. Mitigation: Use MLflow Model Registry (M3) and clear deployment strategies.
- ⚠️ **Resource Management**: Over-provisioning or under-provisioning compute resources. Mitigation: Start with reasonable defaults, monitor usage, and adjust auto-scaling.

**Dependencies**: M2 (Model Development), M3 (Model Training Automation), A1 (ECS Fargate), A3 (CI/CD Pipeline), A4 (Monitoring)

**Build Order**: #29

---

### Story M5: Explainability Feature Generation
#### Description:
As an ML engineer, I want to develop a mechanism to generate concise, human-readable explanations for each transaction's risk score (e.g., "round-number amount, posted 2 AM"), so that auditors can understand the model's rationale.
**Details**:
-   **Tech Stack**: Python (SHAP or LIME, Pandas), integrate with M4 inference service.
-   **Service Logic**:
    -   Input: A single GL transaction's features and its risk score.
    -   Uses an explainability library (e.g., SHAP) to determine feature contributions to the risk score.
    -   Translates feature contributions into human-readable text (e.g., "High amount (contributed +0.3 to risk)", "Round number (contributed +0.2 to risk)").
    -   Aggregates top N contributing features into a concise summary string.
    -   This logic can be integrated directly into the M4 inference service or as a post-processing step. Let's assume integration into M4 for simplicity.
-   **Output**: A string or list of strings explaining the risk score.
-   **Constraints**: Explanations must be concise and understandable by non-ML experts.

#### Acceptance Criteria
- [x] A Python-based mechanism is developed to generate explainability summaries for individual GL transactions.
- [x] The mechanism uses an explainability library (e.g., SHAP or LIME) to identify key features contributing to a transaction's risk score.
- [x] The feature contributions are translated into concise, human-readable text (e.g., "Flagged: round-number amount, posted 2 AM", "Reason: High amount, unusual time").
- [x] The explainability logic is integrated into the M4 inference service, so that explanations can be returned alongside risk scores.
- [x] The inference API (M4) is updated to optionally return the explainability summary.
- [x] The explanations are consistent with the model's behavior (i.e., higher contribution features are reflected in the explanation).
- [x] The mechanism gracefully handles cases where explanations cannot be generated or are not meaningful.
- [x] Documentation for the explainability approach and how to interpret the explanations is provided.
- [x] Unit tests are written for the explanation generation logic.

#### Effort Estimate: **5 SP**
**Complexity**: High

**Breakdown**:
- ML: 100% (5 days)

**Reasoning**:
```
Day 1:
- Research explainability libraries (SHAP, LIME) and their integration with the chosen ML model (M2). (4 hours)
- Set up environment for experimentation. (4 hours)

Day 2:
- Implement basic SHAP/LIME explanation generation for a single transaction. (6 hours)
- Experiment with different explanation formats. (2 hours)

Day 3:
- Develop logic to translate raw feature contributions into human-readable text. (8 hours)

Day 4:
- Integrate explainability logic into the M4 inference service. (5 hours)
- Update M4 API to return explanations. (3 hours)

Day 5:
- Test explainability generation with various transactions (high risk, low risk, edge cases). (5 hours)
- Document the explainability approach and interpretation guidelines. (3 hours)
```

**Risk Factors**:
- ⚠️ **Explanation Quality**: Explanations might be technically correct but not intuitive or actionable for auditors. Mitigation: Iterate with domain experts, refine text generation.
- ⚠️ **Performance Overhead**: Generating explanations can be computationally intensive, adding latency to inference. Mitigation: Optimize explanation generation, consider caching, or generate explanations asynchronously for non-real-time use cases.
- ⚠️ **Model Compatibility**: Some explainability methods work better with certain model types. Mitigation: Ensure chosen library is compatible with M2 model.

**Dependencies**: M2 (Model Development), M4 (Model Inference Service Deployment)

**Build Order**: #30

---

## 📊 Summary

### Effort by Category

| Category | Stories | Total SP | % Effort |
|----------|---------|----------|-----------|
| Architecture & Non-Functional | 10 | 29 | 17.16% |
| Frontend | 15 | 48 | 28.40% |
| Backend | 21 | 67 | 39.64% |
| ML | 5 | 25 | 14.79% |
| **MVP Total** | **51** | **169** | **100%** |

### Team Composition Needed

| Role | % of Total Effort | Days Needed |
|------|-------------------|-------------|
| Frontend Engineer | 28.4% | ~48 days |
| Backend Engineer | 43.5% | ~73.5 days |
| DevOps Engineer | 13.6% | ~23 days |
| ML Engineer | 12.7% | ~21.5 days |
| QA Engineer | 1.8% | ~3 days |
| **Total** | 100% | **~169 engineering days** |

*With 5-person team (1 FE, 2 BE, 1 DevOps, 1 ML): ~8.5 weeks (with parallelization)*

---

## 🗓️ Sprint Plan

### Sprint 1 (Week 1) - Foundational Setup & User Access
**Goal**: Core infrastructure, secure user authentication, and basic GL data upload capability are functional.

-   ✅ A1: Setup Core Cloud Infrastructure (4 days)
-   ✅ A2: Establish Core Database & User Schema (2 days)
-   ✅ A3: Implement CI/CD Pipeline for Backend & Frontend (5 days)
-   ✅ A4: Configure Basic Application Monitoring & Alerting (2 days)
-   ✅ A5: Secure Backend API Gateway & TLS (3 days)
-   ✅ B1: User Authentication & Authorization API (4 days)
-   ✅ B2: Role-Based Access Control (RBAC) API (3 days)
-   ✅ F1: User Login & Registration UI (3 days)
-   ✅ F2: Role-Based Dashboard & Navigation (3 days)
-   ✅ B3: GL Data Upload API Endpoint (3 days)
-   ✅ B4: GL Data Parsing Service (4 days)
-   ✅ F3: GL Data Upload UI (3 days)

**Sprint Goal Complete When**: Users can register, log in, see a role-based dashboard, and successfully upload a GL data file which is then parsed and stored in S3.

### Sprint 2 (Week 2) - Data Ingestion & Validation
**Goal**: Complete GL data ingestion, mapping, validation, and summary display.

-   ✅ B5: GL Data Storage Service (3 days)
-   ✅ B6: GL Data Column Mapping API (3 days)
-   ✅ F4: GL Data Column Mapping UI (4 days)
-   ✅ B7: GL Data Validation API - Missing/Non-numeric Fields (4 days)
-   ✅ B8: GL Data Validation API - Duplicate Transaction IDs (3 days)
-   ✅ F5: GL Data Validation Display & User Correction UI (5 days)
-   ✅ B9: GL Data Summary API (2 days)
-   ✅ F6: GL Data Summary Display UI (2 days)
-   ✅ A6: Design & Implement GL Data Storage Schema (3 days)
-   ✅ A7: Design & Implement Audit Trail Database Schema (2 days)
-   ✅ B10: Audit Trail Logging API (3 days)
-   ✅ B11: Sample Size Calculation API (4 days)
-   ✅ F7: Sample Size Calculation Parameters UI (3 days)
-   ✅ M1: GL Data Feature Engineering Pipeline for Risk Scoring (5 days)

**Sprint Goal Complete When**: Auditors can upload GL data, map columns, review and correct validation errors, view a summary, and input parameters for sample size calculation. ML feature engineering pipeline is ready.

### Sprint 3 (Week 3) - Core Sampling & Audit Trail
**Goal**: Implement core sampling methods, sample size override, sample display/export, and audit trail viewing.

-   ✅ B12: Sample Size Override API (2 days)
-   ✅ F8: Calculated Sample Size Display & Override UI (3 days)
-   ✅ B13: GL Data Filtering API (3 days)
-   ✅ F10: GL Data Filtering UI (4 days)
-   ✅ B14: Random Sampling Algorithm API (3 days)
-   ✅ B15: Systematic Sampling Algorithm API (3 days)
-   ✅ B16: Monetary Unit Sampling (MUS) Algorithm API (5 days)
-   ✅ F9: Sampling Method Selection UI (4 days)
-   ✅ B17: Selected Samples Persistence & Retrieval API (3 days)
-   ✅ F11: Selected Samples Display UI (3 days)
-   ✅ B18: Sample Export API (4 days)
-   ✅ F12: Sample Export Trigger UI (2 days)
-   ✅ B19: Audit Trail Retrieval API (3 days)
-   ✅ F13: Audit Trail Viewing UI (3 days)
-   ✅ A8: Implement Data Encryption at Rest for GL Data (2 days)
-   ✅ A9: Setup Performance Testing Framework (3 days)

**Sprint Goal Complete When**: Auditors can select sampling methods, generate samples, view and export them. Managers can view the audit trail. Data encryption and performance testing framework are in place.

### Sprint 4 (Week 4) - ML Integration & Advanced Sampling
**Goal**: Integrate ML risk scoring, implement risk-stratified sampling, and conduct initial scalability tests.

-   ✅ M2: Initial Risk Scoring Model Development (6 days)
-   ✅ M3: Model Training & Evaluation Automation (5 days)
-   ✅ M4: Model Inference Service Deployment (4 days)
-   ✅ B20: ML Risk Scoring Integration API (3 days)
-   ✅ M5: Explainability Feature Generation (5 days)
-   ✅ B21: Risk-Stratified Sampling Logic API (4 days)
-   ✅ F14: Risk-Stratified Sampling Configuration UI (3 days)
-   ✅ F15: ML Explainability Display UI (3 days)
-   ✅ A10: Scalability Testing for Data Ingestion (3 days)

**Sprint Goal Complete When**: ML risk scoring is integrated, auditors can use risk-stratified sampling with explanations, and the system's scalability for data ingestion is validated.

---

## 🚨 High-Risk Items Requiring Attention

1.  **⚠️ Statistical Correctness of Sampling Algorithms** (Stories B11, B14, B15, B16, B21)
    -   Action: Involve domain experts (auditors) early and frequently in the design and testing of all sampling and sample size calculation logic. Conduct thorough peer reviews of the mathematical implementations.
    -   Blocker: Incorrect algorithms could lead to invalid audit conclusions, undermining the tool's core purpose and potentially exposing users to compliance risks.
2.  **⚠️ Performance with Large Datasets** (Stories A10, B4, B5, B7, B8, B13, B16, B17, B18, B19, M1)
    -   Action: Prioritize efficient database queries, indexing, and bulk operations. Implement asynchronous processing for heavy tasks (parsing, ML scoring). Conduct performance and scalability tests (A9, A10) early and often.
    -   Blocker: Slow processing of large GL files could lead to poor user experience, timeouts, and system instability, making the tool unusable for its target audience.
3.  **⚠️ ML Model Interpretability & Trust** (Stories M2, M5, F15)
    -   Action: Focus on generating clear, concise, and actionable explanations for ML risk scores. Involve auditors in reviewing and providing feedback on the explainability output.
    -   Blocker: If auditors don't understand or trust the ML model's risk prioritization, they will not adopt the feature, negating the value of the ML investment.
4.  **⚠️ Security of Authentication & Data** (Stories A5, A8, B1, B2)
    -   Action: Adhere strictly to security best practices for password hashing, JWT handling, RBAC, and data encryption. Conduct regular security reviews and penetration testing (future story).
    -   Blocker: Security vulnerabilities could lead to unauthorized access, data breaches, and severe reputational and compliance damage.

---

**✅ Backlog Ready**: Review estimates, adjust team calibration in config.yml if needed, then start Sprint 1!