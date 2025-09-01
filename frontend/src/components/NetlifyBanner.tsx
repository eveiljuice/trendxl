import React from 'react';
import { Cloud, Download, Play, ExternalLink } from 'lucide-react';

const NetlifyBanner: React.FC = () => {
  const isNetlify = typeof window !== 'undefined' && window.location.hostname.includes('netlify');

  if (!isNetlify) return null;

  return (
    <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-6 rounded-lg shadow-lg mb-8">
      <div className="flex items-center gap-3 mb-4">
        <Cloud className="w-8 h-8" />
        <h2 className="text-xl font-bold">🚀 TrendXL on Netlify</h2>
      </div>

      <p className="text-blue-100 mb-4">
        This is a frontend-only deployment. For full functionality with backend API,
        please run the application locally.
      </p>

      <div className="bg-white/10 rounded-lg p-4 mb-4">
        <h3 className="font-semibold mb-2 flex items-center gap-2">
          <Download className="w-5 h-5" />
          Quick Local Setup:
        </h3>
        <div className="bg-black/20 rounded p-3 font-mono text-sm">
          git clone https://github.com/eveiljuice/trendxl.git<br/>
          cd trendxl<br/>
          docker-compose up --build
        </div>
      </div>

      <div className="flex flex-wrap gap-3">
        <a
          href="https://github.com/eveiljuice/trendxl"
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-2 bg-white/20 hover:bg-white/30 px-4 py-2 rounded-lg transition-colors"
        >
          <ExternalLink className="w-4 h-4" />
          View on GitHub
        </a>

        <a
          href="https://github.com/eveiljuice/trendxl#readme"
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-2 bg-white/20 hover:bg-white/30 px-4 py-2 rounded-lg transition-colors"
        >
          <Play className="w-4 h-4" />
          Full Documentation
        </a>
      </div>
    </div>
  );
};

export default NetlifyBanner;
