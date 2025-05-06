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
poetry run python -m pytest --cov=src --cov-report=term-missing
```

poetry env info --path

## TODO
- Improve email validation
- Create a validator class