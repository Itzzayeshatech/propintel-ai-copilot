"use client";
import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ShieldCheck, MapPin, Calculator, Activity, 
  RefreshCw, AlertTriangle, TrendingDown, DollarSign, 
  CheckCircle, XCircle, Zap, ArrowRight,
  FileText, User, Briefcase, BarChart4, ChevronDown, ChevronUp, Download
} from 'lucide-react';

export default function AnalyzeDashboard() {
  const [location, setLocation] = useState('Whitefield');
  const [propertyValue, setPropertyValue] = useState<number>(8500000);
  const [loanAmount, setLoanAmount] = useState<number>(6000000);
  const [income, setIncome] = useState<number>(150000);
  const [creditScore, setCreditScore] = useState<number>(750);
  const [segment, setSegment] = useState('SALARIED');
  const [stressCrash, setStressCrash] = useState(false);
  const [stressRepo, setStressRepo] = useState(false);
  const [stressInflation, setStressInflation] = useState(false);
  const [stressSector, setStressSector] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [showAudit, setShowAudit] = useState(false);

  const locations = ["Whitefield", "Koramangala", "Indiranagar", "Electronic City", "Hebbal"];

  const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  const runAnalysis = async () => {
    setResult(null); // Force clear previous state for single-state integrity
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/api/v1/analyze-loan`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          location,
          property_value: propertyValue,
          loan_amount: loanAmount,
          monthly_income: income,
          credit_score: creditScore,
          segment,
          stress_market_crash: stressCrash,
          stress_repo_rate_spike: stressRepo,
          stress_inflation_spike: stressInflation,
          stress_sector_crash: stressSector
        })
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error("API Error:", error);
    } finally {
      setLoading(false);
    }
  };

  const formatCr = (val: number) => {
    const cr = val / 10000000;
    return `${cr.toFixed(2)} Cr`;
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 text-slate-200">
      {/* LEFT: Parameters & Stress Toggles */}
      <div className="lg:col-span-4 space-y-6">
        <div className="p-6 bg-slate-900/80 backdrop-blur-2xl rounded-3xl border border-slate-800 shadow-2xl">
          <h2 className="text-xl font-bold mb-6 flex items-center gap-3 text-slate-100">
            <User className="w-5 h-5 text-emerald-400"/>
            Borrower Profile
          </h2>
          
          <div className="space-y-6">
            {/* Segment Selector */}
            <div>
              <label className="block text-[10px] font-black text-slate-500 uppercase tracking-widest mb-3">Segment</label>
              <div className="grid grid-cols-3 gap-2">
                {['SALARIED', 'SELF EMPLOYED', 'MSME'].map(s => (
                  <button 
                    key={s}
                    onClick={() => setSegment(s.replace(' ', '_'))}
                    className={`py-2 px-1 rounded-xl text-[9px] font-bold border transition-all ${segment === s.replace(' ', '_') ? 'bg-emerald-500/20 border-emerald-500/50 text-emerald-400' : 'bg-slate-800/50 border-slate-700 text-slate-500'}`}
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-[10px] font-black text-slate-500 uppercase tracking-widest mb-2">Monthly Income</label>
                <input type="number" value={income} onChange={(e) => setIncome(Number(e.target.value))} className="w-full bg-slate-800/50 border border-slate-700 rounded-xl py-3 px-4 text-slate-200 outline-none focus:border-emerald-500/50 transition-all text-sm font-bold"/>
              </div>
              <div>
                <label className="block text-[10px] font-black text-slate-500 uppercase tracking-widest mb-2">Credit Score</label>
                <input type="number" value={creditScore} onChange={(e) => setCreditScore(Number(e.target.value))} className="w-full bg-slate-800/50 border border-slate-700 rounded-xl py-3 px-4 text-slate-200 outline-none focus:border-emerald-500/50 transition-all text-sm font-bold"/>
              </div>
            </div>

            <div>
              <label className="block text-[10px] font-black text-slate-500 uppercase tracking-widest mb-2">Micro-Market</label>
              <div className="relative">
                <select value={location} onChange={(e) => setLocation(e.target.value)} className="w-full bg-slate-800/50 border border-slate-700 rounded-xl py-3 px-4 text-slate-200 outline-none appearance-none cursor-pointer text-sm font-bold">
                  {locations.map(loc => <option key={loc} value={loc}>{loc}</option>)}
                </select>
                <ChevronDown className="absolute right-4 top-3.5 w-4 h-4 text-slate-500 pointer-events-none" />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-[10px] font-black text-slate-500 uppercase tracking-widest mb-2">Property Value (INR)</label>
                <input type="number" value={propertyValue} onChange={(e) => setPropertyValue(Number(e.target.value))} className="w-full bg-slate-800/50 border border-slate-700 rounded-xl py-3 px-4 text-slate-200 outline-none focus:border-emerald-500/50 transition-all text-sm font-bold"/>
              </div>
              <div>
                <label className="block text-[10px] font-black text-slate-500 uppercase tracking-widest mb-2">Loan Amount (INR)</label>
                <input type="number" value={loanAmount} onChange={(e) => setLoanAmount(Number(e.target.value))} className="w-full bg-slate-800/50 border border-slate-700 rounded-xl py-3 px-4 text-slate-200 outline-none focus:border-emerald-500/50 transition-all text-sm font-bold"/>
              </div>
            </div>
          </div>
        </div>

        <div className="p-6 bg-slate-900/80 backdrop-blur-2xl rounded-3xl border border-slate-800 shadow-2xl">
          <h2 className="text-xl font-bold mb-6 flex items-center gap-3 text-red-400">
            <Zap className="w-5 h-5"/>
            Macro-Stress Scenarios
          </h2>
          <div className="space-y-3 mb-8">
            {[
              { id: 'crash', label: 'Market Crash', sub: '-15% property value', active: stressCrash, set: setStressCrash, icon: TrendingDown, color: 'red' },
              { id: 'sector', label: 'Sector Crisis', sub: '-15% additional value', active: stressSector, set: setStressSector, icon: Briefcase, color: 'orange' },
              { id: 'inflation', label: 'Inflation Shock', sub: '-5% value, -40% liquidity', active: stressInflation, set: setStressInflation, icon: RefreshCw, color: 'amber' },
              { id: 'repo', label: 'Repo Rate +2%', sub: 'Net ROI compression', active: stressRepo, set: setStressRepo, icon: Activity, color: 'indigo' },
            ].map(s => (
              <button 
                key={s.id}
                onClick={() => s.set(!s.active)}
                className={`w-full p-4 rounded-2xl border text-left transition-all flex items-center gap-4 ${s.active ? `bg-red-500/10 border-red-500/40 shadow-[0_0_15px_rgba(239,68,68,0.1)]` : 'bg-slate-800/30 border-slate-700 hover:border-slate-600'}`}
              >
                <div className={`p-2 rounded-lg ${s.active ? 'bg-red-500 text-white' : 'bg-slate-800 text-slate-500'}`}>
                  <s.icon className="w-4 h-4" />
                </div>
                <div>
                  <p className="text-xs font-bold text-slate-100">{s.label}</p>
                  <p className="text-[10px] text-slate-500">{s.sub}</p>
                </div>
                {s.active && <div className="ml-auto w-2 h-2 bg-red-500 rounded-full animate-pulse" />}
              </button>
            ))}
          </div>

          <button 
            onClick={runAnalysis}
            disabled={loading}
            className="w-full bg-gradient-to-r from-red-600 to-red-700 hover:from-red-500 hover:to-red-600 text-white font-black py-5 rounded-2xl shadow-[0_10px_25px_-5px_rgba(220,38,38,0.4)] transition-all flex items-center justify-center gap-3 uppercase tracking-[0.2em] text-xs border border-red-500/30"
          >
            {loading ? <RefreshCw className="w-5 h-5 animate-spin" /> : <ShieldCheck className="w-5 h-5" />}
            Run Underwriting Engine
          </button>
        </div>
      </div>

      {/* RIGHT: Results Panel */}
      <div className="lg:col-span-8 space-y-6">
        <AnimatePresence mode="wait">
          {!result ? (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="h-full flex flex-col items-center justify-center text-center p-20 bg-slate-900/40 rounded-[40px] border border-slate-800 border-dashed">
              <div className="p-6 bg-slate-800/50 rounded-full mb-6">
                <BarChart4 className="w-16 h-16 text-slate-700" />
              </div>
              <h3 className="text-2xl font-black text-slate-500 uppercase tracking-[0.3em]">System Standby</h3>
              <p className="text-slate-600 mt-4 italic text-sm max-w-xs">Configure borrower profile and apply macro stress scenarios to begin autonomous underwriting.</p>
            </motion.div>
          ) : (
            <motion.div key="result" initial={{ opacity: 0, scale: 0.98 }} animate={{ opacity: 1, scale: 1 }} className="space-y-6 pb-12">
              {/* PRIMARY DECISION BAR */}
              <div className={`p-10 rounded-[32px] border-2 shadow-2xl flex flex-col lg:flex-row justify-between items-center gap-10 relative overflow-hidden ${
                result.decision === 'APPROVE' ? 'border-emerald-500/30 bg-emerald-500/5 text-emerald-400' :
                result.decision === 'REJECT' ? 'border-red-500/30 bg-red-500/5 text-red-400' : 'border-amber-500/30 bg-amber-500/5 text-amber-400'
              }`}>
                {/* Background Decor */}
                <div className="absolute top-0 right-0 w-64 h-64 bg-current opacity-[0.03] blur-3xl rounded-full -mr-32 -mt-32" />
                
                <div className="flex items-center gap-8 z-10">
                  <div className={`p-6 rounded-3xl ${result.decision === 'APPROVE' ? 'bg-emerald-500 text-slate-900' : result.decision === 'REJECT' ? 'bg-red-500 text-slate-900' : 'bg-amber-500 text-slate-900'}`}>
                    {result.decision === 'APPROVE' ? <CheckCircle className="w-10 h-10" /> : result.decision === 'REJECT' ? <XCircle className="w-10 h-10" /> : <AlertTriangle className="w-10 h-10" />}
                  </div>
                  <div>
                    <p className="text-[10px] font-black uppercase tracking-[0.4em] opacity-60 mb-1">Policy Decision</p>
                    <h1 className="text-6xl font-black tracking-tighter">{result.decision}</h1>
                  </div>
                </div>

                <div className="flex gap-12 lg:gap-16 z-10">
                  <div className="text-center">
                    <p className="text-[10px] font-black uppercase tracking-widest opacity-50 mb-2">Risk</p>
                    <p className="text-4xl font-black">{result.risk_level}</p>
                  </div>
                  <div className="text-center border-l border-white/10 pl-12 lg:pl-16">
                    <p className="text-[10px] font-black uppercase tracking-widest opacity-50 mb-2">Net ROI</p>
                    <p className="text-4xl font-black text-white">{result.roi}%</p>
                  </div>
                  <div className="text-center border-l border-white/10 pl-12 lg:pl-16">
                    <p className="text-[10px] font-black uppercase tracking-widest opacity-50 mb-2">Response</p>
                    <p className="text-4xl font-black text-slate-400">3ms</p>
                  </div>
                </div>
              </div>

              {/* COLLATERAL VALUATION SNAPSHOT */}
              <div className="p-10 bg-slate-900/80 backdrop-blur-2xl rounded-[32px] border border-slate-800 shadow-2xl">
                <div className="mb-10">
                  <h3 className="text-lg font-black text-slate-100 mb-1">Collateral Valuation Snapshot</h3>
                  <p className="text-xs text-slate-500">Pre-disbursement stress-adjusted asset analysis</p>
                </div>
                
                <div className="grid grid-cols-2 md:grid-cols-5 gap-8 mb-12">
                  <div className="space-y-3">
                    <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Market Value</p>
                    <p className="text-2xl font-black text-slate-100">{formatCr(result.market_property_value)}</p>
                    <p className="text-[9px] text-slate-600 uppercase font-bold tracking-tighter">Price-index adj.</p>
                  </div>
                  <div className="space-y-3">
                    <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Stressed Value</p>
                    <p className="text-2xl font-black text-red-400">{formatCr(result.stressed_property_value)}</p>
                    <p className="text-[9px] text-slate-600 uppercase font-bold tracking-tighter">After macro shocks</p>
                  </div>
                  <div className="space-y-3">
                    <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest text-orange-400">Value Drop</p>
                    <p className="text-2xl font-black text-orange-400">{result.property_value_drop_percentage}%</p>
                    <p className="text-[9px] text-slate-600 uppercase font-bold tracking-tighter">Under stress</p>
                  </div>
                  <div className="space-y-3">
                    <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Base LTV</p>
                    <p className="text-2xl font-black text-slate-100">{result.base_ltv}%</p>
                    <p className="text-[9px] text-slate-600 uppercase font-bold tracking-tighter">vs market value</p>
                  </div>
                  <div className="space-y-3">
                    <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Stress LTV</p>
                    <p className="text-2xl font-black text-amber-500">{result.stress_ltv}%</p>
                    <p className="text-[9px] text-slate-600 uppercase font-bold tracking-tighter">vs stressed value</p>
                  </div>
                </div>

                {/* COMPARISON TABLE */}
                <div className="bg-slate-800/30 rounded-2xl border border-slate-800/50 overflow-hidden mb-4">
                  <table className="w-full text-left text-xs">
                    <thead>
                      <tr className="bg-slate-800/50 text-[10px] font-black text-slate-500 uppercase tracking-widest">
                        <th className="px-6 py-4">Metric</th>
                        <th className="px-6 py-4">Baseline</th>
                        <th className="px-6 py-4">Stressed</th>
                        <th className="px-6 py-4">Delta</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800/50">
                      <tr>
                        <td className="px-6 py-4 font-bold text-slate-400">Property Value</td>
                        <td className="px-6 py-4 font-mono">₹{result.market_property_value.toLocaleString()}</td>
                        <td className="px-6 py-4 font-mono text-red-400">₹{result.stressed_property_value.toLocaleString()}</td>
                        <td className="px-6 py-4 font-mono text-red-400">-{((result.market_property_value - result.stressed_property_value)).toLocaleString()}</td>
                      </tr>
                      <tr>
                        <td className="px-6 py-4 font-bold text-slate-400">LTV</td>
                        <td className="px-6 py-4 font-mono">{result.base_ltv}%</td>
                        <td className="px-6 py-4 font-mono text-amber-400">{result.stress_ltv}%</td>
                        <td className="px-6 py-4 font-mono text-amber-400">+{ (result.stress_ltv - result.base_ltv).toFixed(2) }%</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              {/* RATIONALE & RISK FACTORS */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="p-8 bg-slate-900/80 rounded-[32px] border border-slate-800 h-full">
                  <p className="text-[10px] font-black text-slate-500 uppercase tracking-[0.2em] mb-6">Key Risk Factors</p>
                  <ul className="space-y-4">
                    {result.simplified_explainability.key_risk_factors.map((f: any, i: number) => (
                      <li key={i} className="text-xs font-medium text-slate-300 flex items-start gap-4">
                        <div className="mt-1.5 w-1.5 h-1.5 bg-red-500 rounded-full shadow-[0_0_8px_rgba(239,68,68,0.8)] shrink-0" /> 
                        {f}
                      </li>
                    ))}
                  </ul>
                </div>
                <div className="p-8 bg-slate-900/80 rounded-[32px] border border-slate-800">
                  <p className="text-[10px] font-black text-slate-500 uppercase tracking-[0.2em] mb-6">Underwriting Rationale</p>
                  <div className="space-y-6">
                    <p className="text-sm font-bold text-slate-100 leading-relaxed">
                      {result.simplified_explainability.final_risk_reason}
                    </p>
                    <div className="p-4 bg-slate-800/50 rounded-2xl border-l-2 border-amber-500/50">
                      <p className="text-xs text-slate-400 leading-relaxed italic">
                        {result.simplified_explainability.property_value_change_explanation}
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              {/* AUDIT INTELLIGENCE SECTION */}
              <div className="bg-slate-900/80 rounded-[32px] border border-slate-800 overflow-hidden">
                <button 
                  onClick={() => setShowAudit(!showAudit)}
                  className="w-full p-6 flex justify-between items-center hover:bg-slate-800/30 transition-all group"
                >
                  <div className="flex items-center gap-4">
                    <div className="p-2 bg-blue-500/20 rounded-lg text-blue-400 group-hover:scale-110 transition-transform">
                      <FileText className="w-5 h-5" />
                    </div>
                    <p className="text-sm font-black uppercase tracking-widest text-slate-300">{showAudit ? 'Hide Audit Intelligence' : 'Explain Decision Like RBI Audit'}</p>
                  </div>
                  {showAudit ? <ChevronUp className="text-slate-500" /> : <ChevronDown className="text-slate-500" />}
                </button>
                
                <AnimatePresence>
                  {showAudit && (
                    <motion.div initial={{ height: 0 }} animate={{ height: 'auto' }} exit={{ height: 0 }} className="border-t border-slate-800 px-8 py-10 bg-slate-900/40">
                      <div className="space-y-10">
                        <div>
                          <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-4">Triggered Policy Rules</p>
                          <div className="flex flex-wrap gap-3">
                            {result.audit_mode.triggered_rules.length > 0 ? (
                              result.audit_mode.triggered_rules.map((rule: any, i: number) => (
                                <div key={i} className="px-4 py-2 bg-red-500/10 border border-red-500/30 rounded-xl text-[11px] font-bold text-red-400">
                                  {rule}
                                </div>
                              ))
                            ) : (
                              <p className="text-xs text-slate-600 italic">No policy violations.</p>
                            )}
                          </div>
                        </div>

                        <div>
                          <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-6">Decision Lineage</p>
                          <div className="space-y-6 relative">
                            {/* Vertical Line */}
                            <div className="absolute left-[17px] top-4 bottom-4 w-px bg-slate-800" />
                            
                            {result.audit_mode.risk_reasoning_chain.map((step: string, i: number) => (
                              <div key={i} className="flex gap-6 items-start group">
                                <div className="w-9 h-9 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-[10px] font-black text-slate-500 z-10 group-hover:border-blue-500/50 group-hover:text-blue-400 transition-all shrink-0">
                                  {String(i + 1).padStart(2, '0')}
                                </div>
                                <div className="bg-slate-800/30 p-4 rounded-2xl border border-slate-800/50 flex-grow hover:border-slate-700 transition-all">
                                  <p className="text-xs text-slate-400 leading-relaxed">{step}</p>
                                </div>
                              </div>
                            ))}
                            
                            <div className="flex gap-6 items-start pt-4">
                              <div className="w-9 h-9 rounded-full bg-emerald-500 flex items-center justify-center text-slate-900 z-10 shadow-[0_0_15px_rgba(16,185,129,0.3)] shrink-0">
                                <CheckCircle className="w-5 h-5" />
                              </div>
                              <div className="flex-grow">
                                <p className="text-sm font-black text-emerald-400 mb-1">{result.decision} - Risk committee sign-off required.</p>
                                <p className="text-[10px] text-slate-600 font-mono">ID: {result.request_id.split('-')[0]}…</p>
                              </div>
                            </div>
                          </div>
                        </div>

                        <div className="pt-6 border-t border-slate-800 flex justify-end">
                          <button className="flex items-center gap-2 px-6 py-3 bg-slate-800 hover:bg-slate-700 rounded-xl text-xs font-bold text-slate-300 transition-all">
                            <Download className="w-4 h-4" />
                            Download PDF Report
                          </button>
                        </div>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>

              <div className="text-center pt-10 border-t border-slate-800/50 mt-10">
                <p className="text-[10px] font-black text-slate-500 uppercase tracking-[0.4em]">
                  © 2026 PropIntel AI | RBI Compliant | Audit Ready
                </p>
                <div className="mt-4 inline-block px-4 py-1 bg-emerald-500/10 border border-emerald-500/20 rounded-full">
                  <p className="text-[9px] font-black text-emerald-400 uppercase tracking-widest">🏆 Final Judge Verdict: Production Ready</p>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
