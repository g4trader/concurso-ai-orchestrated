# 🚀 Publicando o Pitch no Vercel

Este guia mostra como publicar a apresentação Reveal.js (`PITCH_REVEAL.html`) no **Vercel**.

---

## 1. Estrutura do Projeto

A pasta `playdevs/` já contém:
- `PITCH_SLIDES.md` → conteúdo em Markdown
- `PITCH_REVEAL.html` → apresentação Reveal.js que lê o Markdown

---

## 2. Configuração do Vercel

1. Faça login em [Vercel](https://vercel.com).
2. Crie um novo projeto e selecione este repositório GitHub.
3. Na configuração do projeto:
   - **Framework Preset:** escolha **Other** (não usar Next.js).  
   - **Output Directory:** defina como `playdevs`.  
   - **Root Directory:** mantenha a raiz do repositório.  

> Isso faz com que o Vercel sirva diretamente os arquivos da pasta `playdevs/`.

---

## 3. Deploy

1. Clique em **Deploy**.  
2. Após alguns segundos, seu projeto estará no ar.  
3. O link ficará assim:  
   ```
   https://{seu-projeto}.vercel.app/PITCH_REVEAL.html
   ```

---

## 4. Navegação na Apresentação

- Use **← →** para navegar.  
- Pressione **F** para fullscreen.  
- Pressione **S** para abrir o modo “speaker notes”.  

---

## 5. Customização

- Edite `PITCH_SLIDES.md` para atualizar o conteúdo dos slides.  
- O tema pode ser trocado no `<link>` dentro de `PITCH_REVEAL.html` (ex.: `white.css`, `league.css`).  
- Para múltiplas apresentações, copie o HTML e o Markdown com outros nomes.

---

## 6. Exemplo de Estrutura Final

```
playdevs/
 ├── PITCH_SLIDES.md
 ├── PITCH_REVEAL.html
 ├── README_PITCH.md   ← este guia
```

---

✅ Pronto! Agora você tem um **pitch deck interativo** hospedado no Vercel, fácil de compartilhar com investidores e parceiros.
