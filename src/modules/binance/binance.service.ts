import { Injectable, Logger } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import Binance from 'binance-api-node';

@Injectable()
export class BinanceService {
  private readonly logger = new Logger(BinanceService.name);
  private readonly client: any;
  private timeOffset: number = 0;

  constructor(private readonly configService: ConfigService) {
    // Configurar axios para ignorar certificados SSL em desenvolvimento
    if (this.configService.get<string>('NODE_ENV') === 'development') {
      process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';
      this.logger.warn('SSL certificate verification disabled for development');
    }

    // Configurar cliente Binance com configurações customizadas
    this.client = Binance({
      apiKey: this.configService.get<string>('API_KEY'),
      apiSecret: this.configService.get<string>('API_SECRET'),
      httpBase: 'https://api.binance.com',
      httpFutures: 'https://fapi.binance.com',
      wsBase: 'wss://stream.binance.com:9443/ws/',
      wsFutures: 'wss://fstream.binance.com/ws/',
      getTime: () => Date.now() + this.timeOffset,
    });

    // Sincronizar tempo na inicialização
    this.synchronizeTime();
  }

  /**
   * Sincroniza o tempo local com o servidor da Binance
   * Implementação similar à função synchronize_binance_time da aplicação original
   */
  async synchronizeTime(): Promise<void> {
    try {
      this.logger.log('Sincronizando tempo com servidor Binance...');

      const serverTime = await this.client.time(); // isso já é um número
      const localTime = Date.now();

      this.timeOffset = serverTime - localTime;

      if (isNaN(this.timeOffset)) {
        this.logger.warn(
          'Offset de tempo inválido detectado. Resetando para 0.',
        );
        this.timeOffset = 0;
      }

      this.logger.log(
        `Sincronização de tempo concluída. Offset: ${this.timeOffset}ms`,
      );
    } catch (error) {
      this.logger.error(
        'Erro ao sincronizar tempo com Binance:',
        error.message,
      );
      this.timeOffset = 0;
    }
  }

  async ping(): Promise<boolean> {
    try {
      await this.client.ping();
      this.logger.log('Conexão com Binance estabelecida com sucesso');
      return true;
    } catch (error) {
      this.logger.error('Erro ao conectar com a Binance:', error.message);

      // Se for erro de certificado, tentar sincronizar tempo novamente
      if (
        error.message.includes('certificate') ||
        error.message.includes('CERT_')
      ) {
        this.logger.warn(
          'Erro de certificado detectado. Tentando ressincronizar...',
        );
        await this.synchronizeTime();
      }

      return false;
    }
  }

  async getSymbolInfo(symbol: string) {
    try {
      const exchangeInfo = await this.client.exchangeInfo();
      return exchangeInfo.symbols.find((s) => s.symbol === symbol);
    } catch (error) {
      this.logger.error(
        `Erro ao obter informações do símbolo ${symbol}:`,
        error.message,
      );
      throw error;
    }
  }

  async getCandles(symbol: string, interval: string, limit: number = 1000) {
    try {
      return await this.client.candles({
        symbol,
        interval,
        limit,
      });
    } catch (error) {
      this.logger.error(`Erro ao obter candles para ${symbol}:`, error.message);
      throw error;
    }
  }

  async getAccountInfo() {
    try {
      return await this.client.accountInfo();
    } catch (error) {
      this.logger.error('Erro ao obter informações da conta:', error.message);
      throw error;
    }
  }

  async createOrder(orderParams: any) {
    try {
      // Ressincronizar tempo antes de operações críticas
      await this.synchronizeTime();

      return await this.client.order(orderParams);
    } catch (error) {
      this.logger.error('Erro ao criar ordem:', error.message);

      // Se for erro de timestamp, tentar ressincronizar
      if (
        error.message.includes('timestamp') ||
        error.message.includes('time')
      ) {
        this.logger.warn(
          'Erro de timestamp detectado. Ressincronizando tempo...',
        );
        await this.synchronizeTime();

        // Tentar novamente após ressincronização
        try {
          return await this.client.order(orderParams);
        } catch (retryError) {
          this.logger.error(
            'Erro na segunda tentativa de criar ordem:',
            retryError.message,
          );
          throw retryError;
        }
      }

      throw error;
    }
  }

  async getPrice(symbol: string) {
    try {
      const ticker = await this.client.prices({ symbol });
      return parseFloat(ticker[symbol]);
    } catch (error) {
      this.logger.error(`Erro ao obter preço de ${symbol}:`, error.message);
      throw error;
    }
  }

  /**
   * Método para forçar ressincronização de tempo
   * Útil para chamadas manuais quando há problemas de timestamp
   */
  async forceSynchronizeTime(): Promise<void> {
    await this.synchronizeTime();
  }

  /**
   * Retorna o offset de tempo atual
   */
  getTimeOffset(): number {
    return this.timeOffset;
  }
}
