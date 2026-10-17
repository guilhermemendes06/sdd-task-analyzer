# sdd-task-analyzer

Módulo Python que analisa uma lista de tarefas e calcula totais, tempo médio de conclusão (horas, geral e por prioridade) e taxa de atraso. Desenvolvido com Spec-Driven Development: o contrato está em `specs/task_analyzer_spec.md` e as regras de governança de IA em `CONTEXT_RULES.md`.

## Estrutura
```
sdd-task-analyzer/
├── README.md
├── CONTEXT_RULES.md
├── .gitignore
├── requirements.txt
├── specs/task_analyzer_spec.md
├── tests/test_harness.py
└── src/task_analyzer.py
```

## Como executar
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m pytest -v
```

## Uso
```python
from src.task_analyzer import analyze_tasks
resultado = analyze_tasks(lista_de_tarefas)
```

## Status do build
Testes: 8 passed (pytest). Requer Python 3.11+.

Autor: Guilherme Mendes Carlos — Bootcamp III, CEUB.
