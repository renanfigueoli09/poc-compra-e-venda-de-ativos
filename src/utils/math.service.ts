import { Injectable } from '@nestjs/common';

@Injectable()
export class MathService {
  
  /**
   * Trunca um número para o primeiro dígito significativo
   * Melhoria: Arredonda para baixo para evitar erros de saldo
   */
  truncateToFirstSignificantDigit(num: number): number {
    if (num === 0) return 0;
    
    const magnitude = Math.floor(Math.log10(Math.abs(num)));
    const factor = Math.pow(10, magnitude);
    
    // Arredonda para baixo para evitar problemas de saldo
    return Math.floor(num / factor) * factor;
  }

  /**
   * Ajusta a quantidade baseada no step size da Binance
   * Arredonda para baixo para garantir que não exceda o saldo disponível
   */
  adjustQuantityToStepSize(quantity: number, stepSize: number): number {
    if (stepSize === 0) return quantity;
    
    // Calcula quantos steps cabem na quantidade
    const steps = Math.floor(quantity / stepSize);
    
    // Retorna a quantidade ajustada (sempre para baixo)
    return steps * stepSize;
  }

  /**
   * Formata a quantidade com a precisão correta
   * Arredonda para baixo para evitar erros de saldo
   */
  formatQuantity(quantity: number, precision: number): string {
    // Arredonda para baixo usando Math.floor
    const factor = Math.pow(10, precision);
    const adjustedQuantity = Math.floor(quantity * factor) / factor;
    
    return adjustedQuantity.toFixed(precision);
  }

  /**
   * Calcula a quantidade máxima que pode ser comprada com o saldo disponível
   * Aplica uma margem de segurança de 0.1% para evitar erros de saldo insuficiente
   */
  calculateMaxBuyQuantity(usdtBalance: number, price: number, stepSize: number, precision: number): number {
    // Aplica margem de segurança de 0.1%
    const safeBalance = usdtBalance * 0.999;
    
    // Calcula quantidade máxima
    const maxQuantity = safeBalance / price;
    
    // Ajusta para o step size
    const adjustedQuantity = this.adjustQuantityToStepSize(maxQuantity, stepSize);
    
    // Formata com a precisão correta
    return parseFloat(this.formatQuantity(adjustedQuantity, precision));
  }

  /**
   * Calcula a quantidade máxima que pode ser vendida
   * Aplica uma margem de segurança para evitar erros de saldo insuficiente
   */
  calculateMaxSellQuantity(btcBalance: number, stepSize: number, precision: number): number {
    // Aplica margem de segurança de 0.1%
    const safeBalance = btcBalance * 0.999;
    
    // Ajusta para o step size
    const adjustedQuantity = this.adjustQuantityToStepSize(safeBalance, stepSize);
    
    // Formata com a precisão correta
    return parseFloat(this.formatQuantity(adjustedQuantity, precision));
  }

  /**
   * Verifica se a quantidade está dentro dos limites mínimos e máximos
   */
  isQuantityValid(quantity: number, minQty: number, maxQty: number): boolean {
    return quantity >= minQty && quantity <= maxQty;
  }

  /**
   * Calcula médias móveis
   */
  calculateMovingAverage(prices: number[], period: number): number[] {
    const result: number[] = [];
    
    for (let i = period - 1; i < prices.length; i++) {
      const sum = prices.slice(i - period + 1, i + 1).reduce((a, b) => a + b, 0);
      result.push(sum / period);
    }
    
    return result;
  }
}

