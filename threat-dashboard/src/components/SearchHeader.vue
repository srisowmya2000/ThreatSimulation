<template>
  <div class="glass-panel w-full p-6 mb-8 mt-2 sticky top-4 z-40 border-cyan-500/30">
    
    <!-- Defensive Posture Input -->
    <div class="w-full flex flex-col gap-2 mb-6">
      <label class="text-xs uppercase tracking-wider text-green-400 font-mono font-semibold">Your Active Defenses</label>
      <textarea 
        v-model="defensivePosture"
        placeholder="e.g. CrowdStrike EDR on all endpoints, Splunk SIEM, MFA enabled, Palo Alto WAF, weekly patching cycle"
        class="w-full bg-slate-900/80 border border-slate-700 text-slate-200 rounded-lg p-3 min-h-[80px] focus:outline-none focus:border-green-500 focus:ring-1 focus:ring-green-500 transition-all font-mono resize-y"
        :disabled="isSimulating"
      ></textarea>
    </div>

    <div class="flex flex-col md:flex-row gap-4 items-end">
      
      <!-- Target URL Input -->
      <div class="w-full md:w-1/2 flex flex-col gap-2">
        <label class="text-xs uppercase tracking-wider text-cyan-400 font-mono font-semibold">Target Cyber Architecture (URL)</label>
        <div class="relative flex items-center">
          <Globe class="absolute left-3 w-5 h-5 text-gray-400" />
          <input 
            v-model="targetUrl" 
            type="text" 
            placeholder="https://example-company.com" 
            class="w-full bg-slate-900/80 border border-slate-700 text-slate-200 rounded-lg pl-10 pr-4 py-3 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 transition-all font-mono"
            :disabled="isSimulating"
          />
        </div>
      </div>

      <!-- Threat Actor Dropdown -->
      <div class="w-full md:w-1/3 flex flex-col gap-2">
        <label class="text-xs uppercase tracking-wider text-red-400 font-mono font-semibold">Adversary Profile</label>
        <div class="relative flex items-center">
          <UserX class="absolute left-3 w-5 h-5 text-gray-400" />
          <select 
            v-model="selectedActor" 
            class="w-full bg-slate-900/80 border border-slate-700 text-slate-200 rounded-lg pl-10 pr-4 py-3 focus:outline-none focus:border-red-500 focus:ring-1 focus:ring-red-500 transition-all font-mono appearance-none"
            :disabled="isSimulating"
          >
            <option v-for="actor in threatActors" :key="actor" :value="actor">
              {{ actor }}
            </option>
          </select>
          <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 text-gray-400">
            <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
          </div>
        </div>
      </div>

      <!-- Simulate Action Button -->
      <div class="w-full md:w-auto flex-grow flex items-center justify-end">
        <button 
          @click="triggerSimulation" 
          :disabled="isSimulating || !targetUrl.trim()"
          class="w-full md:w-auto relative group overflow-hidden rounded-lg px-8 py-3 bg-gradient-to-r from-red-600 to-rose-600 hover:from-red-500 hover:to-rose-500 text-white font-bold tracking-wide transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed border border-red-400/50 shadow-[0_0_15px_rgba(220,38,38,0.4)] hover:shadow-[0_0_25px_rgba(220,38,38,0.7)]"
        >
          <div class="absolute inset-0 w-full h-full bg-white/20 blur-md transform scale-x-0 group-hover:scale-x-100 transition-transform origin-left duration-500"></div>
          
          <span v-if="!isSimulating" class="relative flex items-center justify-center gap-2">
            <Crosshair class="w-5 h-5" />
            INITIATE ASSAULT
          </span>
          <span v-else class="relative flex items-center justify-center gap-2 animate-pulse">
            <Activity class="w-5 h-5 animate-spin-slow" />
            RUNNING SIMULATION...
          </span>
        </button>
      </div>

    </div>
    
    <!-- Error Handling Display -->
    <div v-if="errorMessage" class="mt-4 p-3 bg-red-900/50 border border-red-500 rounded text-red-200 text-sm font-mono text-center">
      Error: {{ errorMessage }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { Globe, UserX, Crosshair, Activity } from 'lucide-vue-next';

const emit = defineEmits(['simulation-started', 'simulation-completed', 'simulation-error']);

const props = defineProps({
  isSimulating: {
    type: Boolean,
    default: false
  }
});

const targetUrl = ref('');
const selectedActor = ref('Cl0p');
const defensivePosture = ref('');
const errorMessage = ref('');

const threatActors = [
  "Cl0p", "APT28", "APT29", "Lazarus Group", "LockBit", 
  "BlackCat", "Sandworm", "Scattered Spider", "Volt Typhoon", "BlackMatter"
];

const triggerSimulation = async () => {
  if (!targetUrl.value) return;
  
  errorMessage.value = '';
  emit('simulation-started');
  
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 300000); // 5 minutes
  
  try {
    const response = await fetch('http://localhost:8000/api/run', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        target_url: targetUrl.value,
        threat_actor: selectedActor.value,
        defensive_posture: defensivePosture.value
      }),
      signal: controller.signal
    });
    
    clearTimeout(timeoutId);
    
    if (!response.ok) {
      let errorDetail = 'Simulation API Failed';
      try {
        const errorData = await response.json();
        errorDetail = errorData.detail || errorDetail;
      } catch (parseErr) {
        const errText = await response.text();
        errorDetail = `Server Error (${response.status}): ${errText || response.statusText}`;
      }
      throw new Error(errorDetail);
    }
    
    const reportData = await response.json();
    emit('simulation-completed', reportData);
    
  } catch (error) {
    clearTimeout(timeoutId);
    console.error("Simulation Error:", error);
    if (error.name === 'AbortError') {
      errorMessage.value = 'Simulation timed out after 5 minutes. The backend pipeline is likely still running.';
      emit('simulation-error', errorMessage.value);
    } else {
      errorMessage.value = error.message;
      emit('simulation-error', error.message);
    }
  }
};
</script>
