import * as fs from 'fs';
import * as path from 'path';
import YAML from 'yaml';
import { JobSpecification } from './interfaces/spec';

export function loadSpec(filePath: string): JobSpecification {
  const absolutePath = path.resolve(filePath);
  const content = fs.readFileSync(absolutePath, 'utf8');
  return YAML.parse(content) as JobSpecification;
}

export function validateSpec(spec: JobSpecification): void {
  if (!spec?.id || !spec.version || !spec.provider || !spec.graphqlQuery) {
    throw new Error('Spec inválida: id, version, provider e graphqlQuery são obrigatórios.');
  }

  if (!spec.collection || !spec.csv) {
    throw new Error('Spec inválida: collection e csv são obrigatórios para exportação genérica.');
  }

  if (!spec.collection.recordsPath || !Number.isInteger(spec.collection.maxRecords) || spec.collection.maxRecords <= 0) {
    throw new Error('Spec inválida: collection.recordsPath e collection.maxRecords (> 0) são obrigatórios.');
  }

  if (!Array.isArray(spec.csv.columns) || spec.csv.columns.length === 0) {
    throw new Error('Spec inválida: csv.columns deve conter ao menos uma coluna.');
  }

  const names = new Set<string>();
  for (const column of spec.csv.columns) {
    if (!column.name || names.has(column.name)) {
      throw new Error(`Spec inválida: coluna CSV ausente ou duplicada (${column.name || 'sem nome'}).`);
    }
    if (!['string', 'integer', 'number', 'date'].includes(column.type)) {
      throw new Error(`Spec inválida: tipo não suportado na coluna ${column.name}.`);
    }
    if (!column.jsonPath && !column.transform) {
      throw new Error(`Spec inválida: coluna ${column.name} requer jsonPath ou transform.`);
    }
    names.add(column.name);
  }
}
