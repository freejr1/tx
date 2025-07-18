# Bot Free Fire UP System

Sistema completo de automação para Free Fire com bot Telegram e API Flask.

## 🎮 Funcionalidades

### Bot Telegram
- **Comando /add**: Adiciona contas Free Fire via token ou URL Garena
- **Automação**: Mantém contas online e ganha XP automaticamente
- **Segurança**: Detecta e desconecta outros sistemas usando o mesmo token
- **Monitoramento**: Acompanha status, nível e XP das contas

### API Flask
- **CRUD de Contas**: Gerenciamento completo de contas Free Fire
- **Sistema de Automação**: Controle de automação por conta
- **Segurança**: Verificação de conflitos e logs de segurança
- **Criptografia**: Tokens armazenados de forma segura

## 🚀 Como Usar

### 1. Configuração do Ambiente

```bash
# Instalar dependências
cd telegram_freefire_api
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Iniciar a API

```bash
# Iniciar API Flask
python src/main.py
```

A API estará disponível em `http://localhost:5001`

### 3. Iniciar o Bot Telegram

```bash
# Iniciar bot Telegram
python telegram_bot.py
```

### 4. Usar o Bot

1. Abra o Telegram e procure pelo seu bot
2. Use `/start` para ver os comandos disponíveis
3. Use `/add <token_ou_url>` para adicionar uma conta

**Exemplos de uso:**

```
# URL completa do Garena
/add https://reward.ff.garena.com/pt?access_token=306BF4EE4DBB9327CF90E9FAE1E37E6ADCA45761386CB82F2A871CFDA08B974F69D42638C8D05A4981D9716BB2AF9A2859CEBF2B1E38DC29AB9DAAB474DF790CFC6DB77FD0BCA8B5B9E1C205EC32BD22

# Apenas o token
/add 306BF4EE4DBB9327CF90E9FAE1E37E6ADCA45761386CB82F2A871CFDA08B974F69D42638C8D05A4981D9716BB2AF9A2859CEBF2B1E38DC29AB9DAAB474DF790CFC6DB77FD0BCA8B5B9E1C205EC32BD22
```

## 📋 Comandos do Bot

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `/start` | Mensagem de boas-vindas e instruções | `/start` |
| `/add <token>` | Adicionar conta Free Fire | `/add https://reward.ff.garena.com/...` |
| `/list` | Listar todas as suas contas | `/list` |
| `/status` | Ver resumo das contas | `/status` |
| `/start_auto <id>` | Iniciar automação para conta | `/start_auto 1` |
| `/stop_auto <id>` | Parar automação para conta | `/stop_auto 1` |
| `/security <id>` | Verificar segurança da conta | `/security 1` |

## 🔧 API Endpoints

### Contas
- `POST /api/accounts` - Adicionar conta
- `GET /api/accounts/{user_id}` - Listar contas do usuário
- `GET /api/accounts/{user_id}/summary` - Resumo das contas
- `DELETE /api/accounts/{account_id}` - Remover conta

### Automação
- `POST /api/accounts/{account_id}/start-automation` - Iniciar automação
- `POST /api/accounts/{account_id}/stop-automation` - Parar automação
- `GET /api/accounts/{account_id}/status` - Status da automação

### Segurança
- `POST /api/accounts/{account_id}/security-check` - Verificar segurança
- `POST /api/accounts/{account_id}/force-disconnect` - Forçar desconexão
- `GET /api/accounts/{account_id}/security-logs` - Logs de segurança

### Sistema
- `GET /api/health` - Status da API
- `GET /api/security/monitor` - Monitor de segurança

## 🔒 Segurança

### Proteção de Tokens
- Tokens são criptografados antes do armazenamento
- Chave de criptografia configurável via variável de ambiente
- Validação rigorosa de formato de tokens

### Detecção de Conflitos
- Sistema detecta uso do mesmo token em outros sistemas
- Desconexão automática de sessões conflitantes
- Logs detalhados de eventos de segurança

