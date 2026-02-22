# Sprint Backlog

**Generated**: 2026-02-21
**Source**: user_stories.md
**Team Calibration**: 1 SP = 1 day (adjust in config.yml)
**Status**: 🟡 Ready for Sprint Planning

---

## 🏗️ Architecture & Non-Functional Stories

### Story AN1: Establish Core Cloud Infrastructure (VPC, Compute, Database)
#### Description:
As an engineer, I want to set up the foundational cloud infrastructure including VPC, compute resources (e.g., Kubernetes cluster or EC2 instances), and managed relational database (PostgreSQL) instances, so that we have a secure and scalable environment for deploying our services.
**Details**:
- **Tech Stack**: AWS Cloud Services (VPC, EKS, RDS PostgreSQL, S3, IAM)
- **Infrastructure**:
    -   AWS VPC with public and private subnets, NAT Gateways for outbound access.
    -   AWS EKS cluster (Kubernetes) for container orchestration, configured for autoscaling.
    -   AWS RDS PostgreSQL instance (multi-AZ for high availability) for core relational data, provisioned with suitable instance type and storage.
    -   AWS S3 bucket for storing raw and processed audio content.
    -   IAM roles and policies defined for least privilege access for services.
    -   Security Groups configured for network isolation between tiers.
- **Performance Targets**: Initial provisioning aims for high availability and scalability, specific service performance targets will be set in subsequent stories.
- **Security Requirements**: Default AWS encryption for S3 and RDS, network isolation, IAM roles. TLS 1.2+ enforced for all inter-service communication where applicable.
- **Scalability**: EKS autoscaling enabled, RDS read replicas can be added later if needed.
- **Constraints**: Initial setup focuses on core components, advanced features like serverless functions or complex networking will be added as needed.
#### Acceptance Criteria
- [x] AWS VPC configured with at least two public and two private subnets across two Availability Zones.
- [x] AWS EKS cluster provisioned, with worker nodes configured for autoscaling and connected to private subnets.
- [x] AWS RDS PostgreSQL instance (v14+) provisioned in a private subnet, multi-AZ enabled, with necessary security group access for EKS.
- [x] Dedicated S3 bucket created for content storage with appropriate bucket policies and versioning enabled.
- [x] IAM roles created for EKS, RDS, and S3 access with principle of least privilege.
- [x] Basic CI/CD pipeline placeholder (e.g., Jenkins/GitHub Actions) configured to deploy a sample 'hello world' application to EKS.
- [x] All infrastructure components deployed via Infrastructure-as-Code (e.g., Terraform/CloudFormation).
- [x] Documentation for infrastructure setup, network topology, and access configurations.

#### Effort Estimate: **8 SP**
**Complexity**: Medium

**Breakdown**:
- DevOps: 100% (8 days)

**Reasoning**:
```
Day 1: Research and Design
- Review architectural patterns for secure, scalable AWS infrastructure (2 hrs)
- Design VPC network topology, subnets, routing, NAT Gateway placement (3 hrs)
- Define EKS cluster configuration, worker node groups, IAM roles (3 hrs)

Day 2: Terraform/CloudFormation Setup - VPC & Networking
- Initialize Terraform project structure and modules (3 hrs)
- Implement VPC, subnets, Internet Gateway, NAT Gateways, Route Tables (5 hrs)

Day 3: Terraform/CloudFormation Setup - EKS Cluster
- Implement EKS cluster, IAM roles for EKS, worker node launch templates (8 hrs)

Day 4: Terraform/CloudFormation Setup - RDS & S3
- Implement RDS PostgreSQL instance (multi-AZ, encryption, backups) (4 hrs)
- Implement S3 bucket with appropriate policies (3 hrs)
- Configure security groups for EKS-RDS communication (1 hr)

Day 5: Initial Deployment & Testing
- Deploy infrastructure using IaC (2 hrs)
- Basic connectivity tests (EKS nodes to internet, EKS to RDS) (4 hrs)
- Deploy a simple test application to EKS (e.g., nginx) (2 hrs)

Day 6: IAM & Security Hardening
- Refine IAM roles and policies for least privilege (4 hrs)
- Security group review and hardening (2 hrs)
- Initial compliance checks against best practices (2 hrs)

Day 7: Documentation & CI/CD Integration
- Document the deployed architecture, access procedures, troubleshooting (6 hrs)
- Setup basic CI/CD pipeline stub for EKS (e.g., GitHub Actions workflow to apply k8s manifests) (2 hrs)

Day 8: Code Review, Refinement, & Bug Fixes
- Address code review comments (4 hrs)
- Troubleshoot any identified issues (4 hrs)
```

**Risk Factors**:
- ⚠️ **AWS Account Setup/Permissions**: Initial account setup or missing permissions can cause delays. *Mitigation: Ensure necessary AWS admin permissions are granted upfront and verified.*
- ⚠️ **EKS Complexity**: Kubernetes setup can be intricate, especially networking (CNI) and IAM roles. *Mitigation: Leverage existing Terraform modules/best practices; allocate extra time for debugging.*
- ⚠️ **Security Configuration Errors**: Misconfigured security groups or IAM policies can create vulnerabilities or connectivity issues. *Mitigation: Peer review of IaC, automated security scanning tools, thorough testing.*

**Dependencies**: None
**Build Order**: #1

---

### Story AN2: Implement Parent Authentication & Authorization Framework
#### Description:
As an engineer, I want to establish a secure authentication service for parent users, supporting robust password hashing and enabling future MFA options, so that parental accounts are protected and access control can be enforced.
**Details**:
- **Tech Stack**: Spring Boot (Java) for Auth Service, Spring Security, JWT (JSON Web Tokens), BCrypt for password hashing.
- **Infrastructure**: Auth service deployed as a microservice on EKS.
- **Performance Targets**: Authentication API response time < 200ms p95.
- **Security Requirements**:
    -   Passwords hashed using BCrypt with a strong work factor.
    -   JWTs generated for authenticated sessions, signed with a strong secret/key.
    -   Token expiration and refresh mechanisms implemented.
    -   Protection against common web vulnerabilities (e.g., brute-force, injection).
    -   User registration via email verification flow.
- **Scalability**: Stateless JWTs allow horizontal scaling of the Auth service on EKS.
- **Constraints**: Focus on parent authentication; child authentication/selection is handled differently (via parent-managed profiles). MFA is for future, current scope is framework enabling it.
#### Acceptance Criteria
- [x] Auth service implemented in Spring Boot, deployable to EKS.
- [x] `POST /api/v1/auth/register` endpoint allows new parent user registration with email and password.
- [x] Parent passwords are securely hashed using BCrypt before storage in the database.
- [x] `POST /api/v1/auth/login` endpoint authenticates parent users and returns a JWT on successful login.
- [x] JWTs contain necessary claims (e.g., user ID, roles, expiration) and are signed securely.
- [x] `GET /api/v1/auth/me` endpoint allows authenticated users to retrieve their profile using a valid JWT.
- [x] JWT validation middleware/filter integrated into the Auth service for secured endpoints.
- [x] Basic email verification flow implemented for new registrations (e.g., sending a verification link, though actual email sending might be a separate task).
- [x] Unit and integration tests cover registration, login, and token validation.
- [x] API documentation (e.g., OpenAPI/Swagger) for all authentication endpoints.

#### Effort Estimate: **6 SP**
**Complexity**: Medium

**Breakdown**:
- Backend: 90% (5.4 days)
- DevOps: 10% (0.6 days)

**Reasoning**:
```
Day 1: Design & Setup
- Design Auth service architecture, API endpoints, data flow (4 hrs)
- Set up Spring Boot project, add Spring Security dependencies (4 hrs)

Day 2: Registration Implementation
- Implement `User` entity and repository for database interaction (3 hrs)
- Develop registration endpoint, password hashing with BCrypt (5 hrs)

Day 3: Login Implementation
- Develop login endpoint, validate credentials (4 hrs)
- Implement JWT generation and signing logic (4 hrs)

Day 4: JWT Validation & User Context
- Implement JWT validation filter/interceptor for secured endpoints (4 hrs)
- Develop `GET /me` endpoint to return authenticated user details (2 hrs)
- Basic error handling for invalid credentials, missing tokens (2 hrs)

Day 5: Email Verification & Testing
- Implement basic email verification flow (token generation, status update) (4 hrs)
- Write unit tests for all service logic (registration, login, token) (4 hrs)

Day 6: Integration, Documentation & Refinement
- Integrate with EKS (Dockerfile, K8s manifests) (3 hrs)
- Write integration tests for API endpoints (2 hrs)
- Update OpenAPI documentation (1 hr)
- Code review and address feedback (2 hrs)
```

**Risk Factors**:
- ⚠️ **Security Vulnerabilities**: Improper JWT handling or hashing can lead to security flaws. *Mitigation: Use well-vetted libraries (Spring Security), adhere to security best practices, conduct peer code reviews.*
- ⚠️ **Integration with existing systems**: If there's an existing identity provider, integration complexity could increase. *Mitigation: Keep the scope focused on a greenfield auth service for now; identify external IDP needs later.*

**Dependencies**: AN1 (Core Cloud Infrastructure), AN5 (Database Schemas for User)
**Build Order**: #2

---

### Story AN3: Set up Content Delivery Network (CDN) for Audio Streaming
#### Description:
As an engineer, I want to integrate a CDN service and configure it for optimized global audio content delivery, so that users experience low-latency streaming and downloads regardless of their location, supporting NFR3.3.
**Details**:
- **Tech Stack**: AWS CloudFront, AWS S3.
- **Infrastructure**: CloudFront distributions configured to cache content originating from the S3 bucket (AN1).
- **Performance Targets**:
    -   Audio content delivery latency < 100ms p95 globally.
    -   Reduced load on S3 and backend services.
- **Security Requirements**:
    -   HTTPS enforced for all CDN traffic.
    -   Origin access restricted (e.g., Origin Access Control for S3) to prevent direct S3 access.
    -   Signed URLs or cookies for restricted content access (future scope, initial focus on public-accessible content via CDN).
- **Scalability**: CloudFront automatically scales globally.
- **Constraints**: Initial setup assumes content in S3 is publicly accessible *via CDN*, direct S3 access will be blocked. DRM is not part of this story.
#### Acceptance Criteria
- [x] AWS CloudFront distribution created and configured.
- [x] S3 bucket (from AN1) configured as the origin for the CloudFront distribution.
- [x] Origin Access Control (OAC) implemented to restrict direct S3 access to CloudFront only.
- [x] HTTPS enforced for all CloudFront viewer requests.
- [x] Cache behaviors configured for audio file types (e.g., `.mp3`, `.m4a`) with optimal caching policies (e.g., TTLs).
- [x] A sample audio file uploaded to S3 can be successfully streamed/downloaded via the CloudFront URL.
- [x] Latency tests confirm reduced load times for cached content from various geographic locations.
- [x] Documentation for CloudFront setup, origin configuration, and cache invalidation strategies.

#### Effort Estimate: **3 SP**
**Complexity**: High

**Breakdown**:
- DevOps: 100% (3 days)

**Reasoning**:
```
Day 1: Design & Initial Setup
- Research CloudFront best practices for audio streaming (e.g., caching, OAC) (4 hrs)
- Create CloudFront distribution, configure S3 origin (4 hrs)

Day 2: Security & Caching Configuration
- Implement Origin Access Control (OAC) to secure S3 bucket (4 hrs)
- Configure cache behaviors for audio content (e.g., cache all, specific TTLs) (3 hrs)
- Enable HTTPS and review SSL/TLS settings (1 hr)

Day 3: Testing, Validation & Documentation
- Upload sample audio content to S3 (1 hr)
- Test content access via CloudFront URL, verify OAC (3 hrs)
- Perform basic latency checks from different regions (e.g., using online tools) (2 hrs)
- Document CDN configuration, potential troubleshooting steps (2 hrs)
```

**Risk Factors**:
- ⚠️ **Incorrect Caching Behavior**: Misconfigured cache rules could lead to stale content or poor performance. *Mitigation: Thorough testing with cache invalidation strategies; start with simple, broad caching and refine.*
- ⚠️ **Origin Access Misconfiguration**: Incorrect OAC setup could either expose the S3 bucket directly or prevent CDN access. *Mitigation: Step-by-step verification, test direct S3 access blockage immediately after OAC setup.*
- ⚠️ **Cost Optimization**: CloudFront can incur costs quickly if not monitored. *Mitigation: Set up cost alarms; document cost considerations.*

**Dependencies**: AN1 (Core Cloud Infrastructure, specifically S3)
**Build Order**: #3

---

### Story AN4: Implement Centralized Logging and Monitoring for Backend Services
#### Description:
As an engineer, I want to set up centralized logging (e.g., ELK stack, CloudWatch Logs) and application performance monitoring (APM) tools for backend services, so that we can quickly identify and troubleshoot issues and monitor system health (NFR5.3, NFR5.1).
**Details**:
- **Tech Stack**: AWS CloudWatch Logs, CloudWatch Metrics, AWS X-Ray (for tracing), Grafana (for dashboards if needed, integrating with CloudWatch).
- **Infrastructure**:
    -   Log collection agents (e.g., Fluent Bit, CloudWatch Agent) deployed to EKS worker nodes and integrated with container logs.
    -   Services configured to emit structured logs (JSON format).
    -   CloudWatch Log Groups for each service.
    -   CloudWatch Alarms for critical metrics (CPU, memory, error rates).
    -   AWS X-Ray SDK integrated into Spring Boot services for distributed tracing.
- **Performance Targets**: Log ingestion latency < 5 minutes, metric refresh rate < 1 minute.
- **Security Requirements**: Logs encrypted at rest in CloudWatch. Access to logs and dashboards restricted via IAM.
- **Scalability**: CloudWatch and X-Ray are managed services and scale automatically.
- **Constraints**: Initial focus on backend services. Frontend logging and more advanced business intelligence dashboards will be separate.
#### Acceptance Criteria
- [x] CloudWatch Log Groups created for each core backend service deployed on EKS.
- [x] EKS cluster configured to send container logs to respective CloudWatch Log Groups (e.g., via Fluent Bit daemonset).
- [x] Sample Spring Boot service (e.g., Auth service from AN2) configured to output structured JSON logs.
- [x] Basic CloudWatch Dashboards created to display key metrics (CPU utilization, memory usage, error rates) for core services.
- [x] CloudWatch Alarms configured for high error rates or critical resource exhaustion (e.g., 80% CPU usage).
- [x] AWS X-Ray SDK integrated into at least one backend service to demonstrate distributed tracing.
- [x] X-Ray traces visible in the AWS console, showing service calls and latency.
- [x] Documentation for logging standards, how to access logs/metrics, and alarm configurations.

#### Effort Estimate: **5 SP**
**Complexity**: Medium

**Breakdown**:
- DevOps: 70% (3.5 days)
- Backend: 30% (1.5 days)

**Reasoning**:
```
Day 1: Logging Setup - EKS & CloudWatch
- Research best practices for EKS logging to CloudWatch (Fluent Bit) (4 hrs)
- Configure Fluent Bit DaemonSet in EKS to capture container logs (4 hrs)

Day 2: Structured Logging & Metrics
- Configure Spring Boot services for JSON logging (e.g., Logback/Log4j2 setup) (4 hrs)
- Define and implement custom application metrics (e.g., request count, error count) (4 hrs)

Day 3: Monitoring & Alerting
- Create CloudWatch Log Groups and Metric Filters for key log patterns (4 hrs)
- Set up CloudWatch Alarms for critical metrics (error rates, resource utilization) (4 hrs)

Day 4: Distributed Tracing (X-Ray)
- Integrate AWS X-Ray SDK into a sample Spring Boot service (e.g., Auth Service) (5 hrs)
- Verify X-Ray traces are captured and viewable in console (3 hrs)

Day 5: Dashboard, Documentation & Refinement
- Create CloudWatch Dashboards for visualizing key service health metrics (4 hrs)
- Document logging standards, monitoring procedures, and troubleshooting guides (2 hrs)
- Code review and address feedback (2 hrs)
```

**Risk Factors**:
- ⚠️ **Log Volume and Cost**: High log volume can quickly increase CloudWatch costs. *Mitigation: Implement log retention policies, filter out verbose logs, monitor costs.*
- ⚠️ **Tracing Overhead**: X-Ray integration might introduce slight performance overhead or require careful configuration. *Mitigation: Start with sampling, monitor impact, and configure context propagation carefully.*
- ⚠️ **Alert Fatigue**: Poorly configured alarms can lead to excessive notifications. *Mitigation: Start with critical alarms only, refine thresholds based on observed behavior.*

**Dependencies**: AN1 (Core Cloud Infrastructure), AN2 (Auth service as a sample for integration)
**Build Order**: #4

---

### Story AN5: Configure Database Schemas for User & Content Metadata
#### Description:
As an engineer, I want to define and implement the initial relational database schemas for parent accounts, child profiles, subscription information, and core content metadata (titles, descriptions, categories, age ratings), so that we have a structured way to store essential application data.
**Details**:
- **Tech Stack**: PostgreSQL (AWS RDS from AN1), Liquibase/Flyway for schema migrations.
- **Data Model**:
    -   `parents` table: `id (PK), email (unique), password_hash, created_at, updated_at, is_verified`.
    -   `children` table: `id (PK), parent_id (FK), name, avatar_url, age_range_max (int), created_at, updated_at`.
    -   `content_items` table: `id (PK), title, description, category_id (FK), age_rating_min, age_rating_max, audio_file_url, duration, thumbnail_url, is_premium, created_at, updated_at`.
    -   `categories` table: `id (PK), name (unique), description`.
    -   `subscriptions` table: `id (PK), parent_id (FK), external_subscription_id (from payment gateway), status (active/inactive/cancelled), plan_id (FK), start_date, end_date, created_at, updated_at`.
    -   `subscription_plans` table: `id (PK), name, description, monthly_price_usd, features_json`.
- **Infrastructure**: Schema migrations applied to RDS PostgreSQL instance.
- **Security Requirements**: No direct PII in content_items. Parent and child PII stored separately.
- **Constraints**: Initial schema, will evolve. Focus on core entities needed for MVP.
#### Acceptance Criteria
- [x] Database schema designed and documented with entity-relationship diagrams (ERDs).
- [x] Liquibase (or Flyway) set up for managing database migrations.
- [x] Initial migration scripts created for `parents`, `children`, `content_items`, `categories`, `subscriptions`, and `subscription_plans` tables.
- [x] All tables include `id` (UUID or BigInt), `created_at`, `updated_at` columns.
- [x] Foreign key constraints defined for relationships (e.g., `children.parent_id` references `parents.id`).
- [x] Appropriate data types chosen for all columns (e.g., `VARCHAR` for strings, `INTEGER` for age, `TIMESTAMP WITH TIME ZONE` for dates).
- [x] Unique constraints applied where necessary (e.g., `parents.email`, `categories.name`).
- [x] Migration scripts successfully applied to the RDS PostgreSQL instance.
- [x] Verification that tables and columns are created as expected in the database.

#### Effort Estimate: **4 SP**
**Complexity**: Medium

**Breakdown**:
- Backend: 80% (3.2 days)
- DevOps: 20% (0.8 days)

**Reasoning**:
```
Day 1: Schema Design
- Review requirements for parent, child, content, and subscription data (4 hrs)
- Design initial ERD, define tables, columns, data types, relationships (4 hrs)

Day 2: Migration Tool Setup & Parent/Child Schemas
- Set up Liquibase/Flyway project and configuration (3 hrs)
- Create migration scripts for `parents` and `children` tables (5 hrs)

Day 3: Content & Category Schemas
- Create migration scripts for `content_items` and `categories` tables (4 hrs)
- Define indexes for frequently queried columns (e.g., `content_items.category_id`) (2 hrs)
- Review schema for potential performance bottlenecks (2 hrs)

Day 4: Subscription Schemas, Review & Apply
- Create migration scripts for `subscriptions` and `subscription_plans` tables (3 hrs)
- Peer review of all migration scripts and schema design (2 hrs)
- Apply migrations to development database (1 hr)
- Verify database state and documentation (2 hrs)
```

**Risk Factors**:
- ⚠️ **Schema Design Flaws**: Poor schema design can lead to performance issues or data integrity problems later. *Mitigation: Thorough design review with experienced engineers, incremental approach, clear documentation.*
- ⚠️ **Migration Rollback Issues**: Complex migrations can be hard to roll back if failures occur. *Mitigation: Test migrations in a non-production environment, ensure idempotent scripts, have a rollback strategy.*

**Dependencies**: AN1 (Core Cloud Infrastructure, specifically RDS PostgreSQL)
**Build Order**: #5

---

### Story AN6: Implement Data Encryption for PII at Rest and In Transit
#### Description:
As an engineer, I want to ensure all PII and payment data is encrypted at rest (AES-256) and in transit (TLS 1.2+) across all services and databases, so that we comply with NFR2.2 (Data Encryption) and privacy regulations like COPPA and GDPR.
**Details**:
- **Tech Stack**: AWS KMS (Key Management Service), AWS RDS (PostgreSQL with encryption at rest), AWS Load Balancers (ALB/NLB for TLS termination), Spring Boot (for enforcing TLS connections).
- **Infrastructure**:
    -   AWS RDS PostgreSQL configured with KMS-managed encryption at rest (AES-256).
    -   AWS Load Balancers (ALB for HTTP(S) traffic to EKS) configured to enforce TLS 1.2+ and terminate SSL certificates (managed by ACM).
    -   EKS cluster configured to use TLS for inter-service communication (e.g., mutual TLS or service mesh, for MVP simple HTTPS calls).
    -   Application code (Spring Boot) configured to connect to RDS using SSL.
- **Security Requirements**:
    -   PII (parent emails, child names) in database encrypted at rest.
    -   All traffic to and from application services secured with TLS 1.2+.
    -   Key management for encryption keys handled by KMS.
- **Constraints**: Focus on foundational encryption. Application-level encryption for specific sensitive fields is out of scope for now.
#### Acceptance Criteria
- [x] AWS RDS PostgreSQL instance (from AN1) reconfigured or verified to use KMS-managed AES-256 encryption at rest.
- [x] AWS Application Load Balancer (ALB) deployed in front of EKS services, configured to redirect HTTP to HTTPS.
- [x] ALB configured to enforce TLS 1.2+ for all client-to-ALB connections.
- [x] AWS Certificate Manager (ACM) used to provision and integrate an SSL certificate with the ALB.
- [x] Backend services (e.g., Auth service from AN2) configured to listen on HTTPS within EKS or behind the ALB.
- [x] Spring Boot services configured to establish SSL/TLS connections to the RDS PostgreSQL database.
- [x] Verification that all external API endpoints are only accessible via HTTPS, and direct HTTP access is redirected or blocked.
- [x] Confirmation that data stored in the database is encrypted at rest (e.g., via AWS console verification).
- [x] Documentation for TLS configuration, certificate management, and encryption policies.

#### Effort Estimate: **5 SP**
**Complexity**: Medium

**Breakdown**:
- DevOps: 80% (4 days)
- Backend: 20% (1 day)

**Reasoning**:
```
Day 1: RDS Encryption & KMS Setup
- Verify RDS PostgreSQL instance is configured with KMS-managed encryption (2 hrs)
- If not, create new encrypted RDS instance or reconfigure (4 hrs)
- Configure IAM policies for KMS key access for RDS (2 hrs)

Day 2: ALB & TLS Setup
- Deploy AWS Application Load Balancer (ALB) to expose EKS services (4 hrs)
- Provision SSL/TLS certificate using AWS Certificate Manager (ACM) (2 hrs)
- Integrate ACM certificate with ALB (2 hrs)

Day 3: TLS Enforcement & Backend Integration
- Configure ALB to enforce HTTPS (redirect HTTP to HTTPS) and use TLS 1.2+ (4 hrs)
- Update EKS service manifests/ingress to route traffic through ALB (2 hrs)
- Verify ALB is successfully terminating TLS and forwarding traffic to EKS (2 hrs)

Day 4: Database Connection TLS
- Configure Spring Boot application properties to force SSL connection to RDS (e.g., `spring.datasource.url=...ssl=true...`) (4 hrs)
- Test application connectivity to RDS over SSL (3 hrs)
- Peer review of configurations and testing (1 hr)

Day 5: Documentation & Testing
- Document encryption setup, TLS policies, certificate renewal process (5 hrs)
- Comprehensive testing of encryption in transit (e.g., SSL Labs test for ALB, local network traffic capture for DB connection verification) (3 hrs)
```

