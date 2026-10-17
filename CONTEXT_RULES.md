# CONTEXT_RULES — TaskAnalyzer

Regras de governança entregues ao assistente de IA em toda interação de geração de código.

## 1. Diretrizes obrigatórias
- Python 3.11 ou superior.
- Type hints em 100% das funções e parâmetros, inclusive o retorno.
- Docstrings no padrão Google em todas as funções e classes.
- Código em conformidade com PEP 8; cada função com uma única responsabilidade.
- Erros tratados com exceções específicas (`TaskValidationError`); nunca `except:` genérico.
- Prevenção explícita de divisão por zero: médias sem dados retornam `0.0`.
- Uso do módulo `logging` no lugar de `print`.
- O contrato de entrada e saída é o definido em `specs/task_analyzer_spec.md`.

## 2. Proibições
- Não usar bibliotecas externas além do `pytest` (somente para testes).
- Não persistir dados (arquivos, banco de dados, rede).
- Não alterar `tests/test_harness.py` nem a estrutura de pastas.
- Não inventar campos, funções ou regras que não estejam na especificação.

## 3. Interação com a IA
- Sempre enviar este arquivo e a especificação como contexto no início do prompt.
- Se algo não estiver especificado, a IA deve perguntar, não presumir.
- Todo código gerado é revisado criticamente e só entra no repositório após passar no pytest.
- A decisão e a responsabilidade finais são sempre humanas.
