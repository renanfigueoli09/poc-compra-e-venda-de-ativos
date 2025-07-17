# Trading App - NestJS

Aplicação de trading automatizado refatorada para NestJS com melhorias significativas no sistema de compra e venda de ativos.

## 🚀 Principais Melhorias

### 1. **Arquitetura NestJS**
- Estrutura modular e escalável
- Injeção de dependências
- Decorators para organização do código
- Sistema de logging integrado

### 2. **Sistema de Cron Jobs**
- Execução automática a cada 15 minutos
- Timezone configurável (America/Sao_Paulo)
- Health checks automáticos
- Execução manual via API

### 3. **Melhorias no Arredondamento**
- **Problema resolvido**: Erros de saldo insuficiente
- **Solução**: Arredondamento sempre para baixo (Math.floor)
- **Margem de segurança**: 0.1% aplicada em todas as operações
- **Ajuste automático**: Respeita step_size da Binance
- **Validação**: Verifica limites mínimos e máximos

### 4. **Funcionalidades Adicionais**
- API REST para monitoramento
- Verificação de status em tempo real
- Logs detalhados de todas as operações
- Tratamento robusto de erros

## 📁 Estrutura do Projeto

```
src/
├── api/                 # Controladores da API REST
├── binance/            # Serviços da Binance API
├── config/             # Configurações da aplicação
├── scheduler/          # Sistema de cron jobs
├── trading/            # Lógica de trading
├── utils/              # Utilitários (balanço, matemática)
├── app.module.ts       # Módulo principal
└── main.ts            # Ponto de entrada
```

## 🛠️ Instalação

1. **Clone o projeto**
```bash
git clone <repository-url>
cd trading-app
```

2. **Instale as dependências**
```bash
npm install
```

3. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
# Edite o arquivo .env com suas credenciais da Binance
```

4. **Execute a aplicação**
```bash
# Desenvolvimento
npm run start:dev

# Produção
npm run build
npm run start:prod
```

## 🔧 Configuração

### Variáveis de Ambiente

```env
API_KEY=sua_chave_api_binance
API_SECRET=seu_secret_binance
PORT=3000
NODE_ENV=development
TZ=America/Sao_Paulo
```

### Parâmetros de Trading

- **Símbolo**: BTCUSDT
- **Intervalo**: 15 minutos
- **Média Rápida**: 7 períodos
- **Média Lenta**: 40 períodos
- **Execução**: A cada 15 minutos (cron: `0 */15 * * * *`)

## 📊 API Endpoints

### GET /api/status
Retorna o status geral da aplicação
```json
{
  "status": "OK",
  "binanceConnection": true,
  "balances": {
    "usdt": 100.50,
    "btc": 0.001234
  },
  "currentPosition": "USDT",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

### POST /api/execute-strategy
Executa a estratégia manualmente
```json
{
  "status": "SUCCESS",
  "message": "Estratégia executada com sucesso",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

### GET /api/balances
Retorna informações detalhadas dos saldos
```json
{
  "status": "SUCCESS",
  "balances": {
    "usdt": 100.50,
    "btc": 0.001234,
    "btcPrice": 45000.00,
    "totalValueInUsdt": 155.03
  },
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

### GET /api/trading-data
Retorna dados de mercado atuais
```json
{
  "status": "SUCCESS",
  "data": {
    "pricesCount": 1000,
    "latestPrice": 45000.00,
    "latestTimestamp": "2024-01-01T12:00:00.000Z"
  },
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

## 🔒 Melhorias de Segurança no Arredondamento

### Problema Original
A aplicação original tinha problemas com:
- Erros de "insufficient balance" 
- Arredondamentos que excediam o saldo disponível
- Falta de validação de limites da Binance

### Soluções Implementadas

#### 1. **Arredondamento Seguro**
```typescript
// Sempre arredonda para baixo
const adjustedQuantity = Math.floor(quantity * factor) / factor;
```

#### 2. **Margem de Segurança**
```typescript
// Aplica 0.1% de margem de segurança
const safeBalance = usdtBalance * 0.999;
```

#### 3. **Ajuste ao Step Size**
```typescript
// Respeita o step_size da Binance
const steps = Math.floor(quantity / stepSize);
return steps * stepSize;
```

#### 4. **Validação de Limites**
```typescript
// Verifica limites mínimos e máximos
return quantity >= minQty && quantity <= maxQty;
```

## 📈 Estratégia de Trading

### Lógica
- **Compra**: Quando média rápida (7) > média lenta (40) e posição atual é USDT
- **Venda**: Quando média rápida (7) < média lenta (40) e posição atual é BTC

### Execução
- **Automática**: A cada 15 minutos via cron job
- **Manual**: Via endpoint POST /api/execute-strategy
- **Logs**: Todas as operações são logadas com detalhes

## 🚨 Monitoramento

### Logs
A aplicação gera logs detalhados para:
- Execução de estratégias
- Ordens de compra/venda
- Erros e exceções
- Health checks
- Conexão com Binance

### Health Checks
- Verificação de conexão com Binance a cada hora
- Status disponível via API
- Logs automáticos de saúde da aplicação

## 🔄 Deployment

### Docker (Recomendado)
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY dist ./dist
EXPOSE 3000
CMD ["node", "dist/main"]
```

### PM2
```bash
npm install -g pm2
npm run build
pm2 start dist/main.js --name trading-app
```

## ⚠️ Avisos Importantes

1. **Teste em ambiente de desenvolvimento** antes de usar em produção
2. **Configure stop-loss** e outras medidas de segurança
3. **Monitore constantemente** as operações
4. **Mantenha backups** das configurações
5. **Use apenas fundos que pode perder**

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

