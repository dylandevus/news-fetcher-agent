import React, { useState, useEffect, useRef } from 'react';

interface SubSelectorProps {
  onSubsChange: (subs: string[]) => void;
  selectedSources: string[];
  initialSelected?: string[]; // New prop to receive initial selection
}

const SUB_OPTIONS = [
  { label: 'React.js', value: 'reactjs' },
  { label: 'Python', value: 'Python' },
  { label: 'ArtificialInteligence', value: 'ArtificialInteligence' },
  { label: 'ChatGPT Pro', value: 'ChatGPTPro' },
  { label: 'Local LLaMA', value: 'LocalLLaMA' },
];

const SubSelector: React.FC<SubSelectorProps> = ({ onSubsChange, selectedSources, initialSelected = [] }) => {
  const [selectedSubs, setSelectedSubs] = useState<string[]>(initialSelected);
  const [isOpen, setIsOpen] = useState(false);
  const [isRedditSelected, setIsRedditSelected] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Update isRedditSelected whenever selectedSources changes
  useEffect(() => {
    const hasRedditSource = selectedSources.includes('REDDIT');
    setIsRedditSelected(hasRedditSource);
    
    // If Reddit is not selected, clear the sub selections
    if (!hasRedditSource) {
      setSelectedSubs([]);
      onSubsChange([]);
    }
  }, [selectedSources]);

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

  const toggleSub = (sub: string) => {
    const updatedSubs = selectedSubs.includes(sub)
      ? selectedSubs.filter(s => s !== sub)
      : [...selectedSubs, sub];
    
    setSelectedSubs(updatedSubs);
    onSubsChange(updatedSubs);
  };

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  const selectAllSubs = () => {
    const allSubs = SUB_OPTIONS.map(option => option.value);
    setSelectedSubs(allSubs);
    onSubsChange(allSubs);
  };

  const clearAllSubs = () => {
    setSelectedSubs([]);
    onSubsChange([]);
  };

  // Disable the selector if Reddit is not selected
  const isDisabled = !isRedditSelected;

  return (
    <div className="relative" ref={dropdownRef}>
      <button 
        onClick={toggleDropdown}
        disabled={isDisabled}
        className={`px-2 py-1 text-xs font-medium rounded-md border border-gray-300 shadow-sm flex items-center ${
          isDisabled 
            ? 'bg-gray-100 text-gray-400 cursor-not-allowed' 
            : 'bg-white text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-1 focus:ring-blue-500'
        }`}
      >
        {selectedSubs.length > 0 
          ? `${selectedSubs.length} Sub${selectedSubs.length > 1 ? 's' : ''}` 
          : 'Sub-category'}
        <svg className="ml-1 h-3 w-3" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
          <path fillRule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z" clipRule="evenodd" />
        </svg>
      </button>

      {isOpen && (
        <div className="origin-top-left absolute left-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none z-10">
          <div className="py-1 border-b border-gray-200">
            <button
              onClick={selectAllSubs}
              className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
            >
              Select All
            </button>
            <button
              onClick={clearAllSubs}
              className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
            >
              Clear All
            </button>
          </div>
          <div className="py-1">
            {SUB_OPTIONS.map((option) => (
              <div key={option.value} className="flex items-center px-4 py-2 hover:bg-gray-100">
                <input
                  id={`sub-${option.value}`}
                  name={`sub-${option.value}`}
                  type="checkbox"
                  className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                  checked={selectedSubs.includes(option.value)}
                  onChange={() => toggleSub(option.value)}
                />
                <label
                  htmlFor={`sub-${option.value}`}
                  className="ml-3 block text-sm text-gray-700 w-full cursor-pointer"
                >
                  {option.label}
                </label>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default SubSelector;
