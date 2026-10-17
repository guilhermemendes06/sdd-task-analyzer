"""Test Harness do TaskAnalyzer (pytest): Cenário 1, Cenário 2 e casos de borda."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from task_analyzer import TaskValidationError, analyze_tasks  # noqa: E402


@pytest.fixture
def tarefas_validas() -> list[dict]:
    """Três tarefas concluídas (uma atrasada) e uma pendente."""
    return [
        {"id_tarefa": 101, "data_criacao": "2026-10-01T08:00:00", "data_conclusao": "2026-10-01T10:00:00",
         "prazo": "2026-10-01T12:00:00", "prioridade": "alta", "status": "concluida"},
        {"id_tarefa": 102, "data_criacao": "2026-10-01T08:00:00", "data_conclusao": "2026-10-01T12:00:00",
         "prazo": "2026-10-01T13:00:00", "prioridade": "alta", "status": "concluida"},
        {"id_tarefa": 103, "data_criacao": "2026-10-01T08:00:00", "data_conclusao": "2026-10-01T14:00:00",
         "prazo": "2026-10-01T12:00:00", "prioridade": "baixa", "status": "concluida"},
        {"id_tarefa": 104, "data_criacao": "2026-10-01T09:00:00", "data_conclusao": None,
         "prazo": "2026-10-02T09:00:00", "prioridade": "baixa", "status": "pendente"},
    ]


def test_cenario_1_sucesso(tarefas_validas):
    r = analyze_tasks(tarefas_validas)
    assert r["total_tarefas"] == 4
    assert r["total_concluidas"] == 3
    assert r["total_pendentes"] == 1
    assert r["tempo_medio_conclusao_horas"] == 4.0
    assert r["tempo_medio_por_prioridade"] == {"alta": 3.0, "baixa": 6.0}
    assert r["taxa_atraso_percentual"] == pytest.approx(33.33)


def test_cenario_2_conclusao_anterior_a_criacao():
    tarefas = [{"id_tarefa": 999, "data_criacao": "2026-10-02T10:00:00",
                "data_conclusao": "2026-10-01T10:00:00", "prazo": "2026-10-03T10:00:00",
                "prioridade": "alta", "status": "concluida"}]
    with pytest.raises(TaskValidationError):
        analyze_tasks(tarefas)


def test_borda_lista_vazia():
    r = analyze_tasks([])
    assert r["total_tarefas"] == 0
    assert r["tempo_medio_conclusao_horas"] == 0.0
    assert r["taxa_atraso_percentual"] == 0.0


def test_borda_apenas_pendentes():
    tarefas = [{"id_tarefa": 1, "data_criacao": "2026-10-01T08:00:00", "data_conclusao": None,
                "prazo": "2026-10-05T08:00:00", "prioridade": "media", "status": "pendente"}]
    r = analyze_tasks(tarefas)
    assert r["total_pendentes"] == 1
    assert r["total_concluidas"] == 0
    assert r["tempo_medio_conclusao_horas"] == 0.0
    assert r["tempo_medio_por_prioridade"] == {"media": 0.0}
    assert r["taxa_atraso_percentual"] == 0.0


def test_borda_sufixo_z_e_fuso_misto():
    tarefas = [{"id_tarefa": 1, "data_criacao": "2026-10-01T08:00:00Z",
                "data_conclusao": "2026-10-01T10:00:00", "prazo": "2026-10-01T12:00:00",
                "prioridade": "alta", "status": "concluida"}]
    assert analyze_tasks(tarefas)["tempo_medio_conclusao_horas"] == 2.0


def test_borda_status_desconhecido_conta_no_total():
    tarefas = [{"id_tarefa": 1, "prioridade": "alta", "status": "cancelada"}]
    r = analyze_tasks(tarefas)
    assert r["total_tarefas"] == 1
    assert r["total_concluidas"] == 0 and r["total_pendentes"] == 0


def test_excecao_data_invalida():
    tarefas = [{"id_tarefa": 1, "data_criacao": "ontem", "data_conclusao": "2026-10-01T10:00:00",
                "prazo": None, "prioridade": "alta", "status": "concluida"}]
    with pytest.raises(TaskValidationError):
        analyze_tasks(tarefas)


def test_excecao_entrada_nao_lista():
    with pytest.raises(TaskValidationError):
        analyze_tasks("texto")  # type: ignore[arg-type]
