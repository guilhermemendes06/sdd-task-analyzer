"""Módulo TaskAnalyzer: análise de tarefas e produtividade.

Recebe uma lista de tarefas já existente e calcula totais, tempo médio de
conclusão (em horas, geral e por prioridade) e taxa de atraso. O módulo não
cria, edita, exclui nem persiste tarefas.
"""

import logging
from datetime import datetime, timezone
from typing import Any, Union

logger = logging.getLogger(__name__)

STATUS_CONCLUIDA = "concluida"
STATUS_PENDENTE = "pendente"

DateInput = Union[str, datetime, None]


class TaskValidationError(Exception):
    """Erro de validação dos dados de uma tarefa.

    Disparado, por exemplo, quando data_conclusao é anterior a data_criacao,
    quando um campo obrigatório está ausente ou quando uma data é inválida.
    """


def _parse_date(value: DateInput, campo: str, id_tarefa: Any) -> datetime:
    """Converte um valor em datetime com fuso (naive é tratado como UTC).

    Args:
        value: Objeto datetime ou texto em formato ISO 8601 (aceita sufixo "Z").
        campo: Nome do campo, usado na mensagem de erro.
        id_tarefa: Identificador da tarefa, usado na mensagem de erro.

    Returns:
        Datetime com informação de fuso horário.

    Raises:
        TaskValidationError: Se o valor for ausente ou não for uma data válida.
    """
    if isinstance(value, datetime):
        parsed = value
    elif isinstance(value, str):
        try:
            parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
        except ValueError as exc:
            raise TaskValidationError(
                f"Tarefa {id_tarefa}: '{campo}' com formato de data inválido: {value!r}."
            ) from exc
    else:
        raise TaskValidationError(
            f"Tarefa {id_tarefa}: campo obrigatório '{campo}' ausente ou inválido."
        )
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def _average(values: list[float]) -> float:
    """Calcula a média de uma lista, devolvendo 0.0 se ela estiver vazia.

    Args:
        values: Valores numéricos.

    Returns:
        Média dos valores ou 0.0 para lista vazia (evita divisão por zero).
    """
    if not values:
        return 0.0
    return sum(values) / len(values)


def analyze_tasks(tasks: list[dict[str, Any]]) -> dict[str, Any]:
    """Analisa uma lista de tarefas e devolve as métricas de produtividade.

    Cada tarefa é um dicionário com: id_tarefa, data_criacao, data_conclusao
    (None se pendente), prazo, prioridade e status ("concluida" ou "pendente").
    Tarefas com status desconhecido contam no total, mas não são nem
    concluídas nem pendentes.

    Args:
        tasks: Lista de tarefas a analisar.

    Returns:
        Dicionário com total_tarefas, total_concluidas, total_pendentes,
        tempo_medio_conclusao_horas (geral), tempo_medio_por_prioridade
        (prioridade -> horas) e taxa_atraso_percentual. Médias sem dados
        valem 0.0.

    Raises:
        TaskValidationError: Se a entrada não for uma lista, se uma tarefa for
            inválida ou se data_conclusao for anterior a data_criacao.
    """
    if not isinstance(tasks, list):
        raise TaskValidationError("A entrada deve ser uma lista de tarefas.")

    total_concluidas = 0
    total_pendentes = 0
    atrasadas = 0
    duracoes: list[float] = []
    duracoes_por_prioridade: dict[str, list[float]] = {}
    prioridades: set[str] = set()

    for task in tasks:
        if not isinstance(task, dict):
            raise TaskValidationError("Cada tarefa deve ser um dicionário.")
        id_tarefa = task.get("id_tarefa", "?")
        prioridade = str(task.get("prioridade", "")).strip().lower()
        status = str(task.get("status", "")).strip().lower()
        if prioridade:
            prioridades.add(prioridade)

        if status == STATUS_PENDENTE:
            total_pendentes += 1
        elif status == STATUS_CONCLUIDA:
            total_concluidas += 1
            criacao = _parse_date(task.get("data_criacao"), "data_criacao", id_tarefa)
            conclusao = _parse_date(task.get("data_conclusao"), "data_conclusao", id_tarefa)
            if conclusao < criacao:
                raise TaskValidationError(
                    f"Tarefa {id_tarefa}: data_conclusao anterior a data_criacao."
                )
            horas = (conclusao - criacao).total_seconds() / 3600
            duracoes.append(horas)
            duracoes_por_prioridade.setdefault(prioridade, []).append(horas)
            if task.get("prazo") is not None:
                prazo = _parse_date(task.get("prazo"), "prazo", id_tarefa)
                if conclusao > prazo:
                    atrasadas += 1
        else:
            logger.warning("Tarefa %s com status desconhecido: %r.", id_tarefa, status)

    taxa_atraso = atrasadas / total_concluidas * 100 if total_concluidas else 0.0
    por_prioridade = {
        p: round(_average(duracoes_por_prioridade.get(p, [])), 2) for p in sorted(prioridades)
    }
    resultado = {
        "total_tarefas": len(tasks),
        "total_concluidas": total_concluidas,
        "total_pendentes": total_pendentes,
        "tempo_medio_conclusao_horas": round(_average(duracoes), 2),
        "tempo_medio_por_prioridade": por_prioridade,
        "taxa_atraso_percentual": round(taxa_atraso, 2),
    }
    logger.info("Análise concluída: %s", resultado)
    return resultado
