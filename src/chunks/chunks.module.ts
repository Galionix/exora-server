import { Module } from '@nestjs/common';
import { ChunksService } from './chunks.service';
import { ChunksController } from './chunks.controller';

@Module({
  controllers: [ChunksController],
  providers: [ChunksService],
})
export class ChunksModule {}
