import { Module } from '@nestjs/common';
import { ApiController } from './api.controller';
import { SchedulerModule } from '../scheduler/scheduler.module';
import { TradingModule } from '../trading/trading.module';
import { UtilsModule } from '../../utils/utils.module';
import { BinanceModule } from '../binance/binance.module';

@Module({
  imports: [SchedulerModule, TradingModule, UtilsModule, BinanceModule],
  controllers: [ApiController],
})
export class ApiModule {}

