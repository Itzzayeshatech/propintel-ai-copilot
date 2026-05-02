"use client";
import { useAppStore } from '../store/store';
import { MapPin } from 'lucide-react';

const ZONES = [
  "Whitefield, Bangalore",
  "Koramangala, Bangalore",
  "Indiranagar, Bangalore",
  "Rural Risk Zone"
];

export default function PropertyForm() {
  const { form, setForm, evaluateAsset, loading } = useAppStore();

  return (
    <div className="bg-slate-800 rounded-xl p-6 border border-slate-700 shadow-xl w-full">
      <h2 className="text-xl font-semibold mb-6 flex items-center gap-2 text-slate-100">
        <MapPin className="w-5 h-5 text-emerald-400" /> Property Details
      </h2>
      <div className="space-y-4">
        <div>
          <label className="block text-sm text-slate-400 mb-1">Zone</label>
          <select
            className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-sm text-slate-200 focus:ring-2 focus:ring-emerald-500 outline-none"
            value={form.zone}
            onChange={(e) => setForm({ zone: e.target.value })}
          >
            {ZONES.map(z => <option key={z} value={z}>{z}</option>)}
          </select>
        </div>
        <div>
          <label className="block text-sm text-slate-400 mb-1">Area (Sq.ft)</label>
          <input
            type="number"
            className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-sm text-slate-200 outline-none focus:border-emerald-500"
            value={form.area_sqft}
            onChange={(e) => setForm({ area_sqft: Number(e.target.value) })}
            placeholder="1200"
          />
        </div>
        <div>
          <label className="block text-sm text-slate-400 mb-1">Age (Years)</label>
          <input
            type="number"
            className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-sm text-slate-200 outline-none focus:border-emerald-500"
            value={form.age_years}
            onChange={(e) => setForm({ age_years: Number(e.target.value) })}
            placeholder="5"
          />
        </div>
        <button
          onClick={() => evaluateAsset()}
          disabled={loading}
          className="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-medium py-3 rounded-lg mt-4 transition-colors disabled:opacity-50"
        >
          {loading ? "Analyzing..." : "Evaluate Asset"}
        </button>
      </div>
    </div>
  );
}
