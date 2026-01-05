# User registration API

## Context

Dailymotion handles user registrations. To do so, user creates an account and we send a code by email to verify the account.

## Specifications
You have to manage a user registration and his activation. 

The API must support the following use cases:
* Create a user with an email and a password.
* Send an email to the user with a 4 digits code.
* Activate this account with the 4 digits code received. For this step, we consider a `BASIC AUTH` is enough to check if he is the right user.
* The user has only one minute to use this code. After that, an error should be raised.


## Run project using docker compose
To start the project and play with it, with your terminal, go in the `src` directory and run the following command:
````
docker compose up
````
Then with your browser You can:
- Access to the API documentation:
* http://127.0.0.1:8884/api/v1/docs

There is also hidden endpoints for k8s pods healthcheck:
* http://127.0.0.1:8884/health/ready
* http://127.0.0.1:8884/health/live

- Acces to PgAdmin WebUI (to access to postgres database)
* http://127.0.0.1:5050/ (creds: pgs_user/pgs_password)

When you have finish to play with the APIs don't forger to run the following commands to stop all containers:
```
docker compose down
```

## Run the tests
To run the tests, with your terminal, go in the `python-clean-archi` directory and run the following commands:

### Run the unitary tests
````
docker compose -f docker-compose-unit-tests.yml build users-tests
docker compose -f docker-compose-unit-tests.yml up users-tests
````
When it's finish don't forget to run 
````
docker compose -f docker-compose-unit-tests.yml down
````

### Run the integration tests
````
docker compose -f docker-compose-integration-tests.yml build integration-tests
docker compose -f docker-compose-integration-tests.yml up integration-tests
````
When it's finish don't forget to run 
````
docker compose -f docker-compose-integration-tests.yml down
````
Nb: if you didn't the start the application yet and you want to run test before, please make sure the `users-dailymotion` docker image is present on your computer:
````
docker compose build
````

# Architecture

