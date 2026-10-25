# sdd-task-analyzer

![CI](https://github.com/guilhermemendes06/sdd-task-analyzer/actions/workflows/ci.yml/badge.svg)

Módulo Python que analisa uma lista de tarefas e calcula totais, tempo médio de conclusão (horas, geral e por prioridade) e taxa de atraso. Desenvolvido com Spec-Driven Development: o contrato está em `specs/task_analyzer_spec.md` e as regras de governança de IA em `CONTEXT_RULES.md`.

## Estrutura
```
sdd-task-analyzer/
├── .github/workflows/ci.yml    # pipeline de integração contínua
├── Dockerfile
├── docker-compose.yml
├── CONTEXT_RULES.md
├── README.md
├── .gitignore
├── requirements.txt
├── specs/task_analyzer_spec.md
├── tests/test_harness.py
└── src/task_analyzer.py
```

## Como executar localmente
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m pytest tests/test_harness.py -v
```

## Como executar com Docker
```bash
docker build -t sdd-task-analyzer .
docker run --rm sdd-task-analyzer
```
Ou, com Docker Compose:
```bash
docker compose run --rm task-analyzer
```

## Integração contínua
A cada push ou Pull Request em `main` e `develop`, o GitHub Actions executa em `ubuntu-latest` com Python 3.11: instalação das dependências, `pytest tests/test_harness.py -v` e análise estática de segurança com `bandit -r src -ll`.

## Status do build
Testes: 8 passed. Bandit: nenhum problema identificado. Requer Python 3.11+.

Autor: Guilherme Mendes Carlos — Bootcamp III, CEUB.
