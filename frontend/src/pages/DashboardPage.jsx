import React from 'react';

export const DashboardPage = () => {
  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-card">
          <h3 className="text-lg font-semibold text-gray-700">Total Images</h3>
          <p className="text-3xl font-bold text-primary-600 mt-2">0</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-card">
          <h3 className="text-lg font-semibold text-gray-700">Analyzed</h3>
          <p className="text-3xl font-bold text-secondary-600 mt-2">0</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-card">
          <h3 className="text-lg font-semibold text-gray-700">Pending</h3>
          <p className="text-3xl font-bold text-warning mt-2">0</p>
        </div>
      </div>
    </div>
  );
};