**Risk Factors**:
- ⚠️ **Downtime during RDS Reconfiguration**: If RDS encryption needs to be enabled on an existing instance, it might require a new instance or downtime. *Mitigation: Plan for maintenance window or use a blue/green deployment strategy for RDS if necessary.*
- ⚠️ **TLS Handshake Issues**: Misconfigured certificates or protocols can lead to connection failures. *Mitigation: Thorough testing, review server logs for SSL/TLS errors.*
- ⚠️ **Key Management**: Improper KMS key access or policy can lock out services from encrypted resources. *Mitigation: Test IAM policies extensively, follow least privilege principle.*

**Dependencies**: AN1 (Core Cloud Infrastructure - RDS, EKS), AN2 (Auth service as a sample for TLS verification), AN5 (Database Schemas)
**Build Order**: #6

---

### Story AN7: Establish Secure Offline Content Storage Mechanism for Mobile Apps
#### Description:
As an engineer, I want to design and implement a secure local storage mechanism for downloaded audio content on mobile devices, ensuring content protection and integrity for offline playback (NFR4.1).
**Details**:
- **Tech Stack**:
    -   **iOS**: `NSFileProtection` for content encryption, iOS Keychain for storage keys if application-level encryption is needed.
    -   **Android**: EncryptedSharedPreferences (for metadata/keys), Android Keystore system (for cryptographic keys), private app storage (internal storage for actual content files).
    -   **React Native**: Libraries like `react-native-keychain` (for secure key storage), `react-native-fs` (for file system access), and custom native modules for platform-specific encryption.
- **Infrastructure**: Mobile app runtime environment.
- **Security Requirements**:
    -   Downloaded audio files must be encrypted at rest on the device.
    -   Encryption keys must be securely stored (e.g., device keychain/keystore).
    -   Content integrity ensured to prevent tampering.
    -   Content must only be accessible by the application itself.
- **Constraints**: This story is for the *mechanism*, not the actual download UI or logic. Focus on the secure storage primitive.
#### Acceptance Criteria
- [x] Design document detailing the chosen secure offline storage approach for iOS and Android, including encryption strategy (e.g., AES-256 for files, key storage).
- [x] iOS implementation: Demo app securely stores a dummy audio file using `NSFileProtection` (e.g., `complete`).
- [x] iOS implementation: A randomly generated encryption key (if using app-level encryption) is securely stored in the iOS Keychain.
- [x] Android implementation: Demo app securely stores a dummy audio file in app-private storage.
- [x] Android implementation: A randomly generated encryption key (if using app-level encryption) is securely stored using Android Keystore/EncryptedSharedPreferences.
- [x] Verification that a non-app process cannot easily access or decrypt the stored content (manual testing via device file explorer, adb shell).
- [x] Function to safely delete securely stored content and associated keys.
- [x] Technical documentation on how to use the secure storage modules/functions within the mobile applications.

#### Effort Estimate: **7 SP**
**Complexity**: Low

**Breakdown**:
- Frontend: 70% (4.9 days) - *Note: "Frontend" here encompasses mobile platform-specific development.*
- Backend: 0%
- DevOps: 0%
- Research/Design: 30% (2.1 days)

**Reasoning**:
```
Day 1: Research & Design
- Research iOS secure file storage (NSFileProtection, Keychain) (4 hrs)
- Research Android secure file storage (Keystore, EncryptedSharedPreferences, internal storage) (4 hrs)
- Design cross-platform approach for secure storage & key management (e.g., using React Native with native modules) (Focus on "mechanism" not actual download logic)

Day 2: iOS Implementation
- Set up a minimal iOS project/module (if React Native, create native module) (3 hrs)
- Implement `NSFileProtection` for a dummy file (3 hrs)
- Implement secure key storage in iOS Keychain (2 hrs)

Day 3: Android Implementation
- Set up a minimal Android project/module (if React Native, create native module) (3 hrs)
- Implement file storage in app-private internal storage (3 hrs)
- Implement secure key storage using Android Keystore/EncryptedSharedPreferences (2 hrs)

Day 4: React Native Integration (if applicable) & Testing
- Integrate native modules into a React Native sample app (if chosen tech stack) (4 hrs)
- Write unit tests for storage mechanisms (e.g., store, retrieve, delete) (4 hrs)

Day 5: Security Verification & Documentation
- Manual testing: attempt to access/decrypt content from outside the app (4 hrs)
- Document the secure storage API and usage guidelines for mobile developers (4 hrs)

Day 6: Refinement & Code Review
- Address code review comments (4 hrs)
- Final testing and bug fixes (4 hrs)

Day 7: Buffer/Complex Edge Cases
- Additional time for complex platform differences, specific Android versions (8 hrs)
```

**Risk Factors**:
- ⚠️ **Platform Differences**: Secure storage implementations differ significantly between iOS and Android. *Mitigation: Allocate dedicated time for platform-specific research and implementation, leverage cross-platform experts if available.*
- ⚠️ **Key Management Complexity**: Securely generating, storing, and retrieving encryption keys on mobile devices can be tricky. *Mitigation: Use OS-provided secure storage (Keychain, Keystore) and avoid custom crypto implementations.*
- ⚠️ **Rooted/Jailbroken Devices**: On compromised devices, perfect security is unattainable. *Mitigation: Document this limitation, implement basic tamper detection if critical (out of scope for MVP secure storage mechanism itself).*

