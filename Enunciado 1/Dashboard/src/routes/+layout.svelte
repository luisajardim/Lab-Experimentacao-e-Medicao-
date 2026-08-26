<script lang="ts">
  import '../app.css';
  import { LayoutDashboard, Target, GitPullRequest, GitMerge } from 'lucide-svelte';
  
  let { children } = $props();
</script>

<div class="flex min-h-screen bg-slate-50 text-slate-800 overflow-hidden">
  <aside class="w-64 border-r border-slate-200 bg-white flex flex-col hidden md:flex shrink-0 h-screen sticky top-0">
    <div class="p-6 border-b border-slate-200">
      <div class="font-bold text-slate-900 flex items-center gap-2">
        <div class="w-2 h-2 rounded-sm bg-emerald-500"></div>
        Lab01 Miner
      </div>
      <p class="text-xs text-slate-500 mt-1">Dados & Análises</p>
    </div>
    
    <nav class="flex-1 p-4 space-y-1 overflow-y-auto">
      <div class="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-3 mt-2 px-2">Navegação</div>
      
      <a href="#overview" class="flex items-center gap-3 px-3 py-2 text-sm text-emerald-700 bg-emerald-50 rounded-md font-medium">
        <LayoutDashboard size={16} class="text-emerald-600" />
        Visão Geral
      </a>
      <a href="#rq01-04" class="flex items-center gap-3 px-3 py-2 text-sm text-slate-600 hover:text-slate-900 hover:bg-slate-50 rounded-md transition-colors">
        <Target size={16} />
        Métricas de Maturidade
      </a>
      <a href="#rq05-06" class="flex items-center gap-3 px-3 py-2 text-sm text-slate-600 hover:text-slate-900 hover:bg-slate-50 rounded-md transition-colors">
        <GitPullRequest size={16} />
        Linguagens & Issues
      </a>
      <a href="#rq07" class="flex items-center gap-3 px-3 py-2 text-sm text-slate-600 hover:text-slate-900 hover:bg-slate-50 rounded-md transition-colors">
        <GitMerge size={16} />
        Cruzamento (RQ07)
      </a>
    </nav>
  </aside>

  <main class="flex-1 overflow-y-auto h-screen bg-slate-50">
    <header class="h-14 border-b border-slate-200 flex items-center px-6 justify-between bg-white/90 backdrop-blur-md sticky top-0 z-10 md:hidden">
      <div class="flex items-center gap-2">
        <div class="w-2 h-2 rounded-sm bg-emerald-500"></div>
        <span class="font-bold text-slate-900 text-sm">Lab01</span>
      </div>
    </header>

    <div class="p-6 md:p-10 max-w-6xl mx-auto">
      {@render children()}
    </div>
  </main>
</div>
