<script lang="ts">
  import '../app.css';
  import { LayoutDashboard, Target, GitPullRequest, GitMerge, Settings } from 'lucide-svelte';
  
  let { children } = $props();
</script>

<div class="flex min-h-screen bg-zinc-950 text-zinc-300 overflow-hidden">
  <!-- Sidebar -->
  <aside class="w-64 border-r border-zinc-800 bg-zinc-950 flex flex-col hidden md:flex shrink-0 h-screen sticky top-0">
    <div class="p-6 border-b border-zinc-800">
      <div class="font-semibold text-zinc-100 flex items-center gap-2">
        <div class="w-2 h-2 rounded-sm bg-emerald-500"></div>
        Lab01 
      </div>
      <p class="text-xs text-zinc-500 mt-1">Dados & Análises</p>
    </div>
    
    <nav class="flex-1 p-4 space-y-1 overflow-y-auto">
      <div class="text-[10px] font-semibold text-zinc-600 uppercase tracking-widest mb-3 mt-2 px-2">Navegação</div>
      
      <a href="#overview" class="flex items-center gap-3 px-3 py-2 text-sm text-zinc-100 bg-zinc-900 rounded-md font-medium">
        <LayoutDashboard size={16} class="text-emerald-500" />
        Visão Geral
      </a>
      <a href="#rq01-04" class="flex items-center gap-3 px-3 py-2 text-sm text-zinc-400 hover:text-zinc-200 hover:bg-zinc-900/50 rounded-md transition-colors">
        <Target size={16} />
        Métricas de Maturidade
      </a>
      <a href="#rq05-06" class="flex items-center gap-3 px-3 py-2 text-sm text-zinc-400 hover:text-zinc-200 hover:bg-zinc-900/50 rounded-md transition-colors">
        <GitPullRequest size={16} />
        Linguagens & Issues
      </a>
      <a href="#rq07" class="flex items-center gap-3 px-3 py-2 text-sm text-zinc-400 hover:text-zinc-200 hover:bg-zinc-900/50 rounded-md transition-colors">
        <GitMerge size={16} />
        Cruzamento (RQ07)
      </a>
    </nav>
  </aside>

  <!-- Main Content -->
  <main class="flex-1 overflow-y-auto h-screen bg-zinc-950">
    <!-- Top Header (mobile fallback) -->
    <header class="h-14 border-b border-zinc-800 flex items-center px-6 justify-between bg-zinc-950/90 backdrop-blur-md sticky top-0 z-10 md:hidden">
      <div class="flex items-center gap-2">
        <div class="w-2 h-2 rounded-sm bg-emerald-500"></div>
        <span class="font-semibold text-zinc-100 text-sm">Lab01</span>
      </div>
    </header>

    <div class="p-6 md:p-10 max-w-6xl mx-auto">
      {@render children()}
    </div>
  </main>
</div>
