import * as fs from 'fs';
import * as path from 'path';

export type JsonValue = string | number | boolean;
export type JsonRow = Record<string, JsonValue>;
export interface CsvToJsonOptions { inferTypes?: boolean; }

function parseCsvCells(content: string): string[][] {
  const rows: string[][] = [];
  let row: string[] = [];
  let value = '';
  let quoted = false;
  for (let index = 0; index < content.length; index += 1) {
    const character = content[index];
    if (quoted) {
      if (character === '"' && content[index + 1] === '"') { value += '"'; index += 1; }
      else if (character === '"') quoted = false;
      else value += character;
      continue;
    }
    if (character === '"') quoted = true;
    else if (character === ',') { row.push(value); value = ''; }
    else if (character === '\n') { row.push(value); rows.push(row); row = []; value = ''; }
    else if (character !== '\r') value += character;
  }
  if (quoted) throw new Error('CSV inválido: campo entre aspas não foi fechado.');
  if (value.length > 0 || row.length > 0) { row.push(value); rows.push(row); }
  return rows;
}

function toJsonValue(value: string, inferTypes: boolean): JsonValue {
  if (!inferTypes || value === '') return value;
  if (value === 'true') return true;
  if (value === 'false') return false;
  const numberPattern = /^-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?$/;
  if (numberPattern.test(value)) {
    const number = Number(value);
    if (Number.isFinite(number)) return number;
  }
  return value;
}

/** Converte um CSV RFC 4180 em objetos JSON usando a primeira linha como cabeçalho. */
export function parseCsvToJson(content: string, options: CsvToJsonOptions = {}): JsonRow[] {
  const rows = parseCsvCells(content);
  const [headerRow, ...dataRows] = rows;
  if (!headerRow || headerRow.length === 0) return [];
  const headers = headerRow.map((header, index) => {
    const normalized = index === 0 ? header.replace(/^\uFEFF/, '') : header;
    if (!normalized) throw new Error(`CSV inválido: cabeçalho vazio na coluna ${index + 1}.`);
    return normalized;
  });
  if (new Set(headers).size !== headers.length) throw new Error('CSV inválido: há cabeçalhos duplicados.');
  return dataRows.filter((row) => row.some((value) => value !== '')).map((row, rowIndex) => {
    if (row.length !== headers.length) throw new Error(`CSV inválido: linha ${rowIndex + 2} possui ${row.length} colunas; esperado ${headers.length}.`);
    return Object.fromEntries(headers.map((header, index) => [header, toJsonValue(row[index], options.inferTypes ?? true)]));
  });
}

export function convertCsvFileToJson(inputPath: string, outputPath: string, options: CsvToJsonOptions = {}): number {
  const input = path.resolve(inputPath);
  const output = path.resolve(outputPath);
  if (!fs.existsSync(input)) throw new Error(`Arquivo CSV não encontrado: ${input}`);
  const records = parseCsvToJson(fs.readFileSync(input, 'utf8'), options);
  fs.mkdirSync(path.dirname(output), { recursive: true });
  fs.writeFileSync(output, `${JSON.stringify(records, null, 2)}\n`, 'utf8');
  return records.length;
}

function run(): void {
  const argumentsList = process.argv.slice(2);
  const inferTypes = !argumentsList.includes('--no-infer-types');
  const paths = argumentsList.filter((argument) => argument !== '--no-infer-types');
  const input = paths[0] ?? './data/1000_popular_repos.csv';
  const output = paths[1] ?? '../Dashboard/static/data/repos.json';
  if (paths.length > 2) throw new Error('Uso: npm run csv:json -- [arquivo.csv] [saida.json] [--no-infer-types]');
  const count = convertCsvFileToJson(input, output, { inferTypes });
  console.log(`💾 JSON salvo em: ${path.resolve(output)} (${count} registros)`);
}

if (require.main === module) {
  try { run(); } catch (error) {
    console.error('❌ Erro durante a conversão CSV → JSON:', error instanceof Error ? error.message : error);
    process.exitCode = 1;
  }
}
