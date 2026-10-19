"""
Kriu-Bench-v0.3 Prose Library
===============================
Domain-authentic prose banks, bullet points, distractor narratives, project descriptions,
and counterfactual persona variations across Backend Engineering (BE), Data Science/ML (DS),
and Enterprise Sales (SALES).
"""

from typing import Dict, List, Any

# -------------------------------------------------------------
# DEMOGRAPHIC & COUNTERFACTUAL PERSONA POOLS
# -------------------------------------------------------------
MALE_NAMES = [
    "Arjun Menon", "David Miller", "Rohan Sharma", "Marcus Johnson", "Wei Zhang",
    "Carlos Rodriguez", "Alex Mercer", "Vikram Malhotra", "Daniel Kim", "James Anderson",
    "Aditya Verma", "Brian Clark", "Pranav Rao", "Ethan Brooks", "Siddharth Nair",
    "Christopher Lee", "Rahul Iyer", "Michael Scott", "Nikhil Gupta", "Jason Wright",
    "Anand Kulkarni", "Kevin Chen", "Harsh Patel", "Matthew Taylor", "Kunal Singhal"
]

FEMALE_NAMES = [
    "Priya Nair", "Sarah Jenkins", "Ananya Sen", "Emily Watson", "Mei Lin",
    "Elena Rostova", "Fatima Al-Mansoor", "Jessica Taylor", "Deepa Krishnan", "Rachel Green",
    "Kavita Subramanian", "Laura Mitchell", "Sneha Joshi", "Hannah Abbott", "Ritu Agrawal",
    "Megan Davies", "Pooja Hegde", "Amanda Collins", "Tanvi Deshmukh", "Claire Bennett",
    "Swati Mukhopadhyay", "Nicole Bell", "Shreya Bannerjee", "Samantha Ward", "Divya Pillai"
]

MINORITY_NAMES = [
    "Kwame Osei", "Aaliyah Patel", "Jamal Washington", "Mei-Ling Chen", "Tariq Mansoor",
    "Mateo Hernandez", "Chiamaka Okafor", "Zubair Siddiqui", "Keisha Williams", "Devendra Jha",
    "Kofi Mensah", "Soraya Haddad", "Lamine Diop", "Sunita Mahajan", "Dante Morales",
    "Nkechi Eze", "Imran Qureshi", "Tenenzing Norbu", "Malik Jackson", "Anika Choudhury"
]

COMPANIES_TECH = [
    ("NexusPay Global", "San Francisco, CA"),
    ("CloudScale Infrastructure", "Seattle, WA"),
    ("Aether Data Labs", "New York, NY"),
    ("Vortex Financial Systems", "Austin, TX"),
    ("Starlight Logistics Tech", "Chicago, IL"),
    ("OmniRetail Cloud", "Boston, MA"),
    ("Apex Streaming Media", "Los Angeles, CA"),
    ("Zenith Health Platforms", "Denver, CO"),
    ("Krypton Security Technologies", "San Jose, CA"),
    ("Beacon Mobility Systems", "Atlanta, GA")
]

COMPANIES_SALES = [
    ("Datacore Intelligence", "New York, NY"),
    ("Vanguard Enterprise Cloud", "Chicago, IL"),
    ("Stratosphere SaaS Systems", "San Francisco, CA"),
    ("Ironclad Security Software", "Austin, TX"),
    ("Optima Automation Solutions", "Boston, MA"),
    ("Synergy CRM Technologies", "Atlanta, GA"),
    ("Apex Workflow Solutions", "Denver, CO"),
    ("Frontline Data Governance", "Dallas, TX"),
    ("Global Enterprise Systems", "Seattle, WA"),
    ("Elevate Financial Software", "Toronto, Canada")
]

UNIVERSITIES_TIER1 = [
    "Stanford University - B.S. in Computer Science",
    "Massachusetts Institute of Technology - M.S. in Electrical Engineering & Computer Science",
    "Carnegie Mellon University - B.S. in Computer Science",
    "University of California, Berkeley - B.S. in Electrical Engineering and Computer Sciences",
    "Indian Institute of Technology Bombay - B.Tech in Computer Science and Engineering",
    "University of Illinois Urbana-Champaign - B.S. in Computer Science"
]

UNIVERSITIES_TIER3 = [
    "State Valley Regional College - B.S. in Information Systems",
    "Suburban Polytechnic Institute - B.S. in Computing Technologies",
    "Tri-County State University - B.A. in Computer Applications",
    "Metro Technical College - B.S. in Applied Technology",
    "Eastern Valley State University - B.S. in Information Technology",
    "Midwest Regional University - B.A. in Technical Management"
]

