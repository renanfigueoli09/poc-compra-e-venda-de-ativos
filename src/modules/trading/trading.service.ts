import { Injectable, Logger } from '@nestjs/common';
import { BinanceService } from '../binance/binance.service';
import { BalanceService } from '../../utils/balance.service';
import { MathService } from '../../utils/math.service';

interface TradingData {
  prices: number[];
  timestamps: Date[];
}

@Injectable()
export class TradingService {
  private readonly logger = new Logger(TradingService.name);
  private readonly symbol = 'BTCUSDT';
  private readonly interval = '15m';
  private readonly fastPeriod = 7;
  private readonly slowPeriod = 40;

  constructor(
    private readonly binanceService: BinanceService,
    private readonly balanceService: BalanceService,
    private readonly mathService: MathService,
  ) {}

  async getTradingData(): Promise<TradingData> {
    try {
      const candles = await this.binanceService.getCandles(
        this.symbol,
        this.interval,
        1000,
      );

      const prices = candles.map((candle) => parseFloat(candle.close));
      const timestamps = candles.map((candle) => new Date(candle.closeTime));

      return { prices, timestamps };
    } catch (error) {
      this.logger.error('Erro ao obter dados de trading:', error);
      throw error;
    }
  }

  async executeStrategy(): Promise<{ currentPosition: boolean }> {
    try {
      this.logger.log('Iniciando execução da estratégia de trading...');

      // Obter dados de mercado
      const { prices } = await this.getTradingData();

      // Calcular médias móveis
      const fastMA = this.mathService.calculateMovingAverage(
        prices,
        this.fastPeriod,
      );
      const slowMA = this.mathService.calculateMovingAverage(
        prices,
        this.slowPeriod,
      );

      if (fastMA.length === 0 || slowMA.length === 0) {
        this.logger.warn('Dados insuficientes para calcular médias móveis');
        return { currentPosition: false };
      }

      const lastFastMA = fastMA[fastMA.length - 1];
      const lastSlowMA = slowMA[slowMA.length - 1];

      this.logger.log(
        `Última Média Rápida: ${lastFastMA} | Última Média Lenta: ${lastSlowMA}`,
      );

      // Verificar posição atual
      const currentPosition = await this.balanceService.isUsdtBalanceGreater();
      this.logger.log(`Posição atual (USDT > BTC): ${currentPosition}`);

      // Obter informações do símbolo para limites de quantidade
      const symbolInfo = await this.binanceService.getSymbolInfo(this.symbol);
      const lotSizeFilter = symbolInfo.filters.find(
        (f) => f.filterType === 'LOT_SIZE',
      );
      const minQty = parseFloat(lotSizeFilter.minQty);
      const maxQty = parseFloat(lotSizeFilter.maxQty);
      const stepSize = parseFloat(lotSizeFilter.stepSize);

      // Determinar precisão baseada no stepSize
      const precision = this.getPrecisionFromStepSize(stepSize);

      // Estratégia de trading
      if (lastFastMA > lastSlowMA && currentPosition) {
        // Está com USDT e sinal de compra -> comprar BTC
        await this.executeBuy(minQty, maxQty, stepSize, precision);
        return { currentPosition: false }; // Agora está em BTC
      } else if (lastFastMA < lastSlowMA && !currentPosition) {
        // Está com BTC e sinal de venda -> vender para USDT
        await this.executeSell(minQty, maxQty, stepSize, precision);
        return { currentPosition: true }; // Agora está em USDT
      }

      this.logger.log('Nenhum sinal de trading detectado');
      return { currentPosition };
    } catch (error) {
      this.logger.error('Erro na execução da estratégia:', error);
      throw error;
    }
  }

  private async executeBuy(
    minQty: number,
    maxQty: number,
    stepSize: number,
    precision: number,
  ): Promise<void> {
    try {
      this.logger.log('Executando compra...');

      const usdtBalance = await this.balanceService.getUsdtBalance();
      const currentPrice = await this.binanceService.getPrice(this.symbol);

      // Calcular quantidade com melhorias de arredondamento
      const quantity = this.mathService.calculateMaxBuyQuantity(
        usdtBalance,
        currentPrice,
        stepSize,
        precision,
      );

      if (!this.mathService.isQuantityValid(quantity, minQty, maxQty)) {
        this.logger.warn(
          `Quantidade inválida: ${quantity}. Min: ${minQty}, Max: ${maxQty}`,
        );
        return;
      }

      this.logger.log(
        `Comprando ${quantity} BTC por ${currentPrice} USDT cada`,
      );

      const order = await this.binanceService.createOrder({
        symbol: this.symbol,
        side: 'BUY',
        type: 'MARKET',
        quantity: quantity.toString(),
      });

      this.logger.log('Ordem de compra executada:', order);
    } catch (error) {
      this.logger.error('Erro ao executar compra:', error);
      throw error;
    }
  }

  private async executeSell(
    minQty: number,
    maxQty: number,
    stepSize: number,
    precision: number,
  ): Promise<void> {
    try {
      this.logger.log('Executando venda...');

      const btcBalance = await this.balanceService.getBtcBalance();

      // Calcular quantidade com melhorias de arredondamento
      const quantity = this.mathService.calculateMaxSellQuantity(
        btcBalance,
        stepSize,
        precision,
      );

      if (!this.mathService.isQuantityValid(quantity, minQty, maxQty)) {
        this.logger.warn(
          `Quantidade inválida: ${quantity}. Min: ${minQty}, Max: ${maxQty}`,
        );
        return;
      }

      this.logger.log(`Vendendo ${quantity} BTC`);

      const order = await this.binanceService.createOrder({
        symbol: this.symbol,
        side: 'SELL',
        type: 'MARKET',
        quantity: quantity.toString(),
      });

      this.logger.log('Ordem de venda executada:', order);
    } catch (error) {
      this.logger.error('Erro ao executar venda:', error);
      throw error;
    }
  }

  private getPrecisionFromStepSize(stepSize: number): number {
    const stepStr = stepSize.toString();
    if (stepStr.includes('.')) {
      return stepStr.split('.')[1].length;
    }
    return 0;
  }
}
