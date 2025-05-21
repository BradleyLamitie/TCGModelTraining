// download.ts
import mongoose from 'mongoose';
import axios from 'axios';
import fs from 'fs';
import path from 'path';
import Card from './models/Card';
import dotenv from 'dotenv';

dotenv.config();

const DOWNLOAD_DIR = './dataset';

const sanitize = (text: string) => text.replace(/[^\w\d_-]/g, '');

async function downloadImage(url: string, filepath: string): Promise<void> {
  const response = await axios.get(url, { responseType: 'stream' });
  const writer = fs.createWriteStream(filepath);
  await new Promise((resolve, reject) => {
    response.data.pipe(writer);
    writer.on('finish', () => resolve(undefined));
    writer.on('error', reject);
  });
}

async function main() {
  await mongoose.connect(process.env.MONGO_CONNECTION_STRING!);

  const cards = await Card.find({}).limit(500); // sample size

  for (const card of cards) {
    const name = card.cardInfo?.name;
    const setName = card.cardInfo?.set.name;
    const cardNumber = card.cardInfo?.number;
    const imageUrl = card.cardInfo?.images?.large;

    if (!imageUrl || !name || !setName || !cardNumber) continue;

    const label = `${sanitize(name)}_${sanitize(setName)}_${sanitize(cardNumber)}`;
    const labelDir = path.join(DOWNLOAD_DIR, label);
    fs.mkdirSync(labelDir, { recursive: true });

    const filename = `${label}_${Date.now()}.jpg`;
    const filepath = path.join(labelDir, filename);

    try {
      await downloadImage(imageUrl, filepath);
      console.log(`Downloaded: ${filepath}`);
    } catch (err) {
      console.error(`Failed to download ${imageUrl}:`, (err as Error).message);
    }
  }

  await mongoose.disconnect();
}

main().catch(console.error);