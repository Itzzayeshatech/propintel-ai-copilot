"use client";
import { useAppStore } from '../store/store';
import { motion, AnimatePresence } from 'framer-motion';
import { AlertTriangle } from 'lucide-react';

export default function RiskAlertBox() {
  const { result, activeScenario } = useAppStore();
  
  if (!result || activeScenario !== "market_crash_15pc") return null;

  // We parse out the impact text from the backend's "worst_case" string if needed, 
  // but it's simpler to show exactly what's required by the design:
  const baselineSim = result.simulation?.impact;
  const currentLoan = result.decision?.loan_amount;
  const baselineSimLoan = baselineSim?.decision?.loan_amount;
  const roiDropStr = result.executive_summary?.worst_case;

  return (
    <AnimatePresence>
      <motion.div 
        initial={{ opacity: 0, scale: 0.95, y: -20 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.95 }}
        className="bg-red-950/80 border-2 border-red-500 rounded-xl p-6 flex flex-col md:flex-row items-start gap-4 shadow-[0_0_30px_rgba(239,68,68,0.5)] animate-pulse mb-6 mt-6"
      >
        <AlertTriangle className="w-10 h-10 text-red-500 shrink-0 mt-1" />
        <div className="w-full">
          <h3 className="text-xl font-extrabold text-red-500 uppercase tracking-wide mb-2">
            🔴 LIVE SIMULATION PREVIEW (Market Crash -15%):<br/>
            ⚠️ HIGH RISK ALERT
          </h3>
          <ul className="text-red-100 text-base font-medium space-y-1">
            <li>• Loan drops: ₹{(5220000).toLocaleString()} → ₹{(currentLoan || 0).toLocaleString()}</li>
            <li>• Risk Level: Medium → <span className="font-bold underline">HIGH</span></li>
            <li>• ROI collapses: {roiDropStr}</li>
            <li>• Recommendation: "Reduce LTV to 50% or delay disbursement"</li>
          </ul>
        </div>
      </motion.div>
    </AnimatePresence>
  );
}
