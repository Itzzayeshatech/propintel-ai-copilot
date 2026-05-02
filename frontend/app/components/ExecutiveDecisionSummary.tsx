"use client";
import { useAppStore } from '../store/store';
import { motion } from 'framer-motion';
import CountUp from 'react-countup';

export default function ExecutiveDecisionSummary() {
  const { result, activeScenario } = useAppStore();
  if (!result) return null;

  const roi = result.roi?.annualized_roi || 0;
  const isDanger = activeScenario === 'market_crash_15pc' || roi < 0;

  return (
    <motion.div 
      initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }}
      className="bg-slate-800 rounded-xl p-8 border border-slate-700 flex flex-col justify-center relative overflow-hidden"
    >
      <div className="mb-6">
        <p className="text-xl font-medium text-slate-100">
          {result.executive_summary?.one_line}
        </p>
      </div>
      
      <span className="text-sm font-medium text-slate-400 uppercase tracking-wider mb-2">
        Risk-Adjusted ROI (Ann.)
      </span>
      <div className="flex items-baseline gap-2">
        <span className={`text-5xl font-bold ${isDanger ? 'text-red-400' : 'text-emerald-400'}`}>
          <CountUp end={roi} decimals={1} duration={1.5} suffix="%" />
        </span>
      </div>
      <p className="text-xs text-slate-500 mt-4">
        Hero Metric calculated over a 3-year term.
      </p>
    </motion.div>
  );
}