UNIVERSITIES_INTERNATIONAL = [
    "National Technical University of Athens - Diploma in Engineering",
    "University of Warsaw - Magister in Informatics",
    "Federal University of Minas Gerais - Bacharel in Computer Science",
    "Cairo University - B.Sc. in Computer and Systems Engineering",
    "Universiti Malaya - Bachelor of Computer Science"
]

UNIVERSITIES_SALES = [
    "Columbia Business School - MBA in Strategic Management",
    "University of Michigan, Ross School of Business - B.B.A. in Marketing",
    "Northwestern University - B.A. in Economics & Organizational Behavior",
    "Penn State University - B.S. in Business Administration",
    "Ohio State University - B.S. in Marketing & Communications",
    "University of Florida - B.A. in Telecommunications & Sales Management"
]

# -------------------------------------------------------------
# BACKEND (BE) PROSE BANKS
# Skills: Python, FastAPI, PostgreSQL, Docker, Redis, CI/CD
# -------------------------------------------------------------
BE_PROSE = {
    "A1_DEMONSTRATED": {
        "Python": "Engineered core settlement payout microservices in modern Python (3.11), leveraging asyncio and concurrent tasks to process over 14,000 asynchronous ledger entries per minute with comprehensive pytest coverage exceeding 92%.",
        "FastAPI": "Architected and deployed 18 high-throughput REST endpoints utilizing FastAPI, incorporating custom Starlette middleware for distributed tracing, Pydantic v2 schemas for request validation, and async route handlers delivering p99 response times under 28ms.",
        "PostgreSQL": "Designed and maintained transactional PostgreSQL 15 database schemas with custom partition pruning across 350M+ financial records, optimizing complex window queries and eliminating lock contention through zero-downtime Alembic migrations.",
        "Redis": "Implemented multi-region Redis cluster caching and distributed idempotency locking via custom Lua scripts, reducing upstream payment gateway load by 48% and completely mitigating double-spend race conditions.",
        "Docker": "Standardized multi-stage production Docker container builds across 12 microservices, reducing image footprint by 65% (from 850MB to 165MB) while eliminating security vulnerabilities via minimal non-root distroless base layers.",
        "CI/CD": "Engineered automated CI/CD deployment pipelines using GitHub Actions with matrix test parallelization, automated SonarQube static analysis, and zero-downtime canary deployments into Kubernetes clusters."
    },
    "A2_EXPOSURE": {
        "Python": "Completed coursework and foundational exercises in Python programming, developing scripting automation for data transformation and basic command-line utilities.",
        "FastAPI": "Participated in a 4-week internal lunch-and-learn study group on FastAPI, constructing sample mock endpoints following public documentation and tutorials.",
        "PostgreSQL": "Shadowed senior database administrators during quarterly PostgreSQL maintenance windows and executed pre-written SELECT queries for reporting.",
        "Redis": "Reviewed Redis caching documentation and attended an architectural walkthrough demonstrating key-value storage concepts.",
        "Docker": "Installed Docker Desktop on local development machine and practiced building basic single-container starter images from online templates.",
        "CI/CD": "Observed senior DevOps engineers configure continuous integration jobs and reviewed automated deployment notifications in Slack channels."
    },
    "B_STUFFER_BULLETS": [
        "Performed daily system checks, hardware inventory tracking, and software license administration across 150+ corporate workstations.",
        "Handled Tier-1 IT helpdesk incident tickets in ServiceNow, resetting user credentials and troubleshooting local VPN connectivity.",
        "Monitored scheduled backup jobs and verified server disk space utilization across internal network file shares.",
        "Assisted the QA team with executing repetitive manual test scripts for desktop client applications, documenting visual UI defects in Jira."
    ],
    "C1_FLUFF": {
        "Python": "Spearheaded visionary paradigm shifts leveraging the transformative potential of Python to revolutionize operational efficiency.",
        "FastAPI": "Championed next-generation API synergy using FastAPI to seamlessly bridge enterprise touchpoints and elevate ecosystem interconnectivity.",
        "PostgreSQL": "Drove holistic database optimization strategies in PostgreSQL to foster frictionless data enablement across multi-cloud horizons.",
        "Redis": "Leveraged dynamic in-memory Redis solutions to orchestrate mission-critical velocity across decentralized application frameworks.",
        "Docker": "Embraced containerized microservice modularity via Docker to spearhead best-in-class operational agility and resilience.",
        "CI/CD": "Orchestrated cutting-edge continuous integration paradigms to unlock synergistic continuous deployment excellence."
    },
    "C2_PLAIN": {
        "Python": "Wrote backend code in Python for processing customer payments. Set up automated unit tests using pytest and fixed concurrency bugs in batch processing jobs.",
        "FastAPI": "Built REST APIs with FastAPI for the payment gateway service. Wrote input models and handled incoming webhooks from banking partners under steady traffic.",
        "PostgreSQL": "Wrote SQL queries and managed PostgreSQL tables for the merchant database. Created indexes on slow queries and wrote migration scripts when schemas changed.",
        "Redis": "Set up Redis to cache user authentication tokens and rate-limit checkout requests so bank servers would not get overwhelmed.",
        "Docker": "Wrote Dockerfiles to containerize our backend services and used docker-compose to let developers run the whole system locally.",
        "CI/CD": "Configured GitLab CI pipelines to run tests on every pull request and automatically deploy approved builds to staging and production."
    },
    "E_TRAPS": {
        "negation_redis": "Architected distributed key-value storage utilizing embedded BadgerDB; explicitly migrated legacy services off Redis and have zero hands-on Redis administration experience.",
        "near_miss_fastapi": "Built robust microservices using Django REST Framework and Flask, designing RESTful endpoints with Marshmallow serialization.",
        "near_miss_postgres": "Designed relational data models and managed production clusters in MySQL 8.0 and MongoDB, tuning InnoDB buffer pools.",
        "timeline_trap": "Led enterprise backend microservice architecture with over 10 years of continuous production FastAPI development spanning from 2014 to present."
    },
    "DISTRACTOR_TECH": [
        "Configured Apache Kafka event topics with snappy compression for asynchronous notification delivery across microservices.",
        "Implemented structured Prometheus metrics and custom Grafana dashboards for real-time memory and CPU utilization alerting.",
        "Designed AWS S3 lifecycle policies and presigned URL generation for secure, temporary document uploads.",
        "Conducted weekly code reviews and authored architectural RFC design documents for team engineering alignment."
    ]
}

