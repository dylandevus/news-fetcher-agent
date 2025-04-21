import React, { useState, useEffect, useRef } from "react";

interface SourceSelectorProps {
  onSourcesChange: (sources: string[]) => void;
  initialSelected?: string[]; // New prop to receive initial selection
}

const SourceSelector: React.FC<SourceSelectorProps> = ({ onSourcesChange, initialSelected = [] }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedSources, setSelectedSources] = useState<string[]>(initialSelected);
  const dropdownRef = useRef<HTMLDivElement>(null);
  
  const sources = [
    { id: "HNEWS", name: "Hacker News" },
    { id: "REDDIT", name: "Reddit" },
  ];

  // Handle click outside to close dropdown
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }

    // Add event listener when dropdown is open
    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    
    // Cleanup the event listener
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  const toggleSource = (sourceId: string) => {
    const newSources = selectedSources.includes(sourceId)
      ? selectedSources.filter(id => id !== sourceId)
      : [...selectedSources, sourceId];
    
    setSelectedSources(newSources);
    onSourcesChange(newSources);
  };

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={toggleDropdown}
        className="flex items-center justify-between w-auto px-2 py-1 text-xs font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-1 focus:ring-blue-500"
        style={{ backgroundColor: "white", color: "#4b5563" }}
      >
        <span>{selectedSources.length ? `${selectedSources.length} selected` : "Sources"}</span>
        <svg className="w-3 h-3 ml-1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" style={{ color: "#4b5563" }}>
          <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
        </svg>
      </button>

      {isOpen && (
        <div className="absolute right-0 z-10 w-full mt-1 origin-top-right bg-white rounded-md shadow-lg ring-1 ring-black ring-opacity-5">
          <div className="py-1">
            {sources.map((source) => (
              <div
                key={source.id}
                className="flex items-center px-4 py-2 text-sm hover:bg-gray-100 cursor-pointer"
                onClick={() => toggleSource(source.id)}
              >
                <input
                  type="checkbox"
                  checked={selectedSources.includes(source.id)}
                  onChange={() => {}}
                  className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                />
                <span className="ml-2">{source.name}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default SourceSelector;
