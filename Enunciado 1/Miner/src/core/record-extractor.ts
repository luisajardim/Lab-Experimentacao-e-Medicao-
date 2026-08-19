import jp from 'jsonpath';

export function extractRecords(rawData: unknown, recordsPath: string): unknown[] {
  return jp.query(rawData, recordsPath);
}

export function extractSingleValue(record: unknown, jsonPath: string): unknown {
  const values = jp.query(record, jsonPath);
  return values.length === 1 ? values[0] : undefined;
}