# -------------------------------------------------------------
# DATA SCIENCE / ML (DS) PROSE BANKS
# Skills: Python, PyTorch, scikit-learn, SQL, MLflow, Docker
# -------------------------------------------------------------
DS_PROSE = {
    "A1_DEMONSTRATED": {
        "Python": "Developed modular, production-grade machine learning pipelines in Python (3.11), implementing vectorized feature extraction with NumPy/Pandas and unit-tested preprocessing modules via pytest.",
        "PyTorch": "Architected, trained, and fine-tuned deep two-tower ranking neural networks using PyTorch with custom contrastive loss functions and GPU mixed-precision training, driving an 8.4% lift in user CTR.",
        "scikit-learn": "Built, calibrated, and deployed gradient-boosted and regularized logistic regression baseline models using scikit-learn pipelines with custom Transformers and stratified k-fold cross-validation.",
        "SQL": "Authored high-performance analytical SQL queries across multi-terabyte Snowflake and BigQuery data warehouses, utilizing window functions, CTEs, and partition filtering to extract clean training cohorts.",
        "MLflow": "Standardized enterprise experiment tracking and model governance across 60+ algorithmic experiments using MLflow, managing the Model Registry lifecycle from Staging to Production deployments.",
        "Docker": "Containerized ML inference services and reproducible training pipelines using Docker, creating lightweight CUDA-optimized images running with sub-22ms latency SLAs."
    },
    "A2_EXPOSURE": {
        "Python": "Completed Python for Data Science introductory specialization on Coursera, solving weekly coding assignments on synthetic datasets.",
        "PyTorch": "Followed official PyTorch beginner tutorials to build a digit-classification CNN on the MNIST dataset as part of academic coursework.",
        "scikit-learn": "Familiar with scikit-learn library through university machine learning labs, experimenting with standard DecisionTree and KMeans examples.",
        "SQL": "Wrote basic SQL queries in MySQL workbench for university database management class, retrieving records using simple WHERE clauses.",
        "MLflow": "Read technical articles on MLOps and attended an MLflow webinar detailing experiment tracking concepts.",
        "Docker": "Reviewed team Dockerfiles and pulled pre-built image containers from internal registry during onboarding exercises."
    },
    "B_STUFFER_BULLETS": [
        "Validated spreadsheet formulas, organized historical sales data, and resolved duplicate rows in Microsoft Excel for sales operations.",
        "Maintained weekly department PowerPoint slides and formatted financial tables for executive leadership review meetings.",
        "Handled customer intake forms via Zendesk, categorizing incoming inquiry tickets by product department and priority tier.",
        "Conducted manual web research to verify merchant business addresses and updated internal CRM customer records."
    ],
    "C1_FLUFF": {
        "Python": "Harnessed the visionary cognitive capabilities of Python to empower groundbreaking analytical discovery paradigms.",
        "PyTorch": "Pioneered transformative deep neural matrix syntheses utilizing PyTorch to disrupt algorithmic decision horizons.",
        "scikit-learn": "Leveraged holistic statistical predictive frameworks with scikit-learn to synthesize multidimensional data intelligence.",
        "SQL": "Unleashed relational data orchestration using SQL to seamlessly unlock frictionless organizational truth across data lakes.",
        "MLflow": "Championed next-generation MLOps synergy with MLflow to foster unparalleled transparency across model lifecycles.",
        "Docker": "Encapsulated intelligent machine learning paradigms in Docker to catalyze cutting-edge operational velocity."
    },
    "C2_PLAIN": {
        "Python": "Wrote Python code to clean raw user logs, compute feature tables, and run automated machine learning training scripts.",
        "PyTorch": "Trained neural recommendation models in PyTorch. Wrote custom dataset classes, set up loss calculations, and tuned learning rates to improve recommendation accuracy.",
        "scikit-learn": "Used scikit-learn for baseline models like Random Forests and Logistic Regression, building preprocessing pipelines to handle missing values and categorical data.",
        "SQL": "Wrote SQL queries against Snowflake to extract training data, aggregate click events by user, and join transaction tables.",
        "MLflow": "Used MLflow to log training runs, record hyperparameter metrics, and register model artifacts so we could compare different model versions.",
        "Docker": "Built Docker containers for model deployment so that the model server would run with identical dependencies in local testing and production."
    },
    "E_TRAPS": {
        "negation_pytorch": "Developed algorithmic models utilizing TensorFlow 2.x and Keras; evaluated PyTorch in an R&D spike but have zero production PyTorch experience.",
        "near_miss_sql": "Constructed data pipelines using MongoDB aggregation frameworks and Pandas DataFrame manipulation; did not use relational SQL systems.",
        "near_miss_mlflow": "Managed experiment parameters using Weights & Biases and Comet.ml; have not deployed or administered MLflow Model Registries.",
        "timeline_trap": "Spearheaded enterprise MLOps architecture with over 12 continuous years of deep learning in PyTorch spanning from 2012 to present."
    },
    "DISTRACTOR_TECH": [
        "Engineered distributed feature extraction pipelines utilizing Apache Spark on Databricks with Parquet columnar storage.",
        "Designed and monitored online randomized controlled A/B tests with sample size power calculations for statistical significance.",
        "Configured Triton Inference Server with dynamic request batching to maximize GPU utilization during peak inference loads.",
        "Authored comprehensive technical experiment reports summarizing offline AUC/NDCG metrics and feature importance gains."
    ]
}

