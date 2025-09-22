# 🔐 **CREDENCIAIS DE ACESSO LOCAL**

## ✅ **USUÁRIOS DISPONÍVEIS**

### **1. Usuário Admin (Recomendado)**
- **Email**: `admin@admin.com`
- **Senha**: `admin123`
- **Nome**: Admin
- **Status**: ✅ Ativo

### **2. Usuário Teste Local**
- **Email**: `teste@local.com`
- **Senha**: `123456`
- **Nome**: Teste Local
- **Status**: ✅ Ativo

### **3. Usuário Teste Original**
- **Email**: `teste@concursoai.com`
- **Senha**: `123456`
- **Nome**: Usuário Teste
- **Status**: ✅ Ativo

## 🚀 **COMO ACESSAR**

### **Via Frontend (Recomendado)**
1. Acesse: http://localhost:3000
2. Clique em "Entrar"
3. Use as credenciais:
   - **Email**: `admin@admin.com`
   - **Senha**: `admin123`

### **Via API (Para testes)**
```bash
# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@admin.com&password=admin123"

# Resposta esperada:
# {"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...","token_type":"bearer"}
```

## 🧪 **TESTE RÁPIDO**

### **1. Verificar se o sistema está rodando**
```bash
# Backend
curl http://localhost:8000/health
# ✅ {"status":"healthy"}

# Frontend
curl http://localhost:3000
# ✅ Página inicial carregando
```

### **2. Fazer login**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@admin.com&password=admin123"
```

### **3. Testar dashboard**
```bash
# Usar o token retornado no login
curl -X GET http://localhost:8000/dashboard/stats \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

## 📊 **FUNCIONALIDADES DISPONÍVEIS**

Após o login, você terá acesso a:

- ✅ **Dashboard** - Estatísticas e resumo
- ✅ **Gerador de Simulados** - Criar novos simulados
- ✅ **Execução de Simulados** - Fazer simulados
- ✅ **Resultados** - Ver performance e análises
- ✅ **Perfil** - Gerenciar conta

## 🔧 **COMANDOS ÚTEIS**

### **Iniciar o sistema**
```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
python run.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### **Resetar senha (se necessário)**
```bash
cd backend
source venv/bin/activate
python -c "
from app.database import SessionLocal
from app.models import User
from app.auth import get_password_hash

db = SessionLocal()
user = db.query(User).filter(User.email == 'admin@admin.com').first()
if user:
    user.hashed_password = get_password_hash('admin123')
    db.commit()
    print('Senha resetada para: admin123')
db.close()
"
```

## 🎯 **PRÓXIMOS PASSOS**

1. **Acesse o sistema**: http://localhost:3000
2. **Faça login**: admin@admin.com / admin123
3. **Explore as funcionalidades**:
   - Crie um simulado
   - Execute o simulado
   - Veja os resultados
   - Explore o dashboard

---

**Credenciais**: ✅ **PRONTAS PARA USO**  
**Sistema**: 🚀 **FUNCIONANDO LOCALMENTE**  
**Data**: 20/09/2025  
**Hora**: 20:19
