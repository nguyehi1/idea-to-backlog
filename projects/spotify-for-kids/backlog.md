# Sprint Backlog

**Generated**: 2024-05-15
**Source**: user_stories.md
**Team Calibration**: 1 SP = 1 day (adjust in config.yml)
**Status**: 🟡 Ready for Sprint Planning

---

## 🏗️ Architecture & Non-Functional Stories

### Story AN1: Establish Core Cloud Infrastructure (VPC, Compute, Database)
#### Description:
As an engineer, I want to set up the foundational cloud infrastructure including VPC, compute resources (e.g., Kubernetes cluster or EC2 instances), and managed relational database (PostgreSQL) instances, so that we have a secure and scalable environment for deploying our services.
**Details**: Infrastructure requirements, tech stack choices, non-functional constraints (e.g., performance targets, security requirements, scalability needs)

#### Acceptance Criteria
- [ ] VPC created with public and private subnets across at least 2 Availability Zones.
- [ ] Network ACLs and Security Groups configured for secure inbound/outbound traffic, adhering to principle of least privilege.
- [ ] Managed PostgreSQL database instance provisioned (e.g., AWS RDS), configured for high availability (multi-AZ) and automated backups.
- [ ] Compute resources (e.g., AWS EKS cluster with managed node groups, or EC2 Auto Scaling Group) provisioned within private subnets.
- [ ] Basic CI/CD pipeline scaffolding established for infrastructure-as-code (IaC) (e.g., Terraform/CloudFormation).
- [ ] All infrastructure configurations managed via IaC and committed to version control.
- [ ] Initial IAM roles and policies defined for service accounts and engineer access.
- [ ] Connectivity validated between compute resources and the database.
- [ ] Core infrastructure setup documentation provided, including network topology and access procedures.

#### Effort Estimate: **6 SP**
**Complexity**: ⭐⭐⭐ Medium

**Breakdown**:
- DevOps: 100% (6 days)

**Reasoning**:
```
Day 1: Design network topology (VPC, subnets, route tables, internet/NAT gateways). Implement initial Terraform/CloudFormation for VPC and core networking.
Day 2: Provision managed PostgreSQL RDS instance (multi-AZ, backup config). Configure security groups for database access.
Day 3: Begin provisioning compute resources (e.g., EKS cluster with node groups, or ASG with EC2 instances). Initial IAM roles for compute.
Day 4: Complete compute provisioning. Configure basic networking for compute (internal load balancers/service discovery if applicable).
Day 5: Set up basic CI/CD pipeline for infrastructure changes. Validate connectivity between compute and database.
Day 6: Finalize security group rules and network ACLs. Document core infrastructure and access patterns. Perform initial smoke tests.
```

**Risk Factors**:
- ⚠️ **Cloud Provider Specific Issues**: Rate limits, resource availability, or unexpected service behavior could delay provisioning. *Mitigation: Use battle-tested IaC modules, anticipate delays, have fallback regions if critical.*
- ⚠️ **Kubernetes Complexity**: If EKS is chosen, the initial setup can be more complex than anticipated. *Mitigation: Leverage existing modules, dedicate experienced DevOps engineer, senior review.*

**Dependencies**: None

**Build Order**: #1

---

### Story AN2: Implement Parent Authentication & Authorization Framework
#### Description:
As an engineer, I want to establish a secure authentication service for parent users, supporting robust password hashing and enabling future MFA options, so that parental accounts are protected and access control can be enforced.
**Details**: Infrastructure requirements, tech stack choices, non-functional constraints (e.g., performance targets, security requirements, scalability needs)

#### Acceptance Criteria
- [ ] Authentication service (e.g., AWS Cognito, Auth0, or custom JWT service) integrated and deployed.
- [ ] User registration endpoint securely accepts parent credentials (email, password) and creates user accounts.
- [ ] Password hashing (e.g., bcrypt) implemented for all stored passwords, or handled by the managed service.
- [ ] User login endpoint verifies credentials and issues secure, short-lived authentication tokens (e.g., JWT).
- [ ] Token validation middleware/logic implemented and integrated into core backend services for protected API routes.
- [ ] Basic role-based authorization mechanism (`parent` role) defined and assignable.
- [ ] All API endpoints requiring parent authentication enforce token validation and authorization.
- [ ] The framework supports future integration of Multi-Factor Authentication (MFA), even if not enabled initially.
- [ ] API documentation (e.g., OpenAPI spec) for authentication endpoints and token usage provided.
- [ ] Unit and integration tests cover registration, login, token validation, and authorization failures.

#### Effort Estimate: **5 SP**
**Complexity**: ⭐⭐⭐ High

**Breakdown**:
- Backend: 70% (3.5 days)
- DevOps: 20% (1 day)
- Architecture: 10% (0.5 days)

**Reasoning**:
```
Day 1: Research and select appropriate authentication provider (e.g., AWS Cognito, Auth0). Design integration flow and token lifecycle.
Day 2: Configure the chosen authentication service (user pools, app clients, initial user schema).
Day 3: Develop backend endpoints for user registration and login, integrating with the auth service SDK. Implement password hashing where applicable (if not fully managed by provider).
Day 4: Develop and integrate middleware for token validation and basic role-based authorization into core backend services.
Day 5: Write unit and integration tests for authentication flows. Document API endpoints and authorization patterns.
```

**Risk Factors**:
- ⚠️ **Complex Configuration**: Managed auth services can have intricate configurations that are easy to misconfigure. *Mitigation: Leverage official documentation, senior DevOps/security review, start with minimal features.*
- ⚠️ **Security Vulnerabilities**: Improper token handling or password storage could lead to breaches. *Mitigation: Adhere to security best practices, conduct peer code reviews focused on security, plan for future security audits.*

**Dependencies**: AN1 (infrastructure for deployment)

**Build Order**: #2

---

### Story AN3: Set up Content Delivery Network (CDN) for Audio Streaming
#### Description:
As an engineer, I want to integrate a CDN service and configure it for optimized global audio content delivery, so that users experience low-latency streaming and downloads regardless of their location, supporting NFR3.3.
**Details**: Infrastructure requirements, tech stack choices, non-functional constraints (e.g., performance targets, security requirements, scalability needs)

#### Acceptance Criteria
- [ ] CDN service (e.g., AWS CloudFront, Cloudflare) provisioned and configured.
- [ ] Origin server (e.g., AWS S3 bucket for audio content) configured as the CDN source.
- [ ] CDN configured to serve audio content via HTTPS only.
- [ ] Origin access secured (e.g., CloudFront Origin Access Control/Identity for S3, signed URLs).
- [ ] Appropriate caching policies (e.g., cache-control headers) defined for audio files to optimize performance and freshness.
- [ ] CDN configured to support streaming protocols (if specific streaming formats are used, e.g., HLS/DASH manifest handling).
- [ ] Initial performance tests confirm reduced latency for content delivery from various geographic locations (e.g., basic ping/download tests).
- [ ] CDN cache invalidation strategy defined (e.g., automated invalidation on content update).
- [ ] Documentation for CDN setup, content upload process, and cache invalidation procedures.

#### Effort Estimate: **4 SP**
**Complexity**: ⭐⭐⭐ High

**Breakdown**:
- DevOps: 80% (3.2 days)
- Architecture: 20% (0.8 days)

**Reasoning**:
```
Day 1: Design CDN architecture, selecting provider (e.g., CloudFront). Set up S3 bucket for content storage. Configure bucket policies.
Day 2: Create CDN distribution, link to S3 origin. Configure caching behaviors, HTTPS, and WAF if applicable. Implement Origin Access Control/Identity.
Day 3: Configure signed URLs or similar access control for content (essential for B6/B11). Perform initial testing from different geographic regions to validate caching and latency.
Day 4: Document CDN setup, including content upload and cache invalidation procedures.
```

**Risk Factors**:
- ⚠️ **Incorrect Caching Policies**: Can lead to stale content being served or reduced performance. *Mitigation: Thorough testing, peer review of caching headers, start with conservative policies and optimize iteratively.*
- ⚠️ **Security Misconfiguration**: Incorrectly configured signed URLs or origin access could expose content. *Mitigation: Rigorous security review, use cloud provider's recommended secure patterns.*

**Dependencies**: AN1 (S3 bucket for storage, network access)

**Build Order**: #3

---

### Story AN4: Implement Centralized Logging and Monitoring for Backend Services
#### Description:
As an engineer, I want to set up centralized logging (e.g., ELK stack, CloudWatch Logs) and application performance monitoring (APM) tools for backend services, so that we can quickly identify and troubleshoot issues and monitor system health (NFR5.3, NFR5.1).
**Details**: Infrastructure requirements, tech stack choices, non-functional constraints (e.g., performance targets, security requirements, scalability needs)

#### Acceptance Criteria
- [ ] Centralized logging solution (e.g., AWS CloudWatch Logs, Loki, ELK stack) deployed and configured.
- [ ] All backend services configured to send structured logs (e.g., JSON format) to the centralized logging solution.
- [ ] Basic log parsing and indexing established for key log fields (e.g., timestamp, log level, service name, request ID).
- [ ] Application Performance Monitoring (APM) tool (e.g., Prometheus/Grafana, Datadog, AWS X-Ray) integrated with at least one core backend service.
- [ ] Key metrics (e.g., CPU, memory, network I/O, request latency, error rates, active connections) collected and visualized in dashboards.
- [ ] At least three critical alerting rules defined (e.g., high error rates, low available memory, high latency) and configured to trigger notifications (e.g., Slack, email).
- [ ] Runbooks or documentation provided for accessing logs, dashboards, and configuring new service monitoring.
- [ ] System health dashboard created and accessible.

#### Effort Estimate: **5 SP**
**Complexity**: ⭐⭐⭐ Medium

**Breakdown**:
- DevOps: 80% (4 days)
- Backend: 10% (0.5 days)
- Architecture: 10% (0.5 days)

**Reasoning**:
```
Day 1: Research logging solution (e.g., CloudWatch Logs, Loki). Set up log groups/streams. Configure a sample backend service to emit structured logs.
Day 2: Research APM/metrics solution (e.g., Prometheus/Grafana, Datadog). Deploy and configure the collector/agent.
Day 3: Instrument a sample backend service with the APM/metrics SDK. Verify metric collection and integration with the logging solution (e.g., trace IDs in logs).
Day 4: Create initial monitoring dashboards for key service metrics (latency, errors, resource usage). Define and test alert rules for critical thresholds, including notification setup.
Day 5: Document logging and monitoring access procedures, dashboard locations, and how to onboard new services.
```

**Risk Factors**:
- ⚠️ **Log Volume and Cost Management**: Uncontrolled log verbosity can lead to high costs and difficulty finding relevant information. *Mitigation: Implement log level control, structured logging, define retention policies, monitor costs closely.*
- ⚠️ **Alert Fatigue**: Poorly tuned alerts can lead to excessive notifications and ignored warnings. *Mitigation: Start with high-severity alerts, iterate and refine thresholds based on observed behavior, implement escalation policies.*

**Dependencies**: AN1 (infrastructure for deploying logging/monitoring agents or services), B1 (for initial backend service to integrate with monitoring, can be loosely coupled)

**Build Order**: #4

---