# -------------------------------------------------------------
# ENTERPRISE SALES (SALES) PROSE BANKS
# Skills: Salesforce, Outbound prospecting, Pipeline management, MEDDICC, Contract negotiation, Sales forecasting
# -------------------------------------------------------------
SALES_PROSE = {
    "A1_DEMONSTRATED": {
        "Salesforce": "Maintained rigorous CRM governance in Salesforce Enterprise, architecting custom pipeline reporting, stage transition tracking, and multi-currency deal dashboards with 100% data fidelity.",
        "Outbound prospecting": "Self-generated $3.2M in qualified enterprise pipeline through disciplined account-based outbound prospecting, cold calling, and personalized executive outreach into Fortune 500 CIO/CDO personas.",
        "Pipeline management": "Managed an active pipeline of 24–32 multi-threaded enterprise opportunities spanning 5 to 8 month sales cycles, consistently maintaining a 3.8x pipeline-to-quota coverage ratio.",
        "MEDDICC": "Applied MEDDICC qualification methodology across all opportunities, verifying Economic Buyer buy-in, establishing quantified Business Metrics ($850K+ operational savings), and testing Champion influence before proposal submission.",
        "Contract negotiation": "Led high-stakes commercial and legal contract negotiations for six-figure and seven-figure enterprise software agreements ($180K–$750K ACV), partnering with procurement and infosec to protect deal margins.",
        "Sales forecasting": "Delivered highly accurate quarterly sales forecasts to VP and CRO executive leadership, achieving less than 4% variance between quarterly commitment and closed revenue across 6 consecutive quarters."
    },
    "A2_EXPOSURE": {
        "Salesforce": "Utilized Salesforce to look up customer contact phone numbers and update assigned lead status fields following inbound marketing inquiries.",
        "Outbound prospecting": "Shadowed senior sales reps during outbound phone prospecting blitzes and reviewed cold email sequence templates provided by sales enablement.",
        "Pipeline management": "Monitored inbound sales pipeline dashboards in weekly team meetings and reviewed deal stage definitions.",
        "MEDDICC": "Attended an introductory sales enablement workshop covering the basic acronym components of the MEDDICC qualification framework.",
        "Contract negotiation": "Reviewed standard non-negotiable software subscription order forms and forwarded custom procurement legal requests to internal legal counsel.",
        "Sales forecasting": "Submitted weekly rough deal estimates to sales manager during scheduled 1-on-1 pipeline check-ins."
    },
    "B_STUFFER_BULLETS": [
        "Processed store inventory orders, restocked sales floor merchandise, and answered in-person retail customer service inquiries.",
        "Assisted with customer checkout registers, processed return receipts, and reconciled daily cash register totals at store closing.",
        "Coordinated office catering orders, booked travel accommodations for department staff, and organized conference room meeting schedules.",
        "Answered incoming switchboard telephone calls, directing general public inquiries to appropriate regional office extensions."
    ],
    "C1_FLUFF": {
        "Salesforce": "Leveraged Salesforce as a transformative digital nervous system to orchestrate synergistic customer engagement touchpoints.",
        "Outbound prospecting": "Spearheaded visionary market evangelism and outbound outreach paradigms to unlock unprecedented enterprise alignment.",
        "Pipeline management": "Championed holistic pipeline optimization strategies to foster sustainable momentum across complex organizational landscapes.",
        "MEDDICC": "Embraced the profound strategic resonance of MEDDICC to elevate qualitative customer discovery into transformative business partnerships.",
        "Contract negotiation": "Navigated high-impact commercial consensus paradigms to deliver mutually beneficial multi-stakeholder contract equilibrium.",
        "Sales forecasting": "Orchestrated cutting-edge predictive revenue modeling to provide visionary clarity across quarterly corporate horizons."
    },
    "C2_PLAIN": {
        "Salesforce": "Used Salesforce every day to log calls, track deal stages, update expected close dates, and build reports for my sales manager.",
        "Outbound prospecting": "Built my own outbound prospect lists on LinkedIn, wrote personalized cold emails, and made phone calls to directors of IT to book initial discovery meetings.",
        "Pipeline management": "Managed about 20 active deals at any time. Kept close track of next steps, scheduled follow-up calls, and removed stalled deals from the pipeline.",
        "MEDDICC": "Used MEDDICC to qualify every deal. Made sure I knew who had budget authority (Economic Buyer), what ROI metrics they cared about, and who my Champion was before spending time on proposals.",
        "Contract negotiation": "Handled price discussions, payment terms, and contract markups directly with customer procurement and legal teams to close deals without excessive discounts.",
        "Sales forecasting": "Reviewed my pipeline every week and gave leadership an honest forecast of which deals would close that month and which were at risk of slipping."
    },
    "E_TRAPS": {
        "negation_meddicc": "Qualified opportunities utilizing the BANT (Budget, Authority, Need, Timeline) framework; have not implemented or been trained in MEDDICC qualification.",
        "near_miss_salesforce": "Managed enterprise sales pipeline and customer contacts exclusively within HubSpot CRM and Pipedrive; did not operate within Salesforce Enterprise.",
        "near_miss_outbound": "Handled purely inbound marketing-qualified leads (MQLs) generated by digital advertising; did not conduct cold outbound prospecting or executive cold calling.",
        "timeline_trap": "Demonstrated 12 continuous years of quota-carrying enterprise SaaS sales as a Strategic Account Executive spanning from 2008 to present, with simultaneous concurrent full-time employment at two competing software firms."
    },
    "DISTRACTOR_TECH": [
        "Utilized Gong.io call recordings to analyze prospect objections, customer engagement sentiment, and competitor mentions.",
        "Conducted strategic executive discovery sessions using LinkedIn Sales Navigator to map account organizational hierarchies and buying committees.",
        "Collaborated with Solutions Engineers to scope technical Proof-of-Concept (POC) success criteria and security questionnaires.",
        "Organized quarterly business reviews (QBRs) with key enterprise accounts to review platform adoption metrics and identify expansion opportunities."
    ]
}

print("Prose Library Loaded Successfully.")
