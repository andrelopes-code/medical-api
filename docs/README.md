# API de Consultas Médicas
### Visão Geral
Esta é uma API de Consultas Médicas construída usando FastAPI e Python. Ela utiliza JWT para autenticação e está containerizada usando Docker. A API suporta operações CRUD para usuários e consultas, com controle de acesso baseado em funções para médicos, pacientes e administradores. Também inclui testes abrangentes.

Este mini projeto foi desenvolvido para testar uma Arquitetura de Camadas, onde diferentes partes da lógica de negócio são gerenciadas por serviços e repositórios específicos, como `UserService`, `AppointmentService`, `UserRepository`,  `AppointmentRepository`, etc.

### Recursos
- FastAPI para construção da API
- JWT para autenticação segura
- Docker para containerização
- Controle de acesso baseado em funções
- Operações CRUD abrangentes para usuários e consultas
- Testes automatizados

### Estrutura dos arquivos
```
├── alembic.ini
├── app
│  ├── api
│  │  └── v1
│  │     └── routers
│  │        ├── appointment_routes.py
│  │        ├── configure.py
│  │        ├── token_routes.py
│  │        └── user_routes.py
│  ├── core
│  │  ├── __init__.py
│  │  ├── cli.py
│  │  ├── config
│  │  │  ├── default.toml
│  │  │  ├── settings.py
│  │  │  └── settings.toml
│  │  ├── databases
│  │  │  └── postgres.py
│  │  ├── exceptions.py
│  │  ├── logger.py
│  │  ├── main.py
│  │  ├── middlewares.py
│  │  └── security
│  │     ├── auth.py
│  │     └── security.py
│  ├── models
│  │  ├── __init__.py
│  │  ├── address.py
│  │  ├── appointment.py
│  │  ├── doctor.py
│  │  ├── patient.py
│  │  ├── user.py
│  │  └── utils.py
│  ├── repositories
│  │  ├── appointment_repository.py
│  │  ├── base_repositories.py
│  │  └── user_repository.py
│  ├── schemas
│  │  ├── appointment_schemas.py
│  │  └── user_schemas.py
│  ├── services
│  │  ├── appointment_service.py
│  │  └── user_service.py
│  ├── types
│  │  ├── address.py
│  │  └── user.py
│  └── utils
│     ├── decorators.py
│     └── functions.py
├── docker
│  ├── api.dockerfile
│  ├── api_test.dockerfile
│  ├── init-scripts
│  │  └── postgres-init.sh
│  └── postgres.dockerfile
├── docker-compose.yaml
├── docs
│  └── README.md
├── Makefile
├── migrations
│  ├── env.py
│  ├── README
│  ├── script.py.mako
│  └── versions
│     ├── 4ba3bb48b7df_add_hashed_password_user_field.py
│     ├── 92c5951b5953_user_and_address_tables.py
│     ├── 7910ea212366_rename_hashed_password_to_password.py
│     ├── aca7a906c87c_add_doctor_appointment_and_patient_.py
│     ├── c1829d729063_add_is_deleted_field_to_all_tables.py
│     └── f9a075aca5a0_fix_timestamp_with_no_tz_in_address_and_.py
├── poetry.lock
├── pyproject.toml
├── pytest.ini
└── tests
   ├── appointment
   │  ├── test_appointment_repository.py
   │  ├── test_appointment_service.py
   │  └── test_appointments_routes.py
   ├── conftest.py
   ├── test_auth_service.py
   ├── test_security.py
   ├── test_types.py
   ├── tests.py
   ├── user
   │  ├── test_user_repository.py
   │  ├── test_user_routes.py
   │  ├── test_user_schemas.py
   │  └── test_user_service.py
   └── util_functions.py
```


### Endpoints da API
#### Endpoints de Usuário
- `GET /api/v1/user - Obter todos os usuários`
- `POST /api/v1/user - Criar um novo usuário`
- `GET /api/v1/user/me - Obter detalhes do usuário logado`
- `GET /api/v1/user/{user_id} - Obter usuário por ID`
- `PATCH /api/v1/user/{user_id} - Atualizar usuário por ID`
- `DELETE /api/v1/user/{user_id} - Excluir usuário por ID`
#### Endpoints de Autenticação
- `POST /api/v1/token - Obter token de acesso`
- `POST /api/v1/token/refresh - Atualizar token de acesso`
#### Endpoints de Consulta
- `GET /api/v1/appointment - Obter todas as consultas`
- `POST /api/v1/appointment - Criar uma nova consulta`
- `GET /api/v1/appointment/{appointment_id} - Obter consulta por ID`
- `PATCH /api/v1/appointment/{appointment_id} - Atualizar consulta por ID`
- `DELETE /api/v1/appointment/{appointment_id} - Excluir consulta por ID`
- `GET /api/v1/appointment/user/{user_id} - Obter consultas de um usuário`
# 
![Rotas da api](https://github.com/andrelopes-code/medical-api/blob/main/docs/docs.png?raw=true)
