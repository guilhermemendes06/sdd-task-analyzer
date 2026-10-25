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
- Não usar bibliotecas externas no código de produção (`src/`). Somente a biblioteca padrão do Python.
- Ferramentas de desenvolvimento autorizadas, apenas em `requirements.txt`: `pytest` (testes) e `bandit` (análise estática de segurança).
- Não persistir dados (arquivos, banco de dados, rede).
- Não alterar `tests/test_harness.py` nem a estrutura de pastas.
- Não inventar campos, funções ou regras que não estejam na especificação.

## 3. Interação com a IA
- Sempre enviar este arquivo e a especificação como contexto no início do prompt.
- Se algo não estiver especificado, a IA deve perguntar, não presumir.
- Todo código gerado é revisado criticamente e só entra no repositório após passar no pytest.
- A decisão e a responsabilidade finais são sempre humanas.

## 4. Infraestrutura e segurança (Fase 3)
- O pipeline de CI roda no GitHub Actions, em `ubuntu-latest`, com Python 3.11, a cada push ou Pull Request nas branches `main` e `develop`.
- O pipeline executa `pytest tests/test_harness.py -v` e `bandit -r src -ll`; falha em qualquer um bloqueia a integração.
- O ambiente de execução em contêiner usa a imagem `python:3.11-slim` e deve rodar toda a suíte de testes com um único comando.
- Proibido incluir senhas, tokens, chaves ou dados pessoais no repositório.
- Proibido usar `eval`, `exec`, `pickle`, `subprocess` ou execução dinâmica de código.
- Toda sugestão da IA que adicione dependência, arquivo ou etapa de pipeline não prevista nestas regras é rejeitada até revisão humana.
