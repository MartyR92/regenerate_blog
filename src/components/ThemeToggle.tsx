import React, { useState, useEffect } from 'react';

export default function ThemeToggle() {
  const [theme, setTheme] = useState<'macro' | 'micro'>('micro');

  useEffect(() => {
    document.body.className = `theme-${theme}`;
  }, [theme]);

  return (
    <button 
      onClick={() => setTheme(theme === 'macro' ? 'micro' : 'macro')}
      aria-label="Toggle between Macro (Rə:NatureFørce) and Micro (Rə:Vive La Palma) identity"
      className="fixed bottom-8 right-8 z-50 px-6 py-3 rounded-sm leaf-laminate brass-hover font-syne text-sm uppercase tracking-widest cursor-pointer focus:outline-none focus:ring-2 focus:ring-[var(--color-brass-primary)] focus:ring-offset-2 focus:ring-offset-void-primary"
    >
      {theme === 'macro' ? 'Rə:NatureFørce' : 'Rə:Vive La Palma'}
    </button>
  );
}