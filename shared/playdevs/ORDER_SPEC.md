# ORDER.yml — Especificação

Cada `ORDER.yml` deve conter uma lista `steps`, onde cada passo define:

```yaml
steps:
  - role: <string>            # Ex.: "Arquiteta", "Backend", "Data/ML", "QA", "Docs", "Review"
    input: <string|[string]>  # Arquivos lidos pela instância
    prompt: <string>          # Caminho para o prompt desta etapa
    output: <string>          # Caminho do arquivo/zip gerado
    notes: <string>           # (opcional) dicas para a IA
    postconditions:           # (opcional) validações esperadas
      - file_exists: "<path>"
      - contains: { file: "<path>", must_include: ["texto A", "texto B"] }
```

- **role**: papel que executa a etapa.  
- **input**: arquivo(s) que a IA deve ler antes de produzir a saída.  
- **prompt**: prompt que deve ser usado pela IA.  
- **output**: artefato esperado após a execução.  
- **postconditions** (opcional): checks que a própria IA deve validar e relatar no final de sua resposta.
