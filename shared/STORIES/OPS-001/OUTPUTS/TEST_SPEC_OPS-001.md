# TEST_SPEC_OPS-001: Deploy Mínimo (Vercel/Cloud Run) - Especificações de Teste

## 1. Casos de Teste - Deploy Frontend (Vercel)

### **1.1 Deploy Automático via Git**

#### **Caso Feliz: Deploy Sucesso**
- **Objetivo**: Verificar deploy automático bem-sucedido
- **Pré-condições**: 
  - Repositório Git configurado
  - Vercel conectado ao repositório
  - Branch main com código válido
- **Passos**:
  1. Fazer push para branch main
  2. Verificar trigger do build no Vercel
  3. Aguardar conclusão do build
  4. Verificar deploy em produção
- **Resultado Esperado**:
  - Build iniciado automaticamente
  - Build concluído com sucesso
  - Deploy realizado em < 5 minutos
  - Site acessível em produção
- **Critérios de Aceitação**:
  - ✅ Build time < 5 minutos
  - ✅ Deploy success rate = 100%
  - ✅ Site acessível via HTTPS
  - ✅ Todas as rotas funcionando

#### **Caso de Erro: Build Failure**
- **Objetivo**: Verificar tratamento de falha de build
- **Pré-condições**: Código com erro de sintaxe
- **Passos**:
  1. Fazer push com código inválido
  2. Verificar falha do build
  3. Verificar notificação de erro
- **Resultado Esperado**:
  - Build falha com erro claro
  - Deploy anterior mantido
  - Notificação enviada
- **Critérios de Aceitação**:
  - ✅ Build falha rapidamente
  - ✅ Deploy anterior não afetado
  - ✅ Erro reportado claramente

### **1.2 Deploy Manual**

#### **Caso Feliz: Deploy Manual Sucesso**
- **Objetivo**: Verificar deploy manual via dashboard
- **Pré-condições**: Build disponível no Vercel
- **Passos**:
  1. Acessar dashboard Vercel
  2. Selecionar build para deploy
  3. Executar deploy manual
  4. Verificar conclusão
- **Resultado Esperado**:
  - Deploy executado com sucesso
  - Site atualizado
  - Logs disponíveis
- **Critérios de Aceitação**:
  - ✅ Deploy manual funcional
  - ✅ Site atualizado corretamente
  - ✅ Logs de deploy disponíveis

### **1.3 Preview Deployments**

#### **Caso Feliz: Preview de Feature Branch**
- **Objetivo**: Verificar preview de branch de feature
- **Pré-condições**: Feature branch com código
- **Passos**:
  1. Fazer push para feature branch
  2. Verificar criação de preview
  3. Acessar URL de preview
  4. Testar funcionalidades
- **Resultado Esperado**:
  - Preview criado automaticamente
  - URL única gerada
  - Funcionalidades testáveis
- **Critérios de Aceitação**:
  - ✅ Preview criado em < 3 minutos
  - ✅ URL única e acessível
  - ✅ Funcionalidades funcionando

## 2. Casos de Teste - Deploy Backend (Google Cloud Run)

### **2.1 Deploy via Cloud Build**

#### **Caso Feliz: Deploy Backend Sucesso**
- **Objetivo**: Verificar deploy do backend via Cloud Build
- **Pré-condições**:
  - Dockerfile configurado
  - Cloud Build trigger configurado
  - Secrets configurados
- **Passos**:
  1. Fazer push para repositório
  2. Verificar trigger do Cloud Build
  3. Aguardar build da imagem
  4. Verificar deploy no Cloud Run
  5. Testar endpoints da API
- **Resultado Esperado**:
  - Imagem Docker construída
  - Deploy no Cloud Run realizado
  - API acessível e funcional
- **Critérios de Aceitação**:
  - ✅ Build time < 10 minutos
  - ✅ Deploy success rate = 100%
  - ✅ API acessível via HTTPS
  - ✅ Health check passando

#### **Caso de Erro: Falha de Build**
- **Objetivo**: Verificar tratamento de falha de build
- **Pré-condições**: Dockerfile com erro
- **Passos**:
  1. Fazer push com Dockerfile inválido
  2. Verificar falha do build
  3. Verificar notificação
- **Resultado Esperado**:
  - Build falha com erro claro
  - Deploy anterior mantido
  - Notificação enviada
- **Critérios de Aceitação**:
  - ✅ Build falha rapidamente
  - ✅ Deploy anterior não afetado
  - ✅ Erro reportado claramente

### **2.2 Auto-scaling**

