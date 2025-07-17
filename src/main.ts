import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { Logger } from '@nestjs/common';

async function bootstrap() {
  const logger = new Logger('Bootstrap');
  
  const app = await NestFactory.create(AppModule);
  
  // Configurar CORS
  app.enableCors({
    origin: '*',
    methods: 'GET,HEAD,PUT,PATCH,POST,DELETE',
    credentials: true,
  });

  // Configurar porta
  const port = process.env.PORT || 3000;
  
  await app.listen(port);
  
  logger.log(`Aplicação rodando na porta ${port}`);
  logger.log(`Cron jobs configurados para executar a cada 15 minutos`);
}

bootstrap();