### Story AN5: Configure Database Schemas for User & Content Metadata
#### Description:
As an engineer, I want to define and implement the initial relational database schemas for parent accounts, child profiles, subscription information, and core content metadata (titles, descriptions, categories, age ratings), so that we have a structured way to store essential application data.
**Details**: Infrastructure requirements, tech stack choices, non-functional constraints (e.g., performance targets, security requirements, scalability needs)

#### Acceptance Criteria
- [ ] SQL DDL scripts created for the initial tables: `parents`, `children`, `content`, `categories`, `subscriptions`.
- [ ] Schemas include appropriate data types, primary keys, foreign keys, unique constraints, and indexes for performance.
- [ ] Referential integrity constraints enforced for relationships (e.g., `children` linked to `parents`).
- [ ] A schema migration tool (e.g., Flyway, Alembic) integrated into the development workflow.
- [ ] Initial schema successfully applied to development and staging databases using the migration tool.
- [ ] ERD (Entity-Relationship Diagram) or equivalent documentation of the database schema and relationships provided.
- [ ] All sensitive fields (e.g., parent email) are marked for encryption (covered by AN6).
- [ ] Review of schema by a senior engineer for design and scalability considerations.

#### Effort Estimate: **5 SP**
**Complexity**: ⭐⭐⭐ High

**Breakdown**:
- Backend: 70% (3.5 days)
- Architecture: 30% (1.5 days)

**Reasoning**:
```
Day 1: Design database schema (tables: `parents`, `children`, `content`, `subscriptions`, `categories`). Define columns, data types, and relationships. Create an initial ERD.
Day 2: Write DDL (Data Definition Language) scripts for creating the tables and indexes. Ensure proper data types and lengths, considering future scale.
Day 3: Set up a schema migration tool (e.g., Flyway). Integrate migration scripts into the development process. Apply initial schema to development environment.
Day 4: Review schema with team, validate foreign key constraints and indexing strategy. Conduct performance considerations for anticipated queries.
Day 5: Document the finalized schema, including the ERD and any specific considerations.
```

**Risk Factors**:
- ⚠️ **Incorrect Schema Design**: Can lead to data integrity issues, performance bottlenecks, or difficulty adapting to future requirements. *Mitigation: Thorough design review, use standard types, add indexes on common lookup/join columns, consider future growth during initial design.*
- ⚠️ **Migration Tool Issues**: Setup of migration tools can sometimes be tricky or lead to accidental data loss in dev. *Mitigation: Start with simple migrations, test extensively in dev, establish clear rollback procedures.*

**Dependencies**: AN1 (PostgreSQL database provisioned)

**Build Order**: #5

---

### Story AN6: Implement Data Encryption for PII at Rest and In Transit
#### Description:
As an engineer, I want to ensure all PII and payment data is encrypted at rest (AES-256) and in transit (TLS 1.2+) across all services and databases, so that we comply with NFR2.2 (Data Encryption) and privacy regulations like COPPA and GDPR.
**Details**: Infrastructure requirements, tech stack choices, non-functional constraints (e.g., performance targets, security requirements, scalability needs)

