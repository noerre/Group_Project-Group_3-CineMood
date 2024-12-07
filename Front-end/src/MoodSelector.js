import React from "react";

// List of moods
const moods = ["Happy", "Sad", "Excited", "Relaxed", "Nostalgic", "Curious", "Chill"];

const MoodSelector = ({ onMoodSelect }) => {
  return (
    <div className="mb-4 text-center">
      <div className="mood-selector">
        {moods.map((mood) => (
          <button
            key={mood}
            type="button"
            className="btn btn-outline-primary"
            onClick={() => onMoodSelect(mood.toLowerCase())}
            aria-label={`Select ${mood} mood`}
          >
            {mood}
          </button>
        ))}
      </div>
    </div>
  );
};

export default MoodSelector;