# Especificação SDD — TaskAnalyzer (v1.1)

Transposição da especificação da Fase 1, ajustada ao enunciado da Fase 2.

## Propósito
Receber uma lista de tarefas existente e calcular métricas de produtividade. O módulo não cria, edita, exclui nem persiste tarefas.

## Contrato
`analyze_tasks(tasks: list[dict]) -> dict` e `TaskValidationError(Exception)`.

### Entrada (cada tarefa)
| Campo | Tipo | Observação |
|---|---|---|
| id_tarefa | int/str | Identificador |
| data_criacao | str ISO 8601 ou datetime | Obrigatório nas concluídas |
| data_conclusao | str ISO 8601, datetime ou None | None se pendente |
| prazo | str ISO 8601, datetime ou None | Base do cálculo de atraso |
| prioridade | str | alta, media, baixa |
| status | str | `concluida` ou `pendente` |

### Saída
| Campo | Descrição |
|---|---|
| total_tarefas | Quantidade total de tarefas recebidas |
| total_concluidas | Tarefas com status concluida |
| total_pendentes | Tarefas com status pendente |
| tempo_medio_conclusao_horas | Média (data_conclusao − data_criacao) em horas |
| tempo_medio_por_prioridade | Mesma média, por prioridade |
| taxa_atraso_percentual | Concluídas com data_conclusao > prazo ÷ total_concluidas × 100 |

### Regras
1. data_conclusao < data_criacao → `TaskValidationError`.
2. Data ausente ou em formato inválido em tarefa concluída → `TaskValidationError`.
3. Entrada vazia ou sem tarefas concluídas → médias e taxa iguais a `0.0`, sem exceção.
4. Status desconhecido conta em total_tarefas, mas não em concluídas nem pendentes.
5. Datas sem fuso são tratadas como UTC; sufixo "Z" é aceito.

## Cenários de aceite
- **Cenário 1 (sucesso):** tarefas 101–104 → total 4, concluídas 3, pendentes 1, média 4,0 h (alta 3,0 h; baixa 6,0 h), atraso 33,33%.
- **Cenário 2 (exceção):** tarefa 999 com conclusão anterior à criação → `TaskValidationError`.
- **Cenário 3 (borda):** lista vazia ou apenas pendentes → `0.0`, sem exceção.

## Mudanças em relação à v1.0 (Fase 1)
- Unidade do tempo médio: minutos → horas.
- Exceção de dados inválidos renomeada para `TaskValidationError`.
- Python 3.12+ → 3.11+.
- Saída simplificada para os campos exigidos na Fase 2.