#### Acceptance Criteria
- [ ] All database instances (e.g., AWS RDS PostgreSQL) configured for encryption at rest using AES-256 (e.g., KMS managed keys).
- [ ] All S3 buckets (or equivalent object storage) storing PII, payment data, or sensitive content configured for encryption at rest (e.g., SSE-KMS/SSE-S3).
- [ ] All public-facing API endpoints (e.g., via API Gateway or Load Balancer) configured to enforce TLS 1.2+ for all client connections.
- [ ] All service-to-service communication (e.g., internal API calls, database connections) enforced with TLS 1.2 or higher.
- [ ] SSL/TLS certificates provisioned and managed (e.g., AWS ACM, Let's Encrypt) for all public endpoints.
- [ ] An automated process for certificate renewal (e.g., ACM auto-renewal, Certbot cronjob) is in place.
- [ ] Verification through security scans or manual checks confirms encryption at rest and in transit.
- [ ] Documentation of encryption mechanisms, key management strategies, and certificate management.

#### Effort Estimate: **4 SP**
**Complexity**: ⭐⭐⭐ High

**Breakdown**:
- DevOps: 60% (2.4 days)
- Architecture: 20% (0.8 days)
- Backend: 20% (0.8 days)

**Reasoning**:
```
Day 1: Configure database (e.g., RDS) encryption at rest using KMS. Configure S3 bucket encryption for all relevant buckets. Verify configuration.
Day 2: Provision SSL/TLS certificates (e.g., AWS ACM). Configure load balancers/API Gateway to enforce TLS 1.2+. Ensure internal service communication libraries/frameworks are configured to use TLS.
Day 3: Implement automated certificate renewal. Conduct a security audit/scan to verify encryption is enforced end-to-end for sample data paths involving PII.
Day 4: Document encryption mechanisms, key management practices, and certificate rotation procedures.
```

**Risk Factors**:
- ⚠️ **Misconfiguration**: Can lead to unencrypted data exposure or broken connections. *Mitigation: Leverage cloud provider managed encryption, rigorous peer review of configurations, follow security hardening guides.*
- ⚠️ **Certificate Expiry**: Failure to renew certificates can lead to service outages. *Mitigation: Implement automated renewal, set up monitoring and alerting for certificate expiry dates well in advance.*

**Dependencies**: AN1 (core infrastructure, S3, RDS), AN5 (database context)

**Build Order**: #6

---

### Story AN7: Establish Secure Offline Content Storage Mechanism for Mobile Apps
#### Description:
As an engineer, I want to design and implement a secure local storage mechanism for downloaded audio content on mobile devices, ensuring content protection and integrity for offline playback (NFR4.1).
**Details**: Infrastructure requirements, tech stack choices, non-functional constraints (e.g., performance targets, security requirements, scalability needs)

#### Acceptance Criteria
- [ ] A secure local storage mechanism (e.g., platform-specific encrypted file system APIs, app-level encryption) is selected and integrated into the mobile app skeleton (iOS and Android).
- [ ] Downloaded audio content is stored encrypted at rest on the device.
- [ ] Content integrity check (e.g., using checksums or hashes) implemented to verify downloaded files upon storage and before playback.
- [ ] Access to downloaded content is restricted solely to the application itself.
- [ ] Mechanism for securely deleting downloaded content from the device is implemented.
- [ ] A proof-of-concept demonstrates successful secure storage, retrieval, and deletion of a test audio file on both iOS and Android.
- [ ] Documentation of the chosen secure storage solution, implementation details, and usage guidelines for mobile developers.

#### Effort Estimate: **6 SP**
**Complexity**: ⭐⭐⭐ Medium

**Breakdown**:
- Frontend: 60% (3.6 days)
- Architecture: 40% (2.4 days)

**Reasoning**:
```
Day 1: Research native secure offline storage options for iOS (e.g., `NSFileProtection`, Keychain) and Android (e.g., `EncryptedFile`, device encryption capabilities). Design a common interface for the mobile applications to abstract platform specifics.
Day 2: Implement a secure file storage helper class/module for iOS, integrating with chosen platform APIs.
Day 3: Implement a secure file storage helper class/module for Android, integrating with chosen platform APIs.
Day 4: Develop a proof-of-concept (PoC) for securely downloading, storing, and retrieving a dummy audio file on both platforms. Integrate content integrity checks (e.g., MD5 hash verification on download).
Day 5: Implement secure deletion of content from the device.
Day 6: Document the chosen approach, including platform-specific considerations and usage patterns for other developers.
```

**Risk Factors**:
- ⚠️ **Platform Inconsistencies**: Native secure storage APIs can differ significantly, making cross-platform abstraction challenging. *Mitigation: Deep dive into platform security docs, conduct thorough PoC, accept platform-specific code where necessary.*
- ⚠️ **Over-Reliance on OS-level Encryption**: May not cover all scenarios (e.g., rooted devices) or provide sufficient app-level protection. *Mitigation: Implement defense-in-depth with app-level checks/encryption if deemed necessary, consider device integrity checks.*

**Dependencies**: None (precedes B11 and F13, but can run in parallel with other AN stories)

**Build Order**: #7

---

### Story AN8: Implement Subscription & Payment Gateway Integration Framework
#### Description:
As an engineer, I want to integrate with a chosen payment gateway provider (e.g., Stripe) to handle subscription creation, management, and recurring billing securely, so that parents can manage their subscriptions per FR3.7.
**Details**: Infrastructure requirements, tech stack choices, non-functional constraints (e.g., performance targets, security requirements, scalability needs)

#### Acceptance Criteria
- [ ] Payment gateway provider (e.g., Stripe, Braintree) account created and configured for test mode.
- [ ] Backend API integration with the chosen payment gateway for:
    - [ ] Customer creation.
    - [ ] Subscription creation (linking a customer to a product/plan).
    - [ ] Retrieving subscription status and details.
    - [ ] Handling webhook events (e.g., `invoice.payment_succeeded`, `customer.subscription.deleted`, `customer.source.updated`).
- [ ] Secure handling of payment method details implemented (e.g., using client-side tokenization, never processing raw card data on own servers to minimize PCI scope).
- [ ] Basic database schema additions for tracking subscription information (e.g., `subscription_id`, `plan_id`, `status`, `next_billing_date`) linked to parent accounts.
- [ ] A proof-of-concept demonstrates successful creation of a test customer and subscription.
- [ ] Webhook receiver endpoint implemented and configured, including signature verification for authenticity.
- [ ] Documentation provided for payment gateway API integration, webhook handling, and secure data flow.

#### Effort Estimate: **7 SP**
**Complexity**: ⭐⭐⭐ Medium

**Breakdown**:
- Backend: 70% (4.9 days)
- DevOps: 10% (0.7 days)
- Architecture: 20% (1.4 days)

**Reasoning**:
```
Day 1: Research payment gateway options (e.g., Stripe) and design the overall subscription flow. Set up developer account and get API keys.
Day 2: Implement backend API endpoints for customer creation and initial subscription creation, integrating with the payment gateway SDK. Focus on secure tokenization.
Day 3: Implement webhook endpoints to receive and process events from the payment gateway (e.g., `invoice.payment_succeeded`, `customer.subscription.deleted`). Implement signature verification for webhooks.
Day 4: Update database schema (AN5 extension) to store subscription details, linking to parent accounts.
Day 5: Write unit and integration tests for subscription creation, status retrieval, and webhook processing. Test with various success and failure scenarios (using test card numbers).
Day 6: Document payment gateway integration details, including webhook configuration and data flow.
Day 7: Address any security review feedback and finalize implementation.
```

**Risk Factors**:
- ⚠️ **PCI Compliance Overhead**: Mismanaging payment data can incur significant compliance burden. *Mitigation: Strictly adhere to client-side tokenization (e.g., Stripe Elements) and avoid handling sensitive card data directly.*
- ⚠️ **Webhook Reliability and Idempotency**: Webhook events can be delivered out of order or multiple times. *Mitigation: Implement idempotent processing logic for webhooks, utilize message queues for robust delivery, monitor webhook failures.*

**Dependencies**: AN2 (Parent Auth), AN6 (Data Encryption for PII), AN5 (DB schema for subscriptions)

**Build Order**: #8

---

### Story AN9: Plan for COPPA & GDPR Compliance (Privacy Policy, Consent Flow)
#### Description:
As a legal and product owner, I want to draft the privacy policy and outline the parental consent collection flow, ensuring full compliance with COPPA and GDPR requirements, so that our application adheres to critical child privacy regulations (NFR4.1, NFR4.2, NFR4.3).
**Details**: Infrastructure requirements, tech stack choices, non-functional constraints (e.g., performance targets, security requirements, scalability needs)

#### Acceptance Criteria
- [ ] A comprehensive draft of the Privacy Policy document is created, specifically addressing data collection, usage, storage, and sharing practices for children and parents, compliant with COPPA and GDPR.
- [ ] A detailed flow diagram outlining the parental consent collection process is defined, including verifiable parental consent mechanisms and managing consent for child data processing.
- [ ] All types of Personally Identifiable Information (PII) collected by the application are identified, along with a clear justification for its collection and its retention period.
- [ ] Data retention and deletion policies are explicitly defined for all collected data, particularly for child PII.
- [ ] A plan for handling data subject access requests (DSARs) and data portability requests (e.g., right to access, right to be forgotten) is outlined.
- [ ] The proposed privacy policy and consent flows are reviewed by internal legal counsel or external legal experts.
- [ ] A prioritized list of technical requirements (e.g., specific API endpoints, UI screens, data deletion jobs) is generated for subsequent stories based on the compliance plan.

#### Effort Estimate: **6 SP**
**Complexity**: ⭐⭐⭐ High

**Breakdown**:
- Architecture: 70% (4.2 days)
- Product: 30% (1.8 days)

**Reasoning**:
```
Day 1-1.5: Thorough research into COPPA, GDPR, and other relevant child privacy regulations applicable to the target markets. Identify specific requirements for parental consent and data handling.
Day 2-3: Draft the initial Privacy Policy, outlining data collection, use, and parental rights. Ensure it's clear, concise, and easy to understand for parents.
Day 4: Design the parental consent collection flow, including verifiable parental consent mechanisms (e.g., credit card verification, ID check, phone call) and managing consent for child profiles.
Day 5: Review drafted policy and consent flow with internal stakeholders (e.g., product, legal). Incorporate feedback. Outline data retention and DSAR procedures.
Day 6: Finalize the plan, generate a prioritized list of concrete technical requirements (e.g., specific API endpoints, UI screens, data deletion logic) for engineering implementation in future stories.
```

**Risk Factors**:
- ⚠️ **Misinterpretation of Regulations**: Legal and regulatory frameworks are complex and constantly evolving. *Mitigation: Engage legal counsel specializing in child privacy early and often, document assumptions, stay updated on regulatory changes.*
- ⚠️ **Difficulty in Implementing Verifiable Consent**: Verifiable parental consent (VPC) methods can be complex, costly, and impact user conversion. *Mitigation: Research various VPC methods, choose the most appropriate balance of compliance and user experience, start with a minimal viable VPC.*

**Dependencies**: AN6 (PII data encryption is a prerequisite for compliant handling)

**Build Order**: #9

---

## ⚙️ Backend Stories

### Story B1: Develop Parent Account API (Registration & Login)
#### Description:
As a parent, I want to register for an account and log in securely, so that I can access the platform and manage my family's profiles.
**Details**: APIs, data models, business logic

#### Acceptance Criteria
- [ ] `POST /api/v1/parents/register` endpoint accepts parent email, password, and optionally name.
- [ ] Successful registration creates a new parent record in the database and a user in the authentication service (AN2).
- [ ] `POST /api/v1/parents/login` endpoint accepts parent email and password.
- [ ] Successful login returns a valid, short-lived authentication token (JWT from AN2).
- [ ] Failed login attempts (invalid credentials, account locked) return appropriate, generic error messages (e.g., 401 Unauthorized, "Invalid credentials").
- [ ] Input validation implemented for all fields (e.g., email format, password strength requirements).
- [ ] Basic password reset flow initiated (e.g., sends a reset email, actual reset endpoint can be in a later story).
- [ ] API documentation (OpenAPI spec) for registration and login endpoints is updated.
- [ ] Unit and integration tests cover successful/failed registration, successful/failed login, and input validation.

#### Effort Estimate: **5 SP**
**Complexity**: ⭐⭐⭐ High

**Breakdown**:
- Backend: 100% (5 days)

**Reasoning**:
```
Day 1: Design `register` and `login` API endpoints. Implement basic controller logic and request/response DTOs.
Day 2: Integrate `register` endpoint with AN2's authentication service for user creation and AN5's database for storing additional parent metadata. Ensure secure password handling is leveraged from AN2.
Day 3: Integrate `login` endpoint with AN2's authentication service for credential verification and token generation. Add comprehensive input validation for email and password fields.
Day 4: Implement robust error handling for failed registrations/logins. Integrate a basic placeholder for "forgot password" (e.g., generating a token for a reset email).
Day 5: Write comprehensive unit and integration tests for both endpoints, covering happy paths, edge cases (e.g., existing email, invalid password), and security aspects. Update OpenAPI documentation.
```

**Risk Factors**:
- ⚠️ **Security Vulnerabilities**: Improper integration with the auth framework (AN2) could expose tokens or credentials. *Mitigation: Strictly follow AN2 guidelines, leverage SDKs, thorough security-focused peer reviews.*
- ⚠️ **Error Message Leakage**: Providing too much detail in error messages can aid attackers. *Mitigation: Ensure generic error messages are returned for security-sensitive failures.*

**Dependencies**: AN1 (infrastructure), AN2 (auth framework), AN5 (user schema)

**Build Order**: #10

---

### Story B2: Develop Child Profile Management API (CRUD)
#### Description:
As a parent, I want to create, view, update, and delete child profiles linked to my account, so that each child has their personalized settings and listening experience (FR3.1).
**Details**: APIs, data models, business logic

#### Acceptance Criteria
- [ ] `POST /api/v1/children` endpoint creates a child profile (requires parent authentication from AN2).
    - [ ] Child profile includes `name`, `avatar_id` (reference), and `date_of_birth` or `age_range`.
- [ ] `GET /api/v1/children` endpoint retrieves all child profiles associated with the authenticated parent.
- [ ] `GET /api/v1/children/{child_id}` endpoint retrieves a specific child profile, requiring parent authorization (parent owns child).
- [ ] `PUT /api/v1/children/{child_id}` endpoint updates a child profile, requiring parent authorization.
- [ ] `DELETE /api/v1/children/{child_id}` endpoint deletes a child profile, requiring parent authorization.
- [ ] All child profiles are securely linked to the parent's account in the database (AN5).
- [ ] Input validation implemented for all child profile fields (e.g., name length, valid age/date of birth).
- [ ] API documentation (OpenAPI spec) updated for all CRUD endpoints.
- [ ] Unit and integration tests cover all CRUD operations, including successful and failed attempts, and authorization checks.

#### Effort Estimate: **5 SP**
**Complexity**: ⭐⭐⭐ High

**Breakdown**:
- Backend: 100% (5 days)

**Reasoning**:
```
Day 1: Design CRUD API endpoints for child profiles. Implement basic controller logic and DTOs.
Day 2: Implement `create` and `retrieve all` logic, integrating with AN5's child profile schema. Ensure child profiles are linked to the authenticated parent's ID.
Day 3: Implement `retrieve by ID`, `update`, and `delete` logic. Crucially, implement robust authorization checks to ensure a parent can only manage their *own* children's profiles.
Day 4: Add comprehensive input validation for child profile fields (e.g., name length, age validity). Implement error handling for unauthorized access, not found, and validation errors.
Day 5: Write unit and integration tests for all CRUD operations, covering happy paths, edge cases (e.g., non-existent child), and authorization failures. Update OpenAPI documentation.
```

**Risk Factors**:
- ⚠️ **Insecure Authorization**: A bug could allow a parent to view or modify another parent's child profiles. *Mitigation: Implement strict authorization checks on every API call, thorough testing, peer review of security logic.*
- ⚠️ **Data Integrity on Delete**: Accidental deletion of child profiles or associated data. *Mitigation: Consider soft deletes for child profiles initially, implement confirmation steps on deletion.*

**Dependencies**: AN1 (infrastructure), AN5 (child profile schema), B1 (parent authentication)

**Build Order**: #11

---

### Story B3: Develop Content Ingestion API
#### Description:
As a content manager, I want to upload audio files and their associated metadata (title, description, age rating, categories) to the platform, so that the curated content library can be populated (FR1.1, FR1.2, FR1.3).
**Details**: APIs, data models, business logic

#### Acceptance Criteria
- [ ] `POST /api/v1/content` endpoint accepts audio file (multipart/form-data) and associated metadata (title, description, age rating, category IDs, duration, cover art URL/file).
- [ ] Uploaded audio files are securely stored in the designated S3 bucket (or similar object storage) from AN3.
- [ ] Content metadata (including a reference to the stored audio file) is stored in the database (AN5 schema).
- [ ] API endpoint requires specific internal authorization (e.g., an API key or specific content manager role, distinct from parent auth).
- [ ] Input validation implemented for all metadata fields (e.g., title length, valid age rating range, valid category IDs, supported file types/sizes for audio/cover art).
- [ ] Error handling for failed uploads (e.g., file too large, invalid type, missing metadata) is implemented.
- [ ] Basic content processing (e.g., file type validation, initial metadata extraction, triggering a simple transcoding job if desired for adaptive bitrate in B6) is initiated upon successful upload.
- [ ] API documentation (OpenAPI spec) for the content ingestion endpoint is updated.
- [ ] Unit and integration tests cover successful uploads, metadata storage, and various failure scenarios.

#### Effort Estimate: **6 SP**
**Complexity**: ⭐⭐⭐ Medium

**Breakdown**:
- Backend: 90% (5.4 days)
- DevOps: 10% (0.6 days)

**Reasoning**:
```
Day 1-1.5: Design `POST /api/v1/content` endpoint to accept multipart-form data (audio file, cover art) and JSON metadata. Implement controller logic.
Day 2: Integrate with S3 (or similar) SDK for secure audio file and cover art upload. Implement internal authentication/authorization for content managers.
Day 3: Store content metadata (title, description, age rating, category IDs, duration, S3 URLs for audio/cover art) in AN5's content schema.
Day 4: Implement comprehensive input validation for all metadata and file type/size constraints. Trigger a basic async process (e.g., add to a message queue for a future worker) for potential transcoding/DRM preparation.
Day 5: Implement robust error handling for various upload failures. Write unit and integration tests, including cases for large files, invalid types, and missing metadata.
Day 6: Update OpenAPI documentation.
```

**Risk Factors**:
- ⚠️ **Large File Upload Performance**: Direct file uploads can impact server performance or timeout. *Mitigation: Implement file size limits, consider pre-signed URLs for direct S3 upload from client if feasible in the future, use async processing.*
- ⚠️ **Content Processing Failures**: If transcoding or DRM fails, content may not be available for streaming. *Mitigation: Implement robust error handling, retry mechanisms for processing jobs, monitoring (AN4) for processing failures.*

**Dependencies**: AN1 (S3 bucket), AN5 (content schema), AN3 (CDN setup context for content delivery)

**Build Order**: #12

---

### Story B4: Develop Content Browsing & Search API (Categories, Age Filter)
#### Description:
As a child, I want to browse content by categories and search for specific items, and as a parent, I want content filtered by age, so that I can easily discover age-appropriate content (FR1.2, FR1.3, FR1.4).
**Details**: APIs, data models, business logic

#### Acceptance Criteria
- [ ] `GET /api/v1/content` endpoint returns a paginated list of content items.
- [ ] Supports filtering by `category_id` (e.g., `?category_id=123`).
- [ ] Supports full-text search on `title` and `description` fields (e.g., `?search=lion+king`).
- [ ] Supports filtering by `max_age_rating` (e.g., `?max_age=8`), which is applied based on the selected child's profile or a parental setting.
- [ ] `GET /api/v1/categories` endpoint returns a list of available content categories.
- [ ] Content listings are ordered by relevance for search queries and by a default (e.g., recently added, popularity) for browsing.
- [ ] Performance: Content listings return within 200ms for typical queries.
- [ ] API documentation (OpenAPI spec) updated for browsing and search endpoints.
- [ ] Unit and integration tests cover various filter and search combinations, pagination, and empty results.

#### Effort Estimate: **6 SP**
**Complexity**: ⭐⭐⭐ Medium

**Breakdown**:
- Backend: 100% (6 days)

**Reasoning**:
```
Day 1: Design `GET /api/v1/content` (for paginated listing, search, and filters) and `GET /api/v1/categories` endpoints. Implement basic controller logic and DTOs.
Day 2-3: Implement database queries for `GET /api/v1/content` to support category filtering and age filtering (based on `max_age_rating` parameter or from child's profile). Implement efficient pagination logic.
Day 4: Implement basic full-text search functionality (e.g., using `ILIKE` in PostgreSQL or similar) on content `title` and `description`. Ensure appropriate database indexes are in place to optimize queries.
Day 5: Implement default sorting for browsing. Write unit and integration tests covering various filter and search combinations, including edge cases like no results and invalid parameters.
Day 6: Perform basic performance testing to ensure queries are within acceptable limits. Update OpenAPI documentation.
```

**Risk Factors**:
- ⚠️ **Poor Search Performance**: Basic SQL `LIKE` can be inefficient for large datasets. *Mitigation: Ensure proper database indexing on search fields, consider dedicated search solutions (e.g., Elasticsearch) for future scale (future story).*
- ⚠️ **Inaccurate Filtering Logic**: Incorrect application of age filters or category filters can lead to unsuitable content being shown. *Mitigation: Thorough unit and integration testing of all filtering logic, especially age-based rules.*

**Dependencies**: B3 (Content Ingestion, for data), AN5 (content schema)

**Build Order**: #13

---

### Story B5: Develop Parental Control API (Age Filtering)
#### Description:
As a parent, I want to set and update the maximum age-appropriateness filter for each child's profile, so that I can control the content visible to my child (FR3.2).
**Details**: APIs, data models, business logic

#### Acceptance Criteria
- [ ] `PUT /api/v1/children/{child_id}/age-filter` endpoint sets/updates the `max_age_rating` for a specific child profile.
- [ ] Endpoint requires parent authentication (AN2) and authorization (parent owns child, via B2).
- [ ] Input validation ensures `max_age_rating` is a valid, sensible age (e.g., 0-18).
- [ ] The `max_age_rating` is securely stored in the child's profile in the database (AN5 schema extension).
- [ ] The `max_age_rating` is correctly applied by the content browsing API (B4) when retrieving content for that child.
- [ ] API documentation (OpenAPI spec) updated.
- [ ] Unit and integration tests cover setting the age filter, handling invalid input, and verifying its application through the B4 API.

#### Effort Estimate: **3 SP**
**Complexity**: ⭐⭐⭐ High

**Breakdown**:
- Backend: 100% (3 days)

**Reasoning**:
```
Day 1: Design `PUT /api/v1/children/{child_id}/age-filter` endpoint. Implement controller logic to validate input (valid age range) and delegate to B2's update service for persistence.
Day 2: Implement authorization checks (parent owns child) and ensure parent authentication. Verify that the backend's content browsing logic (from B4) correctly applies this `max_age_rating` from the child's profile when retrieving content.
Day 3: Write comprehensive unit and integration tests to verify setting the filter, invalid input handling, and its effect on content retrieval via B4. Update OpenAPI documentation.
```

**Risk Factors**:
- ⚠️ **Filter Not Applied**: The `max_age_rating` might not be correctly applied by B4, leading to inappropriate content being displayed. *Mitigation: Thorough integration testing with B4, ensure the filter is consistently applied at the data retrieval layer, and conduct peer review of the filtering logic.*
- ⚠️ **Data Integrity**: Invalid age values being stored or issues with linking to the child profile. *Mitigation: Strict input validation, leverage B2's existing child profile management logic.*

**Dependencies**: B2 (child profiles), B4 (to verify filter application), AN5 (child profile schema updates for age filter)

**Build Order**: #14

---

### Story B6: Develop Audio Streaming API (Adaptive Bitrate, DRM)
#### Description:
As a child, I want to stream audio content seamlessly with low latency, so that I can enjoy my music and stories without interruption (FR4.1, NFR1.1).
**Details**: APIs, data models, business logic

#### Acceptance Criteria
- [ ] `GET /api/v1/content/{content_id}/stream` endpoint provides a secure, time-limited URL (e.g., CDN-signed URL) for streaming audio.
- [ ] Streamed audio content is delivered via the configured CDN (AN3) to ensure low latency.
- [ ] The API endpoint requires child authentication (token obtained after child profile selection).
- [ ] Access to content is restricted based on:
    - [ ] Active subscription status (if content is premium).
    - [ ] Parental controls: child's age filter (from B5) and blocked content/categories (from B8).
- [ ] Basic support for adaptive bitrate streaming considered in design, if multiple audio qualities are available (e.g., serving different HLS manifests). For MVP, a single bitrate is acceptable but the mechanism should allow for future ABR.
- [ ] Digital Rights Management (DRM) solution integrated to protect premium content (for MVP, CDN signed URLs serve as basic content protection).
- [ ] Performance: Audio stream starts within 1 second for typical network conditions.
- [ ] API documentation (OpenAPI spec) updated.
- [ ] Unit and integration tests cover stream URL generation, access control logic, and performance under typical load.

#### Effort Estimate: **7 SP**
**Complexity**: ⭐⭐⭐ High

**Breakdown**:
- Backend: 80% (5.6 days)
- Architecture: 20% (1.4 days)

**Reasoning**:
```
Day 1: Design `GET /api/v1/content/{content_id}/stream` endpoint. Implement controller logic to handle content requests.
Day 2: Integrate with AN3 (CDN) to generate secure, time-limited signed URLs for the audio content stored in S3/CDN.
Day 3-4: Implement robust authorization logic: verify child's active session token, check subscription status (if applicable), and apply parental controls (age filter from B5, content blocking from B8). This is critical logic.
Day 5: Design for adaptive bitrate streaming: ensure the API can serve appropriate URLs for different bitrates or HLS/DASH manifests, assuming they are available (content ingestion, B3).
Day 6: Write unit and integration tests for stream URL generation, comprehensive access control, and various edge cases (e.g., blocked content, expired subscription, invalid child token). Perform basic performance checks for stream start time.
Day 7: Update OpenAPI documentation.
```

**Risk Factors**:
- ⚠️ **Complex DRM Integration**: True DRM solutions (e.g., Widevine, FairPlay) are highly complex and can significantly increase effort. *Mitigation: For MVP, rely on CDN signed URLs as basic protection. Defer full DRM implementation to a future story.*
- ⚠️ **Authorization Bypass**: Errors in access control logic could allow unauthorized content streaming. *Mitigation: Rigorous security-focused testing, peer code reviews, utilize a robust authorization framework.*
- ⚠️ **CDN Performance Issues**: CDN misconfiguration or origin latency could impact streaming performance. *Mitigation: Closely monitor CDN metrics (AN4), optimize origin response times, ensure proper CDN caching.*

**Dependencies**: B3 (content available), AN3 (CDN setup), AN2 (Auth framework for child token validation), B5 (Age filtering), B8 (Content Blocking - for authorization)

**Build Order**: #15

---

### Story B7: Implement PIN Protection for Parental Dashboard Access
#### Description:
As a parent, I want to set a 4-digit PIN for accessing the parental dashboard and settings changes, so that my child cannot tamper with the controls (FR3.6, NFR2.1).
**Details**: APIs, data models, business logic

#### Acceptance Criteria
- [ ] `POST /api/v1/parents/pin/set` endpoint sets/updates a 4-digit PIN for the authenticated parent.
- [ ] The PIN is securely hashed (e.g., bcrypt) and stored in the database, never in plain text.
- [ ] `POST /api/v1/parents/pin/verify` endpoint verifies the entered PIN against the stored hash.
- [ ] A successful PIN verification issues a short-lived "parental dashboard access" token or flags the parent's active session for a limited duration.
- [ ] All subsequent parental dashboard API endpoints (e.g., for B2, B5, B8, B10, B14) require this additional "PIN verified" flag/token in addition to parent authentication.
- [ ] Input validation for PIN ensures it is exactly 4 digits.
- [ ] Rate limiting implemented for PIN verification attempts to prevent brute-force attacks (e.g., 5 attempts in 5 minutes).
- [ ] API documentation (OpenAPI spec) updated.
- [ ] Unit and integration tests cover setting, verifying, failed PIN attempts, and rate limiting functionality.

#### Effort Estimate: **5 SP**
**Complexity**: ⭐⭐⭐ High

**Breakdown**:
- Backend: 100% (5 days)

**Reasoning**:
```
Day 1: Design `POST /api/v1/parents/pin/set` and `POST /api/v1/parents/pin/verify` endpoints. Implement controller logic.
Day 2: Implement PIN hashing (e.g., bcrypt) and secure storage in the parent's database record (AN5 extension). Implement PIN verification logic.
Day 3: Upon successful PIN verification, issue a temporary, short-lived authorization token or flag the current session to grant access to parental control APIs. Implement input validation for the 4-digit PIN.
Day 4: Implement rate limiting on PIN verification attempts to prevent brute-force attacks. Write unit and integration tests for setting, verifying, and failed attempts, including rate limit checks.
Day 5: Update OpenAPI documentation.
```

**Risk Factors**:
- ⚠️ **Weak PIN Hashing**: Using insecure hashing algorithms could make PINs susceptible to brute-force attacks. *Mitigation: Use strong, industry-standard hashing functions (e.g., bcrypt, Argon2) with appropriate work factors.*
- ⚠️ **Insufficient Rate Limiting**: Can allow brute-force attacks on PINs. *Mitigation: Implement aggressive, multi-layered rate limiting (IP-based, user-based), consider account lockout after too many failures.*
- ⚠️ **Insecure Token Handling**: The "PIN verified" token could be exposed or reused. *Mitigation: Ensure tokens are short-lived, HTTP-only, and follow secure token management practices.*

**Dependencies**: B1 (Parent Login), AN5 (parent schema update for PIN)

**Build Order**: #16

---

### Story B8: Develop Parental Control API (Content Blocking)
#### Description:
As a parent, I want to explicitly block specific songs, audiobooks, or entire categories from a child's profile, so that I can further customize their content access (FR3.3).
**Details**: APIs, data models, business logic

#### Acceptance Criteria
- [ ] `POST /api/v1/children/{child_id}/blocked-content` endpoint to block a specific `content_id` or `category_id` for a child.
- [ ] `DELETE /api/v1/children/{child_id}/blocked-content/{id}` endpoint to unblock a previously blocked item.
- [ ] `GET /api/v1/children/{child_id}/blocked-content` endpoint to retrieve a list of currently blocked content and categories for a child.
- [ ] All endpoints require parent authentication (AN2) and successful PIN verification (B7) to access.
- [ ] Blocked content/categories are stored in the database, securely linked to the specific child profile (AN5 schema extension).
- [ ] The content browsing (B4) and streaming (B6) APIs explicitly filter out blocked content/categories for the associated child.
- [ ] Error handling implemented for blocking non-existent content/categories or unauthorized attempts.
- [ ] API documentation (OpenAPI spec) updated.
- [ ] Unit and integration tests cover blocking/unblocking content and categories, and verifying that B4 and B6 correctly filter blocked items.

#### Effort Estimate: **5 SP**
**Complexity**: ⭐⭐⭐ Medium

**Breakdown**:
- Backend: 100% (5 days)

**Reasoning**:
```
Day 1: Design CRUD API endpoints for blocking content/categories. Implement controller logic and DTOs.
Day 2: Create a new database table (e.g., `child_blocked_content`) to store blocked `content_id`s or `category_id`s, securely linked to `child_id` (AN5 extension).
Day 3: Implement blocking/unblocking logic, ensuring parent authentication and B7's PIN verification are applied. Add input validation (e.g., valid content/category IDs).
Day 4: Modify the content browsing API (B4) and streaming API (B6) to include this new filtering layer, ensuring blocked content is *never* shown or streamed for the associated child. Write unit and integration tests for all CRUD operations and filter verification.
Day 5: Update OpenAPI documentation.
```

**Risk Factors**:
- ⚠️ **Blocked Content Leakage**: A bug in the filtering logic (B4, B6) could accidentally expose blocked content. *Mitigation: Rigorous integration testing with B4/B6, dedicated test cases for blocked items, security-focused peer review.*
- ⚠️ **Performance Impact**: Additional filtering logic could impact content retrieval performance. *Mitigation: Ensure proper database indexing on the `child_blocked_content` table, optimize query joins.*

**Dependencies**: B2 (child profiles), B4 (content identification), B5 (age filtering context), B7 (PIN protection), AN5 (new schema for blocked items)

**Build Order**: #17

---

### Story B9: Develop Listening History Tracking API
#### Description:
As a child, I want my listening history to be recorded, and as a parent, I want to view my child's listening activity, so that recommendations can be generated and parents can monitor usage (FR3.4, FR1.5).
**Details**: APIs, data models, business logic

#### Acceptance Criteria
- [ ] `POST /api/v1/children/{child_id}/listening-history` endpoint accepts `content_id`, `start_time`, `end_time` (or `duration`), and `completion_status` (e.g., partial, complete).
- [ ] The endpoint requires child authentication (via token from child profile selection).
- [ ] Listening events are stored persistently in a scalable data store (e.g., PostgreSQL table, or an event store like Kafka/Kinesis if high volume).
- [ ] `GET /api/v1/children/{child_id}/listening-history` endpoint retrieves a paginated list of listening history for an authenticated parent.
- [ ] Access to retrieve listening history requires parent authentication (AN2) and successful PIN verification (B7).
- [ ] PII handling for listening history (e.g., child ID) aligns with AN6 (encryption) and AN9 (privacy policy).
- [ ] API documentation (OpenAPI spec) updated.
- [ ] Unit and integration tests cover recording history events, retrieving history, and authorization checks.

#### Effort Estimate: **6 SP**
**Complexity**: ⭐⭐⭐ Medium

**Breakdown**:
- Backend: 90% (5.4 days)
- Architecture: 10% (0.6 days)

**Reasoning**:
```
Day 1: Design `POST /api/v1/children/{child_id}/listening-history` (for event recording) and `GET /api/v1/children/{child_id}/listening-history` (for parent view). Implement controllers.
Day 2-3: Implement event ingestion logic. Store listening events (content ID, start/end time, duration, completion status, child ID) in a suitable, performant data store (e.g., a dedicated PostgreSQL table with appropriate indexing, or evaluate a specialized event store for future scale).
Day 4: Implement authorization for both endpoints: child token for posting events, parent auth + B7 PIN for retrieving history.
Day 5: Develop logic for retrieving and paginating listening history for parents. Ensure efficient querying and filtering (e.g., by date).
Day 6: Write unit and integration tests for recording events and retrieving history, covering authorization and pagination. Address potential high volume with performance considerations. Update OpenAPI documentation.
```

**Risk Factors**:
- ⚠️ **High Write Volume**: Listening events can generate significant write volume, potentially impacting database performance if not scaled correctly. *Mitigation: Optimize database writes, consider eventual consistency for high volume, implement batching or event streaming solutions (e.g., Kafka/Kinesis) for future scale.*
- ⚠️ **Privacy Concerns**: Listening history is sensitive PII. *Mitigation: Ensure AN9 privacy guidelines are strictly followed, enforce AN6 encryption, implement robust access controls (B7).*

**Dependencies**: B6 (Audio Streaming, to trigger events), AN5 (listening history schema, possibly NoSQL for scale), B7 (Parental PIN for viewing history)

**Build Order**: #18

---

### Story B10: Develop Parental Control API (Time Limits)
#### Description:
As a parent, I want to set daily listening time limits for each child's profile, so that I can manage their screen time (FR3.5).
**Details**: APIs, data models, business logic

#### Acceptance Criteria
- [ ] `PUT /api/v1/children/{child_id}/time-limit` endpoint sets/updates a daily `listening_time_limit_minutes` for a specific child.
- [ ] Endpoint requires parent authentication (AN2) and successful PIN verification (B7).
- [ ] The time limit is stored in the child's profile in the database (AN5 schema extension).
- [ ] `GET /api/v1/children/{child_id}/remaining-time` endpoint allows a child's device to query their remaining daily listening time.
- [ ] Backend logic to enforce the time limit:
    - [ ] Stop streaming or return "limit reached" error from B6's stream API if the child attempts to play content beyond their limit.
    - [ ] Accurately calculates listening time based on B9's listening history data.
- [ ] A reliable, automated backend process (e.g., scheduled cron job, serverless function) resets daily listening time counters (e.g., at midnight UTC).
- [ ] Input validation for `listening_time_limit_minutes` ensures it's a positive integer.
- [ ] API documentation (OpenAPI spec) updated.
- [ ] Unit and integration tests cover setting limits, querying remaining time, limit enforcement, and daily reset.

#### Effort Estimate: **7 SP**
**Complexity**: ⭐⭐⭐ High

**Breakdown**:
- Backend: 100% (7 days)

**Reasoning**:
```
Day 1: Design `PUT /api/v1/children/{child_id}/time-limit` (set/update) and `GET /api/v1/children/{child_id}/remaining-time` (query) endpoints. Implement controllers.
Day 2: Implement logic to store the daily time limit in the child's profile (AN5 schema extension). Apply parent authentication and B7 PIN verification to `PUT` endpoint.
Day 3: Implement backend logic to calculate a child's *actual* listened time for the current day, based on their listening history from B9. Calculate and return remaining time via `GET` endpoint.
Day 4: Integrate with B6's audio streaming API to enforce the time limit. If a child exceeds their limit, the streaming API should return an appropriate "time limit reached" error, preventing playback.
Day 5: Implement a reliable daily scheduled job (e.g., cron job, AWS Lambda triggered by CloudWatch Events) to reset daily listening time counters (or refresh calculation) at a specified time (e.g., midnight UTC).
Day 6: Write unit and integration tests for setting limits, checking remaining time, and verifying enforcement scenarios (e.g., attempts to stream after limit reached). Test the daily reset mechanism.
Day 7: Update OpenAPI documentation.
```

**Risk Factors**:
- ⚠️ **Inaccurate Time Tracking/Enforcement**: Bugs in listening time calculation or enforcement logic could allow children to exceed limits. *Mitigation: Thorough testing of time calculation and enforcement, use UTC for all backend time calculations, robust scheduled job for daily reset with retry logic.*
- ⚠️ **Timezone Complications**: Different user timezones can complicate "daily" limits. *Mitigation: Standardize on UTC for all backend calculations and convert to local time only for display on the frontend.*

**Dependencies**: B2 (child profiles), B9 (tracking listening duration), B7 (PIN protection), B6 (for enforcement), AN5 (schema update for time limit)

**Build Order**: #19

---

### Story B11: Develop Offline Download Management API
#### Description:
As a child, I want to download content for offline listening, so that I can enjoy content without an internet connection (FR4.2).
**Details**: APIs, data models, business logic

#### Acceptance Criteria
- [ ] `GET /api/v1/content/{content_id}/download` endpoint returns a secure, time-limited URL for downloading the audio file directly from the CDN (AN3).
- [ ] The endpoint requires child authentication (via token from child profile selection).
- [ ] Access to content for download is restricted based on:
    - [ ] Active subscription status (if content is premium).
    - [ ] Parental controls: child's age filter (from B5) and blocked content/categories (from B8).
- [ ] Backend service tracks download attempts for analytics and to potentially limit concurrent downloads per child/device.
- [ ] Content provided by this API is compatible with AN7's secure offline storage mechanism.
- [ ] API documentation (OpenAPI spec) updated.
- [ ] Unit and integration tests cover download URL generation, access control logic, and download tracking.

#### Effort Estimate: **6 SP**
**Complexity**: ⭐⭐⭐ Medium

**Breakdown**:
- Backend: 100% (6 days)

**Reasoning**:
```
Day 1: Design `GET /api/v1/content/{content_id}/download` endpoint. Implement controller logic.
Day 2-3: Integrate with AN3 (CDN) to generate secure, time-limited signed URLs for direct audio file download. This reuses much of the logic from B6.
Day 4: Implement robust authorization logic: verify child's active session token, check subscription status (if applicable), and apply parental controls (age filter from B5, content blocking from B8).
Day 5: Implement basic tracking of download requests (e.g., log to B9's system or a dedicated table) for analytics and potential future features like concurrent download limits.
Day 6: Write unit and integration tests for download URL generation and comprehensive access control. Update OpenAPI documentation.
```

**Risk Factors**:
- ⚠️ **Unauthorized Downloads**: Flaws in access control could allow unauthorized users to download content. *Mitigation: Implement strong token validation and parental control checks, use very short-lived signed URLs.*
- ⚠️ **Broken Downloads**: Large file downloads can be interrupted. *Mitigation: Ensure CDN supports range requests, provide client-side guidance on handling incomplete downloads.*

**Dependencies**: B6 (content context), AN7 (secure local storage strategy to ensure compatibility), AN3 (CDN for downloads), AN2 (Auth)

**Build Order**: #20

---

### Story B12: Develop Playlist Creation & Management API (Child & Curated)
#### Description:
As a child, I want to create and save custom playlists, and I want to access pre-curated playlists, so that I can organize my favorite content and discover new themes (FR4.3, FR4.4).
**Details**: APIs, data models, business logic

#### Acceptance Criteria
- [ ] `POST /api/v1/children/{child_id}/playlists` endpoint creates a new child-managed playlist (requires child authentication).
    - [ ] Playlist includes `name` and can optionally be initialized with `content_id`s.
- [ ] `GET /api/v1/children/{child_id}/playlists` retrieves all child-managed playlists for the authenticated child.
- [ ] `PUT /api/v1/playlists/{playlist_id}/content` adds/removes `content_id`s to/from a specific playlist (child authorization for their own playlist).
- [ ] `DELETE /api/v1/playlists/{playlist_id}` deletes a child's playlist (child authorization).
- [ ] `GET /api/v1/playlists/curated` endpoint retrieves a list of pre-curated playlists.
    - [ ] Curated playlists are also filtered by child's age (B5) and blocked content (B8).
- [ ] Playlist data (title, description, content IDs) stored in the database (AN5 schema extension).
- [ ] Authorization checks ensure a child only manages their own playlists.
- [ ] Input validation for playlist names and content IDs.
- [ ] API documentation (OpenAPI spec) updated.
- [ ] Unit and integration tests for playlist CRUD operations, content management within playlists, and curated playlist retrieval.

#### Effort Estimate: **5 SP**
**Complexity**: ⭐⭐⭐ Medium

**Breakdown**:
- Backend: 100% (5 days)

**Reasoning**:
```
Day 1-1.5: Design CRUD API endpoints for child-managed playlists and `GET /api/v1/playlists/curated`. Implement controller logic and DTOs.
Day 2: Create database schema for playlists (e.g., `playlists` table, `playlist_content` join table, AN5 extension). Implement DB operations for creating, adding/removing content, and deleting playlists.
Day 3: Implement authorization: child token for managing their own playlists. Implement logic for retrieving curated playlists (potentially configured via an admin interface or static data), applying B5 and B8 filters.
Day 4: Implement input validation for playlist names and content IDs. Write unit and integration tests for all playlist operations and content management within playlists.
Day 5: Update OpenAPI documentation.
```

**Risk Factors**:
- ⚠️ **Data Inconsistency**: If content is deleted (via B3) but still referenced in a playlist, it could lead to broken experiences. *Mitigation: Implement cascading deletes or a cleanup process for content references when content is removed. (Can be future story)*
- ⚠️ **Performance for Large Playlists**: Managing hundreds of items in a playlist could be slow. *Mitigation: Optimize database queries, consider pagination for very long playlists (unlikely for MVP).*

**Dependencies**: B4 (content discovery for adding to playlists), B2 (child profile for saving playlists), AN5 (schema extension), B5 (age filtering), B8 (content blocking)

**Build Order**: #21

---

### Story B13: Develop Sleep Timer API
#### Description:
As a child, I want to set a sleep timer for audio playback, so that content stops playing automatically after a set duration or track completion (FR4.5).
**Details**: APIs, data models, business logic

#### Acceptance Criteria
- [ ] `POST /api/v1/children/{child_id}/sleep-timer` endpoint sets/updates a sleep timer for a specific duration (`duration_minutes`) or `tracks_remaining`.
- [ ] The endpoint requires child authentication (via token from child profile selection).
- [ ] Timer settings are stored temporarily (e.g., in a cache or session) for the child's active listening session.
- [ ] Backend logic to notify the client (e.g., via a simple polling mechanism, or a future websocket if implemented) when the timer expires.
- [ ] Backend logic to optionally stop streaming after timer (via B6 integration if client fails to stop).
- [ ] `DELETE /api/v1/children/{child_id}/sleep-timer` endpoint cancels an active timer.
- [ ] Input validation for timer duration/tracks (e.g., positive integers, reasonable limits).
- [ ] API documentation (OpenAPI spec) updated.
- [ ] Unit and integration tests cover setting, querying, and canceling timers.

#### Effort Estimate: **4 SP**
**Complexity**: ⭐⭐⭐ Medium

**Breakdown**:
- Backend: 100% (4 days)

**Reasoning**:
```
Day 1-1.5: Design `POST /api/v1/children/{child_id}/sleep-timer` (set/update) and `DELETE /api/v1/children/{child_id}/sleep-timer` (cancel). Implement controller logic.
Day 2: Implement logic to store the sleep timer settings (duration or tracks) for the child's active session, likely in a fast cache (e.g., Redis) rather than the database for ephemeral state.
Day 3: Design a mechanism for the backend to notify the client when the timer expires (e.g., a simple API poll from client, or push notification if websockets are available). Implement authorization for the child.
Day 4: Implement input validation. Write unit and integration tests for setting, querying, and canceling timers. Update OpenAPI documentation.
```

**Risk Factors**:
- ⚠️ **Client-Server Synchronization Issues**: Inconsistent timer state if client and server drift, leading to inaccurate stopping. *Mitigation: Client-side should be primary driver of stopping, with backend as a secondary source of truth/validation. Thorough testing of various scenarios.*
- ⚠️ **Inaccurate Timer Tracking**: Logic for tracking time or tracks could be buggy. *Mitigation: Careful implementation of countdown logic, use server-side timestamps for verification.*

**Dependencies**: B6 (Audio Playback), AN2 (Auth)

**Build Order**: #22

---

### Story B14: Develop Subscription Management API (Parent Facing)
#### Description:
As a parent, I want to view my subscription status, payment methods, and renewal settings, so that I can manage my paid access to the platform (FR3.7).
**Details**: APIs, data models, business logic

#### Acceptance Criteria
- [ ] `GET /api/v1/parents/subscription` endpoint returns the authenticated parent's current subscription status (e.g., active, past_due, canceled), plan details, and next billing date.
- [ ] `GET /api/v1/parents/payment-methods` endpoint returns masked payment method details (e.g., last 4 digits of card, card type).
- [ ] `POST /api/v1/parents/subscription/cancel` endpoint initiates subscription cancellation with the payment gateway (based on gateway's cancellation logic).
- [ ] `PUT /api/v1/parents/payment-method` endpoint updates payment methods.
    - [ ] This must be done securely via client-side tokenization (AN8) and using the payment gateway's API, not by processing raw card data on own servers.
- [ ] All endpoints require parent authentication (AN2).
- [ ] Data retrieved directly from the payment gateway (AN8) or from the synchronized internal database.
- [ ] Error handling for payment gateway communication failures implemented.
- [ ] API documentation (OpenAPI spec) updated.
- [ ] Unit and integration tests cover all subscription management actions, including successful and failed scenarios.

#### Effort Estimate: **5 SP**
**Complexity**: ⭐⭐⭐ High

**Breakdown**:
- Backend: 100% (5 days)

**Reasoning**:
```
Day 1: Design API endpoints for retrieving subscription status, payment methods, cancelling subscription, and updating payment method. Implement controllers.
Day 2: Implement `GET` endpoints by querying the payment gateway (AN8) using its SDK. Retrieve relevant subscription details (status, plan, billing date) and masked payment method information.
Day 3: Implement `cancel` endpoint by calling the payment gateway's cancellation API. Implement `update payment method` endpoint, ensuring secure client-side tokenization is used and only the token is sent to the backend to update the gateway.
Day 4: Implement robust authorization (parent only) and error handling for payment gateway communication failures. Write unit and integration tests for all endpoints.
Day 5: Update OpenAPI documentation.
```

**Risk Factors**:
- ⚠️ **Inaccurate Subscription Status**: If payment gateway webhooks (AN8) fail to process correctly, internal subscription status might not match the gateway. *Mitigation: Implement robust webhook handling, allow for manual reconciliation, provide a "sync status" option for parents.*
- ⚠️ **Security of Payment Method Updates**: Incorrect implementation can expose payment data or fail PCI compliance. *Mitigation: Strictly follow payment gateway's secure client-side integration guidelines for tokenization, conduct security review.*

**Dependencies**: AN8 (Payment Gateway Integration), B1 (Parent Authentication)

**Build Order**: #23

---

## 💻 Frontend Stories

### Story F1: Web App - Project Setup & Core Layout
#### Description:
As an engineer, I want to set up the foundational web application project with a modern framework (e.g., React), including routing and a basic responsive layout, so that subsequent UI development can proceed efficiently.
**Details**: UI/UX considerations, components needed, interactions

#### Acceptance Criteria
- [ ] React (or chosen framework, e.g., Vue, Angular) project initialized with a standard build tool (e.g., Vite, Webpack).
- [ ] Client-side routing configured (e.g., React Router DOM) for at least `/login`, `/register`, and `/home` routes.
- [ ] A basic responsive layout implemented, including a header, footer, and main content area.
- [ ] A CSS framework or design system (e.g., TailwindCSS, Material-UI, Chakra UI) integrated.
- [ ] Version control initialized (e.g., Git repository).
- [ ] Basic CI/CD pipeline scaffolding configured for automated deployments to a staging environment (e.g., Vercel, Netlify, S3/CloudFront integration).
- [ ] A "hello world" or placeholder page successfully rendered and accessible.
- [ ] Documentation for project structure, build process, dependency management, and local development instructions.

#### Effort Estimate: **4 SP**
**Complexity**: ⭐⭐⭐ High

**Breakdown**:
- Frontend: 90% (3.6 days)
- DevOps: 10% (0.4 days)

**Reasoning**:
```
Day 1: Initialize new React project (e.g., using Vite, Create React App). Configure basic folder structure, ESLint, Prettier.
Day 2: Set up react-router-dom for client-side routing. Implement a basic responsive layout with a placeholder header and footer.
Day 3: Integrate a CSS framework (e.g., Tailwind CSS or Material-UI). Create a "Hello World" component and ensure it renders correctly on different screen sizes. Set up basic CI/CD (e.g., Netlify/Vercel or S3/CloudFront) for automated deployments on push.
Day 4: Document project setup, dependencies, how to run locally, and deployment process.
```

**Risk Factors**:
- ⚠️ **Tooling Conflicts/Dependency Hell**: Issues with package manager or build tool compatibility. *Mitigation: Stick to widely adopted, stable toolchains. Start with minimal dependencies.*
- ⚠️ **Responsive Design Complexity**: Achieving consistent responsiveness across various screen sizes can be tricky. *Mitigation: Use a mature CSS framework, regular testing on different browser sizes/developer tools.*

**Dependencies**: None direct (but AN1 for potential hosting platform if not using PaaS like Vercel/Netlify)

**Build Order**: #24

---

### Story F2: iOS App - Project Setup & Core Layout
#### Description:
As an engineer, I want to set up the foundational iOS application project, including necessary libraries, routing, and a basic app shell, so that native iOS UI development can commence.
**Details**: UI/UX considerations, components needed, interactions

#### Acceptance Criteria
- [ ] Xcode project initialized with Swift/SwiftUI (or UIKit) for native iOS development.
- [ ] Basic navigation stack configured (e.g., `UINavigationController` for UIKit, `NavigationView` for SwiftUI).
- [ ] A basic app shell with a root view controller/view hierarchy.
- [ ] Essential third-party SDKs/libraries integrated (e.g., a networking library like Alamofire/URLSession wrapper, UI component library if applicable).
- [ ] Version control initialized (e.g., Git repository).
- [ ] Basic CI/CD pipeline configured for iOS app (e.g., Fastlane, Xcode Cloud, App Center) for automated builds.
- [ ] A "hello world" or placeholder screen successfully rendered on an iOS simulator.
- [ ] Documentation for project structure, build process, dependency management, and local development instructions.
- [ ] Necessary Apple Developer Program configurations (e.g., provisioning profiles for dev) established.

#### Effort Estimate: **4 SP**
**Complexity**: ⭐⭐⭐ High

**Breakdown**:
- Frontend: 90% (3.6 days)
- DevOps: 10% (0.4 days)

**Reasoning**:
```
Day 1: Create a new Xcode project (SwiftUI or UIKit based). Configure basic project settings (bundle identifier, deployment targets).
Day 2: Set up the root view controller/view hierarchy and a basic navigation flow. Implement a placeholder "Hello World" screen.
Day 3: Integrate essential libraries (e.g., Alamofire for networking). Set up basic CI/CD with Fastlane or Xcode Cloud, including provisioning profiles (dev/ad-hoc).
Day 4: Document project structure, build process, signing requirements, and how to run locally on simulator/device.
```

**Risk Factors**:
- ⚠️ **iOS Provisioning & Signing**: Apple's provisioning profiles and signing process can be notoriously complex for new teams. *Mitigation: Follow Apple's official documentation, use Fastlane for automation, ensure team has necessary Apple Developer Program access.*
- ⚠️ **SDK Conflicts**: Third-party SDKs can sometimes conflict or cause build issues. *Mitigation: Start with minimal, well-maintained dependencies. Isolate integration if issues arise.*

**Dependencies**: None direct

**Build Order**: #25

---

### Story F3: Android App - Project Setup & Core Layout
#### Description:
As an engineer, I want to set up the foundational Android application project, including necessary libraries, routing, and a basic app shell, so that native Android UI development can commence.
**Details**: UI/UX considerations, components needed, interactions

#### Acceptance Criteria
- [ ] Android Studio project initialized with Kotlin/Jetpack Compose (or XML layouts) for native Android development.
- [ ] Basic navigation graph configured (e.g., Jetpack Navigation Component).
- [ ] A basic app shell with a root activity/fragment hierarchy.
- [ ] Essential third-party SDKs/libraries integrated (e.g., a networking library like Retrofit/OkHttp, UI component library if applicable).
- [ ] Version control initialized (e.g., Git repository).
- [ ] Basic CI/CD pipeline configured for Android app (e.g., Fastlane, GitHub Actions, App Center) for automated builds.
- [ ] A "hello world" or placeholder screen successfully rendered on an Android emulator.
- [ ] Documentation for project structure, build process, dependency management, and local development instructions.

#### Effort Estimate: **4 SP**
**Complexity**: ⭐⭐⭐ High

**Breakdown**:
- Frontend: 90% (3.6 days)
- DevOps: 10% (0.4 days)

**Reasoning**:
```
Day 1: Create a new Android Studio project (Jetpack Compose or XML/Kotlin). Configure basic Gradle settings.
Day 2: Set up the root activity/fragment and a basic navigation flow using Jetpack Navigation. Implement a placeholder "Hello World" screen.
Day 3: Integrate essential libraries (e.g., Retrofit for networking). Set up basic CI/CD with Fastlane or GitHub Actions, including signing configurations.
Day 4: Document project structure, Gradle build process, signing requirements, and how to run locally on emulator/device.
```

**Risk Factors**:
- ⚠️ **Gradle Build Times**: Complex Gradle configurations or many dependencies can lead to slow build times. *Mitigation: Keep build.gradle files clean, optimize dependencies, leverage build caches.*
- ⚠️ **Android Fragmentation**: UI/UX consistency across many Android devices/versions can be challenging. *Mitigation: Target recent Android versions, use Jetpack Compose for consistent UI, test on a range of devices/emulators.*

**Dependencies**: None direct

**Build Order**: #26

---

### Story F4: Parent Account Registration & Login UI (Web & Mobile)
#### Description:
As a parent, I want to see a clear registration and login screen, so that I can easily create my account or sign in to the platform.
**Details**: UI/UX considerations, components needed, interactions

#### Acceptance Criteria
- [ ] Responsive login form with email/password input fields and a "Forgot Password" link (link can be a placeholder for now).
- [ ] Responsive registration form with email, password, and "confirm password" fields.
- [ ] Client-side input validation implemented for email format and password strength (matching backend requirements).
- [ ] Successful login redirects the user to a placeholder Parent Dashboard or Child Profile Selection screen (F5).
- [ ] Successful registration redirects to the login screen or a confirmation message.
- [ ] Clear, user-friendly error messages displayed for failed login/registration attempts (e.g., "Invalid credentials", "Email already registered").
- [ ] UI/UX consistent across web, iOS, and Android platforms, following design guidelines.
- [ ] Unit tests for UI components (forms, input fields).
- [ ] Integration tests cover form submission and API interaction (B1).
- [ ] Accessibility considerations (e.g., keyboard navigation, screen reader support, clear focus states) implemented.

#### Effort Estimate: **7 SP**
**Complexity**: ⭐⭐⭐ High

**Breakdown**:
- Frontend: 100% (7 days)

**Reasoning**:
```
Day 1-1.5: Develop responsive Login and Registration UI components for Web. Implement frontend input validation.
Day 1-1.5: Develop native Login and Registration UI for iOS. Implement frontend input validation.
Day 1-1.5: Develop native Login and Registration UI for Android. Implement frontend input validation.
Day 2-3: Integrate Web UI with B1 API for login and registration. Handle success/failure states and display user-friendly messages. Securely store authentication tokens.
Day 2-3: Integrate iOS UI with B1 API.
Day 2-3: Integrate Android UI with B1 API.
Day 3.5-4: Write unit and integration tests for form submission and error handling. Ensure UI consistency and accessibility across platforms.
```

**Risk Factors**:
- ⚠️ **Inconsistent Error Handling**: Displaying different or confusing error messages across platforms/scenarios. *Mitigation: Define clear API error contracts with the backend (B1), ensure consistent frontend mapping to user-friendly messages.*
- ⚠️ **Security Flaws (Frontend)**: Weak client-side validation or insecure storage of auth tokens. *Mitigation: Remember frontend validation is for UX only; backend validation is primary. Use secure, platform-native storage for tokens (e.g., Keychain for iOS, EncryptedSharedPreferences for Android, HttpOnly cookies for web).*

**Dependencies**: F1, F2, F3 (project setup), B1 (Parent Account API)

**Build Order**: #27

---

### Story F5: Child Profile Selection UI (Web & Mobile)
#### Description:
As a child, I want to see a visual list of avatars on app launch and select my profile, so that I can enter my personalized content experience (FR2.4).
**Details**: UI/UX considerations, components needed, interactions

#### Acceptance Criteria
- [ ] After a parent logs in (F4), a dedicated screen displays a visual list of child profiles associated with their account.
- [ ] Each child profile is represented by a customizable avatar and name.
- [ ] A child can tap/click on their avatar to select their profile and proceed to the kid-friendly home screen (F6).
- [ ] The selected child's profile context (e.g., `child_id`, `max_age_rating`) is securely stored and used for subsequent API calls.
- [ ] An intuitive option for parents to add a new child profile (linking to F9's child creation logic) is present on this screen.
- [ ] Visual feedback provided upon profile selection.
- [ ] UI/UX consistent across web, iOS, and Android, adhering to kid-friendly design principles.
- [ ] Unit tests for the child profile list component.
- [ ] Integration tests for profile selection and context switching.

#### Effort Estimate: **5 SP**
**Complexity**: ⭐⭐⭐ High

**Breakdown**:
- Frontend: 100% (5 days)

**Reasoning**:
```
Day 1: Develop responsive UI for child profile selection on Web, showing avatars and names in an appealing, interactive manner.
Day 1: Develop native UI for child profile selection on iOS.
Day 1: Develop native UI for child profile selection on Android.
Day 2-3: Integrate Web UI with B2 API to fetch child profiles for the logged-in parent. Implement selection logic to securely store the selected `child_id` and associated context (e.g., age filter) and transition to F6.
Day 2-3: Integrate iOS UI with B2 API.
Day 2-3: Integrate Android UI with B2 API.
Day 3.5-4: Implement the "Add New Child" action (linking to F9). Write unit and integration tests for profile selection and ensure UI consistency.
```

**Risk Factors**:
- ⚠️ **Inconsistent Child Context Storage**: If the selected child's ID or age filter is not consistently passed/stored, subsequent content filtering could fail. *Mitigation: Use a global state management solution (e.g., Redux, Context API, ViewModel) to manage the active child's context consistently across the app.*
- ⚠️ **UI/UX for Many Children**: While unlikely for MVP, a parent with a very large number of children could make the selection screen cluttered. *Mitigation: Design with scrollability in mind, consider a grid layout. Defer search/pagination to a future story.*

**Dependencies**: B2 (Child Profile Management API), F4 (Parent Account Registration & Login UI)

**Build Order**: #28

---

### Story F6: Kid-Friendly Home Screen UI (Web & Mobile)
#### Description:
As a child, I want to see a simplified home screen with prominent visual cues and large buttons, showing recommended content and recently played items, so that I can easily discover and access content within my age range (FR2.1, FR2.2).
**Details**: UI/UX considerations, components needed, interactions

#### Acceptance Criteria
- [ ] A dedicated, visually appealing, kid-friendly home screen with large, easy-to-tap buttons and clear iconography.
- [ ] Displays a horizontally scrollable "Recently Played" section, populating with data from B9.
- [ ] Displays a "Recommended for You" section (initially populated with popular/curated content from B4, later with M3 recommendations).
- [ ] All content displayed on the home screen respects the currently selected child's age filter (from B5/B2) and content blocking rules (from B8).
- [ ] Visual navigation elements (e.g., large buttons/icons) to content categories (linking to F7).
- [ ] Placeholder for profile switching (back to F5) and parental access (linking to F9).
- [ ] UI/UX consistent with kid-friendly design principles across web, iOS, and Android.
- [ ] Unit tests for home screen sections and content display components.
- [ ] Accessibility considerations for children (e.g., sufficient contrast, clear labels).

#### Effort Estimate: **9 SP**
**Complexity**: ⭐⭐⭐ High

**Breakdown**:
- Frontend: 100% (9 days)

**Reasoning**:
```
Day 1-2: Develop responsive, kid-friendly home screen UI for Web. Create reusable components for horizontally scrollable content carousels (recently played, recommended sections) and large navigation buttons.
Day 1-2: Develop native kid-friendly home screen UI for iOS, focusing on engaging animations and touch targets.
Day 1-2: Develop native kid-friendly home screen UI for Android, optimizing for various screen sizes and orientations.
Day 3-4: Integrate Web UI with B4 to fetch "recommended" (initially popular/curated) content and B9 to fetch "recently played" content. Ensure all content fetched applies the selected child's age filter and content blocking.
Day 3-4: Integrate iOS UI with B4 and B9.
Day 3-4: Integrate Android UI with B4 and B9.
Day 5: Implement basic navigation to content browsing (F7) and placeholder links for profile switching/parental access. Write UI unit tests. Ensure UI consistency and responsiveness across platforms.
```

**Risk Factors**:
- ⚠️ **UI Not Engaging**: The kid-friendly UI might not resonate with the target audience without user testing. *Mitigation: Prioritize simple, intuitive designs, use bright colors/large images. Plan for early user testing/feedback sessions (future).*
- ⚠️ **Performance with Many Content Items**: Slow loading of content sections or many API calls could impact user experience. *Mitigation: Implement skeleton loaders, optimize API calls (e.g., combined requests), client-side caching of frequently accessed data.*

**Dependencies**: F5 (Child Profile Selection), B4 (Content Browsing API), B9 (Listening History API)

**Build Order**: #29

---

### Story F7: Content Browsing UI (Categories & Search - Web & Mobile)
#### Description:
As a child, I want to browse content by intuitive categories (e.g., Music, Stories) and use a simplified search function, so that I can find specific content or explore new types of audio (FR1.3, FR1.4).
**Details**: UI/UX considerations, components needed, interactions

#### Acceptance Criteria
- [ ] A dedicated "Browse" section accessible from the home screen (F6), displaying available categories with prominent visual representation.
- [ ] Clicking a category displays a paginated list of content items within that category.
- [ ] A simplified, prominent search bar is available for entering keywords to search content titles/descriptions.
- [ ] A search results page displays paginated content matching keywords.
- [ ] All content displayed (browsing and search results) adheres to the currently selected child's age filter (from B5/B2) and content blocking rules (from B8).
- [ ] Each content item in lists/grids displays title, cover art, and duration.
- [ ] UI/UX consistent across web, iOS, and Android, maintaining kid-friendly design.
- [ ] Unit tests for UI components (category list, content list, search input).
- [ ] Integration tests for category selection, search functionality, pagination, and filtering.

#### Effort Estimate: **9 SP**
**Complexity**: ⭐⭐⭐ Medium

**Breakdown**:
- Frontend: 100% (9 days)

**Reasoning**:
```
Day 1-2: Develop responsive UI for content browsing on Web. This includes a list of categories, a paginated content listing page (grid/list view) for categories, and a prominent search input with result display.
Day 1-2: Develop native UI for content browsing on iOS, ensuring smooth scrolling and touch interactions.
Day 1-2: Develop native UI for content browsing on Android, optimizing for performance and responsiveness.
Day 3-4: Integrate Web UI with B4 API to fetch categories, category-filtered content, and search results. Implement pagination/infinite scroll for content lists.
Day 3-4: Integrate iOS UI with B4 API.
Day 3-4: Integrate Android UI with B4 API.
Day 5: Implement consistent display of content details (title, cover art, duration). Write unit and integration tests for category selection, search functionality, and correct application of age filters/blocked content. Ensure loading states and empty results are handled gracefully.
```

**Risk Factors**:
- ⚠️ **Slow Search API Response**: If B4 search API is slow, it will lead to a poor user experience. *Mitigation: Implement client-side debounce for search input, display skeleton loaders/loading indicators, ensure B4 is performant.*
- ⚠️ **Inconsistent Filtering**: The application of age filters and content blocking must be robust. *Mitigation: Test comprehensively across all platforms and child profiles, verify API responses for correct filtering.*

**Dependencies**: F6 (home screen for navigation), B4 (Content Browsing & Search API)

**Build Order**: #30

---

### Story F8: Audio Player UI (Basic Controls - Web & Mobile)
#### Description:
As a child, I want to use large, simple play/pause, skip forward/backward buttons, and a volume control while listening, so that I can easily manage my audio playback (FR2.3).
**Details**: UI/UX considerations, components needed, interactions

#### Acceptance Criteria
- [ ] A persistent audio player UI (e.g., mini-player, full-screen player accessible from any screen) displayed when content is playing.
- [ ] Large, clearly identifiable play/pause, skip forward (e.g., 15s), and skip backward (e.g., 15s) buttons.
- [ ] A progress bar indicating current playback position and total duration.
- [ ] Volume control (using native platform controls where appropriate for mobile, or a slider for web).
- [ ] Displays the current content's title, artist (if applicable), and cover art.
- [ ] Plays audio streamed from the B6 streaming API URL.
- [ ] Handles network interruptions gracefully (e.g., buffering indicators, retry logic, error messages).
- [ ] Integration with native media session APIs on mobile for background playback controls (lock screen, control center).
- [ ] UI/UX consistent across web, iOS, and Android, adhering to kid-friendly design.
- [ ] Unit tests for audio player UI components.
- [ ] Integration tests for playback controls and API interaction (B6).

#### Effort Estimate: **9 SP**
**Complexity**: ⭐⭐⭐ High

**Breakdown**:
- Frontend: 100% (9 days)

**Reasoning**:
```
Day 1-2: Develop responsive audio player UI for Web with play/pause, skip, progress bar, volume slider. Use HTML5 Audio API.
Day 1-2: Develop native audio player UI for iOS using AVFoundation, integrating system media controls (Media Playback controls, Control Center).
Day 1-2: Develop native audio player UI for Android using ExoPlayer or MediaPlayer, integrating system media controls (MediaSession API).
Day 3-4: Integrate Web UI with B6 streaming API to fetch and play audio. Display content metadata. Handle buffering and error states effectively.
Day 3-4: Integrate iOS UI with B6.
Day 3-4: Integrate Android UI with B6.
Day 5: Write unit and integration tests for playback controls (play, pause, skip, seek). Ensure seamless playback and robust error handling. Verify background playback controls on mobile platforms.
```

**Risk Factors**:
- ⚠️ **Inconsistent Playback Behavior**: Audio playback can behave differently across browsers, devices, or OS versions. *Mitigation: Use battle-tested, platform-specific libraries (ExoPlayer for Android, AVFoundation for iOS, standard HTML5 Audio for Web). Thorough cross-platform testing.*
- ⚠️ **Buffering Issues**: Poor network conditions or slow CDN response can lead to frequent buffering. *Mitigation: Implement clear buffering indicators, optimize B6 API and AN3 CDN, implement adaptive bitrate streaming (if B6 supports).*

**Dependencies**: F7 (content selection), B6 (Audio Streaming API)

**Build Order**: #31

---

### Story F9: Parental Dashboard UI (Child Profile Management & Age Filter - Web & Mobile)
#### Description:
As a parent, I want to access a PIN-protected dashboard to create/manage child profiles and set age-appropriateness filters for each, so that I can customize my children's access (FR3.1, FR3.2, FR3.6).
**Details**: UI/UX considerations, components needed, interactions

#### Acceptance Criteria
- [ ] A dedicated PIN input screen displayed to parents before granting access to the Parental Dashboard (integrating with B7).
- [ ] Successful PIN entry grants access; unsuccessful attempts display clear error messages and adhere to rate limits.
- [ ] The Parental Dashboard displays a list of child profiles with options to:
    - [ ] Create new child profile (form for name, age/DOB, avatar selection).
    - [ ] Edit existing child profile (update name, age/DOB, avatar).
    - [ ] Delete child profile (with confirmation dialog).
    - [ ] Set/update the maximum age-appropriateness filter (e.g., slider or dropdown for max age) for each child.
- [ ] All forms include client-side input validation and display backend validation errors.
- [ ] UI/UX consistent across web, iOS, and Android, using a more "adult" design language than the child UI.
- [ ] Unit tests for PIN input component, child profile forms, and age filter controls.
- [ ] Integration tests for PIN validation (B7) and child management (B2, B5).
- [ ] Accessibility considerations for forms and navigation within the dashboard.

#### Effort Estimate: **13 SP**
**Complexity**: ⭐⭐⭐ High

**Breakdown**:
- Frontend: 100% (13 days)

**Reasoning**:
```
Day 1-3: Develop responsive PIN entry screen and the core Parental Dashboard layout for Web. Implement forms for creating, editing, and deleting child profiles. Implement a control for setting age filters (e.g., slider, dropdown).
Day 1-3: Develop native PIN entry screen and Parental Dashboard UI for iOS, ensuring secure input fields and platform conventions.
Day 1-3: Develop native PIN entry screen and Parental Dashboard UI for Android, optimizing for various device sizes and orientations.
Day 4-6: Integrate Web UI with B7 API for PIN verification (displaying errors, handling rate limits). Integrate child management forms with B2 CRUD API. Integrate age filter control with B5 API. Handle API response errors gracefully.
Day 4-6: Integrate iOS UI with B7, B2, B5 APIs.
Day 4-6: Integrate Android UI with B7, B2, B5 APIs.
Day 7: Implement robust client-side input validation for all forms and PIN fields. Write comprehensive unit and integration tests for all dashboard functionalities. Ensure UI consistency.
```

**Risk Factors**:
- ⚠️ **Insecure PIN Handling (Frontend)**: Client-side storage or transmission of PIN could lead to vulnerabilities. *Mitigation: Delegate PIN hashing and verification entirely to B7. Frontend should only send the raw PIN over HTTPS. Do not store PIN locally.*
- ⚠️ **Complex State Management**: Managing multiple child profiles and their settings across different forms can be complex. *Mitigation: Use a robust state management framework (e.g., Redux, MobX, MVVM) to centralize state and ensure data consistency.*
- ⚠️ **User Experience for Many Children**: If a parent has many children, managing them could be cumbersome. *Mitigation: Ensure lists are scrollable, provide clear search/sort options if needed (future story).*

**Dependencies**: F4 (Parent Login), B2 (Child Profile Management), B5 (Age Filtering), B7 (PIN Protection)

**Build Order**: #32

---

### Story F10: Parental Dashboard UI (Content Blocking - Web & Mobile)
#### Description:
As a parent, I want to be able to search for and block specific content or entire categories from a child's profile via the dashboard, so that I can ensure only suitable content is available (FR3.3).
**Details**: UI/UX considerations, components needed, interactions

#### Acceptance Criteria
- [ ] A dedicated "Content Blocking" section accessible within the Parental Dashboard (F9).
- [ ] Ability to search for content (reusing F7 search component) or browse categories to select items for blocking.
- [ ] Clear visual indication of currently blocked content items and categories for the selected child.
- [ ] Functionality to add specific `content_id` or `category_id` to a child's block list (integrating with B8).
- [ ] Functionality to remove items from the child's block list.
- [ ] Confirmation dialogs for blocking/unblocking actions.
- [ ] UI/UX consistent across web, iOS, and Android platforms.
- [ ] Unit tests for content blocking components and search integration.
- [ ] Integration tests for blocking/unblocking functionality with B8 API.

#### Effort Estimate: **9 SP**
**Complexity**: ⭐⭐⭐ Medium

**Breakdown**:
- Frontend: 100% (9 days)

**Reasoning**:
```
Day 1-2: Develop responsive "Content Blocking" section within the Web Parental Dashboard (F9). This includes integrating a search input (reusing F7 search logic), a display for search results, and interactive controls to block/unblock content items or categories.
Day 1-2: Develop native "Content Blocking" UI for iOS.
Day 1-2: Develop native "Content Blocking" UI for Android.
Day 3-4: Integrate Web UI with B8 API for blocking, unblocking, and listing currently blocked content