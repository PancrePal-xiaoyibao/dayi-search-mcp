import { rm, cp, mkdir } from 'node:fs/promises';
import { resolve } from 'node:path';
import process from 'node:process';

const packageRoot = resolve(import.meta.dirname, '..');
const sourceDir = resolve(packageRoot, '..', 'src', 'dayi_core');
const targetRoot = resolve(packageRoot, 'python');
const targetDir = resolve(targetRoot, 'dayi_core');

async function main() {
  await rm(targetDir, { recursive: true, force: true });
  await mkdir(targetRoot, { recursive: true });
  await cp(sourceDir, targetDir, {
    recursive: true,
    filter: (source) => {
      const normalized = source.replaceAll('\\', '/');
      if (normalized.includes('/__pycache__/')) return false;
      if (normalized.endsWith('.pyc')) return false;
      return true;
    },
  });
  process.stdout.write(`synced python core: ${sourceDir} -> ${targetDir}\n`);
}

main().catch((error) => {
  process.stderr.write(`sync failed: ${error instanceof Error ? error.message : String(error)}\n`);
  process.exitCode = 1;
});
