// src/CommunityCollegeDropdown.jsx
import React from 'react';
import collegesData from './ca_community_colleges.json';

export default function CommunityCollegeDropdown({ selectedCollege, onChange }) {
  return (
    <select
      value={selectedCollege}
      onChange={(e) => onChange(e.target.value)}
      className="input-field"
      required
    >
      <option value="" disabled>Select your college</option>
      {collegesData.map((college) => (
        <option key={college.name} value={college.name}>
          {college.name}
        </option>
      ))}
    </select>
  );
}