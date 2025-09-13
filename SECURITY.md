# Segurança

## Política
- Sem credenciais no repositório. Use variáveis de ambiente.
- Revisão de PR deve checar: secrets, dados sensíveis, permissões de scraping.

## Reporte de Vulnerabilidades
- Envie e‑mail para `security@example.com` com detalhes e PoC quando possível.

## Revisão Segura de PR (Checklist)
- [ ] Nenhum secret em código/arquivos
- [ ] Logs não vazam dados pessoais
- [ ] Dependências listadas sem versões comprometidas (futuro: SCA)
- [ ] Licenças de dados respeitadas (ver `playdevs/DATA_POLICY.md`)
