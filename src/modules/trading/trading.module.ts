import { Module } from '@nestjs/common';
import { TradingService } from './trading.service';
import { BinanceModule } from '../binance/binance.module';
import { UtilsModule } from '../../utils/utils.module';

@Module({
  imports: [BinanceModule, UtilsModule],
  providers: [TradingService],
  exports: [TradingService],
})
export class TradingModule {}

