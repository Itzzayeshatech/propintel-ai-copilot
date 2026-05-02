"use client";
import { useAppStore } from '../store/store';
import { DollarSign, TrendingDown, Clock, Activity } from 'lucide-react';
import { motion } from 'framer-motion';

export default function ValuationCard() {
  const { result } = useAppStore();
  if (!result) return null;

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
      className="bg-slate-800 rounded-xl p-6 border border-slate-700 shadow-xl mt-6 w-full"
    >
      <h3 className="text-lg font-semibold mb-4 text-slate-200 flex items-center gap-2">
        <Activity className="w-5 h-5 text-slate-400" /> Valuation Metrics
      </h3>
      <div className="space-y-4">
        <div className="flex justify-between items-center">
          <span className="text-sm text-slate-400 flex items-center gap-1"><DollarSign className="w-4 h-4" /> Market Value</span>
          <span className="font-mono text-xl font-bold text-emerald-400">
            ₹{(result.valuation?.market_value || 0).toLocaleString()}
          </span>
        </div>
        <div className="flex justify-between items-center">
          <span className="text-sm text-red-300 flex items-center gap-1"><TrendingDown className="w-4 h-4" /> Distress Value (-25%)</span>
          <span className="font-mono text-base font-medium text-slate-300">
            ₹{(result.valuation?.distress_value || 0).toLocaleString()}
          </span>
        </div>
        <div className="pt-4 border-t border-slate-700 flex justify-between items-center">
          <span className="text-sm text-slate-400 flex items-center gap-1"><Clock className="w-4 h-4" /> Liquidity Timeline</span>
          <span className="bg-slate-700 px-3 py-1 rounded-full text-xs font-medium text-slate-300">
            {result.valuation?.liquidity_days || 0} Days
          </span>
        </div>
      </div>
    </motion.div>
  );
}