### Limitações
- Máximo de 5 contas por usuário
- Rate limiting básico implementado
- Validação de origem das requisições

## 📊 Monitoramento

### Logs de Segurança
O sistema mantém logs detalhados de:
- Tentativas de uso de tokens em outros sistemas
- Desconexões forçadas
- Verificações de segurança
- Eventos de automação

### Métricas
- Total de contas ativas
- Contas online em tempo real
- XP ganho por dia
- Eventos de segurança

## 🛠️ Estrutura do Projeto

```
telegram_freefire_api/
├── src/
│   ├── models/
│   │   ├── user.py          # Modelo de usuário base
│   │   └── account.py       # Modelo de contas Free Fire
│   ├── routes/
│   │   ├── user.py          # Rotas de usuário
│   │   └── account.py       # Rotas de contas e automação
│   ├── static/              # Arquivos estáticos
│   ├── database/
│   │   └── app.db          # Banco SQLite
│   └── main.py             # Aplicação Flask principal
├── telegram_bot.py         # Bot Telegram
├── test_bot_api.py         # Testes automatizados
├── requirements.txt        # Dependências Python
└── README.md              # Esta documentação
```

## 🧪 Testes

Execute os testes automatizados:

```bash
python test_bot_api.py
```

Os testes verificam:
- Conexão com a API
- Adição de contas
- Início de automação
- Verificação de segurança
- Resumo de usuário

## ⚙️ Configuração

### Variáveis de Ambiente

```bash
# Token do bot Telegram (já configurado no código)
BOT_TOKEN=7862652022:AAG22CFcGrGavgTnMKbWjkq_qAqzVHVKjPo

# Chave de criptografia (opcional, gerada automaticamente)
ENCRYPTION_KEY=sua_chave_aqui
```

### Configurações da API

- **Porta**: 5001 (configurável em `src/main.py`)
- **Host**: 0.0.0.0 (permite acesso externo)
- **Debug**: Ativado (desativar em produção)
- **CORS**: Habilitado para todas as origens

## 🚀 Deploy

### Desenvolvimento
O sistema está configurado para desenvolvimento local. Para produção:

1. Desativar modo debug
2. Configurar servidor WSGI (Gunicorn)
3. Usar banco de dados PostgreSQL
4. Configurar HTTPS
5. Implementar rate limiting avançado

### Docker (Opcional)
```dockerfile
# Exemplo de Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5001
CMD ["python", "src/main.py"]
```

## 📝 Logs

### API Flask
- Logs de requisições HTTP
- Erros de aplicação
- Eventos de banco de dados

### Bot Telegram
- Comandos recebidos
- Respostas enviadas
- Erros de comunicação

## 🔄 Automação

### Tipos de Automação
- **stay_online**: Apenas manter online
- **xp_farming**: Apenas ganhar XP
- **both**: Manter online + ganhar XP (padrão)

### Estratégias de XP
- Login diário automático
- Simulação de atividades básicas
- Rotação inteligente de tarefas
- Monitoramento de progresso

## 🆘 Solução de Problemas

### API não responde
1. Verificar se a porta 5001 está livre
2. Verificar logs de erro no terminal
3. Testar endpoint de health: `curl http://localhost:5001/api/health`

### Bot não responde
1. Verificar token do bot Telegram
2. Verificar conexão com a API
3. Verificar logs do bot

### Erro de banco de dados
1. Verificar permissões do arquivo `src/database/app.db`
2. Recriar banco: deletar arquivo e reiniciar API
3. Verificar espaço em disco

## 📞 Suporte

Para problemas ou dúvidas:
1. Verificar logs de erro
2. Executar testes automatizados
3. Consultar esta documentação
4. Verificar configurações de rede

## 🔮 Próximas Funcionalidades

- [ ] Interface web para gerenciamento
- [ ] Suporte a múltiplos jogos
- [ ] Estatísticas avançadas
- [ ] Notificações push
- [ ] Backup automático de dados
- [ ] API de webhooks
- [ ] Integração com Discord