#### **Caso Feliz: Escalamento Automático**
- **Objetivo**: Verificar escalamento automático
- **Pré-condições**: Cloud Run configurado com auto-scaling
- **Passos**:
  1. Gerar carga na API
  2. Verificar criação de novas instâncias
  3. Reduzir carga
  4. Verificar redução de instâncias
- **Resultado Esperado**:
  - Novas instâncias criadas sob carga
  - Instâncias removidas sem carga
  - Performance mantida
- **Critérios de Aceitação**:
  - ✅ Escalamento em < 30 segundos
  - ✅ Performance mantida
  - ✅ Custos otimizados

### **2.3 Health Checks**

#### **Caso Feliz: Health Check Passando**
- **Objetivo**: Verificar health checks funcionando
- **Pré-condições**: Endpoint /health implementado
- **Passos**:
  1. Acessar endpoint /health
  2. Verificar resposta 200
  3. Verificar conteúdo da resposta
- **Resultado Esperado**:
  - Resposta 200 OK
  - JSON com status e timestamp
  - Tempo de resposta < 1 segundo
- **Critérios de Aceitação**:
  - ✅ Health check respondendo
  - ✅ Resposta em < 1 segundo
  - ✅ Formato JSON válido

#### **Caso de Erro: Health Check Falhando**
- **Objetivo**: Verificar tratamento de health check falhando
- **Pré-condições**: Aplicação com problema
- **Passos**:
  1. Simular problema na aplicação
  2. Verificar health check falhando
  3. Verificar ação do Cloud Run
- **Resultado Esperado**:
  - Health check retorna erro
  - Instância marcada como não saudável
  - Nova instância criada
- **Critérios de Aceitação**:
  - ✅ Health check falha corretamente
  - ✅ Instância substituída
  - ✅ Serviço mantido disponível

## 3. Casos de Teste - Integração Frontend/Backend

### **3.1 Comunicação entre Serviços**

#### **Caso Feliz: API Calls Funcionando**
- **Objetivo**: Verificar comunicação frontend-backend
- **Pré-condições**: Ambos serviços deployados
- **Passos**:
  1. Acessar frontend
  2. Executar ação que chama API
  3. Verificar resposta da API
  4. Verificar exibição no frontend
- **Resultado Esperado**:
  - API chamada com sucesso
  - Dados retornados corretamente
  - Frontend exibe dados
- **Critérios de Aceitação**:
  - ✅ CORS configurado corretamente
  - ✅ API respondendo
  - ✅ Dados exibidos corretamente

#### **Caso de Erro: API Indisponível**
- **Objetivo**: Verificar tratamento de API indisponível
- **Pré-condições**: Backend com problema
- **Passos**:
  1. Simular falha no backend
  2. Executar ação no frontend
  3. Verificar tratamento de erro
- **Resultado Esperado**:
  - Erro tratado graciosamente
  - Mensagem de erro exibida
  - Funcionalidade degradada
- **Critérios de Aceitação**:
  - ✅ Erro tratado graciosamente
  - ✅ Usuário informado
  - ✅ Sistema não quebra

### **3.2 Domínios e SSL**

#### **Caso Feliz: Acesso via Domínio Customizado**
- **Objetivo**: Verificar acesso via domínio customizado
- **Pré-condições**: Domínio configurado
- **Passos**:
  1. Acessar via domínio customizado
  2. Verificar redirecionamento HTTPS
  3. Verificar certificado SSL
- **Resultado Esperado**:
  - Site acessível via domínio
  - HTTPS funcionando
  - Certificado válido
- **Critérios de Aceitação**:
  - ✅ Domínio funcionando
  - ✅ HTTPS obrigatório
  - ✅ Certificado válido

## 4. Casos de Teste - Monitoramento

### **4.1 Logs**

#### **Caso Feliz: Coleta de Logs**
- **Objetivo**: Verificar coleta de logs
- **Pré-condições**: Sistema de logs configurado
- **Passos**:
  1. Executar ações no sistema
  2. Verificar logs no dashboard
  3. Verificar estrutura dos logs
- **Resultado Esperado**:
  - Logs coletados automaticamente
  - Logs estruturados
  - Logs pesquisáveis
- **Critérios de Aceitação**:
  - ✅ Logs coletados em tempo real
  - ✅ Formato JSON estruturado
  - ✅ Logs pesquisáveis

#### **Caso de Erro: Falha na Coleta de Logs**
- **Objetivo**: Verificar tratamento de falha de logs
- **Pré-condições**: Sistema de logs com problema
- **Passos**:
  1. Simular falha no sistema de logs
  2. Executar ações no sistema
  3. Verificar tratamento de falha
- **Resultado Esperado**:
  - Falha tratada graciosamente
  - Sistema continua funcionando
  - Logs recuperados quando possível
