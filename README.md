# Car Management API

## Descrição

Esta API foi desenvolvida para gerenciar informações sobre carros em um sistema simples de CRUD (Create, Read, Update, Delete) usando FastAPI. As informações dos carros são armazenadas em um arquivo CSV, e a API oferece endpoints para realizar operações como adicionar, listar, atualizar, excluir, filtrar e fazer backup dos dados. Também inclui funcionalidades extras como o cálculo do hash SHA256 do arquivo CSV e um sistema de logs para auditoria.

## Funcionalidades

1. **Create**: Adicionar novos carros à base de dados (armazenados em um arquivo CSV).
2. **Read**: Listar todos os carros cadastrados ou buscar um carro específico por ID.
3. **Update**: Atualizar as informações de um carro existente.
4. **Delete**: Remover um carro da base de dados.
5. **Contagem**: Retornar a quantidade total de carros cadastrados.
6. **Filtragem**: Filtrar carros com base em atributos específicos como marca, modelo ou preço.
7. **Backup**: Compactar o arquivo CSV em um arquivo ZIP e permitir o download.
8. **Integridade**: Calcular o hash SHA256 do arquivo CSV e verificar sua integridade.
9. **Logs**: Sistema de logs para registrar todas as operações realizadas na API.

## Pré-requisitos

- Python 3.7 ou superior
- FastAPI
- Uvicorn
- Pydantic
