## Deploy na Vercel (Auto)

Este repositório inclui `vercel.json` para deploy estático.

- **Root**: repositório inteiro
- **Builds**: publica tudo de `playdevs/` como estático
- **Routes**: raiz `/` redireciona para `playdevs/PITCH_REVEAL.html`

### Passos
1. Importar repositório no painel da Vercel (**New Project**).
2. Não definir *Framework Preset* (usar **Other**).
3. Deploy — a URL raiz já abrirá os slides.

Caso queira trocar a página inicial, altere as `routes` em `vercel.json`.
