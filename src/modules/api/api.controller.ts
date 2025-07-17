import { Controller, Get, Post, Logger } from '@nestjs/common';
import { SchedulerService } from '../scheduler/scheduler.service';
import { TradingService } from '../trading/trading.service';
import { BalanceService } from '../../utils/balance.service';
import { BinanceService } from '../binance/binance.service';

@Controller('api')
export class ApiController {
  private readonly logger = new Logger(ApiController.name);

  constructor(
    private readonly schedulerService: SchedulerService,
    private readonly tradingService: TradingService,
    private readonly balanceService: BalanceService,
    private readonly binanceService: BinanceService,
  ) {}

  @Get('status')
  async getStatus() {
    try {
        const isConnected = await this.binanceService.ping();
        console.log(isConnected)
      const timeOffset = this.binanceService.getTimeOffset();
      
      let balances = { usdt: 0, btc: 0 };
      let currentPosition = 'UNKNOWN';
      
      if (isConnected) {
        try {
          balances.usdt = await this.balanceService.getUsdtBalance();
          balances.btc = await this.balanceService.getBtcBalance();
          currentPosition = await this.balanceService.isUsdtBalanceGreater() ? 'USDT' : 'BTC';
        } catch (balanceError) {
          this.logger.warn('Erro ao obter saldos, mas conexão está OK:', balanceError.message);
        }
      }

      return {
        status: isConnected ? 'OK' : 'CONNECTION_ERROR',
        binanceConnection: isConnected,
        timeOffset: timeOffset,
        balances,
        currentPosition,
        timestamp: new Date().toISOString(),
      };
    } catch (error) {
      this.logger.error('Erro ao obter status:', error);
      return {
        status: 'ERROR',
        error: error.message,
        timestamp: new Date().toISOString(),
      };
    }
  }

  @Post('sync-time')
  async syncTime() {
    try {
      this.logger.log('Sincronização de tempo solicitada via API');
      await this.binanceService.forceSynchronizeTime();
      const timeOffset = this.binanceService.getTimeOffset();
      
      return {
        status: 'SUCCESS',
        message: 'Tempo sincronizado com sucesso',
        timeOffset: timeOffset,
        timestamp: new Date().toISOString(),
      };
    } catch (error) {
      this.logger.error('Erro ao sincronizar tempo via API:', error);
      return {
        status: 'ERROR',
        error: error.message,
        timestamp: new Date().toISOString(),
      };
    }
  }

  @Post('execute-strategy')
  async executeStrategy() {
    try {
      this.logger.log('Execução manual da estratégia solicitada via API');
      const result = await this.schedulerService.executeManually();
      
      return {
        status: 'SUCCESS',
        message: 'Estratégia executada com sucesso',
        timestamp: new Date().toISOString(),
      };
    } catch (error) {
      this.logger.error('Erro ao executar estratégia via API:', error);
      return {
        status: 'ERROR',
        error: error.message,
        timestamp: new Date().toISOString(),
      };
    }
  }

  @Get('trading-data')
  async getTradingData() {
    try {
      const data = await this.tradingService.getTradingData();
      
      return {
        status: 'SUCCESS',
        data: {
          pricesCount: data.prices.length,
          latestPrice: data.prices[data.prices.length - 1],
          latestTimestamp: data.timestamps[data.timestamps.length - 1],
        },
        timestamp: new Date().toISOString(),
      };
    } catch (error) {
      this.logger.error('Erro ao obter dados de trading:', error);
      return {
        status: 'ERROR',
        error: error.message,
        timestamp: new Date().toISOString(),
      };
    }
  }

  @Get('balances')
  async getBalances() {
    try {
      const usdtBalance = await this.balanceService.getUsdtBalance();
      const btcBalance = await this.balanceService.getBtcBalance();
      const btcPrice = await this.binanceService.getPrice('BTCUSDT');
      const totalValueInUsdt = usdtBalance + (btcBalance * btcPrice);

      return {
        status: 'SUCCESS',
        balances: {
          usdt: usdtBalance,
          btc: btcBalance,
          btcPrice: btcPrice,
          totalValueInUsdt: totalValueInUsdt,
        },
        timestamp: new Date().toISOString(),
      };
    } catch (error) {
      this.logger.error('Erro ao obter saldos:', error);
      return {
        status: 'ERROR',
        error: error.message,
        timestamp: new Date().toISOString(),
      };
    }
  }
}