- **Critérios de Aceitação**:
  - ✅ Sistema não quebra
  - ✅ Logs recuperados
  - ✅ Notificação de falha

### **4.2 Métricas**

#### **Caso Feliz: Coleta de Métricas**
- **Objetivo**: Verificar coleta de métricas
- **Pré-condições**: Sistema de métricas configurado
- **Passos**:
  1. Gerar tráfego no sistema
  2. Verificar métricas no dashboard
  3. Verificar alertas configurados
- **Resultado Esperado**:
  - Métricas coletadas automaticamente
  - Dashboard atualizado
  - Alertas funcionando
- **Critérios de Aceitação**:
  - ✅ Métricas em tempo real
  - ✅ Dashboard funcional
  - ✅ Alertas configurados

### **4.3 Alertas**

#### **Caso Feliz: Alerta de Performance**
- **Objetivo**: Verificar alertas de performance
- **Pré-condições**: Alertas configurados
- **Passos**:
  1. Simular degradação de performance
  2. Verificar trigger do alerta
  3. Verificar notificação
- **Resultado Esperado**:
  - Alerta disparado
  - Notificação enviada
  - Dashboard atualizado
- **Critérios de Aceitação**:
  - ✅ Alerta disparado corretamente
  - ✅ Notificação enviada
  - ✅ Threshold configurado

#### **Caso de Erro: Alerta Falso Positivo**
- **Objetivo**: Verificar tratamento de falso positivo
- **Pré-condições**: Alerta configurado
- **Passos**:
  1. Simular falso positivo
  2. Verificar alerta disparado
  3. Verificar supressão de alerta
- **Resultado Esperado**:
  - Alerta disparado
  - Falso positivo identificado
  - Alerta suprimido
- **Critérios de Aceitação**:
  - ✅ Falso positivo identificado
  - ✅ Alerta suprimido
  - ✅ Threshold ajustado

## 5. Casos de Teste - Rollback

### **5.1 Rollback Automático**

#### **Caso Feliz: Rollback por Health Check**
- **Objetivo**: Verificar rollback automático
- **Pré-condições**: Health check configurado
- **Passos**:
  1. Deploy com problema
  2. Verificar health check falhando
  3. Verificar rollback automático
- **Resultado Esperado**:
  - Health check falha
  - Rollback executado
  - Versão anterior restaurada
- **Critérios de Aceitação**:
  - ✅ Rollback em < 2 minutos
  - ✅ Versão anterior funcionando
  - ✅ Usuários não impactados

#### **Caso de Erro: Rollback Falhando**
- **Objetivo**: Verificar tratamento de falha de rollback
- **Pré-condições**: Sistema de rollback com problema
- **Passos**:
  1. Simular falha no rollback
  2. Verificar tratamento de erro
  3. Verificar ação manual
- **Resultado Esperado**:
  - Falha de rollback identificada
  - Ação manual necessária
  - Sistema em estado conhecido
- **Critérios de Aceitação**:
  - ✅ Falha identificada
  - ✅ Ação manual clara
  - ✅ Estado documentado

### **5.2 Rollback Manual**

#### **Caso Feliz: Rollback Manual Sucesso**
- **Objetivo**: Verificar rollback manual
- **Pré-condições**: Versão anterior disponível
- **Passos**:
  1. Identificar problema
  2. Executar rollback manual
  3. Verificar restauração
- **Resultado Esperado**:
  - Rollback executado
  - Versão anterior restaurada
  - Sistema funcionando
- **Critérios de Aceitação**:
  - ✅ Rollback executado
  - ✅ Versão anterior funcionando
  - ✅ Tempo de rollback < 5 minutos

## 6. Estratégias de Mock

### **6.1 Mock de Serviços Externos**

#### **Vercel API Mock**
```javascript
// Mock para testes de deploy Vercel
const mockVercelAPI = {
  deploy: jest.fn().mockResolvedValue({
    id: 'deploy_123',
    status: 'ready',
    url: 'https://app-123.vercel.app'
  }),
  getDeployment: jest.fn().mockResolvedValue({
    id: 'deploy_123',
    status: 'ready',
    url: 'https://app-123.vercel.app'
  })
};
```

#### **Google Cloud Run API Mock**
```javascript
// Mock para testes de deploy Cloud Run
const mockCloudRunAPI = {
  createService: jest.fn().mockResolvedValue({
    name: 'concurso-ai-backend',
    status: 'READY',
    url: 'https://concurso-ai-backend-123.run.app'
  }),
  getService: jest.fn().mockResolvedValue({
    name: 'concurso-ai-backend',
    status: 'READY',
    url: 'https://concurso-ai-backend-123.run.app'
  })
};
```