- The project was developed by implementing a `hexagonal architecture`, with `use case` of the `clean architecture`.
- This project use FastAPI, Postgres (User Database) et Redis (Otp code management)
```
┌───────────────────────────────────────────────────────────────────────────┐
│                      ADAPTERS                                             │
│  app/adapters/                                                            │
│                                                                           │
│  ┌─ repositories/                                                         │
│  │   ┌─ user_repository/                                                  │
│  │   │   ├─ postgresdb_repository.py (PostgreSQL)                         │
│  │   │   └─ in_memory_repository.py (Tests)                               │
│  │   │                                                                    │
│  │   └─ otp_repositories/                                                 │
│  │       ├─ redis_repository.py (Redis)                                   │
│  │       └─ in_memory_repository.py (Tests)                               │
│  │                                                                        │
│  └─ otp/                                                                  │
│      └─ console_sender.py (Console/Email)                                 │
│  exceptions.py (Adapters exceptions)                                      │
│                                                                           │
│                                                                           │
│  ┌────────────────────────┐  ┌─────────────────────────┐  ┌────────────┐  │
│  │PostgresRepository      │  │  RedisRepository        │  │ Console    │  │
│  │/ InMemoryUserRepository│  │/ InMemoryUserRepository │  │ Sender     │  │
│  │  (implements           │  │   (implements           │  │(implements │  │
│  │  UserRepository)       │  │   OtpRepository)        │  │ OtpSender) │  │
│  │                        │  │                         │  │            │  │
│  └────────┬───────────────┘  └────────┬────────────────┘  └─────┬──────┘  │
│           │                           │                         │         │
└───────────┼───────────────────────────┼─────────────────────────┼─────────┘
            │                           │                         │
            │         PORTS             │                         │
            │    (Interfaces)           │                         │
            │      app/ports/           │                         │
            │                           │                         │
            │  ┌─ repositories/         │                         │
            └──┤   ├─ user_repository.py                          │
               │   └─ otp_repository.py                           │
               │                                                  │
               └─ otp_sender.py ──────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                    DRIVERS                                   │
│  app/drivers/rest/                                           │
│                                                               │
│  ┌─ routes/                                                  │
│  │   ├─ healthcheck.py (k8s endpoints)                       │
│  │   └─ v1/                                                 │
│  │       ├─ user.py (POST /api/v1/create, etc.)            │
│  │       └─ schema.py (Pydantic models)                    │
│  │                                                         │
│  ├─ exception_handlers.py (catch Domain exceptions)        │
│  ├─ dependencies.py (dependencies injection management)    │
│  ├─ config.py                                               │
│  └─ main.py (FastAPI app)                                   │
│                                                              │
│  ┌────────────────────────────────────────────────────┐   │
│  │              REST API (FastAPI)                    │   │
│  │  ┌──────────────┐  ┌──────────────────────────┐    │   │
│  │  │  Endpoints   │  │  Exception Handlers      │    │   │
│  │  │  /api/v1/    │  │  (catch exceptions)      │    │   │
│  │  │              │  │                          │    │   │
│  │  └──────┬───────┘  └──────────────────────────┘    │   │
│  └─────────┼──────────────────────────────────────────┘   │
└────────────┼──────────────────────────────────────────────┘
             │
┌────────────▼─────────────────────────────────────────────────────────┐
│                      USE CASES                                       │
│  app/use_cases/                                                      │
│                                                                      │
│  ├─ create_user_use_case.py                                          │
│  │    - manipulate User (Domain)                                     │
│  │    - use OtpService, OtpSender, OtpRepository, UserRepository     │
│  │    - Make User information verifications                          │
│  │    - throw exceptions                                             │
│  │                                                                   │
│  ├─ enable_user_account_use_case.py                                  │
│  │    - manipulate User (Domain)                                     │
│  │    - use OtpRepository, UserRepository                            │
│  │    - make User information verifications                          │
│  │    - make code verifications                                      │
│  │    - throw exceptions                                             │
│  │                                                                   │
│  ├─ exceptions.py (use case exceptions)                              │
│  └─ utils.py                                                         │
│                                                                      │
│  ┌──────────────────────────────────────────────────────┐            │
│  │  CreateUserUseCase(                                   │           │
│  │    user_repository: UserRepository,                   │           │
│  │    otp_sender: OtpSender,                             │           │
│  │    otp_repository: OtpRepository                      │           │
│  │  )                                                    │           │
│  │                                                        │          │
│  │  EnableUserAccountUseCase(                            │           │
│  │    user_repository: UserRepository,                   │           │
│  │    otp_repository: OtpRepository                      │           │
│  │  )                                                    │           │
│  └──────────────────┬───────────────────────────────────┘            │
└─────────────────────┼────────────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                   SERVICES                                   │
│  app/services/                                               │
│                                                               │
│  └─ otp_service.py                                           │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  OtpService(                                          │  │
│  │    otp_repository: OtpRepository,                     │  │
│  │    sender: OtpSender                                  │  │
│  │  )                                                    │  │
│  │    - _generate_code() → str                           │  │
│  │    - verify_code(user_id, code) → bool                │  │
│  │    - send_otp(user_id, destination) → None           │  │
│  └──────────────────┬───────────────────────────────────┘  │
└─────────────────────┼───────────────────────────────────────┘
                      │
                      │
        ╔═════════════▼═════════════════════════════════╗
        ║              DOMAIN (Core business)           ║
        ║  app/domain/                                  ║
        ║                                               ║
        ║  └─ entities/                                 ║
        ║      └─ user.py                               ║
        ║                                               ║
        ║  ┌────────────────────────────────────────┐   ║
        ║  │  Entities:                             │   ║
        ║  │    - User                              │   ║
        ║  │        • id: UUID,                     │   ║
        ║  │        • email: str                    │   ║
        ║  │        • password: str                 │   ║
        ║  │        • is_enabled: bool              │   ║
        ║  │                                        │   ║
        ║  │  ⚠️  No dependencies                   │   ║
        ║  │  ✅  Used by all layers                │   ║
        ║  └────────────────────────────────────────┘   ║
        ╚═══════════════════════════════════════════════╝
                                                  ↑   ↑   ↑   ↑   ↑
                      │   │   │   │   │
            ┌─────────┴───┴───┴───┴───┴──────────────────────┐
            │  Used by all layers:                           │
            │  - Use Cases (manipulates User)                │
            │  - Adapters (convert User)                     │
            │  - Drivers (convert pydantic models to entity) │
            └────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                      EXCEPTIONS                              │
│                                                              │
│  Domain Exceptions (Core):                                   │
│    app/use_cases/exceptions.py                               │
│      - InvalidEmailFormatError                               │
│      - InvalidPasswordError                                  │
│      - UserEmailAlreadyExistsError                           │
│      - UserInfoDoesntMatchError                              │
│      - IncorrectActivationCodeError                          │
│                                                              │
│  Adapter Exceptions (Technical):                             │
│    app/adapters/exceptions.py                                │
│      - DatabaseError                                         │
│      - ExternalError                                         │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                         SHARED                                │
│  app/shared/                                                  │
│                                                                │
│  └─ logging.py                                                │
│                                                                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Custom Logging (can be used in all layers)       │   │
│  │    - Structured logging (JSON)                        │   │
│  │    - Context enrichment                               │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘

```
```

app/
├── domain/                    🎯 Cœur métier (pas de dépendances)
│   └── entities/
│       └── user.py           → User entity
│
├── use_cases/                 🔄 Logique applicative
│   ├── create_user_use_case.py
│   ├── enable_user_account_use_case.py
│   ├── exceptions.py         → Domain exceptions
│   └── utils.py
│
├── services/                  ⚙️ Services de domaine
│   └── otp_service.py        → Génération/vérification OTP
│
├── ports/                     🔌 Interfaces (contrats)
│   ├── otp_sender.py         → Interface pour envoi OTP
│   └── repositories/
│       ├── user_repository.py    → Interface repo User
│       └── otp_repository.py     → Interface repo OTP
│
├── adapters/                  🔧 Implémentations
│   ├── repositories/
│   │   ├── user_repository/
│   │   │   ├── postgresdb_repository.py  → PostgreSQL
│   │   │   └── in_memory_repository.py   → Tests
│   │   └── otp_repositories/
│   │       ├── redis_repository.py       → Redis
│   │       └── in_memory_repository.py   → Tests
│   ├── otp/
│   │   └── console_sender.py → Envoi console/email
│   └── exceptions.py         → Exceptions techniques
│
├── drivers/                   🚪 Points d'entrée
│   └── rest/
│       ├── main.py           → FastAPI app
│       ├── config.py         → Configuration
│       ├── dependencies.py   → DI container
│       ├── exception_handlers.py → Gestion erreurs HTTP
│       └── routes/
│           ├── healthcheck.py
│           └── v1/
│               ├── user.py   → Endpoints /api/v1/...
│               └── schema.py → Pydantic models
│
└── shared/                    🛠️ Utilitaires transverses
    └── logging.py            → Custom logger
```