**Dependencies**: None (Can run in parallel with other backend/frontend work, as it's a foundational mobile security piece)
**Build Order**: #7

---

### Story AN8: Implement Subscription & Payment Gateway Integration Framework
#### Description:
As an engineer, I want to integrate with a chosen payment gateway provider (e.g., Stripe) to handle subscription creation, management, and recurring billing securely, so that parents can manage their subscriptions per FR3.7.
**Details**:
- **Tech Stack**: Stripe API, Spring Boot (for backend integration), Webhooks.
- **Infrastructure**: Backend service on EKS interacts with Stripe, webhook endpoint for Stripe notifications.
- **Data Model**:
    -   `subscriptions` table (from AN5) will store Stripe's `subscription_id`, `customer_id`, `plan_id`, `status`, `current_period_end`.
    -   `payment_methods` table (linked to parent_id) to store Stripe's `payment_method_id` (tokenized, not raw card details).
- **Security Requirements**:
    -   PCI DSS compliance handled by Stripe (no raw card data stored on our servers).
    -   Stripe webhooks validated using secret signing.
    -   API keys securely stored (e.g., AWS Secrets Manager).
    -   All communication with Stripe via HTTPS.
- **Constraints**: Focus on initial framework: subscription creation, basic webhook handling. Advanced features like proration, refunds, complex trial management are out of scope for MVP.
#### Acceptance Criteria
- [x] Backend service (e.g., a new `SubscriptionService` in Spring Boot) capable of interacting with the Stripe API.
- [x] Stripe customer creation API integrated: `POST /api/v1/parents/{parentId}/stripe-customer`.
- [x] Endpoint for securely accepting tokenized payment method details from frontend and attaching to Stripe customer: `POST /api/v1/parents/{parentId}/payment-method`.
- [x] Endpoint for creating a new subscription in Stripe: `POST /api/v1/parents/{parentId}/subscribe`.
- [x] Webhook endpoint `/api/v1/stripe/webhook` implemented to receive and validate Stripe events (e.g., `customer.subscription.created`, `customer.subscription.updated`, `customer.subscription.deleted`).
- [x] Webhook handler logic to update `subscriptions` table (AN5) based on Stripe events.
- [x] Stripe API keys securely stored (e.g., in AWS Secrets Manager) and retrieved by the service.
- [x] Unit and integration tests for Stripe API calls and webhook processing.
- [x] Documentation for Stripe integration, API key management, and webhook setup.

#### Effort Estimate: **8 SP**
**Complexity**: Medium

**Breakdown**:
- Backend: 80% (6.4 days)
- DevOps: 10% (0.8 days)
- Research: 10% (0.8 days)

**Reasoning**:
```
Day 1: Research & Stripe Account Setup
- Understand Stripe subscription model, API, webhooks (4 hrs)
- Set up Stripe test account, API keys (2 hrs)
- Design SubscriptionService architecture, endpoints (2 hrs)

Day 2: Customer & Payment Method Management
- Implement Stripe customer creation (e.g., linked to parent_id) (4 hrs)
- Implement endpoint to attach a tokenized payment method to a customer (4 hrs)

Day 3: Subscription Creation
- Implement endpoint to create a subscription with a given plan and payment method (8 hrs)
- Update local `subscriptions` table (AN5) with initial data.

Day 4: Webhook Handler - Setup & Validation
- Implement webhook endpoint `/api/v1/stripe/webhook` (4 hrs)
- Implement Stripe webhook signature verification (crucial for security) (4 hrs)

Day 5: Webhook Handler - Event Processing
- Implement logic to handle key webhook events (e.g., `customer.subscription.created`, `updated`, `deleted`) (6 hrs)
- Update local `subscriptions` table based on webhook events (2 hrs)

Day 6: Error Handling & Security
- Implement robust error handling for Stripe API calls and webhooks (4 hrs)
- Securely store Stripe API keys (e.g., integrate with AWS Secrets Manager) (4 hrs)

Day 7: Testing & Documentation
- Write comprehensive unit and integration tests for all Stripe interactions and webhook flows (6 hrs)
- Document Stripe integration details, webhook events, troubleshooting (2 hrs)

Day 8: Code Review & Refinement
- Address code review comments (4 hrs)
- Final bug fixes and testing (4 hrs)
```

**Risk Factors**:
- ⚠️ **PCI Compliance**: While Stripe handles raw card data, improper integration (e.g., logging sensitive data) can expose us to compliance risks. *Mitigation: Strictly adhere to Stripe's recommendations for PCI compliance; use tokenization only; regular security audits.*
- ⚠️ **Webhook Reliability**: Webhooks can fail, be delayed, or be received out of order. *Mitigation: Implement idempotent webhook handlers, utilize dead-letter queues, integrate with monitoring for webhook failures.*
- ⚠️ **API Key Management**: Hardcoding API keys is a significant security risk. *Mitigation: Use AWS Secrets Manager or equivalent; rotate keys regularly.*

**Dependencies**: AN2 (Parent Authentication for `parentId`), AN5 (Database Schemas for `subscriptions` and `subscription_plans`), AN6 (Data Encryption for secure API communication).
**Build Order**: #8

---

### Story AN9: Plan for COPPA & GDPR Compliance (Privacy Policy, Consent Flow)
#### Description:
As a legal and product owner, I want to draft the privacy policy and outline the parental consent collection flow, ensuring full compliance with COPPA and GDPR requirements, so that our application adheres to critical child privacy regulations (NFR4.1, NFR4.2, NFR4.3).
**Details**:
- **Compliance Focus**: Children's Online Privacy Protection Act (COPPA), General Data Protection Regulation (GDPR).
- **Deliverables**:
    -   Detailed outline for a privacy policy specifically addressing child data collection and parental rights.
    -   User flow diagrams for parental consent acquisition (e.g., during registration, when creating child profiles).
    -   Requirements for data minimization: identifying what PII is collected from parents vs. children, and why.
    -   Requirements for data retention policies for child data.
    -   Technical requirements derived for Backend and Frontend teams to implement consent collection and data management.
- **Constraints**: This story is primarily a **design and planning** story, not an implementation one. The output will be requirements for other stories.
#### Acceptance Criteria
- [x] Draft privacy policy outline completed, addressing:
    -   What data is collected from children and parents.
    -   How data is used.
    -   Data sharing practices (if any).
    -   Parents' rights to review/delete child data.
    -   Contact information for privacy inquiries.
- [x] Detailed user flow diagram for parental consent collection during the parent registration process.
- [x] Detailed user flow diagram for parental consent specific to creating a child profile.
- [x] List of specific PII collected from children (e.g., child's name, age range, listening history) and justification.
- [x] Defined data retention periods for child-related data.
- [x] Documented technical requirements for:
    -   Storing parental consent status in the database (e.g., `parents.has_given_child_data_consent`).
    -   Frontend UI elements for displaying privacy policy and collecting consent checkboxes.
    -   Backend APIs for parents to view/request deletion of child data (future stories).
- [x] Review of consent flows by a legal expert (internal or external).

#### Effort Estimate: **4 SP**
**Complexity**: Medium

**Breakdown**:
- Product/Legal: 70% (2.8 days)
- Tech Lead/Architect: 30% (1.2 days)

**Reasoning**:
```
Day 1: Research & Initial Draft
- Review COPPA and GDPR guidelines for child-focused apps (4 hrs)
- Draft initial privacy policy outline, focusing on required sections (4 hrs)

Day 2: Consent Flow Design
- Design parental consent flow for registration (UI/UX wireframes or diagrams) (4 hrs)
- Design parental consent flow for child profile creation (4 hrs)

Day 3: Data Mapping & Technical Requirements
- Map PII collected vs. legal requirements (data minimization) (4 hrs)
- Define technical requirements for backend/frontend for consent storage and UI (3 hrs)
- Outline data retention policies (1 hr)

Day 4: Review & Refinement
- Internal review with relevant stakeholders (product, legal, tech lead) (4 hrs)
- Refine policy outline and flows based on feedback (4 hrs)
```

**Risk Factors**:
- ⚠️ **Legal Misinterpretation**: Incorrect interpretation of COPPA/GDPR can lead to non-compliance and legal penalties. *Mitigation: Involve legal counsel early and explicitly; prioritize compliance.*
- ⚠️ **Ambiguous Requirements**: Vague technical requirements derived from this story could lead to implementation errors. *Mitigation: Tech Lead should actively participate in requirement definition to ensure clarity and specificity.*
- ⚠️ **Scope Creep**: This is a planning story, but could expand into implementation if not managed. *Mitigation: Clearly define deliverables as 'plans' and 'requirements' for *other* stories.*

**Dependencies**: AN6 (Data Encryption, as compliance relies on secure data handling).
**Build Order**: #9

---

## ⚙️ Backend Stories

### Story B1: Develop Parent Account API (Registration & Login)
#### Description:
As a parent, I want to register for an account and log in securely, so that I can access the platform and manage my family's profiles.
**Details**:
- **Endpoints**:
    -   `POST /api/v1/parents/register`:
        -   Request: `{ "email": "string", "password": "string" }`
        -   Response: `201 Created` or `400 Bad Request` with error details.
    -   `POST /api/v1/parents/login`:
        -   Request: `{ "email": "string", "password": "string" }`
        -   Response: `200 OK`, `{ "access_token": "jwt_string", "expires_in": 3600 }` or `401 Unauthorized`.
    -   `GET /api/v1/parents/me`: (Secured with JWT)
        -   Response: `200 OK`, `{ "id": "uuid", "email": "string", "is_verified": true }`
- **Data Model**: `parents` table (from AN5) including `id`, `email`, `password_hash`, `is_verified`, `created_at`, `updated_at`.
- **Business Rules**:
    -   Email must be unique and valid format.
    -   Password must meet strength requirements (e.g., min 8 chars, 1 uppercase, 1 number, 1 special char).
    -   Password hashing using BCrypt.
    -   Email verification required for full account activation (implemented by AN2 framework, but called here).
- **Performance**: Login/Registration < 200ms p95.
- **Error Handling**: Specific error codes/messages for invalid input, email already exists, invalid credentials.
#### Acceptance Criteria
- [x] `POST /api/v1/parents/register` endpoint successfully creates a new parent account with a hashed password.
- [x] Registration fails with `400 Bad Request` if email is invalid or already registered.
- [x] Registration triggers a (mock/placeholder) email verification process.
- [x] `POST /api/v1/parents/login` endpoint successfully authenticates a parent and returns a valid JWT.
- [x] Login fails with `401 Unauthorized` for incorrect email/password.
- [x] `GET /api/v1/parents/me` endpoint returns parent details when a valid JWT is provided in the `Authorization` header.
- [x] `GET /api/v1/parents/me` returns `401 Unauthorized` if no or invalid JWT is provided.
- [x] All endpoints enforce request body validation (e.g., email format, password strength).
- [x] Unit and integration tests cover happy paths and error conditions for all endpoints.
- [x] OpenAPI/Swagger documentation updated for these endpoints.

#### Effort Estimate: **4 SP**
**Complexity**: Low

**Breakdown**:
- Backend: 90% (3.6 days)
- DevOps: 10% (0.4 days)

**Reasoning**:
```
Day 1: Registration Endpoint
- Implement `POST /api/v1/parents/register` endpoint (controller, service logic) (5 hrs)
- Integrate password hashing (BCrypt) and parent entity persistence (3 hrs)

Day 2: Login Endpoint
- Implement `POST /api/v1/parents/login` endpoint (controller, service logic) (5 hrs)
- Integrate JWT generation and return (3 hrs)

Day 3: User Details & Validation
- Implement `GET /api/v1/parents/me` endpoint (3 hrs)
- Add request body validation (email, password strength) (3 hrs)
- Integrate with email verification placeholder from AN2 (2 hrs)

Day 4: Testing, Documentation & Refinement
- Write unit and integration tests for all endpoints (5 hrs)
- Update OpenAPI documentation (1 hr)
- Code review and address feedback (2 hrs)
```

**Risk Factors**:
- ⚠️ **Weak Password Policy**: Insufficient password strength requirements could lead to security breaches. *Mitigation: Implement strong validation rules and communicate them to users.*
- ⚠️ **Brute-force Attacks**: Login endpoints are targets for brute-force. *Mitigation: Implement rate limiting (future story or API Gateway feature).*

**Dependencies**: AN1 (Infrastructure), AN2 (Auth Framework), AN5 (User Schema)
**Build Order**: #10

---

### Story B2: Develop Child Profile Management API (CRUD)
#### Description:
As a parent, I want to create, view, update, and delete child profiles linked to my account, so that each child has their personalized settings and listening experience (FR3.1).
**Details**:
- **Endpoints**:
    -   `POST /api/v1/children`: (Secured, Parent JWT required)
        -   Request: `{ "name": "string", "avatar_url": "string", "age_range_max": "int" }`
        -   Response: `201 Created`, `{ "id": "uuid", "name": "string", ... }` or `400 Bad Request`.
    -   `GET /api/v1/children`: (Secured, Parent JWT required)
        -   Response: `200 OK`, `[ { "id": "uuid", "name": "string", ... }, ... ]`
    -   `GET /api/v1/children/{childId}`: (Secured, Parent JWT required, check parent ownership)
        -   Response: `200 OK`, `{ "id": "uuid", "name": "string", ... }` or `404 Not Found`, `403 Forbidden`.
    -   `PUT /api/v1/children/{childId}`: (Secured, Parent JWT required, check parent ownership)
        -   Request: `{ "name": "string", "avatar_url": "string", "age_range_max": "int" }` (partial updates allowed)
        -   Response: `200 OK`, `{ "id": "uuid", "name": "string", ... }` or `404 Not Found`, `403 Forbidden`.
    -   `DELETE /api/v1/children/{childId}`: (Secured, Parent JWT required, check parent ownership)
        -   Response: `204 No Content` or `404 Not Found`, `403 Forbidden`.
- **Data Model**: `children` table (from AN5) including `id`, `parent_id`, `name`, `avatar_url`, `age_range_max`, `created_at`, `updated_at`.
- **Business Rules**:
    -   A child profile must belong to an authenticated parent.
    -   Parents can only manage their own children's profiles.
    -   `age_range_max` should be within a defined valid range (e.g., 2-12).
    -   `name` must not be empty.
- **Performance**: CRUD operations < 100ms p95.
- **Error Handling**: `400` for invalid input, `403` for unauthorized access (not parent's child), `404` for child not found.
#### Acceptance Criteria
- [x] `POST /api/v1/children` successfully creates a new child profile linked to the authenticated parent.
- [x] `GET /api/v1/children` returns a list of all child profiles belonging to the authenticated parent.
- [x] `GET /api/v1/children/{childId}` returns details for a specific child profile if owned by the parent.
- [x] `PUT /api/v1/children/{childId}` successfully updates an existing child profile's details.
- [x] `DELETE /api/v1/children/{childId}` successfully removes a child profile.
- [x] All endpoints verify parent ownership of the child profile, returning `403 Forbidden` if not owned.
- [x] All creation/update endpoints include validation for `name` and `age_range_max`.
- [x] Unit and integration tests cover happy paths, parent ownership checks, and error conditions.
- [x] OpenAPI/Swagger documentation updated for these endpoints.

#### Effort Estimate: **5 SP**
**Complexity**: Medium

**Breakdown**:
- Backend: 90% (4.5 days)
- DevOps: 10% (0.5 days)

**Reasoning**:
```
Day 1: Setup & Create Endpoint
- Set up Spring Boot controllers, services, repositories for `Child` entity (3 hrs)
- Implement `POST /api/v1/children` for creating child profiles, linking to parent via JWT (5 hrs)

Day 2: Read Endpoints
- Implement `GET /api/v1/children` to list parent's children (4 hrs)
- Implement `GET /api/v1/children/{childId}` to retrieve a single child, including parent ownership check (4 hrs)

Day 3: Update & Delete Endpoints
- Implement `PUT /api/v1/children/{childId}` for updating child profiles, including ownership check (5 hrs)
- Implement `DELETE /api/v1/children/{childId}` for deleting child profiles, including ownership check (3 hrs)

Day 4: Validation & Error Handling
- Add input validation for `name`, `avatar_url`, `age_range_max` (4 hrs)
- Implement specific error handling for `400`, `403`, `404` responses (4 hrs)

Day 5: Testing, Documentation & Refinement
- Write comprehensive unit and integration tests (6 hrs)
- Update OpenAPI documentation (1 hr)
- Code review and address feedback (1 hr)
```

**Risk Factors**:
- ⚠️ **Authorization Logic Flaws**: Incorrect parent ownership checks could allow unauthorized access to child profiles. *Mitigation: Implement robust authorization checks in service layer, strong unit/integration tests for these scenarios.*
- ⚠️ **Data Integrity**: Deleting a child profile might leave orphaned data in other tables (e.g., listening history). *Mitigation: Consider cascade deletes or soft deletes if applicable (future scope, but note as a design consideration).*

**Dependencies**: AN1 (Infrastructure), AN5 (Child Profile Schema), B1 (Parent Authentication)
**Build Order**: #11

---

### Story B3: Develop Content Ingestion API
#### Description:
As a content manager, I want to upload audio files and their associated metadata (title, description, age rating, categories) to the platform, so that the curated content library can be populated (FR1.1, FR1.2, FR1.3).
**Details**:
- **Endpoints**:
    -   `POST /api/v1/content/upload`: (Secured, Content Manager role JWT required, future scope)
        -   Request: `multipart/form-data` including `file` (audio binary) and `metadata` (JSON: `{ "title": "string", "description": "string", "category_id": "uuid", "age_rating_min": "int", "age_rating_max": "int", "is_premium": "boolean" }`).
        -   Response: `201 Created`, `{ "content_id": "uuid", "audio_file_url": "s3_url" }` or `400 Bad Request`.
- **Data Model**: `content_items` table (from AN5) including `id`, `title`, `description`, `category_id`, `age_rating_min`, `age_rating_max`, `audio_file_url`, `duration`, `thumbnail_url`, `is_premium`, `created_at`, `updated_at`.
- **Business Rules**:
    -   Audio files (e.g., MP3, M4A) uploaded to S3.
    -   Metadata stored in PostgreSQL.
    -   `category_id` must reference an existing category.
    -   `age_rating_min` and `age_rating_max` within sensible bounds (e.g., 0-18).
    -   Extract audio duration and possibly generate a basic waveform/thumbnail (future scope, for MVP: metadata manually provided or default).
- **Integrations**: AWS S3 for file storage.
- **Performance**: File upload and metadata processing < 500ms p95 (excluding actual file transfer time).
- **Error Handling**: `400` for invalid metadata, `500` for S3 upload failures.
#### Acceptance Criteria
- [x] `POST /api/v1/content/upload` endpoint successfully accepts a multipart file upload and JSON metadata.
- [x] The uploaded audio file is stored in the configured S3 bucket (AN1).
- [x] Content metadata (title, description, age rating, category, premium status) is saved to the `content_items` table (AN5).
- [x] The `audio_file_url` in the database points to the S3 object URL (or CDN URL if AN3 is integrated).
- [x] Validation ensures `category_id` exists and age ratings are valid.
- [x] The endpoint returns the created `content_id` and the final `audio_file_url`.
- [x] Error handling for invalid input (400) and S3 upload failures (500).
- [x] Unit and integration tests cover file upload, metadata persistence, and error conditions.
- [x] OpenAPI/Swagger documentation updated for this endpoint.

#### Effort Estimate: **6 SP**
**Complexity**: Medium

**Breakdown**:
- Backend: 80% (4.8 days)
- DevOps: 20% (1.2 days)

**Reasoning**:
```
Day 1: Design & Setup
- Design `ContentService`, controller, DTOs for ingestion (4 hrs)
- Configure Spring Boot for multipart file uploads (4 hrs)

Day 2: S3 Integration
- Implement S3 file upload logic in `ContentService` (e.g., using AWS SDK) (6 hrs)
- Secure S3 write access for the service (IAM roles) (2 hrs)

Day 3: Metadata Persistence
- Implement `ContentItem` entity and repository (4 hrs)
- Persist metadata to `content_items` table after successful S3 upload (4 hrs)

Day 4: Validation & Error Handling
- Add validation for all metadata fields (e.g., category existence, age ranges) (5 hrs)
- Implement error handling for S3 failures, DB issues, validation errors (3 hrs)

Day 5: Testing & Documentation
- Write unit tests for content service logic (5 hrs)
- Write integration tests for endpoint, S3 interaction, DB persistence (2 hrs)
- Update OpenAPI documentation (1 hr)

Day 6: Code Review & Refinement
- Address code review comments (4 hrs)
- Final bug fixes and testing (4 hrs)
```

**Risk Factors**:
- ⚠️ **Large File Uploads**: Handling very large audio files might require streaming or specific buffer configurations. *Mitigation: Test with various file sizes; consider pre-signed URLs for direct client-to-S3 uploads for very large files (future optimization).*
- ⚠️ **S3 Permissions**: Incorrect IAM permissions for S3 bucket access can lead to upload failures. *Mitigation: Thoroughly test IAM role policies for the content ingestion service.*
- ⚠️ **Content Processing**: Extracting duration, generating waveforms, or transcoding is not in scope but will become a dependency later. *Mitigation: Plan for a separate microservice for content processing post-upload.*

**Dependencies**: AN1 (Infrastructure, S3), AN5 (Content Schema), AN3 (CDN - for `audio_file_url` to potentially point to CDN).
**Build Order**: #12

---

### Story B4: Develop Content Browsing & Search API (Categories, Age Filter)
#### Description:
As a child, I want to browse content by categories and search for specific items, and as a parent, I want content filtered by age, so that I can easily discover age-appropriate content (FR1.2, FR1.3, FR1.4).
**Details**:
- **Endpoints**:
    -   `GET /api/v1/content`: (Secured, Child/Parent JWT)
        -   Query Params: `category_id` (UUID, optional), `search_term` (string, optional), `child_id` (UUID, required for age filtering).
        -   Response: `200 OK`, `[ { "id": "uuid", "title": "string", "description": "string", "audio_file_url": "url", "category_name": "string", "age_rating_min": "int", "age_rating_max": "int", "is_premium": "boolean", "thumbnail_url": "url", "duration": "int" }, ... ]`.
    -   `GET /api/v1/categories`: (Public)
        -   Response: `200 OK`, `[ { "id": "uuid", "name": "string", "description": "string" }, ... ]`.
- **Data Model**: `content_items`, `categories` tables (from AN5). `children` table (from AN5) to retrieve `age_range_max` for filtering.
- **Business Rules**:
    -   If `child_id` is provided, content must be filtered such that `content_item.age_rating_min <= child.age_range_max`.
    -   `search_term` performs a case-insensitive partial match on `title` and `description`.
    -   Results can be filtered by `category_id`.
    -   Pagination and sorting (e.g., by `created_at`, `title`) are implicit (basic implementation first, advanced later).
- **Performance**: Queries < 300ms p95. Consider indexing `title`, `description` (full-text search later), `category_id`.
- **Error Handling**: `400` for invalid `child_id` or other params, `404` for child not found.
#### Acceptance Criteria
- [x] `GET /api/v1/categories` endpoint returns a list of all available content categories.
- [x] `GET /api/v1/content` endpoint returns all content when no filters are applied (basic browsing).
- [x] `GET /api/v1/content?category_id={uuid}` filters content by a specific category.
- [x] `GET /api/v1/content?search_term={query}` filters content by title and description using case-insensitive partial match.
- [x] `GET /api/v1/content?child_id={uuid}` filters content based on the child's `age_range_max` (i.e., `content.age_rating_min <= child.age_range_max`).
- [x] Multiple filters (category, search, age) can be combined and applied correctly.
- [x] If `child_id` is provided but not found, returns `404 Not Found`.
- [x] Implement pagination for content browsing (e.g., `limit`, `offset` or `page`, `size`).
- [x] Unit and integration tests cover all filtering combinations and edge cases.
- [x] OpenAPI/Swagger documentation updated for these endpoints.

#### Effort Estimate: **6 SP**
**Complexity**: Medium

**Breakdown**:
- Backend: 90% (5.4 days)
- DevOps: 10% (0.6 days)

**Reasoning**:
```
Day 1: Category API & Setup
- Implement `GET /api/v1/categories` endpoint (controller, service, repository) (4 hrs)
- Initial setup for content browsing controller/service (4 hrs)

Day 2: Basic Content Listing & Filtering
- Implement `GET /api/v1/content` to retrieve all content (basic listing) (4 hrs)
- Add filtering by `category_id` (4 hrs)

Day 3: Search & Age Filtering Logic
- Implement `search_term` filtering (SQL `LIKE` or similar) on title/description (4 hrs)
- Implement `child_id` parameter to fetch child's `age_range_max` (from B2/AN5) (2 hrs)
- Apply age-based filtering logic (`content.age_rating_min <= child.age_range_max`) (2 hrs)

Day 4: Combined Filters & Pagination
- Refactor query logic to support combining multiple filters (category, search, age) (6 hrs)
- Implement pagination (e.g., `LIMIT` and `OFFSET` clauses) (2 hrs)

Day 5: Performance & Error Handling
- Add necessary database indexes for `category_id`, `age_rating_min`, `title`, `description` (2 hrs)
- Implement error handling for invalid child ID, no content found (404) (4 hrs)
- Review query performance (2 hrs)

Day 6: Testing, Documentation & Refinement
- Write comprehensive unit and integration tests for all filters and combinations (6 hrs)
- Update OpenAPI documentation (1 hr)
- Code review and address feedback (1 hr)
```

**Risk Factors**:
- ⚠️ **Search Performance**: Simple `LIKE` queries can be slow on large datasets. *Mitigation: Add appropriate indexes; consider migrating to a dedicated search engine (e.g., OpenSearch/Elasticsearch) if performance becomes an issue (future optimization).*
- ⚠️ **Complex Query Logic**: Combining multiple filters can lead to complex and error-prone SQL queries. *Mitigation: Use a query builder/ORM effectively; extensive unit testing of query generation.*
- ⚠️ **Data Volume**: As content grows, pagination and filter performance might degrade. *Mitigation: Proactive indexing; explore cursor-based pagination for deep queries (future optimization).*

**Dependencies**: AN1 (Infrastructure), AN5 (Content & Category Schemas), B2 (Child Profiles for age filtering context), B3 (Content Ingestion to populate data).
**Build Order**: #13

---

### Story B5: Develop Parental Control API (Age Filtering)
#### Description:
As a parent, I want to set and update the maximum age-appropriateness filter for each child's profile, so that I can control the content visible to my child (FR3.2).
**Details**:
- **Endpoints**:
    -   `PUT /api/v1/children/{childId}/age-filter`: (Secured, Parent JWT required, check parent ownership)
        -   Request: `{ "age_range_max": "int" }`
        -   Response: `200 OK` or `400 Bad Request`, `403 Forbidden`, `404 Not Found`.
- **Data Model**: `children` table (from AN5) - specifically updating the `age_range_max` column.
- **Business Rules**:
    -   The `age_range_max` must be a valid age (e.g., 2-16).
    -   Only the owning parent can update this setting for their child.
    -   Updates should be reflected immediately in content browsing APIs (B4).
- **Performance**: Update operation < 50ms p95.
- **Error Handling**: `400` for invalid age, `403` for unauthorized, `404` for child not found.
#### Acceptance Criteria
- [x] `PUT /api/v1/children/{childId}/age-filter` successfully updates the `age_range_max` for the specified child profile.
- [x] The endpoint returns `403 Forbidden` if the authenticated parent does not own `childId`.
- [x] The endpoint returns `404 Not Found` if `childId` does not exist.
- [x] `age_range_max` value is validated to be within a reasonable range (e.g., 2 to 16).
- [x] Content browsing API (B4) immediately reflects the updated age filter for the child.
- [x] Unit and integration tests cover happy path, unauthorized access, invalid input, and non-existent child.
- [x] OpenAPI/Swagger documentation updated for this endpoint.

#### Effort Estimate: **2 SP**
**Complexity**: Low

**Breakdown**:
- Backend: 90% (1.8 days)
- DevOps: 10% (0.2 days)

**Reasoning**:
```
Day 1: Endpoint Implementation
- Implement `PUT /api/v1/children/{childId}/age-filter` controller and service logic (4 hrs)
- Integrate with `ChildService` (B2) to update `age_range_max` (3 hrs)
- Implement parent ownership check using context from JWT (1 hr)

Day 2: Validation, Testing & Documentation
- Add validation for `age_range_max` (e.g., 2-16) (2 hrs)
- Write unit and integration tests (happy path, error conditions, authorization) (4 hrs)
- Update OpenAPI documentation (1 hr)
- Code review and address feedback (1 hr)
```

**Risk Factors**:
- ⚠️ **Authorization Bypass**: Critical to ensure strong parent ownership check. *Mitigation: Re-use and thoroughly test authorization logic from B2.*
- ⚠️ **Inconsistent Data**: If content browsing API doesn't pick up changes immediately, UX will be poor. *Mitigation: Ensure caching layers (if any) are invalidated or bypassed for real-time updates.*

**Dependencies**: B2 (Child Profile Management API for updating child data, parent ownership checks), B4 (Content Browsing API relies on this setting).
**Build Order**: #14

---

### Story B6: Develop Audio Streaming API (Adaptive Bitrate, DRM)
#### Description:
As a child, I want to stream audio content seamlessly with low latency, so that I can enjoy my music and stories without interruption (FR4.1, NFR1.1).
**Details**:
- **Endpoints**:
    -   `GET /api/v1/stream/{contentId}`: (Secured, Child/Parent JWT, check content access)
        -   Response: `200 OK` with audio stream (HLS/DASH manifest or direct audio file), or `403 Forbidden`, `404 Not Found`.
- **Data Model**: `content_items` table (from AN5) for `audio_file_url`. `children` table (for age/content blocking checks).
- **Business Rules**:
    -   Must check if content is accessible to the current `child_id` (based on age filter, content blocking from B5/B8).
    -   Serve audio from CDN (AN3) for low latency.
    -   For MVP, adaptive bitrate will be handled by providing multiple pre-encoded files in S3 or relying on a single high-quality stream. **DRM (Digital Rights Management) is complex and will be considered out of initial MVP scope, or a basic token-based access control will serve as a placeholder.** This story focuses on delivering the stream.
- **Integrations**: AWS S3 (origin for CDN), AWS CloudFront (AN3).
- **Performance**: Stream initiation < 100ms p95.
- **Error Handling**: `403` if child cannot access content, `404` if content not found.
#### Acceptance Criteria
- [x] `GET /api/v1/stream/{contentId}` endpoint is implemented to serve audio content.
- [x] The endpoint verifies if the `contentId` exists and is available (404 if not).
- [x] The endpoint verifies if the requested content is accessible to the current child profile (based on age filter and future content blocking rules), returning `403 Forbidden` if not accessible.
- [x] The endpoint returns a redirect or serves the audio content directly from the CDN (AN3) or S3 (if CDN not yet integrated/cached).
- [x] Content is streamed without interruption for typical network conditions.
- [x] For MVP, a single audio file format (e.g., MP3) is served. (Adaptive bitrate encoding itself is a pre-processing step, the API serves the output).
- [x] Unit and integration tests cover content access checks and successful stream initiation.
- [x] OpenAPI/Swagger documentation updated for this endpoint.

#### Effort Estimate: **5 SP**
**Complexity**: Medium

**Breakdown**:
- Backend: 90% (4.5 days)
- DevOps: 10% (0.5 days)

**Reasoning**:
```
Day 1: Setup & Basic Stream Retrieval
- Design `StreamingService` and controller (4 hrs)
- Implement basic logic to retrieve `audio_file_url` from `content_items` table (4 hrs)

Day 2: Access Control Logic
- Integrate `ChildService` (B2) and `ContentService` (B4) to check age-appropriateness (B5) (5 hrs)
- Implement content blocking checks (placeholder for B8) (3 hrs)

Day 3: CDN/S3 Integration
- Implement secure redirection or proxying to CloudFront URL (AN3) (6 hrs)
- Ensure generated URLs have appropriate temporary tokens/signatures for limited access if needed (2 hrs)

Day 4: Stream Delivery & Error Handling
- Configure Spring Boot to serve large files/redirect efficiently (4 hrs)
- Implement robust error handling (403 forbidden, 404 not found) (4 hrs)

Day 5: Testing, Documentation & Refinement
- Write comprehensive unit and integration tests (happy path, access denied, not found) (6 hrs)
- Update OpenAPI documentation (1 hr)
- Code review and address feedback (1 hr)
```

**Risk Factors**:
- ⚠️ **DRM Scope Creep**: DRM is highly complex and costly. *Mitigation: Clearly define MVP as "token-based access control" not full DRM. Document this as a future, high-effort item.*
- ⚠️ **Content Accessibility Issues**: Incorrect access control logic could lead to children accessing inappropriate content or legitimate content being blocked. *Mitigation: Rigorous testing of access control logic across various child profiles and content age ratings.*
- ⚠️ **Network Latency**: While CDN helps, network issues can still cause buffering. *Mitigation: Monitor CDN performance, ensure efficient client-side buffering (Frontend).*

**Dependencies**: AN3 (CDN), AN5 (Content Schema), B3 (Content Ingestion), B4 (Content Browsing), B5 (Age Filtering), B8 (Parental Control - Content Blocking, placeholder for now).
**Build Order**: #15

---

### Story B7: Implement PIN Protection for Parental Dashboard Access
#### Description:
As a parent, I want to set a 4-digit PIN for accessing the parental dashboard and settings changes, so that my child cannot tamper with the controls (FR3.6, NFR2.1).
**Details**:
- **Endpoints**:
    -   `POST /api/v1/parents/pin/set`: (Secured, Parent JWT required)
        -   Request: `{ "pin": "string" }`
        -   Response: `200 OK` or `400 Bad Request`.
    -   `POST /api/v1/parents/pin/verify`: (Secured, Parent JWT required)
        -   Request: `{ "pin": "string" }`
        -   Response: `200 OK` or `401 Unauthorized`.
- **Data Model**: `parents` table (AN5) updated with a new column `pin_hash` (string) and `pin_set_at` (timestamp).
- **Business Rules**:
    -   PIN must be exactly 4 digits.
    -   PIN stored as a hash (e.g., using BCrypt, similar to passwords).
    -   Parent can only set/verify their own PIN.
    -   After successful verification, a temporary token (different from session JWT) can be issued for dashboard access (Frontend stores this, not explicitly API's responsibility to generate, but could be).
- **Performance**: PIN set/verify < 100ms p95.
- **Error Handling**: `400` for invalid PIN format, `401` for incorrect PIN.
#### Acceptance Criteria
- [x] `parents` table schema updated with `pin_hash` and `pin_set_at` columns.
- [x] `POST /api/v1/parents/pin/set` endpoint successfully hashes and stores a 4-digit PIN for the authenticated parent.
- [x] Setting a PIN fails with `400 Bad Request` if the PIN is not exactly 4 digits.
- [x] `POST /api/v1/parents/pin/verify` endpoint successfully verifies the provided PIN against the stored hash.
- [x] Verification fails with `401 Unauthorized` for an incorrect PIN.
- [x] PINs are hashed using a strong, industry-standard algorithm (e.g., BCrypt).
- [x] Unit and integration tests cover PIN setting, verification (correct/incorrect), and invalid input.
- [x] OpenAPI/Swagger documentation updated for these endpoints.

#### Effort Estimate: **3 SP**
**Complexity**: Low

**Breakdown**:
- Backend: 90% (2.7 days)
- DevOps: 10% (0.3 days)

**Reasoning**:
```
Day 1: Schema Update & Set PIN Endpoint
- Add `pin_hash` and `pin_set_at` to `parents` table via Liquibase migration (AN5 context) (2 hrs)
- Implement `POST /api/v1/parents/pin/set` controller and service (4 hrs)
- Integrate PIN hashing with BCrypt (2 hrs)

Day 2: Verify PIN Endpoint & Validation
- Implement `POST /api/v1/parents/pin/verify` controller and service (4 hrs)
- Implement 4-digit PIN validation for set/verify endpoints (2 hrs)
- Integrate PIN hash comparison (2 hrs)

Day 3: Testing, Documentation & Refinement
- Write unit and integration tests for set/verify (happy path, bad input, wrong PIN) (5 hrs)
- Update OpenAPI documentation (1 hr)
- Code review and address feedback (2 hrs)
```

**Risk Factors**:
- ⚠️ **PIN Security**: Storing PINs insecurely or using weak hashing algorithms. *Mitigation: Use BCrypt with a strong work factor; ensure `pin_hash` is not directly exposed.*
- ⚠️ **Brute-Force Attack on PIN**: Rapid attempts to guess PIN. *Mitigation: Implement rate limiting on the `/verify` endpoint (future story or API Gateway feature).*

**Dependencies**: B1 (Parent Login for parent context), B2 (Child Profile context for parental dashboard). AN5 (Parent Schema Update).
**Build Order**: #16

---

### Story B8: Develop Parental Control API (Content Blocking)
#### Description:
As a parent, I want to explicitly block specific songs, audiobooks, or entire categories from a child's profile, so that I can further customize their content access (FR3.3).
**Details**:
- **Endpoints**:
    -   `POST /api/v1/children/{childId}/blocked-content`: (Secured, Parent JWT, check parent ownership)
        -   Request: `{ "content_item_id": "uuid", "category_id": "uuid" }` (either one, not both)
        -   Response: `201 Created` or `400 Bad Request`, `403 Forbidden`, `404 Not Found`.
    -   `DELETE /api/v1/children/{childId}/blocked-content`: (Secured, Parent JWT, check parent ownership)
        -   Request: `{ "content_item_id": "uuid", "category_id": "uuid" }` (either one, not both)
        -   Response: `204 No Content` or `404 Not Found`, `403 Forbidden`.
    -   `GET /api/v1/children/{childId}/blocked-content`: (Secured, Parent JWT, check parent ownership)
        -   Response: `200 OK`, `{ "blocked_content_items": ["uuid", ...], "blocked_categories": ["uuid", ...] }`.
- **Data Model**: New join tables to track blocked content:
    -   `child_blocked_content_items`: `child_id (FK), content_item_id (FK)` (composite PK).
    -   `child_blocked_categories`: `child_id (FK), category_id (FK)` (composite PK).
- **Business Rules**:
    -   A parent can block/unblock content or categories for their own child only.
    -   Blocking a category implies all content within that category is blocked.
    -   Content browsing (B4) and streaming (B6) APIs must enforce these blocks.
- **Performance**: Block/unblock operations < 100ms p95. Retrieval of blocked list < 150ms p95.
- **Error Handling**: `400` for invalid input, `403` for unauthorized, `404` for child/content/category not found.
#### Acceptance Criteria
- [x] Database schemas (AN5) updated with `child_blocked_content_items` and `child_blocked_categories` tables.
- [x] `POST /api/v1/children/{childId}/blocked-content` successfully blocks a specific content item or category for a child.
- [x] `DELETE /api/v1/children/{childId}/blocked-content` successfully unblocks a specific content item or category.
- [x] `GET /api/v1/children/{childId}/blocked-content` returns a list of all content items and categories blocked for a child.
- [x] All endpoints enforce parent ownership of `childId` and `403 Forbidden` if not owned.
- [x] Content browsing (B4) and streaming (B6) APIs correctly filter out blocked content/categories for the child.
- [x] Validation ensures `content_item_id` and `category_id` exist when blocking/unblocking.
- [x] Unit and integration tests cover blocking/unblocking, retrieval, authorization, and how B4/B6 APIs respond.
- [x] OpenAPI/Swagger documentation updated for these endpoints.

#### Effort Estimate: **6 SP**
**Complexity**: Medium

**Breakdown**:
- Backend: 90% (5.4 days)
- DevOps: 10% (0.6 days)

**Reasoning**:
```
Day 1: Schema Update & Design
- Add `child_blocked_content_items` and `child_blocked_categories` tables (AN5 context) (3 hrs)
- Design `ParentalControlService` and controller for blocking (5 hrs)

Day 2: Block Content/Category Endpoints
- Implement `POST /api/v1/children/{childId}/blocked-content` for content item blocking (4 hrs)
- Implement `POST /api/v1/children/{childId}/blocked-content` for category blocking (4 hrs)

Day 3: Unblock & Get Blocked List
- Implement `DELETE /api/v1/children/{childId}/blocked-content` for content/category unblocking (5 hrs)
- Implement `GET /api/v1/children/{childId}/blocked-content` to retrieve blocked lists (3 hrs)

Day 4: Integration with Browsing/Streaming
- Update `ContentBrowsingService` (B4) to filter out blocked content/categories (6 hrs)
- Update `StreamingService` (B6) to deny access to blocked content (2 hrs)

Day 5: Validation, Error Handling & Testing
- Add validation for `content_item_id`, `category_id` existence (3 hrs)
- Implement error handling (400, 403, 404) (3 hrs)
- Write unit tests for blocking/unblocking logic (2 hrs)

Day 6: Integration Testing, Documentation & Refinement
- Write integration tests for all blocking endpoints, verify B4/B6 filtering (6 hrs)
- Update OpenAPI documentation (1 hr)
- Code review and address feedback (1 hr)
```

**Risk Factors**:
- ⚠️ **Performance Impact on Content APIs**: Extensive blocking rules, especially category blocking, could impact performance of B4/B6 queries. *Mitigation: Optimize database queries, consider caching blocked lists for a child profile.*
- ⚠️ **Authorization Logic**: Another critical area for parent ownership checks. *Mitigation: Re-use and rigorously test authorization logic from B2.*
- ⚠️ **Conflicting Rules**: What happens if a category is blocked, but an item within that category is explicitly unblocked? (Out of scope for MVP, assume category blocking takes precedence). *Mitigation: Document this behavior clearly.*

**Dependencies**: AN5 (Child/Content/Category Schemas), B2 (Child Profile Management for parent ownership), B4 (Content Browsing API), B6 (Audio Streaming API).
**Build Order**: #17

---

### Story B9: Develop Listening History Tracking API
#### Description:
As a child, I want my listening history to be recorded, and as a parent, I want to view my child's listening activity, so that recommendations can be generated and parents can monitor usage (FR3.4, FR1.5).
**Details**:
- **Endpoints**:
    -   `POST /api/v1/children/{childId}/listening-history`: (Secured, Child/Parent JWT, check parent ownership)
        -   Request: `{ "content_item_id": "uuid", "duration_played_seconds": "int", "event_type": "string" }` (e.g., "PLAY", "COMPLETE")
        -   Response: `201 Created` or `400 Bad Request`, `403 Forbidden`, `404 Not Found`.
    -   `GET /api/v1/children/{childId}/listening-history`: (Secured, Parent JWT, check parent ownership)
        -   Query Params: `start_date` (optional), `end_date` (optional), `limit` (int, default 20), `offset` (int, default 0).
        -   Response: `200 OK`, `[ { "id": "uuid", "content_item_id": "uuid", "content_title": "string", "event_type": "string", "duration_played_seconds": "int", "timestamp": "datetime" }, ... ]`.
- **Data Model**: New table `listening_history`: `id (PK), child_id (FK), content_item_id (FK), event_type (enum/string), duration_played_seconds, timestamp`.
- **Business Rules**:
    -   Records should be immutable once created.
    -   `duration_played_seconds` should be non-negative.
    -   Parents can only view their own child's listening history.
    -   History should be ordered by `timestamp` (descending).
- **Performance**: Write operation < 100ms p95. Read history with pagination < 200ms p95.
- **Error Handling**: `400` for invalid input, `403` for unauthorized, `404` for child/content not found.
#### Acceptance Criteria
- [x] Database schema (AN5) updated with `listening_history` table.
- [x] `POST /api/v1/children/{childId}/listening-history` successfully records a listening event for a child.
- [x] Endpoint returns `403 Forbidden` if parent does not own child or child is attempting to log for another child.
- [x] `GET /api/v1/children/{childId}/listening-history` returns the paginated listening history for a child, ordered by most recent.
- [x] History retrieval supports filtering by `start_date` and `end_date`.
- [x] Response includes content title along with event details for parent readability.
- [x] All endpoints validate input (`childId`, `content_item_id`, `duration_played_seconds`).
- [x] Unit and integration tests cover event recording, history retrieval, pagination, filtering, and authorization.
- [x] OpenAPI/Swagger documentation updated for these endpoints.

#### Effort Estimate: **6 SP**
**Complexity**: Medium

**Breakdown**:
- Backend: 90% (5.4 days)
- DevOps: 10% (0.6 days)

**Reasoning**:
```
Day 1: Schema Update & Event Recording Design
- Add `listening_history` table (AN5 context) with appropriate indexes (child_id, content_item_id, timestamp) (3 hrs)
- Design `ListeningHistoryService` and controller (5 hrs)

Day 2: Record Listening Event Endpoint
- Implement `POST /api/v1/children/{childId}/listening-history` (controller, service logic) (6 hrs)
- Implement parent/child ownership checks (2 hrs)

Day 3: Retrieve Listening History Endpoint
- Implement `GET /api/v1/children/{childId}/listening-history` (controller, service logic) (6 hrs)
- Integrate content title retrieval for display (JOIN with `content_items`) (2 hrs)

Day 4: Pagination & Filtering
- Add pagination (limit, offset) to history retrieval (4 hrs)
- Implement `start_date`/`end_date` filtering (4 hrs)

Day 5: Validation, Error Handling & Testing
- Add input validation for event details (content ID, duration, event type) (4 hrs)
- Implement error handling (400, 403, 404) (2 hrs)
- Write unit tests for service logic (2 hrs)

Day 6: Integration Testing, Documentation & Refinement
- Write integration tests for all history endpoints (record, retrieve, filters, auth) (6 hrs)
- Update OpenAPI documentation (1 hr)
- Code review and address feedback (1 hr)
```

**Risk Factors**:
- ⚠️ **Data Volume**: Listening history can grow rapidly. *Mitigation: Ensure proper indexing on `child_id` and `timestamp`; consider partitioning for very large datasets (future optimization).*
- ⚠️ **Performance of Reads**: Complex joins for content titles on large history tables could be slow. *Mitigation: Optimize query with indexes; consider denormalization or caching if needed.*
- ⚠️ **Privacy Concerns**: This data is sensitive. *Mitigation: Ensure strong access control (parent only), adhere to retention policies (AN9).*

**Dependencies**: AN5 (Child/Content/Listening History Schemas), B2 (Child Profile for context), B6 (Audio Streaming for event triggering).
**Build Order**: #18

---

### Story B10: Develop Parental Control API (Time Limits)
#### Description:
As a parent, I want to set daily listening time limits for each child's profile, so that I can manage their screen time (FR3.5).
**Details**:
- **Endpoints**:
    -   `PUT /api/v1/children/{childId}/time-limit`: (Secured, Parent JWT, check parent ownership)
        -   Request: `{ "daily_limit_minutes": "int", "is_enabled": "boolean" }`
        -   Response: `200 OK` or `400 Bad Request`, `403 Forbidden`, `404 Not Found`.
    -   `GET /api/v1/children/{childId}/time-limit`: (Secured, Parent JWT, check parent ownership)
        -   Response: `200 OK`, `{ "daily_limit_minutes": "int", "is_enabled": "boolean", "time_spent_today_minutes": "int" }`.
- **Data Model**: `children` table (AN5) updated with `daily_limit_minutes` (int, nullable), `time_limit_enabled` (boolean).
- **Business Rules**:
    -   `daily_limit_minutes` must be a positive integer (e.g., 0-360).
    -   `is_enabled` allows toggling the limit.
    -   Parents can only manage time limits for their own children.
    -   `time_spent_today_minutes` calculated from `listening_history` for the current day.
- **Performance**: Update/Get < 100ms p95.
- **Error Handling**: `400` for invalid input, `403` for unauthorized, `404` for child not found.
#### Acceptance Criteria
- [x] `children` table schema (AN5) updated with `daily_limit_minutes` and `time_limit_enabled` columns.
- [x] `PUT /api/v1/children/{childId}/time-limit` successfully updates the daily listening limit and enabled status for a child.
- [x] `daily_limit_minutes` is validated to be a non-negative integer.
- [x] `GET /api/v1/children/{childId}/time-limit` returns the configured limit and whether it's enabled.
- [x] `GET /api/v1/children/{childId}/time-limit` includes `time_spent_today_minutes` calculated from the child's `listening_history` (B9) for the current day.
- [x] All endpoints enforce parent ownership of `childId` and return `403 Forbidden` if not owned.
- [x] Unit and integration tests cover setting/getting limits, enabled status, calculation of `time_spent_today_minutes`, and authorization.
- [x] OpenAPI/Swagger documentation updated for these endpoints.

#### Effort Estimate: **4 SP**
**Complexity**: Medium

**Breakdown**:
- Backend: 90% (3.6 days)
- DevOps: 10% (0.4 days)

**Reasoning**:
```
Day 1: Schema Update & Set/Get Time Limit Endpoints
- Add `daily_limit_minutes` and `time_limit_enabled` to `children` table (AN5 context) (2 hrs)
- Implement `PUT /api/v1/children/{childId}/time-limit` for setting limit/status (4 hrs)
- Implement `GET /api/v1/children/{childId}/time-limit` for retrieving configured limit (2 hrs)

Day 2: Calculate Time Spent & Validation
- Integrate `ListeningHistoryService` (B9) to calculate `time_spent_today_minutes` (6 hrs)
- Add validation for `daily_limit_minutes` (positive integer) (2 hrs)

Day 3: Authorization, Testing & Documentation
- Implement parent ownership checks (4 hrs)
- Write unit and integration tests (set/get, calculation, validation, auth) (3 hrs)
- Update OpenAPI documentation (1 hr)

Day 4: Refinement & Code Review
- Address code review comments (4 hrs)
- Final bug fixes and testing (4 hrs)
```

**Risk Factors**:
- ⚠️ **Time Zone Issues**: Calculating "today" for time spent can be tricky with different user time zones. *Mitigation: Store timestamps in UTC; calculate "today" based on the parent's configured time zone or a universal app time zone (initial approach: UTC day, refine later).*
- ⚠️ **Real-time Enforcement**: This API provides the limit, enforcement (e.g., stopping playback) is a frontend responsibility. *Mitigation: Clearly define the contract: backend provides data, frontend enforces.*
- ⚠️ **Performance of History Aggregation**: Aggregating `listening_history` can be heavy on large datasets. *Mitigation: Optimize query (indexes); consider a cached daily sum if performance becomes an issue.*

**Dependencies**: AN5 (Child Schema Update), B2 (Child Profile for context), B9 (Listening History for `time_spent_today_minutes` calculation).
**Build Order**: #19

---

### Story B11: Develop Offline Download Management API
#### Description:
As a child, I want to download content for offline listening, so that I can enjoy content without an internet connection (FR4.2).
**Details**:
- **Endpoints**:
    -   `GET /api/v1/download/{contentId}`: (Secured, Child/Parent JWT, check content access)
        -   Response: `200 OK` with audio file stream, or `403 Forbidden`, `404 Not Found`.
- **Data Model**: `content_items` table (from AN5) for `audio_file_url`. `children` table (for age/content blocking checks).
- **Business Rules**:
    -   Must check if content is accessible to the current `child_id` (based on age filter, content blocking from B5/B8).
    -   The backend provides the direct download link (preferably signed, limited-time URL) to the content from S3/CDN.
    -   The actual download and secure storage on the device are frontend responsibilities (AN7).
- **Integrations**: AWS S3 (origin for CDN), AWS CloudFront (AN3). Generate pre-signed S3 URLs or CloudFront signed URLs.
- **Performance**: Download URL generation < 100ms p95. Actual download speed dependent on CDN/network.
- **Security**: Download links should be time-limited and single-use if possible (pre-signed URLs).
#### Acceptance Criteria
- [x] `GET /api/v1/download/{contentId}` endpoint is implemented to provide a secure download link for content.
- [x] The endpoint verifies if the `contentId` exists and is available (404 if not).
- [x] The endpoint verifies if the requested content is accessible to the current child profile (based on age filter and content blocking rules), returning `403 Forbidden` if not accessible.
- [x] The endpoint returns a pre-signed S3 URL or a CloudFront signed URL that is time-limited (e.g., 5-10 minutes validity).
- [x] The URL allows direct download of the audio file.
- [x] Unit and integration tests cover content access checks and successful URL generation.
- [x] OpenAPI/Swagger documentation updated for this endpoint.

#### Effort Estimate: **4 SP**
**Complexity**: Medium

**Breakdown**:
- Backend: 90% (3.6 days)
- DevOps: 10% (0.4 days)

**Reasoning**:
```
Day 1: Design & Setup
- Design `DownloadService` and controller (4 hrs)
- Research AWS SDK methods for generating pre-signed S3/CloudFront URLs (4 hrs)

Day 2: Access Control & URL Generation
- Integrate `ChildService` (B2) and `ContentService` (B4) for age/blocking checks (B5, B8) (5 hrs)
- Implement logic to generate time-limited pre-signed S3 or CloudFront URLs (3 hrs)

Day 3: Error Handling & Security
- Implement robust error handling (403 forbidden, 404 not found) (4 hrs)
- Ensure generated URLs are short-lived and secure (e.g., not guessable) (2 hrs)
- Configure necessary IAM permissions for pre-signing (2 hrs)

Day 4: Testing, Documentation & Refinement
- Write comprehensive unit and integration tests (happy path, access denied, not found, URL validity) (5 hrs)
- Update OpenAPI documentation (1 hr)
- Code review and address feedback (2 hrs)
```

**Risk Factors**:
- ⚠️ **Pre-signed URL Abuse**: While time-limited, a shared URL could be used by multiple clients during its validity window. *Mitigation: Short validity times; consider adding client-specific tokens if necessary (more complex, future scope).*
- ⚠️ **Permission Issues**: Incorrect IAM policies for pre-signing can lead to `403` errors for valid requests. *Mitigation: Rigorous testing of IAM role permissions.*
- ⚠️ **Content Accessibility**: The same access control checks from streaming (B6) apply here. *Mitigation: Re-use and thoroughly test access control logic.*

**Dependencies**: AN3 (CDN), AN7 (Secure Local Storage Mechanism - consumed by frontend using this API's output), B3 (Content Ingestion), B4 (Content Browsing), B5 (Age Filtering), B8 (Content Blocking).
**Build Order**: #20

---

### Story B12: Develop Playlist Creation & Management API (Child & Curated)
#### Description:
As a child, I want to create and save custom playlists, and I want to access pre-curated playlists, so that I can organize my favorite content and discover new themes (FR4.3, FR4.4).
**Details**:
- **Endpoints**:
    -   `POST /api/v1/children/{childId}/playlists`: (Secured, Parent JWT, check parent ownership)
        -   Request: `{ "name": "string", "description": "string", "content_item_ids": ["uuid", ...] }`
        -   Response: `201 Created`, `{ "id": "uuid", ... }` or `400 Bad Request`, `403 Forbidden`, `404 Not Found`.
    -   `GET /api/v1/children/{childId}/playlists`: (Secured, Parent JWT, check parent ownership)
        -   Response: `200 OK`, `[ { "id": "uuid", "name": "string", "description": "string", "is_curated": false, "item_count": 5 }, ... ]`.
    -   `GET /api/v1/playlists/curated`: (Public)
        -   Response: `200 OK`, `[ { "id": "uuid", "name": "string", "description": "string", "is_curated": true, "item_count": 10 }, ... ]`.
    -   `GET /api/v1/playlists/{playlistId}/content`: (Secured, Child/Parent JWT, check content access)
        -   Response: `200 OK`, `[ { "id": "uuid", "title": "string", "audio_file_url": "url", ... }, ... ]`.
    -   `PUT /api/v1/children/{childId}/playlists/{playlistId}`: (Secured, Parent JWT, check parent ownership)
        -   Request: `{ "name": "string", "description": "string", "content_item_ids": ["uuid", ...] }`
        -   Response: `200 OK` or `400 Bad Request`, `403 Forbidden`, `404 Not Found`.
    -   `DELETE /api/v1/children/{childId}/playlists/{playlistId}`: (Secured, Parent JWT, check parent ownership)
        -   Response: `204 No Content` or `403 Forbidden`, `404 Not Found`.
- **Data Model**:
    -   `playlists` table: `id (PK), child_id (FK, nullable for curated), name, description, is_curated (boolean), created_at, updated_at`.
    -   `playlist_content_items`: `playlist_id (FK), content_item_id (FK), item_order (int)` (composite PK).
- **Business Rules**:
    -   Child-created playlists are linked to a specific `child_id`. Curated playlists have `child_id` as NULL.
    -   When retrieving playlist content, apply age filtering (B5) and content blocking (B8) for the active child.
    -   `content_item_ids` in request must refer to existing content.
    -   Parent ownership enforced for child's playlists.
- **Performance**: CRUD operations < 200ms p95.
- **Error Handling**: `400` for invalid input, `403` for unauthorized, `404` for child/playlist/content not found.
#### Acceptance Criteria
- [x] Database schemas (AN5) updated with `playlists` and `playlist_content_items` tables.
- [x] `POST /api/v1/children/{childId}/playlists` successfully creates a new child-specific playlist.
- [x] `GET /api/v1/children/{childId}/playlists` returns a list of child-created playlists for the specified child.
- [x] `GET /api/v1/playlists/curated` returns a list of all curated playlists.
- [x] `GET /api/v1/playlists/{playlistId}/content` returns content items for a playlist, filtered by the active child's age (B5) and blocked content (B8).
- [x] `PUT /api/v1/children/{childId}/playlists/{playlistId}` updates a child's playlist (name, description, content items).
- [x] `DELETE /api/v1/children/{childId}/playlists/{playlistId}` deletes a child's playlist.
- [x] All child-specific endpoints enforce parent ownership for `childId`.
- [x] Validation ensures `content_item_ids` exist when creating/updating playlists.
- [x] Unit and integration tests cover all CRUD operations, content filtering, and authorization.
- [x] OpenAPI/Swagger documentation updated for these endpoints.

#### Effort Estimate: **8 SP**
**Complexity**: Medium

**Breakdown**:
- Backend: 90% (7.2 days)
- DevOps: 10% (0.8 days)

**Reasoning**:
```
Day 1: Schema Update & Playlist Design
- Add `playlists` and `playlist_content_items` tables (AN5 context) (4 hrs)
- Design `PlaylistService` and controller (4 hrs)

Day 2: Create Playlist (Child) & List Child Playlists
- Implement `POST /api/v1/children/{childId}/playlists` (controller, service) (6 hrs)
- Implement `GET /api/v1/children/{childId}/playlists` (2 hrs)

Day 3: Curated Playlists & Get Playlist Content
- Implement `GET /api/v1/playlists/curated` (3 hrs)
- Implement `GET /api/v1/playlists/{playlistId}/content` (5 hrs) - initial, no filtering yet.

Day 4: Update & Delete Playlist
- Implement `PUT /api/v1/children/{childId}/playlists/{playlistId}` for updating playlists (6 hrs)
- Implement `DELETE /api/v1/children/{childId}/playlists/{playlistId}` (2 hrs)

Day 5: Content Filtering in Playlists
- Integrate age filtering (B5) and content blocking (B8) into `GET /api/v1/playlists/{playlistId}/content` (6 hrs)
- Ensure only accessible content is returned, handling unavailable items gracefully (2 hrs)

Day 6: Validation, Authorization & Error Handling
- Add validation for playlist name, content_item_ids existence (4 hrs)
- Implement parent ownership checks for child-specific endpoints (4 hrs)

Day 7: Testing
- Write comprehensive unit tests for service logic (4 hrs)
- Write integration tests for all endpoints, including content filtering and authorization (4 hrs)

Day 8: Documentation & Refinement
- Update OpenAPI documentation (2 hrs)
- Code review and address feedback (3 hrs)
- Final bug fixes (3 hrs)
```

**Risk Factors**:
- ⚠️ **Content Filtering Complexity**: Applying multiple filters (age, blocked content) on playlist items could be complex and impact performance. *Mitigation: Optimize database queries, consider caching playlist content if accessed frequently.*
- ⚠️ **Orphaned Content**: Deleting a `content_item` might leave invalid references in `playlist_content_items`. *Mitigation: Implement foreign key `ON DELETE CASCADE` or cleanup logic.*
- ⚠️ **Authorization**: Multiple authorization checks (parent ownership, child content access) need careful implementation. *Mitigation: Re-use and thoroughly test authorization components.*

**Dependencies**: AN5 (Child/Content/Playlist Schemas), B2 (Child Profile Management), B4 (Content Browsing), B5 (Age Filtering), B8 (Content Blocking).
**Build Order**: #21

---

### Story B13: Develop Sleep Timer API
#### Description:
As a child, I want to set a sleep timer for audio playback, so that content stops playing automatically after a set duration or track completion (FR4.5).
**Details**:
- **Endpoints**:
    -   `POST /api/v1/children/{childId}/sleep-timer`: (Secured, Parent/Child JWT, check parent ownership)
        -   Request: `{ "duration_minutes": "int", "stop_after_track_complete": "boolean" }`
        -   Response: `200 OK` or `400 Bad Request`, `403 Forbidden`, `404 Not Found`.
    -   `DELETE /api/v1/children/{childId}/sleep-timer`: (Secured, Parent/Child JWT, check parent ownership)
        -   Response: `204 No Content` or `403 Forbidden`, `404 Not Found`.
    -   `GET /api/v1/children/{childId}/sleep-timer`: (Secured, Parent/Child JWT, check parent ownership)
        -   Response: `200 OK`, `{ "duration_minutes": "int", "stop_after_track_complete": "boolean", "is_active": "boolean" }`.
- **Data Model**: `children` table (AN5) updated with `sleep_timer_duration_minutes` (int, nullable), `sleep_timer_stop_after_track_complete` (boolean, nullable), `sleep_timer_active_until` (timestamp, nullable).
- **Business Rules**:
    -   `duration_minutes` must be a positive integer (e.g., 5-120).
    -   If `stop_after_track_complete` is true, `duration_minutes` is optional/ignored for timer *setting* but UI can display it.
    -   Timer is child-specific.
    -   Backend stores the timer configuration, but the *enforcement* (stopping playback) is primarily a frontend responsibility. Backend `is_active` might rely on `sleep_timer_active_until`.
- **Performance**: CRUD operations < 100ms p95.
- **Error Handling**: `400` for invalid input, `403` for unauthorized, `404` for child not found.
#### Acceptance Criteria
- [x] `children` table schema (AN5) updated with `sleep_timer_duration_minutes`, `sleep_timer_stop_after_track_complete`, and `sleep_timer_active_until` columns.
- [x] `POST /api/v1/children/{childId}/sleep-timer` successfully sets a sleep timer configuration for a child.
- [x] `duration_minutes` is validated to be a positive integer if provided.
- [x] `DELETE /api/v1/children/{childId}/sleep-timer` successfully clears the sleep timer configuration.
- [x] `GET /api/v1/children/{childId}/sleep-timer` returns the current sleep timer configuration and its active status.
- [x] All endpoints enforce parent ownership of `childId` and return `403 Forbidden` if not owned.
- [x] Unit and integration tests cover setting/clearing/getting timers, validation, and authorization.
- [x] OpenAPI/Swagger documentation updated for these endpoints.

#### Effort Estimate: **3 SP**
**Complexity**: Low

**Breakdown**:
- Backend: 90% (2.7 days)
- DevOps: 10% (0.3 days)

**Reasoning**:
```
Day 1: Schema Update & Set/Clear Endpoints
- Add sleep timer columns to `children` table (AN5 context) (2 hrs)
- Implement `POST /api/v1/children/{childId}/sleep-timer` for setting (4 hrs)
- Implement `DELETE /api/v1/children/{childId}/sleep-timer` for clearing (2 hrs)

Day 2: Get Endpoint & Validation
- Implement `GET /api/v1/children/{childId}/sleep-timer` (4 hrs)
- Add validation for `duration_minutes` (positive int) (2 hrs)
- Implement parent ownership checks (2 hrs)

Day 3: Testing, Documentation & Refinement
- Write unit and integration tests (set/clear/get, validation, auth) (5 hrs)
- Update OpenAPI documentation (1 hr)
- Code review and address feedback (2 hrs)
```

**Risk Factors**:
- ⚠️ **Enforcement Responsibility**: The backend stores the timer, but frontend is responsible for playback control. *Mitigation: Clearly communicate this division of responsibility to frontend teams.*
- ⚠️ **Time Synching**: Backend's `sleep_timer_active_until` might slightly differ from device's local time. *Mitigation: Use UTC timestamps on backend; frontend should handle local time display/calculation.*

**Dependencies**: AN5 (Child Schema Update), B2 (Child Profile Management for parent ownership).
**Build Order**: #22

---

### Story B14: Develop Subscription Management API (Parent Facing)
#### Description:
As a parent, I want to view my subscription status, payment methods, and renewal settings, so that I can manage my paid access to the platform (FR3.7).
**Details**:
- **Endpoints**:
    -   `GET /api/v1/parents/me/subscription`: (Secured, Parent JWT required)
        -   Response: `200 OK`, `{ "status": "active", "plan_name": "Premium", "current_period_end": "datetime", "payment_method_last_4": "1234", "next_billing_amount": 14.99 }` or `404 Not Found` if no subscription.
    -   `POST /api/v1/parents/me/subscription/cancel`: (Secured, Parent JWT required)
        -   Response: `200 OK` or `400 Bad Request`.
    -   `POST /api/v1/parents/me/subscription/reactivate`: (Secured, Parent JWT required)
        -   Response: `200 OK` or `400 Bad Request`.
    -   `PUT /api/v1/parents/me/payment-method`: (Secured, Parent JWT required)
        -   Request: `{ "stripe_payment_method_id": "string" }` (tokenized ID from frontend)
        -   Response: `200 OK` or `400 Bad Request`.
- **Data Model**: `subscriptions`, `subscription_plans` tables (from AN5). Parent ID from JWT.
- **Business Rules**:
    -   Interact with Stripe (AN8) for actual subscription/payment method changes.
    -   Update local `subscriptions` table based on Stripe API responses or webhooks.
    -   Cancellation can be immediate or at the end of the current period. (For MVP: end of period).
    -   Reactivation only possible for cancelled-at-period-end subscriptions.
- **Integrations**: Stripe API (AN8).
- **Performance**: All operations < 250ms p95.
- **Error Handling**: `400` for invalid operations (e.g., reactivating an active sub), `404` for no subscription.
#### Acceptance Criteria
- [x] `GET /api/v1/parents/me/subscription` returns the authenticated parent's subscription details, including status, plan, next billing date, and obfuscated payment method.
- [x] Endpoint returns `404 Not Found` if the parent has no active subscription.
- [x] `POST /api/v1/parents/me/subscription/cancel` calls the Stripe API (AN8) to cancel the subscription at the end of the current billing period.
- [x] Local `subscriptions` table status is updated to `cancelled_at_period_end` (or similar) upon successful cancellation.
- [x] `POST /api/v1/parents/me/subscription/reactivate` calls the Stripe API (AN8) to reactivate a previously cancelled subscription.
- [x] Local `subscriptions` table status is updated to `active` upon successful reactivation.
- [x] `PUT /api/v1/parents/me/payment-method` calls the Stripe API (AN8) to update the default payment method for the parent's Stripe customer.
- [x] All Stripe API interactions are handled gracefully with error responses mapped to appropriate HTTP status codes.
- [x] Unit and integration tests cover all endpoints, Stripe interactions, and local database updates.
- [x] OpenAPI/Swagger documentation updated for these endpoints.

#### Effort Estimate: **7 SP**
**Complexity**: Medium

**Breakdown**:
- Backend: 90% (6.3 days)
- DevOps: 10% (0.7 days)

**Reasoning**:
```
Day 1: Setup & Get Subscription Details
- Design `SubscriptionManagementService` and controller (4 hrs)
- Implement `GET /api/v1/parents/me/subscription` (5 hrs)
  - Retrieve local subscription data.
  - Call Stripe API if needed for real-time status (e.g., payment method details).

Day 2: Cancel Subscription
- Implement `POST /api/v1/parents/me/subscription/cancel` (6 hrs)
- Call Stripe API to cancel subscription.
- Update local database status. (2 hrs)

Day 3: Reactivate Subscription
- Implement `POST /api/v1/parents/me/subscription/reactivate` (6 hrs)
- Call Stripe API to reactivate subscription.
- Update local database status. (2 hrs)

Day 4: Update Payment Method
- Implement `PUT /api/v1/parents/me/payment-method` (6 hrs)
- Call Stripe API to update customer's default payment method.
- Handle tokenized payment method ID. (2 hrs)

Day 5: Error Handling & Security
- Implement comprehensive error handling for all Stripe API calls (5 hrs)
- Ensure all sensitive data (e.g., payment method IDs) are tokenized and not logged (3 hrs)

Day 6: Testing
- Write unit tests for service logic (4 hrs)
- Write integration tests for all endpoints, verifying Stripe calls and DB updates (4 hrs)

Day 7: Documentation & Refinement
- Update OpenAPI documentation (2 hrs)
- Code review and address feedback (3 hrs)
- Final bug fixes and testing (3 hrs)
```

**Risk Factors**:
- ⚠️ **Stripe API Latency**: External API calls can introduce latency. *Mitigation: Implement timeouts and retries; optimize local data fetching.*
- ⚠️ **Inconsistent State**: Discrepancies between Stripe's state and our local database state. *Mitigation: Rely heavily on Stripe webhooks (AN8) for ultimate source of truth, but also allow explicit API calls to sync if needed.*
- ⚠️ **Payment Gateway Failures**: Stripe APIs can return errors. *Mitigation: Implement robust error handling, logging, and alerts for failures.*

**Dependencies**: AN8 (Stripe Integration Framework), B1 (Parent Login for parent context), AN5 (Subscription Schemas).
**Build Order**: #23

---

## 💻 Frontend Stories

### Story F1: Web App - Project Setup & Core Layout
#### Description:
As an engineer, I want to set up the foundational web application project with a modern framework (e.g., React), including routing and a basic responsive layout, so that subsequent UI development can proceed efficiently.
**Details**:
- **Tech Stack**: React 18, Next.js 14, TypeScript, Tailwind CSS for styling, Storybook for component isolation, Jest/React Testing Library for testing.
- **Components**: Basic `Header` (with placeholder logo/nav), `Footer`, `MainLayout` component.
- **UX Flow**:
    1.  User navigates to the web app.
    2.  Basic layout is rendered with header, main content area, and footer.
    3.  Routing (e.g., `/`, `/login`, `/dashboard`) is functional, showing placeholder content.
- **State Management**: React Context API for global UI state; local component state for simple needs.
- **Responsive Design**: Mobile-first approach, targeting breakpoints for mobile (320px), tablet (768px), and desktop (1024px).
- **Edge Cases**: Empty content area placeholder.
#### Acceptance Criteria
- [x] New Next.js (React/TypeScript) project initialized.
- [x] Tailwind CSS configured and integrated for styling.
- [x] Basic responsive `Header` component (containing app logo/name) created.
- [x] Basic responsive `Footer` component (containing copyright info) created.
- [x] `MainLayout` component established, wrapping content with `Header` and `Footer`.
- [x] React Router (Next.js App Router) configured for basic routes (e.g., `/`, `/login`).
- [x] Placeholder pages for `/` and `/login` rendering within the `MainLayout`.
- [x] Storybook configured and running, showcasing `Header` and `Footer` components.
- [x] Jest and React Testing Library configured for unit/component testing.
- [x] Project build and local development server are fully functional.
- [x] Readme file updated with project setup instructions and common commands.

#### Effort Estimate: **4 SP**
**Complexity**: Low

**Breakdown**:
- Frontend: 90% (3.6 days)
- DevOps: 10% (0.4 days)

**Reasoning**:
```
Day 1: Project Setup & Core Configuration
- Initialize Next.js project with TypeScript (3 hrs)
- Configure Tailwind CSS (2 hrs)
- Set up basic folder structure (components, pages, styles) (1 hr)
- Configure Jest/React Testing Library (2 hrs)

Day 2: Basic Components & Layout
- Create Header component (responsive) (3 hrs)
- Create Footer component (responsive) (2 hrs)
- Create MainLayout component to compose Header, content, Footer (3 hrs)

Day 3: Routing & Placeholders
- Implement basic Next.js routing (e.g., '/', '/login') (4 hrs)
- Create placeholder pages (e.g., 'Home', 'Login') (2 hrs)
- Verify responsive behavior on different screen sizes (2 hrs)

Day 4: Storybook, Documentation & Review
- Set up Storybook and create stories for Header/Footer (4 hrs)
- Update README with setup, running, testing instructions (2 hrs)
- Code review and address feedback (2 hrs)
```

**Risk Factors**:
- ⚠️ **Tooling Setup Issues**: Conflicts between packages, versioning problems during initial setup. *Mitigation: Use recommended/stable versions, consult documentation, start with minimal dependencies.*
- ⚠️ **Responsive Design Overlook**: Neglecting mobile-first from the start can lead to re-work. *Mitigation: Enforce mobile-first design reviews from day one; use browser dev tools extensively.*

**Dependencies**: None (foundational)
**Build Order**: #24

---

### Story F2: iOS App - Project Setup & Core Layout
#### Description:
As an engineer, I want to set up the foundational iOS application project, including necessary libraries, routing, and a basic app shell, so that native iOS UI development can commence.
**Details**:
- **Tech Stack**: Swift, SwiftUI (or UIKit if chosen), Xcode, Cocoapods/Swift Package Manager.
- **Components**: Basic `AppView` (root), `ContentView`, `NavigationView` (for routing).
- **UX Flow**:
    1.  User opens the iOS app.
    2.  A basic app shell (header, content area) is displayed.
    3.  Placeholder views for different sections.
- **State Management**: SwiftUI `State` and `ObservableObject` for local and shared view state.
- **Responsive Design**: Utilizes Auto Layout/SwiftUI's layout system for adaptive UI.
- **Edge Cases**: Empty states.
#### Acceptance Criteria
- [x] New Xcode project initialized with Swift and SwiftUI.
- [x] Project configured to support target iOS version (e.g., iOS 15+).
- [x] Basic `ContentView` created as the root of the app's UI.
- [x] `NavigationView` (or equivalent for routing) integrated.
- [x] Placeholder screens/views implemented for at least two major sections (e.g., "Home", "Login").
- [x] Basic header-like element (e.g., `navigationTitle`) and footer-like element (e.g., `Toolbar`) displayed.
- [x] App successfully builds and runs on an iOS simulator and/or physical device.
- [x] Unit testing framework (XCTest) configured.
- [x] Readme file updated with project setup instructions.

#### Effort Estimate: **3 SP**
**Complexity**: Low

**Breakdown**:
- Frontend: 100% (3 days)

**Reasoning**:
```
Day 1: Project Initialization & Basic Structure
- Create new Xcode project (Swift, SwiftUI) (3 hrs)
- Configure project settings, target iOS version (1 hr)
- Establish root `App` and `ContentView` (4 hrs)

Day 2: Navigation & Placeholder Views
- Implement `NavigationView` for basic screen transitions (4 hrs)
- Create placeholder views for "Home" and "Login" (3 hrs)
- Add basic header (`navigationTitle`) and a footer placeholder (1 hr)

Day 3: Build, Test & Documentation
- Build and run on simulator/device, resolve build issues (4 hrs)
- Verify basic UI responsiveness (e.g., landscape/portrait) (1 hr)
- Configure XCTest for future unit tests (1 hr)
- Update README with setup/build instructions (2 hrs)
```

**Risk Factors**:
- ⚠️ **Xcode/Simulator Issues**: Environment setup problems. *Mitigation: Use latest stable Xcode, verify simulator installation.*
- ⚠️ **SwiftUI Learning Curve**: If the team is new to SwiftUI, initial ramp-up. *Mitigation: Leverage experienced team members, dedicate time for learning.*

**Dependencies**: None (foundational)
**Build Order**: #25

---

### Story F3: Android App - Project Setup & Core Layout
#### Description:
As an engineer, I want to set up the foundational Android application project, including necessary libraries, routing, and a basic app shell, so that native Android UI development can commence.
**Details**:
- **Tech Stack**: Kotlin, Jetpack Compose (or XML layouts if chosen), Android Studio, Gradle.
- **Components**: `MainActivity` (root), `NavHost` (for routing), `Scaffold` (for basic layout).
- **UX Flow**:
    1.  User opens the Android app.
    2.  A basic app shell (app bar, content area) is displayed.
    3.  Placeholder views for different sections.
- **State Management**: Jetpack Compose `State` and `ViewModel` for local and shared view state.
- **Responsive Design**: Utilizes Compose's layout system for adaptive UI.
- **Edge Cases**: Empty states.
#### Acceptance Criteria
- [x] New Android Studio project initialized with Kotlin and Jetpack Compose.
- [x] Project configured to support target Android version (e.g., API 24+).
- [x] `MainActivity` set up as the entry point.
- [x] Jetpack Navigation Component integrated with `NavHost` for basic routing.
- [x] Placeholder screens/composables implemented for at least two major sections (e.g., "Home", "Login").
- [x] Basic app bar (top) and navigation-like element (bottom bar or drawer) displayed.
- [x] App successfully builds and runs on an Android emulator and/or physical device.
- [x] Unit testing framework (JUnit, Robolectric) configured.
- [x] Readme file updated with project setup instructions.

#### Effort Estimate: **3 SP**
**Complexity**: Low

**Breakdown**:
- Frontend: 100% (3 days)

**Reasoning**:
```
Day 1: Project Initialization & Basic Structure
- Create new Android Studio project (Kotlin, Jetpack Compose) (3 hrs)
- Configure project settings, target API level (1 hr)
- Establish `MainActivity` and basic `Composable` structure (4 hrs)

Day 2: Navigation & Placeholder Views
- Implement Jetpack Navigation Component with `NavHost` (4 hrs)
- Create placeholder Composables for "Home" and "Login" (3 hrs)
- Add basic app bar (`TopAppBar`) and bottom navigation/drawer placeholder (1 hr)

Day 3: Build, Test & Documentation
- Build and run on emulator/device, resolve build issues (4 hrs)
- Verify basic UI responsiveness (e.g., landscape/portrait, different screen sizes) (1 hr)
- Configure JUnit/Robolectric for future unit tests (1 hr)
- Update README with setup/build instructions (2 hrs)
```

**Risk Factors**:
- ⚠️ **Android Studio/Emulator Issues**: Environment setup problems. *Mitigation: Use latest stable Android Studio, verify emulator/ADB setup.*
- ⚠️ **Jetpack Compose Learning Curve**: If the team is new to Compose, initial ramp-up. *Mitigation: Leverage experienced team members, dedicate time for learning.*

**Dependencies**: None (foundational)
**Build Order**: #26

---

### Story F4: Parent Account Registration & Login UI (Web & Mobile)
#### Description:
As a parent, I want to see a clear registration and login screen, so that I can easily create my account or sign in to the platform.
**Details**:
- **Components**: `RegistrationForm`, `LoginForm`, `TextInput`, `Button`, `ErrorMessage` components.
- **UX Flow**:
    1.  User lands on `/login` or `/register` route.
    2.  Presents form with email and password fields.
    3.  Submits data to B1 (Parent Account API).
    4.  Handles success (redirect to child profile selection) or error (display message).
- **State Management**: Local component state for form inputs, global context/store for authentication status (JWT token).
- **API Calls**: B1 (Parent Account API) - `POST /api/v1/parents/register`, `POST /api/v1/parents/login`.
- **Responsive Design**: Optimized for mobile and desktop.
- **Edge Cases**: Invalid email format, weak password, email already exists, incorrect credentials, API errors.
#### Acceptance Criteria
- [x] **Web**: `RegistrationForm` and `LoginForm` components implemented with email and password input fields.
- [x] **Mobile (iOS/Android)**: Registration and Login screens implemented with email and password input fields.
- [x] Both forms include a submit button.
- [x] Input fields display real-time validation feedback (e.g., "invalid email format," "password too short").
- [x] Upon successful registration/login, user is redirected to a placeholder "success" screen (e.g., `/children-selection`).
- [x] Error messages from B1 API (e.g., "Email already registered," "Invalid credentials") are displayed clearly to the user.
- [x] Password input field masks characters.
- [x] Form submission is disabled while API request is in progress (loading state).
- [x] Unit tests for form validation logic.
- [x] Integration tests covering form submission and API interaction mock.

#### Effort Estimate: **7 SP**
**Complexity**: Medium

**Breakdown**:
- Frontend: 90% (6.3 days)
- Research/Design: 10% (0.7 days)

**Reasoning**:
```
Day 1: Design & Web Login/Register UI
- Design UI/UX for login/registration forms (including error states) (4 hrs)
- Implement basic Web Login Form layout with input fields and button (4 hrs)

Day 2: Web Form Validation & State
- Implement client-side validation for email, password strength (Web) (4 hrs)
- Manage form state (input values, errors, loading) (Web) (4 hrs)

Day 3: Web API Integration & Error Handling
- Integrate with B1 Login API (`POST /api/v1/parents/login`) (Web) (4 hrs)
- Handle API responses (success redirect, display errors) (Web) (4 hrs)

Day 4: Mobile Login/Register UI (Cross-platform with React Native or native equivalent)
- Implement basic Mobile Login Form layout with input fields and button (4 hrs)
- Implement basic Mobile Registration Form layout (4 hrs)

Day 5: Mobile Form Validation & API Integration
- Implement client-side validation (Mobile) (4 hrs)
- Integrate with B1 Login/Register APIs (Mobile) (4 hrs)
- Handle API responses (Mobile) (if React Native, same logic as web, but native UI)

Day 6: Mobile Error Handling, Redirection & UX
- Display API error messages (Mobile) (3 hrs)
- Implement redirection on success (Mobile) (2 hrs)
- Ensure password masking, loading states (Web & Mobile) (3 hrs)

Day 7: Testing & Documentation
- Write unit tests for form validation (Web & Mobile) (4 hrs)
- Write integration tests for API interactions (mocking B1) (2 hrs)
- Document UI components and API contracts (2 hrs)
```

**Risk Factors**:
- ⚠️ **API Contract Changes**: If B1 API changes without notice, frontend integration breaks. *Mitigation: Strong communication with backend team; use OpenAPI spec to generate client code.*
- ⚠️ **Security Vulnerabilities**: Client-side storage of JWT, improper password handling. *Mitigation: Store JWT securely (e.g., HTTP-only cookies for web, secure storage for mobile); never store raw passwords.*
- ⚠️ **Complex Form Validation**: Detailed validation logic can be time-consuming. *Mitigation: Use a well-known form library (e.g., React Hook Form, Formik) to streamline validation.*

**Dependencies**: F1 (Web Setup), F2 (iOS Setup), F3 (Android Setup), B1 (Parent Account API).
**Build Order**: #27

---

### Story F5: Child Profile Selection UI (Web & Mobile)
#### Description:
As a child, I want to see a visual list of avatars on app launch and select my profile, so that I can enter my personalized content experience (FR2.4).
**Details**:
- **Components**: `ChildAvatarCard` (displays child's name and avatar), `AddChildButton`.
- **UX Flow**:
    1.  After parent login, user is redirected to this screen.
    2.  Displays a grid/list of child `ChildAvatarCard`s linked to the logged-in parent.
    3.  Clicking an avatar selects the child and redirects to the Kid-Friendly Home Screen (F6).
    4.  An "Add Child" button (for parents) is visible.
- **State Management**: Local component state for selected child. Global context/store for the list of child profiles.
- **API Calls**: B2 (Child Profile Management API) - `GET /api/v1/children`.
- **Responsive Design**: Grid/list layout adapts to screen size.
- **Edge Cases**: No child profiles created yet (empty state, prominent "Add Child" button).
#### Acceptance Criteria
- [x] **Web**: Screen displays a grid/list of `ChildAvatarCard` components.
- [x] **Mobile (iOS/Android)**: Screen displays a grid/list of child profiles.
- [x] Each `ChildAvatarCard` displays the child's name and a default/custom avatar image.
- [x] The list of children is fetched from B2 `GET /api/v1/children` API.
- [x] Clicking a `ChildAvatarCard` stores the selected `childId` in local storage/global state and redirects to a placeholder home screen (F6).
- [x] An "Add Child" button is present and navigates to a placeholder "Create Child Profile" screen (related to F9).
- [x] Displays an appropriate message and prompts to add a child if no profiles are returned from the API (empty state).
- [x] Loading state displayed while fetching child profiles.
- [x] Error handling for API failures, displaying a user-friendly message.
- [x] Unit/snapshot tests for `ChildAvatarCard` and the overall screen layout.

#### Effort Estimate: **4 SP**
**Complexity**: Low

**Breakdown**:
- Frontend: 90% (3.6 days)
- Research/Design: 10% (0.4 days)

**Reasoning**:
```
Day 1: Design & Web UI
- Design UI/UX for child selection screen, including empty state (4 hrs)
- Implement basic Web UI: grid/list layout, placeholder for ChildAvatarCard (4 hrs)

Day 2: Web API Integration & State Management
- Integrate with B2 `GET /api/v1/children` API (4 hrs)
- Implement loading and error states for API call (2 hrs)
- Implement ChildAvatarCard component (name, avatar) (2 hrs)

Day 3: Web Interactions & Mobile UI
- Implement click handler for avatar: store childId, redirect to F6 placeholder (4 hrs)
- Implement "Add Child" button navigation (2 hrs)
- Implement basic Mobile UI for child selection (grid/list) (2 hrs)

Day 4: Mobile API Integration, Testing & Docs
- Integrate Mobile with B2 `GET /api/v1/children` (if React Native, same logic) (3 hrs)
- Implement Mobile interactions (select, add child) (2 hrs)
- Write unit/snapshot tests for components and screen (2 hrs)
- Document API contracts and state management (1 hr)
```

**Risk Factors**:
- ⚠️ **Performance with Many Children**: If a parent has many children, rendering could be slow. *Mitigation: Design for efficient rendering (e.g., virtualized lists if needed, but unlikely for typical number of children).*
- ⚠️ **Global State Management**: Ensuring the `childId` is correctly stored and accessible globally. *Mitigation: Use a consistent and well-understood state management pattern (React Context/Redux slice/ViewModel).*

**Dependencies**: F1 (Web Setup), F2 (iOS Setup), F3 (Android Setup), B2 (Child Profile API), F4 (Parent Login redirection).
**Build Order**: #28

---

### Story F6: Kid-Friendly Home Screen UI (Web & Mobile)
#### Description:
As a child, I want to see a simplified home screen with prominent visual cues and large buttons, showing recommended content and recently played items, so that I can easily discover and access content within my age range (FR2.1, FR2.2).
**Details**:
- **Components**: `ContentCard` (large, visual), `HorizontalScrollList` (for categories/recommendations), `RecentlyPlayedList`.
- **UX Flow**:
    1.  After child profile selection, user lands on this screen.
    2.  Displays a welcome message for the selected child.
    3.  Sections for "Recommended for You" and "Recently Played."
    4.  Each section uses `HorizontalScrollList` of `ContentCard`s.
    5.  Clicking a `ContentCard` initiates playback (F8) or navigates to content details.
- **State Management**: Global state for selected child profile and content data.
- **API Calls**: B4 (Content Browsing) for recommended content, B9 (Listening History) for recently played. (M3 for actual recommendations if available).
- **Responsive Design**: Flexible layout with scrollable sections for various screen sizes.
- **Edge Cases**: No recently played items, no recommendations (display placeholder message).
#### Acceptance Criteria
- [x] **Web & Mobile**: Home screen displays a welcome message including the selected child's name.
- [x] **Web & Mobile**: "Recently Played" section displays a `HorizontalScrollList` of `ContentCard`s.
- [x] **Web & Mobile**: "Recommended for You" section displays a `HorizontalScrollList` of `ContentCard`s (initially showing popular content or content filtered by age, using B4).
- [x] Content for "Recently Played" is fetched from B9 `GET /api/v1/children/{childId}/listening-history` API (top N unique items).
- [x] Content for "Recommended for You" is fetched from B4 `GET /api/v1/content` (filtered by child's age) or M3 if implemented.
- [x] `ContentCard` component is implemented to show content thumbnail, title.
- [x] Tapping/clicking a `ContentCard` on the home screen navigates to a placeholder content detail/player screen (F8).
- [x] Displays appropriate messages for empty "Recently Played" or "Recommended" sections.
- [x] Loading states for content sections while API calls are in progress.
- [x] Error handling for API failures, displaying user-friendly messages.
- [x] Unit/snapshot tests for `ContentCard` and screen sections.

#### Effort Estimate: **7 SP**
**Complexity**: Medium

**Breakdown**:
- Frontend: 90% (6.3 days)
- Research/Design: 10% (0.7 days)

**Reasoning**:
```
Day 1: Design & Core Layout (Web & Mobile)
- Design kid-friendly home screen UI (visual cues, large buttons) (4 hrs)
- Implement basic screen layout (welcome message, section headers, placeholders) (4 hrs)

Day 2: ContentCard & HorizontalScrollList (Web & Mobile)
- Create `ContentCard` component (thumbnail, title) (4 hrs)
- Create `HorizontalScrollList` component to display cards (4 hrs)

Day 3: Recently Played Integration (Web & Mobile)
- Integrate with B9 `GET /api/v1/children/{childId}/listening-history` to fetch recently played (6 hrs)
- Populate `RecentlyPlayedList` with `ContentCard`s (2 hrs)

Day 4: Recommended Content Integration (Web & Mobile)
- Integrate with B4 `GET /api/v1/content` (with age filter) for recommendations (6 hrs)
- Populate `RecommendedList` with `ContentCard`s (2 hrs)

Day 5: Click Interactions & Placeholder Navigation (Web & Mobile)
- Implement click handler for `ContentCard` to navigate to F8 placeholder (4 hrs)
- Implement loading and empty states for both lists (4 hrs)

Day 6: Error Handling & Responsive Adjustments (Web & Mobile)
- Implement error handling for API failures (4 hrs)
- Fine-tune responsive behavior across different devices/orientations (4 hrs)

Day 7: Testing & Documentation
- Write unit/snapshot tests for `ContentCard`, lists, and screen (4 hrs)
- Integration tests (mocking B4, B9) (2 hrs)
- Document component usage and API contracts (2 hrs)
```

**Risk Factors**:
- ⚠️ **API Response Latency**: Fetching multiple content lists concurrently could lead to slower load times. *Mitigation: Implement skeleton loaders, parallel API calls, optimize image loading.*
- ⚠️ **UX/UI for Kids**: Ensuring the design is genuinely appealing and easy for children to use. *Mitigation: Conduct quick user feedback sessions with target audience (if possible) or internal review with child-focused lens.*
- ⚠️ **Recommendation Logic**: If M3 is not ready, the "Recommended" section might feel generic. *Mitigation: Start with simple age-filtered popular content from B4; manage expectations for personalization until M3 is mature.*

**Dependencies**: F1 (Web Setup), F2 (iOS Setup), F3 (Android Setup), B4 (Content Browsing API), B9 (Listening History API), F5 (Child Profile Selection).
**Build Order**: #29

---

### Story F7: Content Browsing UI (Categories & Search - Web & Mobile)
#### Description:
As a child, I want to browse content by intuitive categories (e.g., Music, Stories) and use a simplified search function, so that I can find specific content or explore new types of audio (FR1.3, FR1.4).
**Details**:
- **Components**: `CategorySelector` (horizontal scroll or grid), `SearchBar`, `ContentGrid/List` (using `ContentCard`).
- **UX Flow**:
    1.  User navigates to a "Browse" or "Search" screen.
    2.  Displays a `CategorySelector` (e.g., "Music", "Stories").
    3.  A `SearchBar` is present for keyword search.
    4.  Below, `ContentGrid/List` displays content filtered by category and/or search term, respecting the active child's age (F5) and blocked content (F10 - future).
    5.  Clicking a `ContentCard` initiates playback (F8) or navigates to content details.
- **State Management**: Local state for active category, search term. Global state for selected child profile.
- **API Calls**: B4 (Content Browsing & Search API) - `GET /api/v1/content`, `GET /api/v1/categories`.
- **Responsive Design**: Layout adjusts from grid to single-column list on smaller screens.
- **Edge Cases**: No content for selected category/search term (empty state), API errors.
#### Acceptance Criteria
- [x] **Web & Mobile**: "Browse" screen displays a `CategorySelector` with categories fetched from B4 `GET /api/v1/categories`.
- [x] **Web & Mobile**: A `SearchBar` component is present for text input.
- [x] **Web & Mobile**: Below the controls, a `ContentGrid/List` displays `ContentCard`s.
- [x] Selecting a category from `CategorySelector` filters the `ContentGrid/List` using B4 `GET /api/v1/content?category_id={uuid}` (respecting child's age).
- [x] Entering text in `SearchBar` and submitting filters `ContentGrid/List` using B4 `GET /api/v1/content?search_term={query}` (respecting child's age).
- [x] Filters (category and search) can be combined.
- [x] `ContentCard`s in the grid/list are clickable, leading to F8 placeholder.
- [x] Displays an appropriate empty state message if no content matches the filters.
- [x] Loading states for content fetching.
- [x] Error handling for API failures, displaying user-friendly messages.
- [x] Unit/snapshot tests for `CategorySelector`, `SearchBar`, and screen interactions.

#### Effort Estimate: **6 SP**
**Complexity**: Medium

**Breakdown**:
- Frontend: 90% (5.4 days)
- Research/Design: 10% (0.6 days)

**Reasoning**:
```
Day 1: Design & Core Layout (Web & Mobile)
- Design browse/search UI (category selector, search bar, content grid) (4 hrs)
- Implement basic screen layout (Web & Mobile) (4 hrs)

Day 2: Category Selector & Search Bar (Web & Mobile)
- Create `CategorySelector` component, fetch categories from B4 `GET /api/v1/categories` (4 hrs)
- Create `SearchBar` component (input, submit logic) (4 hrs)

Day 3: Content Grid/List & Filtering (Web)
- Implement `ContentGrid/List` component using `ContentCard` (4 hrs)
- Integrate with B4 `GET /api/v1/content` (Web) (4 hrs)
- Implement filtering logic based on selected category and search term (Web)

Day 4: Content Filtering (Mobile) & Combined Filters
- Integrate with B4 `GET /api/v1/content` (Mobile) (4 hrs)
- Implement combined filtering (category + search term) (Web & Mobile) (4 hrs)

Day 5: Interactions, Empty States & Loading (Web & Mobile)
- Implement click handler for `ContentCard` to navigate to F8 placeholder (4 hrs)
- Implement loading states, empty states (no results) (4 hrs)

Day 6: Testing, Documentation & Refinement
- Write unit/snapshot tests for components (4 hrs)
- Write integration tests for API calls and filtering (mocking B4) (2 hrs)
- Document component usage and API contracts (2 hrs)
```

**Risk Factors**:
- ⚠️ **Search Performance**: Frontend responsiveness can suffer if B4 search API is slow. *Mitigation: Implement debouncing for search input; optimize rendering for large content lists.*
- ⚠️ **Complex Filter Logic**: Managing multiple active filters and their interplay. *Mitigation: Use a dedicated state management approach (e.g., Redux Toolkit query params slice) to manage filter state.*
- ⚠️ **Accessibility**: Ensuring categories and search are navigable for all users. *Mitigation: Implement ARIA attributes, keyboard navigation.*

**Dependencies**: F1 (Web Setup), F2 (iOS Setup), F3 (Android Setup), B4 (Content Browsing & Search API), F5 (Child Profile selection for age context).
**Build Order**: #30

---

### Story F8: Audio Player UI (Basic Controls - Web & Mobile)
#### Description:
As a child, I want to use large, simple play/pause, skip forward/backward buttons, and a volume control while listening, so that I can easily manage my audio playback (FR2.3).
**Details**:
- **Components**: `AudioPlayer` (main component), `PlayPauseButton`, `SkipButton`, `ProgressBar`, `VolumeSlider`.
- **UX Flow**:
    1.  User clicks on a `ContentCard` (from F6 or F7).
    2.  Navigates to the `AudioPlayer` screen.
    3.  `AudioPlayer` fetches the stream URL from B6.
    4.  Displays large, child-friendly controls for play/pause, skip (e.g., 15s forward/backward), and volume.
    5.  A progress bar shows current playback position.
- **State Management**: Local player state (playing, paused, current time, duration, volume). Global state for currently playing `contentId`.
- **API Calls**: B6 (Audio Streaming API) - `GET /api/v1/stream/{contentId}`.
- **Responsive Design**: Controls are large and accessible on all screen sizes.
- **Edge Cases**: Network errors, content not found/accessible, end of track.
#### Acceptance Criteria
- [x] **Web & Mobile**: `AudioPlayer` screen is implemented, capable of playing audio.
- [x] Audio stream is fetched from B6 `GET /api/v1/stream/{contentId}`.
- [x] Large, child-friendly `PlayPauseButton` component functions correctly.
- [x] `SkipForwardButton` (e.g., 15 seconds) and `SkipBackwardButton` (e.g., 15 seconds) components function correctly.
- [x] `ProgressBar` component visually represents current playback position and updates in real-time.
- [x] `VolumeSlider` component controls audio output volume.
- [x] Displays content title and thumbnail of the currently playing item.
- [x] Handles playback errors gracefully (e.g., network issues, stream unavailable) with user-friendly messages.
- [x] Updates the listening history via B9 (implicitly, as part of player lifecycle - for "COMPLETE" event).
- [x] Unit/integration tests for player controls and API interactions (mocking B6).

#### Effort Estimate: **8 SP**
**Complexity**: Medium

**Breakdown**:
- Frontend: 90% (7.2 days)
- Research/Design: 10% (0.8 days)

**Reasoning**:
```
Day 1: Design & Core Player Layout (Web & Mobile)
- Design child-friendly audio player UI (large buttons, clear progress) (4 hrs)
- Implement basic `AudioPlayer` screen layout (Web & Mobile) (4 hrs)

Day 2: Audio Engine Integration (Web & Mobile)
- Research and integrate web audio API (Web) or native media players (Mobile) (e.g., `react-native-track-player` or native equivalent) (8 hrs)

Day 3: Playback Controls (Web & Mobile)
- Implement `PlayPauseButton` functionality (4 hrs)
- Implement `SkipForwardButton` and `SkipBackwardButton` (e.g., 15s) (4 hrs)

Day 4: Progress Bar & Volume Slider (Web & Mobile)
- Implement `ProgressBar` (display current time/duration, seek functionality) (6 hrs)
- Implement `VolumeSlider` (2 hrs)

Day 5: API Integration (B6) & Content Display (Web & Mobile)
- Integrate with B6 `GET /api/v1/stream/{contentId}` to fetch audio source (4 hrs)
- Display current content's title and thumbnail (4 hrs)

Day 6: Listening History Integration (B9) (Web & Mobile)
- Implement logic to trigger B9 `POST /api/v1/children/{childId}/listening-history` on track start, progress, and completion (6 hrs)
- Consider throttling/debounce for progress updates (2 hrs)

Day 7: Error Handling & UX Refinements (Web & Mobile)
- Implement robust error handling for network issues, stream errors (4 hrs)
- Fine-tune UX for responsiveness, button sizes, visual feedback (4 hrs)

Day 8: Testing & Documentation
- Write unit tests for player controls (4 hrs)
- Integration tests (mocking B6, B9) (2 hrs)
- Document player component, API interactions, and state management (2 hrs)
```

**Risk Factors**:
- ⚠️ **Media Playback Complexity**: Cross-browser/cross-platform media playback can have quirks and require specific codecs. *Mitigation: Use well-established media player libraries; focus on widely supported audio formats.*
- ⚠️ **Real-time Updates**: Updating progress bar and sending history events in real-time. *Mitigation: Optimize event listeners, use throttling for performance.*
- ⚠️ **API Latency (B6)**: If B6 is slow to return the stream, it impacts playback start time. *Mitigation: Implement loading indicators, optimize B6 performance.*

**Dependencies**: F1 (Web Setup), F2 (iOS Setup), F3 (Android Setup), B6 (Audio Streaming API), B9 (Listening History API), F6/F7 (Content selection to initiate playback).
**Build Order**: #31

---

### Story F9: Parental Dashboard UI (Child Profile Management & Age Filter - Web & Mobile)
#### Description:
As a parent, I want to access a PIN-protected dashboard to create/manage child profiles and set age-appropriateness filters for each, so that I can customize my children's access (FR3.1, FR3.2, FR3.6).
**Details**:
- **Components**: `PINInput`, `ChildProfileForm` (for create/edit), `AgeFilterSlider`, `ChildProfileList` (using `ChildAvatarCard`), `Modal/Dialog` for PIN entry.
- **UX Flow**:
    1.  Parent navigates to "Parental Dashboard" from main app menu.
    2.  If PIN not set, prompts to set one (using B7). If set, prompts for PIN entry.
    3.  Upon successful PIN entry, displays a list of child profiles.
    4.  For each child, provides options to "Edit" or "Delete" profile.
    5.  "Edit" opens `ChildProfileForm` with an `AgeFilterSlider`.
    6.  "Add New Child" button opens `ChildProfileForm`.
- **State Management**: Local component state for forms, global state for child profiles.
- **API Calls**: B7 (PIN Protection) - `POST /api/v1/parents/pin/verify`, `POST /api/v1/parents/pin/set`. B2 (Child Profile Management) - `POST`, `GET`, `PUT`, `DELETE /api/v1/children`. B5 (Age Filtering) - `PUT /api/v1/children/{childId}/age-filter`.
- **Responsive Design**: Dashboard layout adapts, forms are scrollable.
- **Edge Cases**: No PIN set, incorrect PIN, API errors during CRUD, invalid age filter.
#### Acceptance Criteria
- [x] **Web & Mobile**: Parental Dashboard entry point requires PIN verification via `PINInput` component, interacting with B7 `POST /api/v1/parents/pin/verify`.
- [x] If PIN is not set, dashboard prompts parent to set a 4-digit PIN via B7 `POST /api/v1/parents/pin/set`.
- [x] After successful PIN entry, a `ChildProfileList` displays all child profiles (from B2 `GET /api/v1/children`).
- [x] An "Add New Child" button is present, which opens a `ChildProfileForm`.
- [x] `ChildProfileForm` (for create/edit):
    -   Includes fields for child's name, avatar selection (placeholder), and an `AgeFilterSlider`.
    -   Submits to B2 (`POST /api/v1/children` for create, `PUT /api/v1/children/{childId}` for update).
    -   `AgeFilterSlider` allows setting `age_range_max` for a child, interacting with B5 `PUT /api/v1/children/{childId}/age-filter`.
- [x] Each child in `ChildProfileList` has "Edit" and "Delete" options:
    -   "Edit" pre-populates `ChildProfileForm` with child's data.
    -   "Delete" triggers B2 `DELETE /api/v1/children/{childId}` with a confirmation dialog.
- [x] All forms and interactions include loading states and display API error messages.
- [x] Unit/integration tests for PIN entry, forms, and list interactions (mocking B2, B5, B7).

#### Effort Estimate: **10 SP**
**Complexity**: High

**Breakdown**:
- Frontend: 90% (9 days)
- Research/Design: 10% (1 day)

**Reasoning**:
```
Day 1: Design & PIN Entry UI (Web & Mobile)
- Design parental dashboard layout, PIN entry flow (4 hrs)
- Implement `PINInput` component (visuals, input handling) (4 hrs)

Day 2: PIN Verification & Setting (Web & Mobile)
- Integrate `PINInput` with B7 `POST /api/v1/parents/pin/verify` (4 hrs)
- Implement logic for "PIN not set, set now" flow, integrating B7 `POST /api/v1/parents/pin/set` (4 hrs)

Day 3: Child Profile List & Basic CRUD UI (Web & Mobile)
- Implement `ChildProfileList` to display children from B2 `GET /api/v1/children` (5 hrs)
- Implement "Add New Child" button (navigation to form) (1 hr)
- Implement "Edit" and "Delete" buttons for each child in the list (2 hrs)

Day 4: ChildProfileForm (Create) (Web & Mobile)
- Implement `ChildProfileForm` with name, avatar placeholder, `AgeFilterSlider` (6 hrs)
- Integrate create logic with B2 `POST /api/v1/children` (2 hrs)

Day 5: ChildProfileForm (Edit) & Age Filter (Web & Mobile)
- Implement edit logic for `ChildProfileForm` (pre-populate data, integrate with B2 `PUT /api/v1/children/{childId}`) (6 hrs)
- Integrate `AgeFilterSlider` with B5 `PUT /api/v1/children/{childId}/age-filter` (2 hrs)

Day 6: Delete Child & Confirmation (Web & Mobile)
- Implement "Delete" functionality with confirmation dialog (3 hrs)
- Integrate with B2 `DELETE /api/v1/children/{childId}` (3 hrs)
- Refresh child list after CRUD operations (2 hrs)

Day 7: Loading, Error States & Form Validation (Web & Mobile)
- Implement loading states for all API interactions (4 hrs)
- Display API error messages for all forms/actions (4 hrs)

Day 8: Navigation, State Management & Responsive Polish (Web & Mobile)
- Ensure correct navigation between dashboard, forms (4 hrs)
- Fine-tune state management for child profiles (2 hrs)
- Responsive layout adjustments (2 hrs)

Day 9: Testing
- Write comprehensive unit tests for all components and logic (PIN, forms, list) (5 hrs)
- Write integration tests for API calls (mocking B2, B5, B7) (3 hrs)

Day 10: Documentation & Refinement
- Update documentation for dashboard components (2 hrs)
- Code review and address feedback (3 hrs)
- Final bug fixes (3 hrs)
```

**Risk Factors**:
- ⚠️ **Complex State Management**: Multiple forms, lists, and API calls require careful state management. *Mitigation: Use a global state library (e.g., Redux Toolkit) to centralize state; break down into smaller, focused components.*
- ⚠️ **Security of PIN**: Ensuring PIN is never sent in plain text or stored client-side (beyond temporary input). *Mitigation: Enforce HTTPS; rely on B7 for hashing/verification.*
- ⚠️ **UX/UI for Parental Controls**: Balancing intuitive design with robust functionality for sensitive actions. *Mitigation: Thorough design review, potentially user testing with parents.*
- ⚠️ **Error Propagation**: Handling errors from multiple backend APIs. *Mitigation: Consistent error handling patterns, centralized error display components.*

**Dependencies**: F1 (Web Setup), F2 (iOS Setup), F3 (Android Setup), B2 (Child Profile Management API), B5 (Age Filtering API), B7 (PIN Protection API), F4 (Parent Login).
**Build Order**: #32

---

### Story F10: Parental Dashboard UI (Content Blocking - Web & Mobile)
#### Description:
As a parent, I want to be able to search for and block specific content or entire categories from a child's profile via the dashboard, so that I can ensure only suitable content is available (FR3.3).
**Details**:
- **Components**: `SearchableContentList`, `CategoryBlockingList`, `BlockButton`, `UnblockButton`, `Modal/Dialog` for confirmation.
- **UX Flow**:
    1.  From Parental Dashboard (F9), navigate to "Content Blocking" for a specific child.
    2.  Displays two main sections: "Block Specific Content" and "Block Categories."
    3.  "Block Specific Content":
        -   `SearchBar` to find content (using B4).
        -   Results display `ContentCard`s with a "Block" button.
        -   A list of already blocked content is visible with "Unblock" options.
    4.  "Block Categories":
        -   A list of all categories (from B4) with toggle/checkbox to block/unblock.
        -   Visually indicates which categories are currently blocked.
- **State Management**: Local component state for search query, global state for child's blocked content/categories.
- **API Calls**: B8 (Content Blocking API) - `POST`, `DELETE`, `GET /api/v1/children/{childId}/blocked-content`. B4 (Content Browsing & Search API) - `GET /api/v1/content`, `GET /api/v1/categories`.
- **Responsive Design**: Sections adapt to screen size, lists are scrollable.
- **Edge Cases**: No content found in search, no categories.
#### Acceptance Criteria
- [x] **Web & Mobile**: A "Content Blocking" section is accessible from the Parental Dashboard (F9) for a selected child.
- [x] The screen displays two main sections: "Block Specific Content" and "Block Categories."
- [x] **Block Specific Content**:
    -   Includes a `SearchBar` to search content (using B4 `GET /api/v1/content`).
    -   Search results display `ContentCard`s with a "Block" button.
    -   A list of already blocked content items for the child (from B8 `GET /api/v1/children/{childId}/blocked-content`) is displayed with "Unblock" buttons.
    -   "Block" button submits to B8 `POST /api/v1/children/{childId}/blocked-content` (for content item).
    -   "Unblock" button submits to B8 `DELETE /api/v1/children/{childId}/blocked-content` (for content item).
- [x] **Block Categories**:
    -   Displays a list of all categories (from B4 `GET /api/v1/categories`).
    -   Each category has a toggle/checkbox to block/unblock it.
    -   Toggling submits to B8 `POST/DELETE /api/v1/children/{childId}/blocked-content` (for category).
    -   Currently blocked categories (from B8 `GET /api/v1/children/{childId}/blocked-content`) are visually indicated.
- [x] All forms and interactions include loading states and display API error messages.
- [x] Unit/integration tests for search, blocking/unblocking, and list interactions (mocking B4, B8).

#### Effort Estimate: **8 SP**
**Complexity**: Medium

**Breakdown**:
- Frontend: 90% (7.2 days)
- Research/Design: 10% (0.8 days)

**Reasoning**:
```
Day 1: Design & Core Layout (Web & Mobile)
- Design content blocking UI (search, blocked lists, category toggles) (4 hrs)
- Implement basic screen layout with two sections (Web & Mobile) (4 hrs)

Day 2: Category List & Blocking (Web & Mobile)
- Implement `CategoryBlockingList`: fetch all categories from B4 `GET /api/v1/categories` (4 hrs)
- Integrate toggle/checkbox for each category (2 hrs)
- Integrate toggle with B8 `POST/DELETE /api/v1/children/{childId}/blocked-content` for categories (2 hrs)

Day 3: Blocked Categories Display (Web & Mobile)
- Fetch and display currently blocked categories from B8 `GET /api/v1/children/{childId}/blocked-content` (4 hrs)
- Visually indicate blocked categories (2 hrs)
- Refresh blocked state after action (2 hrs)

Day 4: Content Search & Blocking UI (Web & Mobile)
- Implement `SearchBar` for content search (4 hrs)
- Display search results as `ContentCard`s with "Block" button (4 hrs)

Day 5: Content Search & Blocking Logic (Web & Mobile)
- Integrate content search with B4 `GET /api/v1/content` (5 hrs)
- Integrate "Block" button with B8 `POST /api/v1/children/{childId}/blocked-content` for content items (3 hrs)

Day 6: Display & Unblock Blocked Content Items (Web & Mobile)
- Fetch and display currently blocked content items from B8 `GET /api/v1/children/{childId}/blocked-content` (4 hrs)
- Implement "Unblock" button for blocked content items, integrating with B8 `DELETE` (4 hrs)

Day 7: Loading, Error States & UX (Web & Mobile)
- Implement loading states for all API interactions (4 hrs)
- Display API error messages (4 hrs)
- Responsive adjustments and polish (2 hrs)

Day 8: Testing & Documentation
- Write unit/snapshot tests for components (4 hrs)
- Write integration tests (mocking B4, B8) (2 hrs)
- Document UI components and API contracts (2 hrs)
```

**Risk Factors**:
- ⚠️ **Complexity of Blocked State**: Managing and updating the blocked state (categories vs. specific items) across the UI. *Mitigation: Centralize blocked state for a child in a global store; ensure efficient updates.*
- ⚠️ **Search Performance**: Frontend responsiveness during content search. *Mitigation: Implement debouncing for search input; display skeleton loaders.*
- ⚠️ **UX for Blocking**: Clearly communicating the effect of blocking (especially categories). *Mitigation: Clear on-screen labels and possibly confirmation dialogues.*

**Dependencies**: F9 (Parental Dashboard access), B8 (Content Blocking API), B4 (Content Browsing API), B2 (Child Profile Context).
**Build Order**: #33

---

### Story F11: Parental Dashboard UI (Listening Activity Monitoring - Web & Mobile)
#### Description:
As a parent, I want to view my child's listening history in the dashboard, so that I can monitor their content consumption (FR3.4).
**Details**:
- **Components**: `ListeningHistoryList` (showing content title, duration, timestamp), `DatePicker` (for filtering).
- **UX Flow**:
    1.  From Parental Dashboard (F9), navigate to "Listening Activity" for a specific child.
    2.  Displays a paginated list of listening events.
    3.  Allows filtering the list by date range using `DatePicker`.
    4.  Each item shows content title, duration played, and timestamp.
- **State Management**: Local component state for pagination, date filters. Global state for selected child profile.
- **API Calls**: B9 (Listening History Tracking API) - `GET /api/v1/children/{childId}/listening-history`.
- **Responsive Design**: List layout adjusts to screen size, pagination controls are accessible.
- **Edge Cases**: No listening history for child, no history in selected date range, API errors.
#### Acceptance Criteria
- [x] **Web & Mobile**: "Listening Activity" section is accessible from the Parental Dashboard (F9) for a selected child.
- [x] Screen displays a `ListeningHistoryList` showing content title, duration played, and timestamp for each event.
- [x] Listening history is fetched from B9 `GET /api/v1/children/{childId}/listening-history` API.
- [x] Pagination controls are implemented and functional (e.g., "Next Page", "Previous Page"), interacting with `limit`/`offset` in B9.
- [x] `DatePicker` component allows selecting a date range, filtering history using `start_date`/`end_date` in B9.
- [x] Displays an appropriate message if no listening history is available or found for the selected date range (empty state).
- [x] Loading states for history fetching.
- [x] Error handling for API failures, displaying user-friendly messages.
- [x] Unit/integration tests for list rendering, pagination, and date filtering (mocking B9).

#### Effort Estimate: **5 SP**
**Complexity**: Medium

**Breakdown**:
- Frontend: 90% (4.5 days)
- Research/Design: 10% (0.5 days)

**Reasoning**:
```
Day 1: Design & Core Layout (Web & Mobile)
- Design listening history UI (list, date picker, pagination) (4 hrs)
- Implement basic screen layout (Web & Mobile) (4 hrs)

Day 2: Listening History List & API Integration (Web & Mobile)
- Implement `ListeningHistoryList` component (displaying title, duration, timestamp) (5 hrs)
- Integrate with B9 `GET /api/v1/children/{childId}/listening-history` (3 hrs)

Day 3: Pagination & Filtering (Web & Mobile)
- Implement pagination controls (next/prev, page numbers) (4 hrs)
- Integrate `DatePicker` component for date range filtering (4 hrs)
- Apply date filters to B9 API calls.

Day 4: Loading, Empty States & Error Handling (Web & Mobile)
- Implement loading states for history fetching (4 hrs)
- Implement empty states (no history, no history for date range) (2 hrs)
- Implement error handling for API failures (2 hrs)

Day 5: Testing, Documentation & Refinement
- Write unit/integration tests for list rendering, pagination, date filtering (6 hrs)
- Document component usage and API contracts (1 hr)
- Code review and address feedback (1 hr)
```

**Risk Factors**:
- ⚠️ **Data Volume/Pagination**: Large history could lead to performance issues if pagination is not correctly implemented or optimized. *Mitigation: Ensure efficient backend pagination; use skeleton loaders on frontend.*
- ⚠️ **Date Range Logic**: Handling date range selection and UTC conversion reliably. *Mitigation: Use a robust date library (e.g., Moment.js, date-fns) for date manipulation and display.*
- ⚠️ **UX for Monitoring**: Presenting potentially large amounts of data in a digestible way for parents. *Mitigation: Focus on clear presentation; consider summary views as a future enhancement.*

**Dependencies**: F9 (Parental Dashboard access), B9 (Listening History API), B2 (Child Profile Context).
**Build Order**: #34

---

### Story F12: Parental Dashboard UI (Time Limits - Web & Mobile)
#### Description:
As a parent, I want to set daily listening time limits for each child via the dashboard, so that I can manage their screen time (FR3.5).
**Details**:
- **Components**: `TimeLimitSlider/Input`, `ToggleSwitch` (for enable/disable), `TimeSpentGauge` (visualizing time spent vs. limit).
- **UX Flow**:
    1.  From Parental Dashboard (F9), navigate to "Time Limits" for a specific child.
    2.  Displays the current `daily_limit_minutes` and a `ToggleSwitch` for `is_enabled`.
    3.  A `TimeLimitSlider/Input` allows setting the daily limit.
    4.  A `TimeSpentGauge` visually shows `time_spent_today_minutes` against the `daily_limit_minutes`.
    5.  Saving changes submits to B10.
- **State Management**: Local component state for limit value and toggle status. Global state for selected child profile.
- **API Calls**: B10 (Parental Control API - Time Limits) - `GET /api/v1/children/{childId}/time-limit`, `PUT /api/v1/children/{childId}/time-limit`.
- **Responsive Design**: Controls and gauge adapt to screen size.
- **Edge Cases**: No limit set, limit exceeded, API errors.
#### Acceptance Criteria
- [x] **Web & Mobile**: "Time Limits" section is accessible from the Parental Dashboard (F9) for a selected child.
- [x] Screen displays the current `daily_limit_minutes` and `is_enabled` status fetched from B10 `GET /api/v1/children/{childId}/time-limit`.
- [x] A `TimeLimitSlider` (or input field) allows the parent to adjust the `daily_limit_minutes`.
- [x] A `ToggleSwitch` allows enabling/disabling the time limit.
- [x] A `TimeSpentGauge` component visually represents `time_spent_today_minutes` against the `daily_limit_minutes`.
- [x] Saving changes (limit or enabled status) submits to B10 `PUT /api/v1/children/{childId}/time-limit`.
- [x] Displays appropriate messages for loading states and API errors.
- [x] The `time_spent_today_minutes` is updated periodically or on screen refresh.
- [x] Unit/integration tests for components, interactions, and API calls (mocking B10).

#### Effort Estimate: **6 SP**
**Complexity**: Medium

**Breakdown**:
- Frontend: 90% (5.4 days)
- Research/Design: 10% (0.6 days)

**Reasoning**:
```
Day 1: Design & Core Layout (Web & Mobile)
- Design time limits UI (slider, toggle, gauge) (4 hrs)
- Implement basic screen layout (Web & Mobile) (4 hrs)

Day 2: Get Time Limits & Display (Web & Mobile)
- Integrate with B10 `GET /api/v1/children/{childId}/time-limit` (5 hrs)
- Display initial `daily_limit_minutes`, `is_enabled`, `time_spent_today_minutes` (3 hrs)

Day 3: Time Limit Input & Toggle (Web & Mobile)
- Implement `TimeLimitSlider/Input` component (4 hrs)
- Implement `ToggleSwitch` component (4 hrs)

Day 4: Save Time Limit (Web & Mobile)
- Implement save button logic to submit changes to B10 `PUT /api/v1/children/{childId}/time-limit` (6 hrs)
- Handle API responses (success, error) (2 hrs)

Day 5: Time Spent Gauge & Real-time Updates (Web & Mobile)
- Implement `TimeSpentGauge` component (visualizing spent vs. limit) (5 hrs)
- Implement polling/refresh mechanism for `time_spent_today_minutes` (3 hrs)

Day 6: Loading, Error States & Testing
- Implement loading states for API interactions (4 hrs)
- Implement error handling for API failures (2 hrs)
- Write unit/integration tests (components, API calls, state) (2 hrs)
```

**Risk Factors**:
- ⚠️ **Real-time Accuracy**: `time_spent_today_minutes` might not be perfectly real-time due to polling. *Mitigation: Clarify to users that it's approximate, or implement more sophisticated real-time updates (e.g., WebSockets, future scope).*
- ⚠️ **UX for Limit Exceeded**: How the UI reacts when the limit is reached is critical. *Mitigation: Implement clear visual cues; rely on other stories for actual playback interruption.*
- ⚠️ **Input Validation**: Ensuring the slider/input prevents invalid `daily_limit_minutes`. *Mitigation: Client-side validation to complement backend validation.*

**Dependencies**: F9 (Parental Dashboard access), B10 (Time Limits API), B2 (Child Profile Context).
**Build Order**: #35

---

### Story F13: Offline Download UI (Initiate & Access - Web & Mobile)
#### Description:
As a child (or parent browsing for child), I want to see an option to download content and later access my downloaded content for offline listening, so that I can enjoy content without an internet connection (FR4.2).
**Details**:
- **Components**: `DownloadButton`, `DownloadProgressIndicator`, `DownloadedContentList` (using `ContentCard`).
- **UX Flow**:
    1.  User browses content (F7).
    2.  `DownloadButton` visible on `ContentCard` or content detail page.
    3.  Clicking `DownloadButton` initiates download.
    4.  `DownloadProgressIndicator` shows download progress.
    5.  "My Downloads" section displays `DownloadedContentList`.
    6.  Offline content can be played from this list.
- **State Management**: Local component state for download progress. Global state for list of downloaded content.
- **API Calls**: B11 (Offline Download Management API) - `GET /api/v1/download/{contentId}`.
- **Responsive Design**: Buttons, lists adapt to screen size.
- **Edge Cases**: No storage space, network error during download, content already downloaded, download in progress.
#### Acceptance Criteria
- [x] **Web & Mobile**: `DownloadButton` component displayed on content cards (F6/F7) or content detail pages for downloadable content.
- [x] Clicking `DownloadButton` calls B11 `GET /api/v1/download/{contentId}` to get a download URL.
- [x] The UI initiates the download of the audio file to secure local storage (AN7).
- [x] `DownloadProgressIndicator` visually shows the progress of an ongoing download.
- [x] **Web & Mobile**: A "My Downloads" section is accessible, displaying a `DownloadedContentList` using `ContentCard`s.
- [x] Content in `DownloadedContentList` can be played offline (using F8 logic, but pointing to local file).
- [x] `DownloadButton` changes state (e.g., "Downloading...", "Downloaded") appropriately.
- [x] Handles download errors (e.g., network loss, storage full) with user-friendly messages.
- [x] Displays an appropriate empty state message if no content is downloaded.
- [x] Unit/integration tests for download initiation, progress updates, and downloaded list display (mocking B11).

#### Effort Estimate: **7 SP**
**Complexity**: Medium

**Breakdown**:
- Frontend: 90% (6.3 days)
- Research/Design: 10% (0.7 days)

**Reasoning**:
```
Day 1: Design & Download Button (Web & Mobile)
- Design download flow and UI elements (button states, progress) (4 hrs)
- Implement `DownloadButton` component on `ContentCard` (4 hrs)

Day 2: Download Initiation & Progress (Web & Mobile)
- Integrate `DownloadButton` with B11 `GET /api/v1/download/{contentId}` to get URL (4 hrs)
- Implement client-side logic to initiate file download to secure storage (AN7) (4 hrs)
- Implement `DownloadProgressIndicator` (displaying percentage) (2 hrs)

Day 3: "My Downloads" List (Web & Mobile)
- Implement "My Downloads" screen layout (4 hrs)
- Implement `DownloadedContentList` (re-using `ContentCard`) (4 hrs)
- Integrate with local storage to list downloaded content (AN7) (2 hrs)

Day 4: Offline Playback & State Management (Web & Mobile)
- Modify F8 `AudioPlayer` to handle local file paths for downloaded content (6 hrs)
- Manage global state for tracking downloaded content (available, in progress) (2 hrs)

Day 5: Error Handling & UX (Web & Mobile)
- Implement error handling for download failures (network, storage) (4 hrs)
- Display appropriate states (downloading, downloaded, failed, no storage) (4 hrs)

Day 6: Responsive & Cleanup (Web & Mobile)
- Ensure responsive behavior for download UI (4 hrs)
- Implement option to delete downloaded content (2 hrs)
- Implement cleanup/refresh of lists (2 hrs)

Day 7: Testing & Documentation
- Write unit tests for download logic (4 hrs)
- Integration tests (mocking B11 and local storage) (2 hrs)
- Document download manager logic and API contracts (2 hrs)
```

**Risk Factors**:
- ⚠️ **Reliable Downloads**: Ensuring downloads are robust against network interruptions. *Mitigation: Implement retry logic, background downloads (mobile-specific).*
- ⚠️ **Storage Management**: Handling limited device storage. *Mitigation: Display clear warnings, allow user to delete content; implement storage monitoring (future scope).*
- ⚠️ **Offline Playback Logic**: Correctly switching between online streaming and local file playback. *Mitigation: Clear logic in F8, thorough testing of network switching scenarios.*

**Dependencies**: F7 (Content Browsing), F6 (Home Screen), B11 (Offline Download API), AN7 (Secure Local Storage Mechanism), F8 (Audio Player UI).
**Build Order**: #36

---

### Story F14: Playlist Creation & Management UI (Child & Curated - Web & Mobile)
#### Description:
As a child, I want to easily create and save my own custom playlists and discover pre-curated playlists, so that I can personalize my listening experience (FR4.3, FR4.4).
**Details**:
- **Components**: `PlaylistCard`, `PlaylistCreatorForm`, `ContentSelector` (for adding items to playlist).
- **UX Flow**:
    1.  User navigates to a "Playlists" section.
    2.  Displays "My Playlists" (child's own) and "Curated Playlists."
    3.  "My Playlists" section:
        -   "Create New Playlist" button opens `PlaylistCreatorForm`.
        -   `PlaylistCreatorForm` allows name, description, and selecting content (from available content, filtered by child's access).
        -   `PlaylistCard`s for existing playlists with "Edit", "Delete" options.
    4.  "Curated Playlists" section:
        -   `PlaylistCard`s for curated lists.
    5.  Clicking `PlaylistCard` navigates to playlist content view.
- **State Management**: Local component state for forms, global state for child's playlists and curated playlists.
- **API Calls**: B12 (Playlist Creation & Management API) - `POST`, `GET`, `PUT`, `DELETE /api/v1/children/{childId}/playlists`, `GET /api/v1/playlists/curated`, `GET /api/v1/playlists/{playlistId}/content`. B4 (Content Browsing) for content selection.
- **Responsive Design**: Lists and forms adapt to screen size.
- **Edge Cases**: No playlists created, no curated playlists, invalid content selection.
#### Acceptance Criteria
- [x] **Web & Mobile**: "Playlists" screen displays two sections: "My Playlists" and "Curated Playlists."
- [x] "My Playlists" section:
    -   Displays a list of `PlaylistCard`s for child's own playlists (from B12 `GET /api/v1/children/{childId}/playlists`).
    -   "Create New Playlist" button opens `PlaylistCreatorForm`.
    -   `PlaylistCreatorForm` allows entering name/description and selecting content items (using a `ContentSelector` integrated with B4).
    -   `PlaylistCreatorForm` submits to B12 `POST /api/v1/children/{childId}/playlists`.
    -   Each child playlist `PlaylistCard` has "Edit" and "Delete" options.
    -   "Edit" pre-populates `PlaylistCreatorForm` and submits to B12 `PUT`.
    -   "Delete" triggers B12 `DELETE /api/v1/children/{childId}/playlists/{playlistId}` with confirmation.
- [x] "Curated Playlists" section displays `PlaylistCard`s for curated lists (from B12 `GET /api/v1/playlists/curated`).
- [x] Clicking a `PlaylistCard` navigates to a placeholder "Playlist Content" screen, displaying items from B12 `GET /api/v1/playlists/{playlistId}/content`.
- [x] All forms and interactions include loading states and display API error messages.
- [x] Unit/integration tests for forms, list rendering, and API interactions (mocking B4, B12).

#### Effort Estimate: **9 SP**
**Complexity**: High

**Breakdown**:
- Frontend: 90% (8.1 days)
- Research/Design: 10% (0.9 days)

**Reasoning**:
```
Day 1: Design & Core Layout (Web & Mobile)
- Design playlist management UI (My Playlists, Curated, Create/Edit forms) (4 hrs)
- Implement basic screen layout (Web & Mobile) (4 hrs)

Day 2: Display Playlists & Create Button (Web & Mobile)
- Implement `PlaylistCard` component (name, item count, thumbnail) (4 hrs)
- Fetch and display child's playlists (B12 `GET /api/v1/children/{childId}/playlists`) (2 hrs)
- Fetch and display curated playlists (B12 `GET /api/v1/playlists/curated`) (2 hrs)

Day 3: PlaylistCreatorForm (Web & Mobile)
- Implement `PlaylistCreatorForm` (name, description, placeholder for content selection) (6 hrs)
- Implement "Create New Playlist" button to open the form (2 hrs)

Day 4: ContentSelector (Web & Mobile)
- Implement `ContentSelector` component within `PlaylistCreatorForm` (search/browse content from B4, multi-select) (8 hrs)

Day 5: Create Playlist Logic (Web & Mobile)
- Integrate `PlaylistCreatorForm` submit with B12 `POST /api/v1/children/{childId}/playlists` (6 hrs)
- Handle API responses, refresh playlist list (2 hrs)

Day 6: Edit & Delete Playlist (Web & Mobile)
- Implement "Edit" action: pre-populate `PlaylistCreatorForm`, submit to B12 `PUT` (6 hrs)
- Implement "Delete" action: confirmation dialog, submit to B12 `DELETE` (2 hrs)

Day 7: Playlist Content View & Click Interactions (Web & Mobile)
- Implement placeholder "Playlist Content" screen (displaying `ContentCard`s from B12 `GET /api/v1/playlists/{playlistId}/content`) (4 hrs)
- Implement `PlaylistCard` click to navigate to this view (4 hrs)

Day 8: Loading, Error States & Validation (Web & Mobile)
- Implement loading states for all API interactions (4 hrs)
- Display API error messages (4 hrs)
- Client-side validation for playlist name, content selection (2 hrs)

Day 9: Testing & Documentation
- Write unit/integration tests for all playlist components and flows (6 hrs)
- Document UI components and API contracts (2 hrs)
```

**Risk Factors**:
- ⚠️ **Content Selection Complexity**: A `ContentSelector` that allows browsing/searching and multi-selecting content can be a mini-app in itself. *Mitigation: Start with a simplified selection, iterate; ensure B4 is performant.*
- ⚠️ **State Management for Nested Data**: Managing playlists with nested content items, especially during edits. *Mitigation: Use a robust state management library and normalize data.*
- ⚠️ **Performance with Many Playlists/Content**: Rendering many playlists or large playlists. *Mitigation: Implement pagination/virtualization for lists if performance becomes an issue.*

**Dependencies**: F7 (Content Browsing for `ContentSelector`), B12 (Playlist API), B4 (Content Browsing/Search API), F8 (Audio Player to play content from playlist).
**Build Order**: #37

---

### Story F15: Sleep Timer UI (Web & Mobile)
#### Description:
As a child, I want to set a sleep timer for audio playback, so that my audio content automatically stops after a chosen duration (FR4.5).
**Details**:
- **Components**: `SleepTimerModal/BottomSheet`, `TimerDurationSelector` (e.g., slider, buttons for 5/10/15 min), `ToggleSwitch` (for "stop after track complete"), `CancelTimerButton`.
- **UX Flow**:
    1.  From the `AudioPlayer` (F8), a "Sleep Timer" button is accessible.
    2.  Clicking it opens a `SleepTimerModal/BottomSheet`.
    3.  Allows setting `duration_minutes` or `stop_after_track_complete`.
    4.  "Start Timer" button saves settings to B13 and starts a local countdown.
    5.  "Cancel Timer" button clears settings from B13 and stops countdown.
    6.  The timer visually updates on the UI.
    7.  When timer reaches 0, the `AudioPlayer` pauses.
- **State Management**: Local component state for timer configuration and countdown.
- **API Calls**: B13 (Sleep Timer API) - `POST /api/v1/children/{childId}/sleep-timer`, `DELETE /api/v1/children/{childId}/sleep-timer`, `GET /api/v1/children/{childId}/sleep-timer`.
- **Responsive Design**: Modal/bottom sheet is responsive.
- **Edge Cases**: Timer already running, invalid duration, API errors.
#### Acceptance Criteria
- [x] **Web & Mobile**: A "Sleep Timer" button is available on the `AudioPlayer` (F8).
- [x] Clicking the "Sleep Timer" button opens a `SleepTimerModal/BottomSheet`.
- [x] The modal displays options for setting `duration_minutes` (e.g., slider/buttons) and `stop_after_track_complete` (toggle).
- [x] Initial timer configuration is fetched from B13 `GET /api/v1/children/{childId}/sleep-timer` when the modal opens.
- [x] A "Start Timer" button saves the configuration to B13 `POST /api/v1/children/{childId}/sleep-timer` and starts a client-side countdown.
- [x] A "Cancel Timer" button clears the configuration via B13 `DELETE /api/v1/children/{childId}/sleep-timer` and stops the countdown.
- [x] The `AudioPlayer` (F8) automatically pauses playback when the client-side timer reaches zero or `stop_after_track_complete` condition is met.
- [x] The UI visually indicates if a timer is active and displays remaining time.
- [x] All interactions include loading states and display API error messages.
- [x] Unit/integration tests for modal interactions, timer logic, and API calls (mocking B13).

#### Effort Estimate: **6 SP**
**Complexity**: Medium

**Breakdown**:
- Frontend: 90% (5.4 days)
- Research/Design: 10% (0.6 days)

**Reasoning**:
```
Day 1: Design & Modal Layout (Web & Mobile)
- Design sleep timer modal UI (duration selector, toggle, start/cancel buttons) (4 hrs)
- Implement "Sleep Timer" button on F8 `AudioPlayer` (1 hr)
- Implement `SleepTimerModal/BottomSheet` layout (3 hrs)

Day 2: Get Timer & Input Controls (Web & Mobile)
- Integrate with B13 `GET /api/v1/children/{childId}/sleep-timer` to pre-populate (4 hrs)
- Implement `TimerDurationSelector` (slider/buttons) (4 hrs)

Day 3: Toggle & Set Timer (Web & Mobile)
- Implement `ToggleSwitch` for `stop_after_track_complete` (2 hrs)
- Implement "Start Timer" button to submit to B13 `POST` (4 hrs)
- Implement client-side countdown timer logic (2 hrs)

Day 4: Cancel Timer & Playback Control (Web & Mobile)
- Implement "Cancel Timer" button to submit to B13 `DELETE` (4 hrs)
- Implement logic in F8 `AudioPlayer` to pause when local timer completes (4 hrs)

Day 5: Visual Feedback, Error Handling & UX (Web & Mobile)
- Display active timer status and remaining time (4 hrs)
- Implement loading states, error handling (4 hrs)
- Ensure responsive behavior (2 hrs)

Day 6: Testing & Documentation
- Write unit/integration tests for modal, timer logic, API calls (6 hrs)
- Document timer component, API interactions (1 hr)
- Code review and address feedback (1 hr)
```

**Risk Factors**:
- ⚠️ **Client-side Timer Accuracy**: Browser/OS background limitations can affect timer accuracy. *Mitigation: Frontend should primarily handle timer, but acknowledge potential OS-level inconsistencies; use `setInterval` or `setTimeout` with careful state management.*
- ⚠️ **Sync with Backend**: While enforcement is client-side, the backend stores the *configuration*. *Mitigation: Ensure settings are consistently saved/loaded from B13.*
- ⚠️ **UX for Complex Timer**: If "stop after track" is combined with duration, UX can be tricky. *Mitigation: Start with simpler options, ensure clear visual feedback for selected mode.*

**Dependencies**: F8 (Audio Player UI), B13 (Sleep Timer API), B2 (Child Profile Context).
**Build Order**: #38

---

### Story F16: Parental Dashboard UI (Subscription Management - Web & Mobile)
#### Description:
As a parent, I want to view and manage my subscription status, payment methods, and renewal settings within the dashboard, so that I have full control over my billing (FR3.7).
**Details**:
- **Components**: `SubscriptionStatusCard`, `PaymentMethodDisplay`, `ManageSubscriptionButtons` (cancel, reactivate, update payment), `PaymentMethodForm` (for update).
- **UX Flow**:
    1.  From Parental Dashboard (F9), navigate to "Subscription Management."
    2.  Displays current subscription status (active, cancelled, trial), plan name, next billing date.
    3.  Displays current payment method (e.g., card type, last 4 digits).
    4.  Buttons for "Cancel Subscription", "Reactivate Subscription", "Update Payment Method."
    5.  "Update Payment Method" opens a form (e.g., Stripe Elements) to securely collect new payment details.
    6.  All actions interact with B14.
- **State Management**: Local component state for forms, global state for subscription details.
- **API Calls**: B14 (Subscription Management API) - `GET /api/v1/parents/me/subscription`, `POST /api/v1/parents/me/subscription/cancel`, `POST /api/v1/parents/me/subscription/reactivate`, `PUT /api/v1/parents/me/payment-method`. Stripe.js for tokenizing payment methods.
- **Responsive Design**: Layout adapts, forms are scrollable.
- **Edge Cases**: No subscription, subscription cancelled, payment method failed, API errors.
#### Acceptance Criteria
- [x] **Web & Mobile**: "Subscription Management" section accessible from Parental Dashboard (F9).
- [x] Screen displays `SubscriptionStatusCard` showing:
    -   Current subscription status (e.g., "Active", "Cancelled", "Trialing").
    -   Subscription plan name.
    -   Next billing date/renewal information.
- [x] Screen displays `PaymentMethodDisplay` showing obfuscated details of the primary payment method (e.g., "Visa ending in 1234").
- [x] "Cancel Subscription" button is visible for active subscriptions and calls B14 `POST /api/v1/parents/me/subscription/cancel` (with confirmation).
- [x] "Reactivate Subscription" button is visible for certain cancelled subscriptions and calls B14 `POST /api/v1/parents/me/subscription/reactivate`.
- [x] "Update Payment Method" button is visible and opens `PaymentMethodForm`.
- [x] `PaymentMethodForm` (e.g., integrating Stripe Elements) securely collects new card details and tokenizes them.
- [x] The tokenized payment method ID is sent to B14 `PUT /api/v1/parents/me/payment-method`.
- [x] All interactions include loading states and display API error messages.
- [x] Unit/integration tests for component rendering, button states, and API calls (mocking B14 and Stripe.js).

#### Effort Estimate: **8 SP**
**Complexity**: Medium

**Breakdown**:
- Frontend: 90% (7.2 days)
- Research/Design: 10% (0.8 days)

**Reasoning**:
```
Day 1: Design & Core Layout (Web & Mobile)
- Design subscription management UI (status card, payment method, action buttons) (4 hrs)
- Implement basic screen layout (Web & Mobile) (4 hrs)

Day 2: Get Subscription Data & Display (Web & Mobile)
- Integrate with B14 `GET /api/v1/parents/me/subscription` (5 hrs)
- Display subscription status, plan, billing info (3 hrs)

Day 3: Payment Method Display & Update UI (Web & Mobile)
- Display obfuscated payment method details (4 hrs)
- Implement "Update Payment Method" button to open `PaymentMethodForm` (2 hrs)
- Research and integrate Stripe.js/Stripe Elements for secure input/tokenization (2 hrs)

Day 4: Update Payment Method Logic (Web & Mobile)
- Implement `PaymentMethodForm` with Stripe Elements (JS) to get token (6 hrs)
- Submit tokenized ID to B14 `PUT /api/v1/parents/me/payment-method` (2 hrs)

Day 5: Cancel Subscription (Web & Mobile)
- Implement "Cancel Subscription" button (visibility, confirmation) (5 hrs)
- Integrate with B14 `POST /api/v1/parents/me/subscription/cancel` (3 hrs)

Day 6: Reactivate Subscription (Web & Mobile)
- Implement "Reactivate Subscription" button (visibility) (5 hrs)
- Integrate with B14 `POST /api/v1/parents/me/subscription/reactivate` (3 hrs)

Day 7: Loading, Error States & UX (Web & Mobile)
- Implement loading states for all API interactions (4 hrs)
- Display API error messages (4 hrs)
- Handle button enablement/disabling based on subscription status (2 hrs)

Day 8: Testing & Documentation
- Write unit/integration tests for components, API calls (mocking B14, Stripe.js) (6 hrs)
- Document subscription components, API contracts (2 hrs)
```

**Risk Factors**:
- ⚠️ **PCI Compliance**: Front-end must *never* handle raw card data. *Mitigation: Strict use of Stripe.js/Elements for all card input and tokenization; avoid custom payment forms.*
- ⚠️ **Stripe.js Integration**: Can be tricky to integrate securely and correctly. *Mitigation: Follow Stripe documentation carefully, use official libraries.*
- ⚠️ **Complex Subscription States**: Handling various subscription states (trialing, active, past_due, cancelled, etc.) in the UI. *Mitigation: Clearly map backend states to UI presentation; robust conditional rendering.*

**Dependencies**: F9 (Parental Dashboard access), B14 (Subscription Management API), AN8 (Stripe Integration Framework).
**Build Order**: #39

---

## 🤖 ML Stories

### Story M1: Establish Data Pipeline for Listening History
#### Description:
As an ML engineer, I want to create a robust data pipeline that collects, stores, and processes child listening events, so that this data can be used for recommendation engine training and analytics (FR1.5, FR3.4).
**Details**:
- **Tech Stack**: AWS Kinesis Data Streams (for real-time ingestion), AWS Lambda (for processing), AWS S3 (for raw data lake), AWS Glue (for cataloging), AWS Athena (for querying).
- **Training Data**: Raw listening event data from B9 `POST /api/v1/children/{childId}/listening-history`.
- **Input Features**: `child_id`, `content_item_id`, `duration_played_seconds`, `timestamp`, `event_type`.
- **Output**: Cleaned, structured listening event data in S3 (e.g., Parquet format), cataloged by Glue, queryable by Athena.
- **Inference Requirements**: N/A for this story (data collection only).
- **Evaluation Metrics**: Data pipeline reliability (e.g., 99.9% data ingestion success rate), data freshness (e.g., events available for query within 15 minutes of ingestion).
- **Retraining Strategy**: N/A for this story.
- **Data Model**:
    -   **Raw**: JSON event records in Kinesis/S3.
    -   **Processed**: Parquet files in S3 data lake, partitioned by `year/month/day/child_id`. Schema for processed data will include: `event_id (uuid), child_id (uuid), content_item_id (uuid), duration_played_seconds (int), event_type (string), event_timestamp (timestamp)`.
#### Acceptance Criteria
- [x] AWS Kinesis Data Stream created for ingesting raw listening events.
- [x] Backend B9 (Listening History Tracking API) configured to send listening events to Kinesis Data Stream.
- [x] AWS Lambda function created to consume data from Kinesis and write raw events to an S3 bucket (raw data lake).
- [x] S3 raw data lake bucket configured with appropriate naming conventions and partitioning (e.g., `s3://raw-listening-events/year=YYYY/month=MM/day=DD/`).
- [x] An AWS Glue Crawler configured to catalog the raw data in S3 into an AWS Glue Data Catalog.
- [x] An AWS Glue job (or another Lambda) configured to transform raw JSON data into a structured format (e.g., Parquet) and store in a separate S3 processed data lake, partitioned by `year/month/day`.
- [x] A Glue Crawler catalogs the processed data into the Glue Data Catalog.
- [x] Processed data is queryable via AWS Athena (e.g., `SELECT COUNT(*) FROM processed_listening_events`).
- [x] Data freshness: Listening events are available for query in Athena within 15 minutes of being recorded by B9.
- [x] Documentation for pipeline architecture, data schema, and querying instructions.

#### Effort Estimate: **8 SP**
**Complexity**: High

**Breakdown**:
- ML: 60% (4.8 days)
- DevOps: 40% (3.2 days)

**Reasoning**:
```
Day 1: Design & Kinesis Setup
- Design end-to-end data pipeline for listening history (4 hrs)
- Create AWS Kinesis Data Stream (2 hrs)
- Configure B9 to send events to Kinesis (2 hrs)

Day 2: Raw Data Ingestion to S3
- Create AWS Lambda function to consume Kinesis stream (4 hrs)
- Implement Lambda logic to write raw JSON events to S3 raw data lake (partitioned) (4 hrs)

Day 3: AWS Glue Cataloging (Raw) & Data Processing (Lambda/Glue Job)
- Configure AWS Glue Crawler for raw data S3 bucket (4 hrs)
- Develop Python script (Lambda or Glue job) to read raw JSON, transform to Parquet (4 hrs)

Day 4: Processed Data to S3
- Implement Lambda/Glue job to write Parquet files to S3 processed data lake (partitioned) (5 hrs)
- Optimize partitioning strategy (e.g., by child_id for user-centric queries) (3 hrs)

Day 5: AWS Glue Cataloging (Processed) & Athena
- Configure AWS Glue Crawler for processed data S3 bucket (4 hrs)
- Test querying processed data via AWS Athena (2 hrs)
- Optimize Athena query performance (e.g., using partition pruning) (2 hrs)

Day 6: Monitoring, Alerting & IAM
- Set up CloudWatch alarms for Kinesis throughput, Lambda errors, Glue job failures (4 hrs)
- Refine IAM roles for all pipeline components (Kinesis, Lambda, S3, Glue, Athena) (4 hrs)

Day 7: Data Validation & Initial ETL
- Implement basic data validation in processing Lambda (e.g., check for required fields) (4 hrs)
- Backfill/run initial ETL for any existing B9 data if available (2 hrs)
- Review data quality in S3/Athena (2 hrs)

Day 8: Documentation & Refinement
- Document pipeline architecture, component configurations, data flow (6 hrs)
- Code review and address feedback (2 hrs)
```

**Risk Factors**:
- ⚠️ **Data Volume/Throughput**: If listening events are very high, Kinesis/Lambda/S3 might need scaling/optimization. *Mitigation: Monitor Kinesis metrics; design Lambda for concurrency; S3 scales automatically.*
- ⚠️ **Schema Evolution**: Changes in event structure from B9. *Mitigation: Use schema registry (future scope) or defensive programming in Lambda; Glue Crawlers help with schema inference.*
- ⚠️ **Cost Management**: Managed services can accumulate costs. *Mitigation: Monitor AWS costs, optimize Lambda memory/duration, S3 lifecycle policies.*
- ⚠️ **Data Latency**: Meeting the 15-minute freshness target requires efficient processing. *Mitigation: Optimize Lambda execution time, Glue job run frequency.*

**Dependencies**: B9 (Listening History Tracking API to generate events), AN1 (Core Cloud Infrastructure).
**Build Order**: #40

---

### Story M2: Develop Basic Recommendation Engine (Rule-Based / Simple Content-Based)
#### Description:
As a child, I want to see personalized content suggestions on my home screen based on my declared age range and a simple analysis of my listening history (e.g., recently played, popular in age group, genre affinity), so that I can easily discover new, relevant content (FR1.5).
**Details**:
- **Model Type**: Rule-based recommendation engine or a simple content-based filtering approach. Not a complex ML model initially.
    -   **Rules**:
        1.  Content popular within the child's age group.
        2.  Content from categories recently listened to by the child.
        3.  Content that is highly rated (if ratings implemented, otherwise popular).
        4.  Exclude content already in child's listening history.
- **Training Data**: Processed listening history from M1. Content metadata from AN5.
- **Input Features**: `child_id`, `age_range_max`, `listening_history` (list of `content_item_id`s, `event_type`, `timestamp`).
- **Output**: A ranked list of `content_item_id`s.
- **Inference Requirements**: Recommendation generation < 300ms. Batch generation (e.g., daily) or real-time (on-demand). For MVP, on-demand.
- **Evaluation Metrics**: Precision@K (e.g., top 10 recommended items), novelty, diversity.
- **Retraining Strategy**: N/A for rule-based.
- **Tech Stack**: Python script leveraging Pandas/SQL for data aggregation, running as an AWS Lambda function.
#### Acceptance Criteria
- [x] Python script developed that takes `child_id` and optional parameters (e.g., number of recommendations) as input.
- [x] The script can access processed listening history data (from M1) and content metadata (from AN5 via B4/B9's database).
- [x] **Rule 1**: The engine identifies and recommends content items popular among children in the same age group as the input child.
- [x] **Rule 2**: The engine prioritizes content from categories the child has recently listened to (based on M1 history).
- [x] **Rule 3**: The engine excludes content already present in the child's recent listening history.
- [x] The script returns a list of unique `content_item_id`s.
- [x] The recommendation generation process runs within 300ms for a typical child profile.
- [x] Unit tests for each rule's logic (e.g., popularity calculation, category affinity, exclusion).
- [x] Documentation for the recommendation logic and how to run the script.

#### Effort Estimate: **7 SP**
**Complexity**: Medium

**Breakdown**:
- ML: 80% (5.6 days)
- Backend: 20% (1.4 days) - for data access/integration with existing APIs

**Reasoning**:
```
Day 1: Design & Data Access
- Design rule-based recommendation logic (4 hrs)
- Set up Python environment with necessary libraries (Pandas, database connector) (2 hrs)
- Implement data access layer to retrieve content metadata (AN5) and child's listening history (M1/B9) (2 hrs)

Day 2: Implement Rule 1: Age-Group Popularity
- Implement logic to fetch listening history for all children in the same age group (4 hrs)
- Calculate popularity scores (e.g., total play count, unique listeners) for content within that group (4 hrs)

Day 3: Implement Rule 2: Category Affinity
- Implement logic to identify categories recently listened to by the target child (from M1/B9) (4 hrs)
- Filter content based on these preferred categories (4 hrs)

Day 4: Implement Rule 3: Exclusion & Combining Rules
- Implement logic to exclude content already in the child's recent listening history (4 hrs)
- Develop a scoring/ranking mechanism to combine the rules and prioritize recommendations (4 hrs)

Day 5: Performance Optimization & Testing
- Optimize data retrieval queries for performance (4 hrs)
- Write unit tests for each implemented rule and the overall ranking logic (4 hrs)

Day 6: Script Refinement & Integration Prep
- Refine Python script for clean input/output (4 hrs)
- Prepare script for potential deployment as a Lambda function (dependency for M3) (4 hrs)

Day 7: Performance Testing & Documentation
- Measure recommendation generation time for various child profiles (4 hrs)
- Document recommendation logic, data sources, and potential improvements (4 hrs)
```

**Risk Factors**:
- ⚠️ **Data Latency/Consistency**: If M1 pipeline is slow, recommendations might be based on stale data. *Mitigation: Monitor M1 pipeline freshness; design M2 to gracefully handle older data.*
- ⚠️ **Rule Complexity**: Overly complex rules can be hard to maintain and debug. *Mitigation: Start simple, iterate; clearly document each rule's contribution.*
- ⚠️ **Performance**: Aggregating data from M1/AN5 for recommendation can be slow if not optimized. *Mitigation: Ensure efficient SQL queries; consider pre-calculating some aggregations (e.g., popular content per age group) if batch processing is introduced.*

**Dependencies**: M1 (Data Pipeline for Listening History), AN5 (Content Metadata Schema), B9 (Listening History API for detailed event data).
**Build Order**: #41

---

### Story M3: Integrate Recommendation Engine with Backend API
#### Description:
As a backend engineer, I want to expose the recommendations via an API, so that the frontend can display personalized content suggestions on the child's home screen (FR1.5).
**Details**:
- **Endpoints**:
    -   `GET /api/v1/children/{childId}/recommendations`: (Secured, Child/Parent JWT, check parent ownership)
        -   Query Params: `limit` (int, default 10).
        -   Response: `200 OK`, `[ { "id": "uuid", "title": "string", "description": "string", "audio_file_url": "url", "category_name": "string", "age_rating_min": "int", "age_rating_max": "int", "is_premium": "boolean", "thumbnail_url": "url", "duration": "int" }, ... ]`.
- **Data Model**: Uses `content_items` table (AN5) to enrich recommended `content_item_id`s from M2.
- **Business Rules**:
    -   Call the M2 recommendation engine (e.g., via internal RPC, Lambda invocation).
    -   Filter the raw recommended `content_item_id`s by the child's current age filter (B5) and content blocking rules (B8) *before* returning to the frontend.
    -   Enrich recommendations with full content metadata.
- **Integrations**: M2 (Recommendation Engine).
- **Performance**: Recommendation API response < 500ms p95 (including M2 engine execution).
- **Error Handling**: `400` for invalid `childId`, `403` for unauthorized, `500` for recommendation engine errors.
- **Tech Stack**: Spring Boot (Backend service on EKS), internal HTTP client to invoke the deployed M2 function (e.g., AWS Lambda Function URL or API Gateway).
#### Acceptance Criteria
- [x] `GET /api/v1/children/{childId}/recommendations` endpoint implemented in the backend service.
- [x] The endpoint invokes the M2 recommendation engine (e.g., calls a deployed Lambda function or an internal service).
- [x] Raw `content_item_id`s returned by M2 are enriched with full content metadata from `content_items` table (AN5).
- [x] Recommendations are filtered by the child's `age_range_max` (B5) and any active content blocking rules (B8).
- [x] The endpoint returns a list of enriched, filtered content items.
- [x] All endpoints enforce parent ownership of `childId` and return `403 Forbidden` if not owned.
- [x] The API response time is within the target of 500ms p95.
- [x] Error handling for M2 engine failures or timeouts.
- [x] Unit and integration tests cover M2 invocation, content enrichment, filtering, and authorization.
- [x] OpenAPI/Swagger documentation updated for this endpoint.

#### Effort Estimate: **5 SP**
**Complexity**: Medium

**Breakdown**:
- Backend: 70% (3.5 days)
- ML: 30% (1.5 days) - for deployment and integration of M2

**Reasoning**:
```
Day 1: Design & M2 Deployment
- Design integration strategy between backend and M2 (e.g., Lambda invocation) (4 hrs)
- Deploy M2 Python script as an AWS Lambda function (or similar service) (4 hrs)

Day 2: Backend Endpoint & M2 Invocation
- Implement `GET /api/v1/children/{childId}/recommendations` controller and service (5 hrs)
- Implement HTTP client to invoke the deployed M2 recommendation engine (3 hrs)

Day 3: Content Enrichment & Filtering
- Retrieve `content_item_id`s from M2 response (4 hrs)
- Fetch full content metadata from `content_items` table (AN5) for these IDs (4 hrs)
- Integrate age filtering (B5) and content blocking (B8) logic on the recommended content (2 hrs)

Day 4: Error Handling & Performance
- Implement robust error handling for M2 invocation failures or timeouts (4 hrs)
- Measure and optimize API response time (2 hrs)
- Implement parent ownership checks (2 hrs)

Day 5: Testing, Documentation & Refinement
- Write unit/integration tests (M2 invocation, enrichment, filtering, auth) (5 hrs)
- Update OpenAPI documentation (1 hr)
- Code review and address feedback (2 hrs)
```

**Risk Factors**:
- ⚠️ **M2 Performance**: If M2 engine is slow, this API will be slow. *Mitigation: Optimize M2 first; consider caching recommendations for a period.*
- ⚠️ **Data Discrepancies**: Filters applied here (B5, B8) might conflict or be redundant with M2's internal filtering. *Mitigation: Clarify responsibilities; ensure M2 provides *all* potentially relevant content for post-filtering.*
- ⚠️ **Invocation Overhead**: Latency from invoking a separate service/Lambda for M2. *Mitigation: Monitor invocation latency; optimize Lambda cold start if an issue.*

**Dependencies**: M2 (Recommendation Engine), B4 (Content Browsing API for metadata), B5 (Age Filtering), B8 (Content Blocking), B2 (Child Profile Context).
**Build Order**: #42

---

## 📊 Summary

### Effort by Category

| Category | Stories | Total SP | % Effort |
|----------|---------|----------|-----------|
| Architecture & Non-Functional | 9 | 46 | 23.35% |
| Backend | 14 | 74 | 37.56% |
| Frontend | 16 | 99 | 50.25% |
| ML | 3 | 20 | 10.15% |
| **MVP Total** | **42** | **239** | **121.31%** |

*Note: % Effort sums to >100% due to overlapping contributions from ML/DevOps within Backend/Frontend stories.*

### Team Composition Needed

| Role | % of Total Effort (approx) | Days Needed |
|------|----------------------------|-------------|
| Frontend Engineer | 41.4% (99 SP) | ~99 days |
| Backend Engineer | 37.7% (90.2 SP) | ~90 days |
| DevOps | 12.1% (29 SP) | ~29 days |
| ML Engineer | 8.8% (21.2 SP) | ~21 days |
| **Total** | **100%** | **~239 engineering days** |

*With 5-person team (2 FE, 2 BE, 1 DevOps/ML) working in parallel: ~10-12 weeks (with parallelization)*
*   2 FE: 99 days / 2 = 49.5 days (~10 weeks)
*   2 BE: 90 days / 2 = 45 days (~9 weeks)
*   1 DevOps/ML: 29 + 21 = 50 days (~10 weeks)
    *   This implies FE is the critical path slightly, but BE and DevOps/ML are close.
    *   Need to ensure 1 DevOps/ML person can handle both roles for 10 weeks. This might be a stretch given the complexity. Potentially split or dedicated roles.

---

## 🗓️ Sprint Plan

### Sprint 1 (Week 1) - Core Foundations
**Goal**: Establish cloud infrastructure, secure parent authentication, initial database schemas, and foundational app projects.
- ✅ **AN1**: Establish Core Cloud Infrastructure (VPC, Compute, Database) (8 SP)
- ✅ **AN2**: Implement Parent Authentication & Authorization Framework (6 SP)
- ✅ **AN5**: Configure Database Schemas for User & Content Metadata (4 SP)
- ✅ **AN6**: Implement Data Encryption for PII at Rest and In Transit (5 SP)
- ✅ **F1**: Web App - Project Setup & Core Layout (4 SP)
- ✅ **F2**: iOS App - Project Setup & Core Layout (3 SP)
- ✅ **F3**: Android App - Project Setup & Core Layout (3 SP)
**Sprint Goal Complete When**: Core cloud environment is functional, parent authentication service is deployed, database schemas are applied, and all three app projects can build and run with basic layout.

### Sprint 2 (Week 2-3) - Initial User & Content Flow
**Goal**: Enable parent/child login, basic child profile management, content ingestion, and initial content browsing.
- ✅ **AN3**: Set up Content Delivery Network (CDN) for Audio Streaming (3 SP)
- ✅ **AN4**: Implement Centralized Logging and Monitoring for Backend Services (5 SP)
- ✅ **B1**: Develop Parent Account API (Registration & Login) (4 SP)
- ✅ **B2**: Develop Child Profile Management API (CRUD) (5 SP)
- ✅ **B3**: Develop Content Ingestion API (6 SP)
- ✅ **B4**: Develop Content Browsing & Search API (Categories, Age Filter) (6 SP)
- ✅ **F4**: Parent Account Registration & Login UI (Web & Mobile) (7 SP)
- ✅ **F5**: Child Profile Selection UI (Web & Mobile) (4 SP)
**Sprint Goal Complete When**: Parents can register/login and manage child profiles. Content managers can ingest content. Children can select profiles and see initial content categories/search results.

### Sprint 3 (Week 4-5) - Core Content Consumption & Parental Controls
**Goal**: Enable audio streaming, basic kid home screen, essential parental controls (age filter, PIN), and offline storage mechanism.
- ✅ **AN7**: Establish Secure Offline Content Storage Mechanism for Mobile Apps (7 SP)
- ✅ **B5**: Develop Parental Control API (Age Filtering) (2 SP)
- ✅ **B6**: Develop Audio Streaming API (Adaptive Bitrate, DRM placeholder) (5 SP)
- ✅ **B7**: Implement PIN Protection for Parental Dashboard Access (3 SP)
- ✅ **F6**: Kid-Friendly Home Screen UI (Web & Mobile) (7 SP)
- ✅ **F7**: Content Browsing UI (Categories & Search - Web & Mobile) (6 SP)
- ✅ **F8**: Audio Player UI (Basic Controls - Web & Mobile) (8 SP)
- ✅ **F9**: Parental Dashboard UI (Child Profile Management & Age Filter - Web & Mobile) (10 SP)
**Sprint Goal Complete When**: Children can browse content, stream audio with basic controls, and parents can manage child profiles, set age filters, and access the dashboard via PIN. Secure offline storage mechanism is ready.

### Sprint 4 (Week 6-7) - Advanced Parental Controls & Monetization
**Goal**: Implement comprehensive parental controls (blocking, time limits), listening history, and the subscription payment framework.
- ✅ **AN8**: Implement Subscription & Payment Gateway Integration Framework (8 SP)
- ✅ **AN9**: Plan for COPPA & GDPR Compliance (Privacy Policy, Consent Flow) (4 SP)
- ✅ **B8**: Develop Parental Control API (Content Blocking) (6 SP)
- ✅ **B9**: Develop Listening History Tracking API (6 SP)
- ✅ **B10**: Develop Parental Control API (Time Limits) (4 SP)
- ✅ **B14**: Develop Subscription Management API (Parent Facing) (7 SP)
- ✅ **F10**: Parental Dashboard UI (Content Blocking - Web & Mobile) (8 SP)
- ✅ **F11**: Parental Dashboard UI (Listening Activity Monitoring - Web & Mobile) (5 SP)
- ✅ **F12**: Parental Dashboard UI (Time Limits - Web & Mobile) (6 SP)
- ✅ **F16**: Parental Dashboard UI (Subscription Management - Web & Mobile) (8 SP)
**Sprint Goal Complete When**: All core parental controls are functional end-to-end. Parents can manage subscriptions. Listening history is tracked and viewable.

### Sprint 5 (Week 8-9) - Content Engagement & ML Foundation
**Goal**: Complete all core functional features (offline, playlists, sleep timer) and establish the ML data pipeline for recommendations.
- ✅ **B11**: Develop Offline Download Management API (4 SP)
- ✅ **B12**: Develop Playlist Creation & Management API (Child & Curated) (8 SP)
- ✅ **B13**: Develop Sleep Timer API (3 SP)
- ✅ **M1**: Establish Data Pipeline for Listening History (8 SP)
- ✅ **F13**: Offline Download UI (Initiate & Access - Web & Mobile) (7 SP)
- ✅ **F14**: Playlist Creation & Management UI (Child & Curated - Web & Mobile) (9 SP)
- ✅ **F15**: Sleep Timer UI (Web & Mobile) (6 SP)
**Sprint Goal Complete When**: Offline downloads, playlists, and sleep timer are fully implemented and usable. The ML data pipeline is robustly collecting listening history.

### Sprint 6 (Week 10) - Initial Recommendations & MVP Polish
**Goal**: Integrate the basic recommendation engine and achieve MVP readiness.
- ✅ **M2**: Develop Basic Recommendation Engine (Rule-Based / Simple Content-Based) (7 SP)
- ✅ **M3**: Integrate Recommendation Engine with Backend API (5 SP)
**Sprint Goal Complete When**: Basic personalized content recommendations are displayed on the child's home screen. All MVP features are functional and tested.

---

## 🚨 High-Risk Items Requiring Attention

1.  **⚠️ Backend-Frontend API Contract Mismatch** (Stories B1-B14, F4-F16)
    -   Action: Establish clear API contracts using OpenAPI (Swagger) from the start. Backend should publish and communicate changes proactively. Frontend to use generated client code if feasible. Joint API design sessions.
    -   Blocker: Significant integration delays and bug fixing if contracts are misaligned.
2.  **⚠️ Mobile Platform Specifics & React Native Limitations** (Stories F2, F3, AN7, F4-F16)
    -   Action: Identify platform-specific challenges (e.g., secure storage, background downloads, media playback) early. Allocate experienced mobile developers. Leverage native modules for complex functionalities where React Native might fall short.
    -   Blocker: Unexpected technical hurdles leading to delays or inferior mobile UX.
3.  **⚠️ COPPA/GDPR Compliance Interpretation & Implementation** (Stories AN9, AN6, all B & F stories dealing with PII)
    -   Action: Legal counsel to provide clear, actionable requirements (AN9). Technical leads to ensure these are translated into concrete, verifiable ACs for implementation. Conduct regular reviews.
    -   Blocker: Legal penalties, reputational damage, or rework if compliance is not met.
4.  **⚠️ ML Recommendation Engine Performance & Data Quality** (Stories M1, M2, M3, B9)
    -   Action: Robust monitoring on M1 data pipeline. Start with simple rules (M2) and optimize for performance. Backend should apply post-filtering (B5, B8) defensively.
    -   Blocker: Slow recommendations impacting user experience, or inaccurate recommendations leading to user dissatisfaction.
5.  **⚠️ Security Vulnerabilities in Auth & Payments** (Stories AN2, AN6, AN8, B1, B7, B14, F4, F9, F16)
    -   Action: Adhere strictly to security best practices (password hashing, JWT handling, PCI compliance via Stripe). Conduct internal security reviews and consider external penetration testing for critical components. Secure API key management (Secrets Manager).
    -   Blocker: Data breaches, unauthorized access, financial fraud, legal/reputational damage.

---

**✅ Backlog Ready**: Review estimates, adjust team calibration in config.yml if needed, then start Sprint 1!