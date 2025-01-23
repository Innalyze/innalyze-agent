import React from 'react';
import { Languages } from 'lucide-react';

export const LanguageToggle: React.FC = () => {
  return (
    <div className="flex items-center gap-2 px-3 py-1.5 rounded-md">
      <Languages className="w-4 h-4" />
      <span className="text-sm font-medium">FR</span>
    </div>
  );
};