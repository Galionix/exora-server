import { Test, TestingModule } from '@nestjs/testing';
import { ChunksService } from './chunks.service';

describe('ChunksService', () => {
  let service: ChunksService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [ChunksService],
    }).compile();

    service = module.get<ChunksService>(ChunksService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
