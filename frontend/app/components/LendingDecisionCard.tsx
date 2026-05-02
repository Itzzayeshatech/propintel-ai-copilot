"use client";
import { useAppStore } from '../store/store';
import { motion } from 'framer-motion';

export default function LendingDecisionCard() {
  const { result } = useAppStore();
  if (!result) return null;

  const isApproved = result.decision?.decision?.includes("APPROVED");

  return (
    <motion.div 
      initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.1 }}
      className="bg-slate-800 rounded-xl p-8 border border-slate-700 h-full flex flex-col justify-center"
    >
      <div className="flex justify-between items-start mb-6">
        <span className="text-sm font-medium text-slate-400 uppercase tracking-wider mb-2">Lending Decision</span>
        <span className={`px-3 py-1 rounded-full text-xs font-bold ${
          isApproved ? (result.decision.decision.includes("CAUTION") ? "bg-yellow-500/20 text-yellow-400" : "bg-emerald-500/20 text-emerald-400") 
          : "bg-red-500/20 text-red-400"
        }`}>
          {result?.decision?.decision}
        </span>
      </div>
      
      <div className="space-y-4">
        <div>
          <span className="block text-xs text-slate-400 mb-1">Approved Loan Amount</span>
          <span className="text-3xl font-mono font-semibold text-slate-100">
            ₹{(result?.decision?.loan_amount || 0).toLocaleString()}
          </span>
        </div>
        <div className="flex justify-between items-center bg-slate-900 rounded-lg p-4 border border-slate-700 mt-6">
          <div>
            <span className="block text-xs text-slate-400">LTV Applied</span>
            <span className="font-semibold text-lg text-slate-200">{(result?.decision?.ltv * 100 || 0).toFixed(0)}%</span>
          </div>
          <div className="text-right">
            <span className="block text-xs text-slate-400">Risk-Based Rate</span>
            <span className="font-semibold text-lg text-blue-400">{result?.decision?.interest_rate || 0}%</span>
          </div>
          <div className="text-right">
            <span className="block text-xs text-slate-400">Risk Assessed</span>
            <span className="bg-yellow-500/20 text-yellow-300 px-2 py-0.5 rounded text-xs font-bold uppercase">{result?.risk?.risk_level}</span>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
