import { Module } from '@nestjs/common';
import { BalanceService } from './balance.service';
import { MathService } from './math.service';
import { BinanceModule } from '../modules/binance/binance.module';

@Module({
  imports: [BinanceModule],
  providers: [BalanceService, MathService],
  exports: [BalanceService, MathService],
})
export class UtilsModule {}

