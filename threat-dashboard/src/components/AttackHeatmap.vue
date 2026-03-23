<template>
  <div class="glass-panel p-6 flex flex-col h-[500px]">
    <div class="flex items-center gap-3 mb-6 border-b border-white/10 pb-4">
      <Grid class="text-cyber-accent w-6 h-6" />
      <h2 class="text-xl font-bold tracking-wider text-cyber-text">ATT&CK HEATMAP</h2>
      
      <div v-if="reportData && reportData.breach_probability_score !== undefined" class="ml-4 px-3 py-1 bg-cyber-alert/20 border border-cyber-alert/50 rounded flex items-center gap-2">
        <span class="text-xs font-mono text-cyber-alert tracking-widest">BREACH PROBABILITY:</span>
        <span class="font-bold text-cyber-alert">{{ reportData.breach_probability_score }}%</span>
      </div>

      <div v-if="!reportData" class="ml-auto flex items-center gap-2">
        <Loader2 class="w-4 h-4 animate-spin text-cyber-muted" />
        <span class="text-xs text-cyber-muted font-mono tracking-widest">LOADING</span>
      </div>
    </div>
    
    <div v-if="reportData && reportData.attack_heatmap" class="flex-1 overflow-y-auto pr-2 scrollbar-thin">
      <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
        <div v-for="t in reportData.attack_heatmap" :key="t.mitre_id"
             class="p-4 rounded border transition-all hover:scale-105 cursor-default relative overflow-hidden"
             :class="getHeatmapColor(t.success_count, t.usage_count)">
          
          <div class="relative z-10 flex flex-col h-full justify-between">
             <div class="font-mono text-sm font-bold opacity-80 mb-2">{{ t.mitre_id }}</div>
             <div class="text-sm font-semibold leading-tight line-clamp-2" :title="t.technique_name">{{ t.technique_name }}</div>
             
             <div class="mt-4 flex justify-between items-end text-xs font-mono opacity-80">
               <div>Usage: {{ t.usage_count }}</div>
               <div>Success: {{ t.success_count }}</div>
             </div>
          </div>
          
          <!-- background intensity layer based on usage -->
          <div class="absolute inset-0 z-0 opacity-20 bg-gradient-to-t from-black/60 to-transparent"></div>
        </div>
      </div>
      
      <div v-if="reportData.attack_heatmap.length === 0" class="text-center text-cyber-muted py-10 font-mono">
        NO TECHNIQUES RECORDED
      </div>
    </div>
    <div v-else-if="error" class="text-cyber-alert text-center font-mono py-10 flex flex-col items-center">
      <AlertTriangle class="w-8 h-8 mb-2 opacity-80" />
      Report Data Not Found.
      <span class="text-xs text-cyber-muted mt-2">Make sure simulation is complete and reporter.py was run.</span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { Grid, Loader2, AlertTriangle } from 'lucide-vue-next';

const reportData = ref(null);
const error = ref(false);

const getHeatmapColor = (successes, usages) => {
  if (usages === 0) return 'bg-cyber-panel border-white/10 text-cyber-muted';
  
  const ratio = successes / usages;
  if (ratio > 0.6) return 'bg-cyber-alert/20 border-cyber-alert/50 text-cyber-alert'; // High success -> Red
  if (ratio > 0) return 'bg-orange-500/20 border-orange-500/50 text-orange-400'; // Partial/Some -> Orange
  return 'bg-blue-500/20 border-blue-500/50 text-blue-400'; // Blocked/0% -> Blue
};

const fetchData = async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/report');
    if (res.data) {
      reportData.value = res.data;
      error.value = false;
    }
  } catch (e) {
    error.value = true;
  }
};

onMounted(fetchData);

defineExpose({ fetchData });
</script>
