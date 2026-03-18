import React from 'react';
import ReactECharts from 'echarts-for-react';

interface ChartProps {
  options: any;
  height?: string;
  theme?: 'dark' | 'light';
}

export default function Chart({ options, height = '400px', theme = 'dark' }: ChartProps) {
  const brandOptions = {
    color: ['#C5B388', '#1A3D2B', '#F5EFE0', '#2C3330', '#0F1A15'],
    backgroundColor: 'transparent',
    textStyle: {
      fontFamily: 'Inter, sans-serif'
    },
    tooltip: {
      backgroundColor: '#2C3330',
      borderColor: '#C5B388',
      textStyle: { color: '#F5EFE0' },
      ...(options.tooltip || {})
    },
    ...options
  };

  return (
    <div className="leaf-laminate rounded-lg p-6 my-8 border border-[var(--color-brass-primary)]/20 shadow-2xl">
      <ReactECharts 
        option={brandOptions} 
        style={{ height, width: '100%' }} 
        theme={theme}
      />
    </div>
  );
}