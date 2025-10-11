import React from 'react';
import { useParams } from 'react-router-dom';

export const ResultsPage = () => {
  const { id } = useParams();

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Analysis Results</h1>
      <div className="bg-white rounded-lg shadow-card p-6">
        <p>Analysis results for image {id} will be displayed here</p>
      </div>
    </div>
  );
};
