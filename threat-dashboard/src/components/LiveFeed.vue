<template>
  <div class="glass-panel p-6 h-[500px] flex flex-col">
    <div class="flex items-center gap-3 mb-4 border-b border-white/10 pb-4">
      <Activity class="text-cyber-accent w-6 h-6" />
      <h2 class="text-xl font-bold tracking-wider text-cyber-text">LIVE EXPLOIT FEED</h2>
      
      <div class="ml-auto flex items-center gap-2">
        <span class="relative flex h-3 w-3">
          <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyber-alert opacity-75"></span>
          <span class="relative inline-flex rounded-full h-3 w-3 bg-cyber-alert"></span>
        </span>
        <span class="text-xs text-cyber-muted font-mono tracking-widest">MONITORING</span>
      </div>
    </div>
    
    <div class="flex-1 overflow-y-auto pr-2 space-y-4 font-mono text-sm scrollbar-thin scrollbar-thumb-white/20" ref="feedContainer">
      <div v-if="logs.length === 0" class="text-center text-cyber-muted py-10">
        Waiting for simulation events...
      </div>
      
      <transition-group name="list">
        <div v-for="(log, idx) in logs" :key="idx" 
             class="p-3 rounded bg-black/40 border-l-2 transition-all"
             :class="{
               'border-cyber-alert': log.agent.includes('Attacker') || log.agent.includes('Threat'),
               'border-blue-500': log.agent.includes('Defender'),
               'border-cyber-muted': log.agent.includes('Environment')
             }">
          <div class="flex justify-between items-start mb-1 text-xs text-cyber-muted">
            <span>{{ new Date(log.timestamp).toLocaleTimeString() }} | STEP {{ log.step }}</span>
            <span class="font-bold tracking-wide"
                  :class="{
                    'text-cyber-alert': log.agent.includes('Attacker') || log.agent.includes('Threat'),
                    'text-blue-500': log.agent.includes('Defender'),
                    'text-cyber-accent': log.agent.includes('Environment')
                  }">
              {{ log.agent.toUpperCase() }}
            </span>
          </div>
          <div class="text-cyber-text font-semibold mb-1">{{ log.action.toUpperCase() }}</div>
          <p class="whitespace-pre-wrap text-white/70">{{ log.details }}</p>
          
          <div v-if="log.mitre_attack_ids?.length" class="mt-2 flex gap-2 flex-wrap">
            <span v-for="id in log.mitre_attack_ids" :key="id" 
                  class="px-2 py-0.5 bg-cyber-alert/20 text-cyber-alert border border-cyber-alert/30 rounded text-xs font-bold">
              {{ id }}
            </span>
          </div>
        </div>
      </transition-group>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue';
import axios from 'axios';
import { Activity } from 'lucide-vue-next';

const logs = ref([]);
const feedContainer = ref(null);
let pollInterval;

const fetchLogs = async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/logs');
    if (res.data) {
      const isNewData = res.data.length !== logs.value.length;
      logs.value = res.data;
      
      if (isNewData) {
        // Auto-scroll to bottom only if new data
        nextTick(() => {
          if (feedContainer.value) {
            feedContainer.value.scrollTop = feedContainer.value.scrollHeight;
          }
        });
      }
    }
  } catch (error) {
    console.warn("Failed to fetch logs. Backend might be offline.");
  }
};

onMounted(() => {
  fetchLogs();
  pollInterval = setInterval(fetchLogs, 2000); // Poll every 2s
});

onUnmounted(() => {
  if (pollInterval) clearInterval(pollInterval);
});
</script>

<style scoped>
.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}
.list-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}
.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
/* Scrollbar styles */
::-webkit-scrollbar {
  width: 6px;
}
::-webkit-scrollbar-track {
  background: rgba(0,0,0,0.2); 
}
::-webkit-scrollbar-thumb {
  background: rgba(255,255,255,0.1); 
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 240, 255, 0.4); 
}
</style>
