<script lang="ts">
  import { onMount, tick } from 'svelte';
  import { Chart, registerables } from 'chart.js';
  import { loadAllData, calcQuartiles, langCounts, crossTabRQ07, type RepoRow } from '$lib/data';
  import { Loader2, FileText, CheckCircle, Clock, GitPullRequest, GitMerge, AlertCircle } from 'lucide-svelte';

  Chart.register(...registerables);

  let data = $state<RepoRow[]>([]);
  let langs = $state<ReturnType<typeof langCounts>>([]);
  let loading = $state(true);

  // RQ01-RQ04 stats
  let ageStats = $state({ q1: 0, median: 0, q3: 0 });
  let prsStats = $state({ q1: 0, median: 0, q3: 0 });
  let relStats = $state({ q1: 0, median: 0, q3: 0 });
  let updStats = $state({ q1: 0, median: 0, q3: 0 });

  // RQ07 Data
  let crossData = $state<any[]>([]);

  // Canvas
  let canvasRQ05 = $state<HTMLCanvasElement | null>(null);
  let canvasRQ06 = $state<HTMLCanvasElement | null>(null);

  function makeBarChart(canvas: HTMLCanvasElement, labels: string[], values: number[]) {
    // Cores inspiradas no tema SaaS: tons de verde/esmeralda e ciano
    const bgColors = labels.map((_, i) => {
      if (i === 0) return '#10b981'; // emerald-500 para o Top 1
      if (i === 1) return '#059669'; // emerald-600
      if (i === 2) return '#0ea5e9'; // sky-500
      return '#2a2a2a'; // zinc-800 genérico
    });

    new Chart(canvas, {
      type: 'bar',
      data: {
        labels,
        datasets: [{ 
          data: values, 
          backgroundColor: bgColors,
          borderColor: 'transparent', 
          borderRadius: 2 
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { 
            ticks: { color: '#71717a' }, 
            grid: { color: '#2a2a2a', tickLength: 4 },
            border: { display: false }
          },
          y: { 
            ticks: { color: '#a1a1aa', font: { size: 12 } }, 
            grid: { color: 'transparent' },
            border: { display: false }
          }
        }
      }
    });
  }

  function makePieChartRQ06(canvas: HTMLCanvasElement) {
    const values = data.map(r => r.ratio_closed_issues).filter(v => isFinite(v));
    let q1 = 0, q2 = 0, q3 = 0, q4 = 0;
    values.forEach(v => {
      if (v <= 0.25) q1++;
      else if (v <= 0.5) q2++;
      else if (v <= 0.75) q3++;
      else q4++;
    });
    
    new Chart(canvas, {
      type: 'doughnut',
      data: {
        labels: ['0% - 25%', '26% - 50%', '51% - 75%', '76% - 100%'],
        datasets: [{
          data: [q1, q2, q3, q4],
          backgroundColor: ['#ef4444', '#f59e0b', '#3b82f6', '#10b981'],
          borderColor: '#141414',
          borderWidth: 2,
          hoverOffset: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { 
          legend: { position: 'right', labels: { color: '#a1a1aa' } }
        }
      }
    });
  }

  onMount(async () => {
    data = await loadAllData();
    
    // Processamento
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
    if (canvasRQ06) makePieChartRQ06(canvasRQ06);
  });
</script>

<svelte:head>
  <title>Lab01 - Dashboard Analítico</title>
</svelte:head>

{#if loading}
  <div class="flex flex-col items-center justify-center min-h-[70vh] text-zinc-500 gap-4">
    <Loader2 class="animate-spin w-8 h-8 text-emerald-500" />
    <span class="text-sm">Processando dados do repositório...</span>
  </div>
{:else}
  <div class="animate-in fade-in duration-700 space-y-12 pb-10" id="overview">
    <!-- Header -->
    <header>
      <h1 class="text-3xl font-bold tracking-tight text-white mb-1">Laboratório de Experimentação de Software</h1>
      <p class="text-zinc-500 text-sm">Visualize e analise os 1000 repositórios mais populares do GitHub.</p>
    </header>

    <!-- Top Summary Cards (RQ01-RQ04 Medians) -->
    <section class="grid grid-cols-1 md:grid-cols-4 gap-4" id="rq01-04">
      <!-- Card 1 -->
      <div class="bg-[#141414] border border-[#2a2a2a] p-5 rounded-lg hover:border-[#3a3a3a] transition-colors relative overflow-hidden">
        <div class="flex items-center justify-between mb-4">
          <span class="text-sm font-medium text-zinc-400">Total de Repositórios</span>
          <FileText size={16} class="text-zinc-500" />
        </div>
        <div class="text-3xl font-bold text-white tabular-nums mb-1">{data.length}</div>
        <div class="text-xs text-emerald-500 flex items-center gap-1 font-medium">
        </div>
      </div>

      <!-- Card 2 -->
      <div class="bg-[#141414] border border-[#2a2a2a] p-5 rounded-lg hover:border-[#3a3a3a] transition-colors">
        <div class="flex items-center justify-between mb-4">
          <span class="text-sm font-medium text-zinc-400">Idade Mediana (RQ01)</span>
          <Clock size={16} class="text-zinc-500" />
        </div>
        <div class="text-3xl font-bold text-white tabular-nums mb-1">{ageStats.median.toFixed(1)}</div>
        <div class="text-xs text-zinc-500 font-medium">Anos</div>
      </div>

      <!-- Card 3 -->
      <div class="bg-[#141414] border border-[#2a2a2a] p-5 rounded-lg hover:border-[#3a3a3a] transition-colors">
        <div class="flex items-center justify-between mb-4">
          <span class="text-sm font-medium text-zinc-400">Mediana de PRs (RQ02)</span>
          <GitPullRequest size={16} class="text-zinc-500" />
        </div>
        <div class="text-3xl font-bold text-white tabular-nums mb-1">{prsStats.median}</div>
        <div class="text-xs text-zinc-500 font-medium">Pull Requests Aceitos</div>
      </div>

      <!-- Card 4 -->
      <div class="bg-[#141414] border border-red-900/30 p-5 rounded-lg hover:border-red-900/50 transition-colors">
        <div class="flex items-center justify-between mb-4">
          <span class="text-sm font-medium text-zinc-400">Dias sem Update (RQ04)</span>
          <AlertCircle size={16} class="text-red-500/70" />
        </div>
        <div class="text-3xl font-bold text-white tabular-nums mb-1">{updStats.median}</div>
        <div class="text-xs text-red-500/70 font-medium flex items-center gap-1">
        </div>
      </div>
    </section>

    <!-- Main Charts Area -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      
      <!-- Linguagens Populares (RQ05) -->
      <section class="bg-[#141414] border border-[#2a2a2a] rounded-lg p-6" id="rq05-06">
        <div class="flex items-center justify-between mb-6">
          <div>
            <h3 class="text-base font-semibold text-white">Distribuição de Linguagens</h3>
            <p class="text-sm text-zinc-500">RQ05: Linguagens mais populares</p>
          </div>
          <span class="text-emerald-500 bg-emerald-500/10 px-2.5 py-1 rounded-md text-xs font-semibold">Top 10</span>
        </div>
        <div class="chart-wrap" style="height: 320px;">
          <canvas bind:this={canvasRQ05}></canvas>
        </div>
      </section>

      <!-- Ratio Issues (RQ06) -->
      <section class="bg-[#141414] border border-[#2a2a2a] rounded-lg p-6">
        <div class="flex items-center justify-between mb-6">
          <div>
            <h3 class="text-base font-semibold text-white">Razão de Issues Fechadas</h3>
            <p class="text-sm text-zinc-500">RQ06: Distribuição de status</p>
          </div>
        </div>
        <div class="chart-wrap" style="height: 320px;">
          <canvas bind:this={canvasRQ06}></canvas>
        </div>
      </section>

    </div>

    <!-- Tabela Cruzada RQ07 -->
    <section class="bg-[#141414] border border-[#2a2a2a] rounded-lg overflow-hidden" id="rq07">
      <div class="p-6 border-b border-[#2a2a2a] flex items-center justify-between">
        <div>
          <h3 class="text-base font-semibold text-white">Linguagem vs Métricas</h3>
          <p class="text-sm text-zinc-500">RQ07: Correlação cruzada para o top 5 linguagens</p>
        </div>
      </div>
      
      <div class="overflow-x-auto">
        <table class="w-full text-sm text-left">
          <thead class="text-xs text-zinc-400 uppercase bg-[#0f0f0f] border-b border-[#2a2a2a]">
            <tr>
              <th class="px-6 py-4 font-medium">Linguagem</th>
              <th class="px-6 py-4 font-medium text-right">Repositórios</th>
              <th class="px-6 py-4 font-medium text-right">PRs (Mediana)</th>
              <th class="px-6 py-4 font-medium text-right">Releases (Mediana)</th>
              <th class="px-6 py-4 font-medium text-right">Idade (Mediana)</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-[#2a2a2a]">
            {#each crossData as row}
              <tr class="hover:bg-[#1a1a1a] transition-colors">
                <td class="px-6 py-4 font-medium text-zinc-200">{row.linguagem}</td>
                <td class="px-6 py-4 text-right text-zinc-400 tabular-nums">{row.repos}</td>
                <td class="px-6 py-4 text-right text-zinc-400 tabular-nums">{row.prs}</td>
                <td class="px-6 py-4 text-right text-zinc-400 tabular-nums">{row.releases}</td>
                <td class="px-6 py-4 text-right text-zinc-400 tabular-nums">{row.idade.toFixed(1)} anos</td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    </section>
    
  </div>
{/if}
