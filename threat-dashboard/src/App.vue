<template>
  <div class="min-h-screen bg-cyber-dark text-cyber-text font-sans p-6 overflow-x-hidden relative">
    
    <!-- Background Accents -->
    <div class="fixed top-[-20%] left-[-10%] w-[50%] h-[50%] bg-cyber-accent opacity-5 blur-[150px] pointer-events-none z-0"></div>
    <div class="fixed bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-cyber-alert opacity-5 blur-[100px] pointer-events-none z-0"></div>
    
    <div class="max-w-7xl mx-auto relative z-10">
      
      <!-- Header -->
      <header class="mb-4 border-b border-white/10 pb-6 flex items-center justify-between">
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 rounded bg-cyber-accent/10 border border-cyber-accent flex items-center justify-center">
             <ShieldAlert class="text-cyber-accent w-6 h-6" />
          </div>
          <div>
            <h1 class="text-3xl font-bold tracking-widest text-white shadow-cyber-accent drop-shadow-lg">
              THREAT<span class="text-cyber-accent">GRAPH</span> DASHBOARD
            </h1>
            <p class="text-cyber-muted font-mono tracking-widest text-sm mt-1">SIMULATION DIAGNOSTICS & TELEMETRY</p>
          </div>
        </div>
      </header>

      <!-- Dynamic Search Header -->
      <SearchHeader 
        :is-simulating="isGlobalSimulating"
        @simulation-started="handleSimulationStart"
        @simulation-completed="handleSimulationComplete"
        @simulation-error="handleSimulationError"
      />

      <!-- Breach Probability Forecast Banner -->
      <transition enter-active-class="transition-all duration-500 ease-out" enter-from-class="opacity-0 translate-y-[-20px]" enter-to-class="opacity-100 translate-y-0">
        <div v-if="globalReport !== null && globalReport.breach_probability_score !== undefined && !isGlobalSimulating" class="mb-6 w-full relative overflow-hidden rounded-xl border border-cyber-alert/50 bg-black/60 shadow-[0_0_30px_rgba(220,38,38,0.15)] flex items-center p-6 gap-6">
          <div class="absolute inset-0 bg-gradient-to-r from-cyber-alert/20 to-transparent pointer-events-none"></div>
          
          <div class="w-16 h-16 rounded-full bg-cyber-alert/20 border-2 border-cyber-alert flex items-center justify-center shrink-0 z-10 shadow-[0_0_15px_rgba(220,38,38,0.5)]">
            <AlertTriangle class="text-cyber-alert w-8 h-8 animate-pulse" />
          </div>
          
          <div class="z-10 flex-1">
            <h2 class="text-cyber-alert font-bold tracking-widest text-sm uppercase mb-1">Breach Probability Forecast</h2>
            <div class="text-xl md:text-2xl font-mono text-white">
              <span class="font-extrabold text-cyber-alert text-3xl md:text-4xl mr-2">{{ globalReport.breach_probability_score }}%</span> 
              Probability of Compromise based on 5 Swarm Worlds
            </div>
          </div>
        </div>
      </transition>

      <!-- Main Grid Layout (Fades during loading) -->
      <main class="grid grid-cols-1 lg:grid-cols-3 gap-6 transition-opacity duration-500 mt-2" :class="{'opacity-30 pointer-events-none blur-sm grayscale': isGlobalSimulating}">
        
        <!-- Left Column (Live Feed) -->
        <div class="col-span-1 lg:col-span-2 flex flex-col gap-6">
          <LiveFeed ref="feedRef" />
          <KillChainTimeline ref="killChainRef" />
        </div>
        
        <!-- Right Column (Heatmap & Reporting) -->
        <div class="col-span-1 flex flex-col gap-6">
           <AttackHeatmap ref="heatmapRef" />
           <ReportDownload ref="downloadRef" class="flex-1" />
        </div>
        
      </main>
      
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { ShieldAlert, AlertTriangle } from 'lucide-vue-next';
import axios from 'axios';
import LiveFeed from './components/LiveFeed.vue';
import AttackHeatmap from './components/AttackHeatmap.vue';
import KillChainTimeline from './components/KillChainTimeline.vue';
import ReportDownload from './components/ReportDownload.vue';
import SearchHeader from './components/SearchHeader.vue';

// Global Simulation State
const isGlobalSimulating = ref(false);
const globalReport = ref(null);

const fetchGlobalReport = async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/report');
    if (res.data) {
      globalReport.value = res.data;
    }
  } catch (error) {
    console.warn("Could not fetch global report on load.");
  }
};

onMounted(() => {
  fetchGlobalReport();
});

const handleSimulationStart = () => {
  isGlobalSimulating.value = true;
};

const heatmapRef = ref(null);
const killChainRef = ref(null);

const handleSimulationComplete = () => {
  isGlobalSimulating.value = false;
  
  if (heatmapRef.value && typeof heatmapRef.value.fetchData === 'function') {
    heatmapRef.value.fetchData();
  }
  if (killChainRef.value && typeof killChainRef.value.fetchData === 'function') {
    killChainRef.value.fetchData();
  }
  
  fetchGlobalReport();
};

const handleSimulationError = (errorMsg) => {
  isGlobalSimulating.value = false;
  alert(`Simulation Pipeline Failed: ${errorMsg}`);
};
</script>
