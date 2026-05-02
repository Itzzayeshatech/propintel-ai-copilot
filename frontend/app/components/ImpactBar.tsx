"use client";

export default function ImpactBar() {
  return (
    <div className="fixed bottom-0 left-0 right-0 z-50 bg-slate-800 border-t border-slate-700 shadow-2xl p-4">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between text-sm">
        <span className="font-bold text-slate-100 flex items-center gap-2 mb-2 md:mb-0">
          📊 Impact of PropIntel AI <span className="text-slate-400 font-normal">(vs. Traditional Underwriting):</span>
        </span>
        <div className="flex flex-wrap justify-center gap-6 text-slate-300">
          <span>Overvaluation: <span className="line-through opacity-50">22%</span> <strong className="text-emerald-400">→ 6%</strong></span>
          <span className="hidden md:inline text-slate-600">|</span>
          <span>Defaults: <span className="line-through opacity-50">4.2%</span> <strong className="text-emerald-400">→ 2.8%</strong></span>
          <span className="hidden md:inline text-slate-600">|</span>
          <span>Recovery: <span className="line-through opacity-50">14mo</span> <strong className="text-emerald-400">→ 8mo</strong></span>
          <span className="hidden md:inline text-slate-600">|</span>
          <span>ROI: <span className="line-through opacity-50">8.2%</span> <strong className="text-emerald-400">→ 11.6%</strong></span>
        </div>
      </div>
    </div>
  );
}
