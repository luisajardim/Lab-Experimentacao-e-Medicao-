<script lang="ts">
  import { onMount, tick } from 'svelte';
  import { Chart, registerables } from 'chart.js';
  import { loadAllData, calcQuartiles, langCounts, crossTabRQ07, type RepoRow } from '$lib/data';
  import { Loader2, FileText, CheckCircle, Clock, GitPullRequest, GitMerge, AlertCircle } from 'lucide-svelte';

  Chart.register(...registerables);

  let data = $state<RepoRow[]>([]);
  let langs = $state<ReturnType<typeof langCounts>>([]);
  let loading = $state(true);

  let ageStats = $state({ q1: 0, median: 0, q3: 0 });
  let prsStats = $state({ q1: 0, median: 0, q3: 0 });
  let relStats = $state({ q1: 0, median: 0, q3: 0 });
  let updStats = $state({ q1: 0, median: 0, q3: 0 });

  let crossData = $state<any[]>([]);

  let canvasRQ05 = $state<HTMLCanvasElement | null>(null);
  let canvasRQ06 = $state<HTMLCanvasElement | null>(null);

  function makeBarChart(canvas: HTMLCanvasElement, labels: string[], values: number[]) {
    const bgColors = labels.map((_, i) => {
      if (i === 0) return '#10b981';
      if (i === 1) return '#059669';
      if (i === 2) return '#0ea5e9';
      return '#e2e8f0';
    });

    new Chart(canvas, {
      type: 'bar',
      data: {
        labels,
        datasets: [{ 
          data: values, 
          backgroundColor: bgColors,
          borderColor: 'transparent', 
          borderRadius: 4 
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { 
            ticks: { color: '#64748b' }, 
            grid: { color: '#f1f5f9', tickLength: 4 },
            border: { display: false }
          },
          y: { 
            ticks: { color: '#475569', font: { size: 12, weight: '500' } }, 
            grid: { color: 'transparent' },
            border: { display: false }
          }
        }
      }
    });
  }

  function makeHistogramRQ06(canvas: HTMLCanvasElement) {
    const values = data.map(r => r.ratio_closed_issues).filter(v => isFinite(v));
    const bins = 10;
    const counts = Array(bins).fill(0);
    const labels: string[] = [];
    
    for (let i = 0; i < bins; i++) {
      const lo = i / bins;
      const hi = (i + 1) / bins;
      labels.push(`${(lo * 100).toFixed(0)}-${(hi * 100).toFixed(0)}%`);
      counts[i] = values.filter(v => v >= lo && (i === bins - 1 ? v <= hi : v < hi)).length;
    }
    
    new Chart(canvas, {
      type: 'bar',
      data: {
        labels,
        datasets: [{
          data: counts,
          backgroundColor: '#3b82f6',
          borderRadius: 4,
          borderSkipped: false
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { 
            ticks: { color: '#64748b', maxRotation: 45, minRotation: 45 }, 
            grid: { color: 'transparent' },
            border: { display: false }
          },
          y: { 
            ticks: { color: '#64748b' }, 
            grid: { color: '#f1f5f9' },
            border: { display: false }
          }
        }
      }
    });
  }

  onMount(async () => {
    data = await loadAllData();
    langs = langCounts(data);
    
    const idades = data.map(r => r.idade_anos);
    const prs = data.map(r => r.merged_prs);
    const rels = data.map(r => r.releases);
    const upds = data.map(r => r.dias_desde_ultima_atualizacao);
    
    ageStats = calcQuartiles(idades);
    prsStats = calcQuartiles(prs);
    relStats = calcQuartiles(rels);
    updStats = calcQuartiles(upds);

    const topLangs = langs.slice(0, 5).map(l => l.label);
    crossData = crossTabRQ07(data, topLangs);

    loading = false;
    await tick();
    const top10Langs = langs.slice(0, 10);
    if (canvasRQ05) makeBarChart(canvasRQ05, top10Langs.map(l => l.label), top10Langs.map(l => l.count));
    if (canvasRQ06) makeHistogramRQ06(canvasRQ06);
  });
</script>

<svelte:head>
  <title>Lab01 - Dashboard Analítico</title>
</svelte:head>

{#if loading}
  <div class="flex flex-col items-center justify-center min-h-[70vh] text-slate-500 gap-4">
    <Loader2 class="animate-spin w-8 h-8 text-emerald-500" />
    <span class="text-sm">Processando dados do repositório...</span>
  </div>
{:else}
  <div class="animate-in fade-in duration-700 space-y-12 pb-10" id="overview">
    <header>
      <h1 class="text-3xl font-extrabold tracking-tight text-slate-900 mb-1">Laboratório de Experimentação de Software</h1>
      <p class="text-slate-500 text-sm">Visualize e analise os 1000 repositórios mais populares do GitHub.</p>
    </header>

    <section class="grid grid-cols-1 md:grid-cols-4 gap-4" id="rq01-04">
      <div class="bg-white border border-slate-200 shadow-sm p-5 rounded-xl relative overflow-hidden">
        <div class="flex items-center justify-between mb-4">
          <span class="text-sm font-semibold text-slate-500">Total de Repositórios</span>
          <FileText size={16} class="text-slate-400" />
        </div>
        <div class="text-3xl font-black text-slate-800 tabular-nums mb-1">{data.length}</div>
        <div class="text-xs text-emerald-600 flex items-center gap-1 font-semibold">
        </div>
      </div>

      <div class="bg-white border border-slate-200 shadow-sm p-5 rounded-xl">
        <div class="flex items-center justify-between mb-4">
          <span class="text-sm font-semibold text-slate-500">Idade Mediana (RQ01)</span>
          <Clock size={16} class="text-slate-400" />
        </div>
        <div class="text-3xl font-black text-slate-800 tabular-nums mb-1">{ageStats.median.toFixed(1)}</div>
        <div class="text-xs text-slate-500 font-semibold">Anos</div>
      </div>

      <div class="bg-white border border-slate-200 shadow-sm p-5 rounded-xl">
        <div class="flex items-center justify-between mb-4">
          <span class="text-sm font-semibold text-slate-500">Mediana de PRs (RQ02)</span>
          <GitPullRequest size={16} class="text-slate-400" />
        </div>
        <div class="text-3xl font-black text-slate-800 tabular-nums mb-1">{prsStats.median}</div>
        <div class="text-xs text-slate-500 font-semibold">Pull Requests Aceitos</div>
      </div>

      <div class="bg-white border border-red-100 shadow-sm p-5 rounded-xl">
        <div class="flex items-center justify-between mb-4">
          <span class="text-sm font-semibold text-slate-500">Dias sem Update (RQ04)</span>
          <AlertCircle size={16} class="text-red-500/70" />
        </div>
        <div class="text-3xl font-black text-slate-800 tabular-nums mb-1">{updStats.median}</div>
        <div class="text-xs text-red-600 font-semibold flex items-center gap-1">
        </div>
      </div>
    </section>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      
      <section class="bg-white border border-slate-200 shadow-sm rounded-xl p-6" id="rq05-06">
        <div class="flex items-center justify-between mb-6">
          <div>
            <h3 class="text-base font-bold text-slate-900">Distribuição de Linguagens</h3>
            <p class="text-sm text-slate-500">RQ05: Linguagens mais populares</p>
          </div>
          <span class="text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-md text-xs font-bold border border-emerald-100">Top 10</span>
        </div>
        <div class="chart-wrap" style="height: 320px;">
          <canvas bind:this={canvasRQ05}></canvas>
        </div>
      </section>

      <section class="bg-white border border-slate-200 shadow-sm rounded-xl p-6">
        <div class="flex items-center justify-between mb-6">
          <div>
            <h3 class="text-base font-bold text-slate-900">Razão de Issues Fechadas</h3>
            <p class="text-sm text-slate-500">RQ06: Distribuição de status (Histograma)</p>
          </div>
        </div>
        <div class="chart-wrap" style="height: 320px;">
          <canvas bind:this={canvasRQ06}></canvas>
        </div>
      </section>

    </div>

    <section class="bg-white border border-slate-200 shadow-sm rounded-xl overflow-hidden" id="rq07">
      <div class="p-6 border-b border-slate-100 flex items-center justify-between bg-slate-50/50">
        <div>
          <h3 class="text-base font-bold text-slate-900">Linguagem vs Métricas</h3>
          <p class="text-sm text-slate-500">RQ07: Correlação cruzada para o top 5 linguagens</p>
        </div>
      </div>
      
      <div class="overflow-x-auto">
        <table class="w-full text-sm text-left">
          <thead class="text-xs text-slate-500 uppercase bg-slate-50 border-b border-slate-200">
            <tr>
              <th class="px-6 py-4 font-bold">Linguagem</th>
              <th class="px-6 py-4 font-bold text-right">Repositórios</th>
              <th class="px-6 py-4 font-bold text-right">PRs (Mediana)</th>
              <th class="px-6 py-4 font-bold text-right">Releases (Mediana)</th>
              <th class="px-6 py-4 font-bold text-right">Idade (Mediana)</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            {#each crossData as row}
              <tr class="hover:bg-slate-50/80 transition-colors">
                <td class="px-6 py-4 font-bold text-slate-800">{row.linguagem}</td>
                <td class="px-6 py-4 text-right text-slate-600 tabular-nums">{row.repos}</td>
                <td class="px-6 py-4 text-right text-slate-600 tabular-nums">{row.prs}</td>
                <td class="px-6 py-4 text-right text-slate-600 tabular-nums">{row.releases}</td>
                <td class="px-6 py-4 text-right text-slate-600 tabular-nums">{row.idade.toFixed(1)} anos</td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    </section>
    
  </div>
{/if}
