# Sistema de Gerenciamento de Pedidos

Sistema para cadastro de pedidos com clientes, seguindo os princípios de Clean Architecture, SOLID e Design Patterns.

## Requisitos

- Python 3.12+
- Poetry (gerenciador de dependências)

## Configuração do Ambiente de Desenvolvimento

1. Clone o repositório
2. Instale as dependências: `poetry install`
3. Ative o ambiente virtual: `poetry shell`

## Estrutura do Projeto

O projeto segue a Clean Architecture com as seguintes camadas:

- **Domain**: Entidades e regras de negócio
- **Application**: Casos de uso e lógica de aplicação
- **Infrastructure**: Implementações técnicas (banco de dados, mensageria)
- **Presentation**: Interfaces com o usuário (API REST)

## Executando Testes

```bash
poetry run pytest
```


# Comands
- poetry add --dev black
- poetry env info --path
- poetry run which python
- poetry run python manage.py runserver
- poetry run pytest
- poetry run ruff format --check .
- poetry run ruff format .
- poetry run ruff check --fix .


- DDD
- Clean Arch
- SOLID
- Automated tests
- Design patterns utilizados
    - Factory
    - Repository
    - Builder no validation
    - Mediator/Observer -> Monta notificacao assim que order é criada

## TODO
- Improve email validation
- 04/06
    - Fazer mediator/observer para ver evento de nova order, buscar nome do usuario na api de users e publicar evento no kafka