"use client";
import { useAppStore } from '../store/store';
import { motion, AnimatePresence } from 'framer-motion';
import { useState } from 'react';
import { Brain, ChevronDown, ChevronUp } from 'lucide-react';

export default function ExplainabilityBox() {
  const { result } = useAppStore();
  const [isOpen, setIsOpen] = useState(false);

  if (!result) return null;

  // Ideally the API would return an array, but if it returns a string we can just split or show it directly.
  const explanation = result.executive_summary?.one_line; 
  // Let's create bullet points from the data structure, since the API doesn't give us perfectly formatted bullets by default.
  
  return (
    <div className="bg-slate-800 rounded-xl border border-slate-700 shadow-xl overflow-hidden">
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="w-full p-5 flex items-center justify-between text-left hover:bg-slate-700/50 transition-colors"
      >
        <span className="font-semibold text-slate-100 flex items-center gap-2">
          <Brain className="w-5 h-5 text-indigo-400" />
          Why This Decision? (Explainable AI)
        </span>
        {isOpen ? <ChevronUp className="w-5 h-5 text-slate-400" /> : <ChevronDown className="w-5 h-5 text-slate-400" />}
      </button>
      
      <AnimatePresence>
        {isOpen && (
          <motion.div 
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="border-t border-slate-700 bg-slate-900/50"
          >
            <div className="p-5 space-y-3 text-sm text-slate-300">
              <ul className="list-disc pl-5 space-y-2">
                <li>Loan adjusted to {result.decision.ltv * 100}% LTV to safeguard against liquidity limits ({result.valuation.liquidity_days} days to liquidate).</li>
                <li>Interest rate locked at {result.decision.interest_rate}%: Derived mathematically from base + risk premiums for a {result.risk.risk_level} asset.</li>
                <li>{explanation}</li>
                <li>Recovery recommendation generated as "{result.recovery.strategy}" securing a projected {result.roi.annualized_roi}% ROI trajectory.</li>
              </ul>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
