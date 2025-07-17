import { Module } from '@nestjs/common';
import { ConfigModule } from './config/config.module';
import { BinanceModule } from './modules/binance/binance.module';
import { UtilsModule } from './utils/utils.module';
import { TradingModule } from './modules/trading/trading.module';
import { SchedulerModule } from './modules/scheduler/scheduler.module';
import { ApiModule } from './modules/api/api.module';

@Module({
  imports: [
    ConfigModule,
    BinanceModule,
    UtilsModule,
    TradingModule,
    SchedulerModule,
    ApiModule,
  ],
})
export class AppModule {}
