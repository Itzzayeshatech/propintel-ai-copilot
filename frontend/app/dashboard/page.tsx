"use client";
import React from 'react';
import AnalyzeDashboard from '../../components/AnalyzeDashboard';

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-[#0a0e17] text-slate-100 pb-20 font-sans selection:bg-emerald-500/30">
      <div className="max-w-7xl mx-auto p-6 lg:p-10 space-y-8">
        
        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center border-b border-slate-700 pb-6 gap-4">
          <div>
            <h1 className="text-3xl font-extrabold tracking-tight bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">
              PropIntel AI Copilot
            </h1>
            <p className="text-slate-400 mt-1 text-sm md:text-base font-medium">
              Autonomous Risk & Underwriting Intelligence
            </p>
          </div>
          <div className="flex items-center gap-3">
             <div className="flex h-3 w-3 relative">
               <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
               <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
             </div>
             <p className="text-xs text-slate-400 font-mono">
               Demo Mode Ready
             </p>
          </div>
        </div>

        {/* Main Dashboard Component */}
        <AnalyzeDashboard />

      </div>
    </div>
  );
}
