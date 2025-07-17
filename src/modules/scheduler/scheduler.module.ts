import { Module } from '@nestjs/common';
import { ScheduleModule } from '@nestjs/schedule';
import { SchedulerService } from './scheduler.service';
import { TradingModule } from '../trading/trading.module';
import { BinanceModule } from '../binance/binance.module';

@Module({
  imports: [
    ScheduleModule.forRoot(),
    TradingModule,
    BinanceModule,
  ],
  providers: [SchedulerService],
  exports: [SchedulerService],
})
export class SchedulerModule {}

