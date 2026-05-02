"use client";
import { useAppStore } from '../store/store';
import { Activity } from 'lucide-react';

export default function SimulationPanel() {
  const { activeScenario, evaluateAsset, loading } = useAppStore();

  return (
    <div className="bg-slate-800 rounded-xl p-6 border border-slate-700 shadow-xl mt-6">
      <h3 className="text-lg font-semibold mb-4 text-slate-100 flex items-center gap-2">
        <Activity className="w-5 h-5 text-indigo-400" /> Future Risk Simulation
      </h3>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <button 
          onClick={() => evaluateAsset("normal")}
          disabled={loading}
          className={`p-4 rounded-lg border text-left transition-all ${
            activeScenario === 'normal' ? 'bg-slate-700 border-slate-500' : 'bg-slate-900 border-slate-700 hover:border-slate-500 hover:bg-slate-800'
          }`}
        >
          <span className="block font-semibold mb-1 text-slate-200">Baseline</span>
          <span className="text-xs text-slate-400">Current market conditions</span>
        </button>
        
        <button 
          onClick={() => evaluateAsset("market_crash_15pc")}
          disabled={loading}
          className={`p-4 rounded-lg border text-left transition-all relative overflow-hidden ${
            activeScenario === 'market_crash_15pc' ? 'bg-red-900/50 border-red-500' : 'bg-slate-900 border-slate-700 hover:border-red-500 hover:bg-red-950/30'
          }`}
        >
          <span className="block font-semibold mb-1 text-red-400">Market Crash</span>
          <span className="text-xs text-slate-400">-15% property value drop</span>
        </button>
        
        <button 
          onClick={() => evaluateAsset("demand_drop")}
          disabled={loading}
          className={`p-4 rounded-lg border text-left transition-all ${
            activeScenario === 'demand_drop' ? 'bg-orange-900/50 border-orange-500' : 'bg-slate-900 border-slate-700 hover:border-orange-500 hover:bg-orange-950/30'
          }`}
        >
          <span className="block font-semibold mb-1 text-orange-400">Demand Drop</span>
          <span className="text-xs text-slate-400">Liquidity days x2</span>
        </button>
      </div>
    </div>
  );
}
