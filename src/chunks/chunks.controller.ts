import { Response } from 'express';
import { createReadStream, existsSync } from 'fs';
import { join } from 'path';

import { Controller, Get, NotFoundException, Param, Res } from '@nestjs/common';
import { ApiParam, ApiResponse, ApiTags } from '@nestjs/swagger';

import { ChunksService } from './chunks.service';

@ApiTags('Chunks')
@Controller('chunks')
export class ChunksController {
  constructor(private readonly chunksService: ChunksService) {}

  // @Post()
  // create(@Body() createChunkDto: CreateChunkDto) {
  //   return this.chunksService.create(createChunkDto);
  // }

  // @Get()
  // findAll() {
  //   return this.chunksService.findAll();
  // }

  // @Get(':id')
  // findOne(@Param('id') id: string) {
  //   return this.chunksService.findOne(+id);
  // }

  // @Patch(':id')
  // update(@Param('id') id: string, @Body() updateChunkDto: UpdateChunkDto) {
  //   return this.chunksService.update(+id, updateChunkDto);
  // }

  // @Delete(':id')
  // remove(@Param('id') id: string) {
  //   return this.chunksService.remove(+id);
  // }
  @Get(':chunkName')
  @ApiParam({
    name: 'chunkName',
    description: 'Chunk file name, format: xNyN.gz',
    example: 'x1y2.gz'
  })
  @ApiResponse({ status: 200, description: 'Returns the requested chunk as a gzipped file' })
  @ApiResponse({ status: 404, description: 'Chunk not found or invalid name' })
  getChunk(@Param('chunkName') chunkName: string, @Res() res: Response) {
    if (!/^x\d+y\d+\.gz$/.test(chunkName)) {
      throw new NotFoundException('Invalid chunk name');
    }

    const filePath = join(__dirname, '..', '..', '..', 'chunks', chunkName);

    if (!existsSync(filePath)) {
      throw new NotFoundException('Chunk not found');
    }

    res.set({
      'Content-Encoding': 'gzip',
      'Content-Type': 'application/octet-stream',
    });

    const fileStream = createReadStream(filePath);
    fileStream.pipe(res);
  }
}