#### **GitHub API Mock**
```javascript
// Mock para testes de webhook GitHub
const mockGitHubAPI = {
  createWebhook: jest.fn().mockResolvedValue({
    id: 123456,
    url: 'https://api.github.com/repos/owner/repo/hooks/123456'
  }),
  triggerWebhook: jest.fn().mockResolvedValue({
    status: 'success',
    message: 'Webhook triggered successfully'
  })
};
```

### **6.2 Mock de Monitoramento**

#### **Logs Service Mock**
```javascript
// Mock para testes de logs
const mockLogsService = {
  collectLogs: jest.fn().mockResolvedValue({
    logs: [
      {
        timestamp: '2024-01-01T00:00:00Z',
        level: 'info',
        message: 'Deploy started',
        service: 'frontend'
      }
    ]
  }),
  searchLogs: jest.fn().mockResolvedValue({
    logs: [],
    total: 0
  })
};
```

#### **Metrics Service Mock**
```javascript
// Mock para testes de métricas
const mockMetricsService = {
  collectMetrics: jest.fn().mockResolvedValue({
    metrics: {
      responseTime: 150,
      errorRate: 0.01,
      throughput: 1000
    }
  }),
  getMetrics: jest.fn().mockResolvedValue({
    metrics: {
      responseTime: 150,
      errorRate: 0.01,
      throughput: 1000
    }
  })
};
```

## 7. Timeouts e Re-tentativas

### **7.1 Timeouts**

#### **Deploy Timeouts**
- **Frontend Deploy**: 10 minutos
- **Backend Deploy**: 15 minutos
- **Health Check**: 30 segundos
- **API Call**: 5 segundos
- **Log Collection**: 1 minuto

#### **Test Timeouts**
- **Unit Tests**: 30 segundos
- **Integration Tests**: 5 minutos
- **E2E Tests**: 10 minutos
- **Performance Tests**: 15 minutos

### **7.2 Re-tentativas**

#### **Deploy Re-tentativas**
- **Build Failure**: 3 tentativas
- **Deploy Failure**: 2 tentativas
- **Health Check**: 5 tentativas
- **API Call**: 3 tentativas

#### **Test Re-tentativas**
- **Flaky Tests**: 3 tentativas
- **Network Tests**: 2 tentativas
- **Performance Tests**: 1 tentativa

## 8. Critérios de Cobertura

### **8.1 Cobertura de Código**
- **Deploy Scripts**: 90%
- **Health Checks**: 95%
- **Error Handling**: 95%
- **Monitoring**: 85%

### **8.2 Cobertura de Testes**
- **Unit Tests**: 90%
- **Integration Tests**: 80%
- **E2E Tests**: 70%
- **Performance Tests**: 60%

### **8.3 Cobertura de Cenários**
- **Happy Path**: 100%
- **Error Cases**: 90%
- **Edge Cases**: 80%
- **Failure Scenarios**: 85%

## 9. Plano de Testes

### **9.1 Testes Unitários**
- **Deploy Scripts**: Testes de cada função
- **Health Checks**: Testes de endpoints
- **Error Handling**: Testes de tratamento de erro
- **Monitoring**: Testes de coleta de dados

### **9.2 Testes de Integração**
- **Frontend-Backend**: Comunicação entre serviços
- **Deploy Pipeline**: Fluxo completo de deploy
- **Monitoring**: Integração com serviços externos
- **Rollback**: Processo de rollback

### **9.3 Testes E2E**
- **User Journey**: Fluxo completo do usuário
- **Deploy Process**: Deploy end-to-end
- **Monitoring**: Monitoramento end-to-end
- **Rollback**: Rollback end-to-end

### **9.4 Testes de Performance**
- **Deploy Speed**: Tempo de deploy
- **API Performance**: Tempo de resposta
- **Monitoring**: Latência de coleta
- **Rollback**: Tempo de rollback

### **9.5 Testes de Segurança**
- **Secrets**: Gerenciamento de secrets
- **SSL/TLS**: Certificados e criptografia
- **Access Control**: Controle de acesso
- **Audit**: Logs de auditoria

### **9.6 Testes de Acessibilidade**
- **Frontend**: Acessibilidade do frontend
- **Dashboard**: Acessibilidade do dashboard
- **Documentation**: Acessibilidade da documentação
- **Error Messages**: Acessibilidade de mensagens

### **9.7 Testes Exploratórios**
- **Deploy Process**: Exploração do processo
- **Monitoring**: Exploração do monitoramento
- **Error Handling**: Exploração de erros
- **User Experience**: Exploração da UX

---

**Este documento define as especificações de teste para o sistema de deploy mínimo, incluindo casos de teste, estratégias de mock, timeouts, re-tentativas e critérios de cobertura.**
