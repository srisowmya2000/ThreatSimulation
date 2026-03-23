<template>
  <div class="glass-panel p-6 h-[400px] flex flex-col">
    <div class="flex items-center gap-3 mb-6 border-b border-white/10 pb-4">
      <FastForward class="text-cyber-accent w-6 h-6" />
      <h2 class="text-xl font-bold tracking-wider text-cyber-text">KILL CHAIN TIMELINE</h2>
    </div>
    
    <div class="flex-1 overflow-x-auto overflow-y-hidden pb-4 scrollbar-thin flex items-center px-4" v-if="reportData?.kill_chain_timeline">
      <div class="flex items-center relative min-w-max h-full">
        <!-- Connecting Line -->
        <div class="absolute top-1/2 left-0 right-0 h-1 bg-white/10 -translate-y-1/2 rounded-full z-0"></div>
        
        <div v-for="(event, i) in reportData.kill_chain_timeline" :key="i" class="relative z-10 flex flex-col items-center mx-8 w-48 shrink-0 group">
          
          <!-- Node -->
          <div class="w-8 h-8 rounded-full border-2 border-cyber-accent bg-cyber-dark flex items-center justify-center font-mono text-xs text-cyber-accent shadow-[0_0_15px_rgba(0,240,255,0.5)] transition-all group-hover:scale-125 group-hover:bg-cyber-accent group-hover:text-black">
            {{ event.step }}
          </div>
          
          <!-- Data Top/Bottom alternation -->
          <div :class="['absolute w-48 text-center transition-all opacity-70 group-hover:opacity-100', i % 2 === 0 ? 'bottom-12' : 'top-12']">
             <div class="text-[10px] font-mono text-cyber-muted mb-1">{{ new Date(event.timestamp).toLocaleTimeString() }}</div>
             <div class="font-bold text-xs"
               :class="{
                  'text-cyber-alert': event.agent.includes('Attacker') || event.agent.includes('Threat'),
                  'text-blue-500': event.agent.includes('Defender'),
                  'text-cyber-accent': event.agent.includes('Environment')
               }">
               {{ event.agent }}
             </div>
             <div class="text-xs text-white/80 line-clamp-3 mt-1">{{ event.action_summary }}</div>
          </div>
          
        </div>
      </div>
    </div>
    <div v-else class="m-auto text-cyber-muted font-mono flex items-center justify-center align-middle w-full h-full pb-10">
      WAITING FOR REPORT DATA...
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { FastForward } from 'lucide-vue-next';

const reportData = ref(null);

const fetchData = async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/report');
    if (res.data) {
      reportData.value = res.data;
    }
  } catch (e) {
    // silently fail, layout handles null state
  }
};

onMounted(fetchData);

defineExpose({ fetchData });
</script>
