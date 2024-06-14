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
