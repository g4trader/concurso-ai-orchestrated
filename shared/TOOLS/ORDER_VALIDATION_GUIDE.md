# Verificação de ORDER.yml e Artefatos — Guia

Este guia define como validar **automaticamente** a execução de cada história usando os `postconditions` dentro do `ORDER.yml`.

## 1) Validar ORDER.yml contra o schema
- Arquivo do schema: `playdevs/SCHEMAS/order.schema.json`
- Verifique se todas as chaves `steps[].{role,input,prompt,output}` existem.

## 2) Executar checks de `postconditions`
Para cada `step`:
- `file_exists`: o caminho declarado deve existir no repositório.
- `contains`: o arquivo de texto deve conter todas as strings listadas em `must_include`.

> Observação: para artefatos `.zip`, apenas `file_exists` é aplicado nesta fase.

## 3) Relatório
A validação deve produzir um relatório com:
- **OK**: passo atende todas as `postconditions`.
- **FAIL**: quais checks falharam (arquivo ausente / trechos não encontrados).

## 4) Sinal verde para PR
Somente abrir PR quando **todos** os `steps` da história estiverem validados.

---

Consulte `verify_order_pseudo.py` para um esqueleto de implementação (sem dependências externas).
