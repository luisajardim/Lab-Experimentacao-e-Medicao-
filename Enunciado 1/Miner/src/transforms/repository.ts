export type Transform = (value: unknown, collectedAt: Date) => unknown;

function ageInYears(value: unknown, collectedAt: Date): number {
  const createdAt = new Date(String(value));
  if (Number.isNaN(createdAt.getTime())) return 0;
  const years = (collectedAt.getTime() - createdAt.getTime()) / (1000 * 60 * 60 * 24 * 365.25);
  return years < 0 ? 0 : Number(years.toFixed(2));
}

function daysSince(value: unknown, collectedAt: Date): number {
  const pushedAt = new Date(String(value));
  if (Number.isNaN(pushedAt.getTime())) return 0;
  const days = Math.round((collectedAt.getTime() - pushedAt.getTime()) / (1000 * 60 * 60 * 24));
  return Math.max(0, days);
}

function closedIssuesRatio(value: unknown): number {
  if (!value || typeof value !== 'object') return 0;
  const repository = value as {
    totalIssues?: { totalCount?: unknown };
    closedIssues?: { totalCount?: unknown };
  };
  const total = Number(repository.totalIssues?.totalCount);
  const closed = Number(repository.closedIssues?.totalCount);
  if (!Number.isFinite(total) || !Number.isFinite(closed) || total <= 0) return 0;
  return Number(Math.max(0, closed / total).toFixed(4));
}

export const transforms: Record<string, Transform> = {
  repositoryAgeYears: ageInYears,
  daysSinceLastPush: daysSince,
  closedIssuesRatio,
  collectedAt: (_value, collectedAt) => collectedAt.toISOString(),
};
