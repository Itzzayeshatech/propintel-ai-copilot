"use client";

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { Lock } from 'lucide-react';

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    if (!email.includes('@')) {
      setError('Invalid credentials: Email must contain @.');
      return;
    }
    if (password.length < 6) {
      setError('Invalid credentials: Password must be at least 6 characters.');
      return;
    }
    
    // Auth mocked for demo
    router.push('/dashboard');
  };

  return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center relative overflow-hidden font-sans">
      
      {/* Animated Background Orbs */}
      <motion.div 
        animate={{ scale: [1, 1.2, 1], rotate: [0, 90, 0] }}
        transition={{ duration: 15, repeat: Infinity, ease: "linear" }}
        className="absolute -top-40 -left-40 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none"
      />
      <motion.div 
        animate={{ scale: [1, 1.5, 1], rotate: [0, -90, 0] }}
        transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
        className="absolute -bottom-40 -right-40 w-[30rem] h-[30rem] bg-cyan-500/10 rounded-full blur-3xl pointer-events-none"
      />

      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="relative z-10 w-full max-w-md p-8 bg-slate-800/80 backdrop-blur-xl border border-slate-700/50 rounded-2xl shadow-2xl"
      >
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-slate-800 border border-emerald-500/30 mb-4 shadow-[0_0_15px_rgba(16,185,129,0.2)]">
            <Lock className="w-6 h-6 text-emerald-400" />
          </div>
          <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-emerald-400 to-cyan-400 mb-2">
            PropIntel AI Copilot
          </h1>
          <p className="text-slate-400 text-sm">Autonomous Lending Intelligence & Risk Simulation</p>
        </div>

        {error && (
          <motion.div initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} className="mb-6 bg-red-500/10 border border-red-500/50 text-red-500 text-sm p-3 rounded-lg text-center">
            {error}
          </motion.div>
        )}

        <form onSubmit={handleLogin} className="space-y-5">
          <div>
            <label className="block text-sm text-slate-400 mb-1">Work Email</label>
            <input 
              type="email" 
              required
              autoComplete="username"
              className="w-full bg-slate-900/50 border border-slate-700 rounded-lg p-3 text-slate-200 outline-none focus:border-emerald-500 transition-colors"
              placeholder="cfo@nbfc.com"
              value={email}
              onChange={e => { setEmail(e.target.value); setError(''); }}
            />
          </div>
          <div>
            <div className="flex justify-between items-center mb-1">
              <label className="block text-sm text-slate-400">Password</label>
              <a href="#" className="text-xs text-emerald-500 hover:text-emerald-400">Forgot Password?</a>
            </div>
            <input 
              type="password" 
              required
              autoComplete="current-password"
              className="w-full bg-slate-900/50 border border-slate-700 rounded-lg p-3 text-slate-200 outline-none focus:border-emerald-500 transition-colors"
              placeholder="••••••••"
              value={password}
              onChange={e => { setPassword(e.target.value); setError(''); }}
            />
          </div>

          <button 
            type="submit"
            className="w-full bg-gradient-to-r from-emerald-500 to-cyan-500 hover:from-emerald-400 hover:to-cyan-400 text-slate-900 font-bold py-3 rounded-lg mt-4 transition-transform hover:scale-[1.02] active:scale-95 shadow-lg shadow-emerald-500/20"
          >
            Authenticate Terminal
          </button>
        </form>

        <div className="mt-8 text-center text-xs text-slate-500 border-t border-slate-700/50 pt-6">
          © 2026 PropIntel AI. RBI Compliant.<br/>
          Explainable. Auditable. Privacy-Safe.
        </div>
      </motion.div>
    </div>
  );
}
