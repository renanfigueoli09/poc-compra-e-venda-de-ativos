import { Injectable, Logger } from '@nestjs/common';
import { BinanceService } from '../modules/binance/binance.service';

@Injectable()
export class BalanceService {
  private readonly logger = new Logger(BalanceService.name);

  constructor(private readonly binanceService: BinanceService) {}

  async getUsdtBalance(): Promise<number> {
    try {
      const account = await this.binanceService.getAccountInfo();
      const usdtBalance = account.balances.find(balance => balance.asset === 'USDT');
      return parseFloat(usdtBalance?.free || '0');
    } catch (error) {
      this.logger.error('Erro ao obter saldo USDT:', error);
      return 0;
    }
  }

  async getBtcBalance(): Promise<number> {
    try {
      const account = await this.binanceService.getAccountInfo();
      const btcBalance = account.balances.find(balance => balance.asset === 'BTC');
      return parseFloat(btcBalance?.free || '0');
    } catch (error) {
      this.logger.error('Erro ao obter saldo BTC:', error);
      return 0;
    }
  }

  async convertUsdtToBtc(usdtAmount: number): Promise<number> {
    try {
      const btcPrice = await this.binanceService.getPrice('BTCUSDT');
      return usdtAmount / btcPrice;
    } catch (error) {
      this.logger.error('Erro ao converter USDT para BTC:', error);
      return 0;
    }
  }

  async isUsdtBalanceGreater(): Promise<boolean> {
    try {
      const usdtBalance = await this.getUsdtBalance();
      const btcBalance = await this.getBtcBalance();
      const btcPrice = await this.binanceService.getPrice('BTCUSDT');
      const btcValueInUsdt = btcBalance * btcPrice;
      
      return usdtBalance > btcValueInUsdt;
    } catch (error) {
      this.logger.error('Erro ao comparar saldos:', error);
      return false;
    }
  }
}

