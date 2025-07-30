import { Module } from '@nestjs/common';

import { AppController } from './app.controller';
import { AppService } from './app.service';
import { ChunksModule } from './chunks/chunks.module';

@Module({
  imports: [ChunksModule, ChunksModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
