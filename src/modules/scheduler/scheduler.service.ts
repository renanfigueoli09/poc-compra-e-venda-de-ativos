import { Injectable, Logger } from '@nestjs/common';
import { Cron, CronExpression } from '@nestjs/schedule';
import { TradingService } from '../trading/trading.service';
import { BinanceService } from '../binance/binance.service';

@Injectable()
export class SchedulerService {
  private readonly logger = new Logger(SchedulerService.name);

  constructor(
    private readonly tradingService: TradingService,
    private readonly binanceService: BinanceService,
  ) {}

  @Cron('0 */15 * * * *', {
    name: 'trading-strategy',
    timeZone: 'America/Sao_Paulo',
  })
  async handleTradingCron() {
    this.logger.log('Executando estratégia de trading a cada 15 minutos...');
    
    try {
      // Verificar conexão com a Binance
      const isConnected = await this.binanceService.ping();
      if (!isConnected) {
        this.logger.error('Falha na conexão com a Binance');
        return;
      }

      // Executar estratégia de trading
      const result = await this.tradingService.executeStrategy();
      
      this.logger.log(`Estratégia executada. Posição atual: ${result.currentPosition ? 'BTC' : 'USDT'}`);
      
    } catch (error) {
      this.logger.error('Erro durante execução do cron job:', error);
    }
  }

  // Método para executar manualmente (útil para testes)
  async executeManually() {
    this.logger.log('Execução manual da estratégia de trading...');
    return this.handleTradingCron();
  }

  // Cron job para verificar status da aplicação a cada hora
  @Cron(CronExpression.EVERY_HOUR, {
    name: 'health-check',
    timeZone: 'America/Sao_Paulo',
  })
  async handleHealthCheck() {
    this.logger.log('Verificação de saúde da aplicação...');
    
    try {
      const isConnected = await this.binanceService.ping();
      this.logger.log(`Status da conexão Binance: ${isConnected ? 'OK' : 'FALHA'}`);
    } catch (error) {
      this.logger.error('Erro na verificação de saúde:', error);
    }
  }
}

