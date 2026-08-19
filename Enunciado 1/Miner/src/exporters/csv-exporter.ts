import * as fs from 'fs';
import * as path from 'path';
import { Parser } from 'json2csv';
import { CsvColumn } from '../core/interfaces/spec';
import { extractSingleValue } from '../core/record-extractor';
import { transforms } from '../transforms/repository';

type CsvRow = Record<string, string | number>;

function normalize(value: unknown, column: CsvColumn): string | number {
  const fallback = column.default ?? (column.type === 'string' || column.type === 'date' ? '' : 0);
  if (column.type === 'string') return typeof value === 'string' ? value : String(value ?? fallback);
  if (column.type === 'date') {
    const date = new Date(String(value ?? ''));
    return Number.isNaN(date.getTime()) ? String(fallback) : date.toISOString();
  }
  const number = typeof value === 'number' ? value : Number(value);
  if (!Number.isFinite(number)) return Number(fallback) || 0;
  return column.type === 'integer' ? Math.max(0, Math.trunc(number)) : number;
}

export function buildCsvRows(records: unknown[], columns: CsvColumn[], collectedAt: Date): CsvRow[] {
  return records.map((record) => Object.fromEntries(columns.map((column) => {
    const source = column.sourcePath ?? column.jsonPath;
    // Transformações sem sourcePath/jsonPath recebem o registro inteiro.
    const rawValue = source ? extractSingleValue(record, source) : record;
    const transformed = column.transform ? transforms[column.transform]?.(rawValue, collectedAt) : rawValue;
    if (column.transform && !transforms[column.transform]) {
      throw new Error(`Transformação CSV não registrada: ${column.transform}`);
    }
    return [column.name, normalize(transformed, column)];
  })));
}

export function saveToCsv(rows: CsvRow[], columns: CsvColumn[], directory: string, fileName: string): string | undefined {
  if (rows.length === 0) return undefined;
  const dataDirectory = path.resolve(directory);
  fs.mkdirSync(dataDirectory, { recursive: true });
  const parser = new Parser({ fields: columns.map((column) => column.name) });
  const outputPath = path.join(dataDirectory, fileName);
  fs.writeFileSync(outputPath, parser.parse(rows), 'utf8');
  return outputPath;
}
