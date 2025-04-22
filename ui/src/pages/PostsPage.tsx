import React, { useState, useEffect } from "react";
import PostsList from "../components/PostsList";
import PostContent from "../components/PostContent";
import Header from "../components/Header";
import SourceSelector from "../components/SourceSelector";
import SubSelector from "../components/SubSelector";

const PostsPage: React.FC = () => {
  // Define the post type to match PostContent requirements
  type Post = {
    id: string;
    source: string; // Required by PostContent component
    sub?: string;
    title: string;
    text: string;
    publishedDate?: string;
    upvotes?: number;
    url?: string;
    commentUrl?: string;
    commentHtml?: string;
  };

  const [selectedPost, setSelectedPost] = useState<Post | null>(null);
  
  // Add state for the filter mode (All or Top)
  const [filterMode, setFilterMode] = useState<'all' | 'top'>('all');
  
  // Initialize selected sources from sessionStorage or default to empty array
  const [selectedSources, setSelectedSources] = useState<string[]>(() => {
    try {
      const savedSources = sessionStorage.getItem('selectedSources');
      return savedSources ? JSON.parse(savedSources) : [];
    } catch (e) {
      console.error('Error loading sources from sessionStorage:', e);
      return [];
    }
  });
  
  // Initialize selected subs from sessionStorage or default to empty array
  const [selectedSubs, setSelectedSubs] = useState<string[]>(() => {
    try {
      const savedSubs = sessionStorage.getItem('selectedSubs');
      return savedSubs ? JSON.parse(savedSubs) : [];
    } catch (e) {
      console.error('Error loading subs from sessionStorage:', e);
      return [];
    }
  });

  // Save selected sources to sessionStorage when they change
  useEffect(() => {
    sessionStorage.setItem('selectedSources', JSON.stringify(selectedSources));
  }, [selectedSources]);

  // Save selected subs to sessionStorage when they change
  useEffect(() => {
    sessionStorage.setItem('selectedSubs', JSON.stringify(selectedSubs));
  }, [selectedSubs]);

  const handlePostClick = (post: {
    id: string;
    title: string;
    text: string;
    publishedDate?: string;
    url?: string;
    source?: string;
    sub?: string;
    commentUrl?: string;
    commentHtml?: string;
  }) => {
    // Ensure source is a string as required by PostContent
    setSelectedPost({
      ...post,
      source: post.source || 'UNKNOWN' // Provide default value if source is undefined
    });
  };
  
  const handleSourcesChange = (sources: string[]) => {
    setSelectedSources(sources);
    // If REDDIT is not selected, clear subreddit selections
    if (!sources.includes('REDDIT')) {
      setSelectedSubs([]);
    }
  };

  const handleSubsChange = (subs: string[]) => {
    setSelectedSubs(subs);
  };

  // Handler for switching between All and Top filters
  const toggleFilterMode = (mode: 'all' | 'top') => {
    setFilterMode(mode);
    
    // If switching to "All" mode, reset all filters
    if (mode === 'all') {
      setSelectedSources([]);
      setSelectedSubs([]);
    }
  };

  return (
    <div className="flex flex-col w-full h-screen overflow-hidden">
      <Header />
      
      {/* Main content */}
      <div className="flex flex-1 w-full">
        {/* Left Column: Posts List */}
        <div className="w-1/3 bg-white border-r border-gray-200 overflow-hidden">
          <div className="p-4 border-b border-gray-200 bg-gray-50 sticky top-0 z-10 flex justify-between items-center">
            <div className="flex space-x-3">
              <SourceSelector 
                onSourcesChange={handleSourcesChange} 
                initialSelected={selectedSources} 
              />
              <SubSelector 
                onSubsChange={handleSubsChange} 
                selectedSources={selectedSources} 
                initialSelected={selectedSubs} 
              />
            </div>
            <div className="text-lg font-medium text-gray-800 flex items-center">
              <span 
                className={`cursor-pointer mr-2 ${filterMode === 'all' ? 'text-blue-600 font-semibold' : 'text-gray-500 hover:text-gray-700'}`}
                onClick={() => toggleFilterMode('all')}
              >
                All
              </span>
              <span className="text-gray-400">|</span>
              <span 
                className={`cursor-pointer ml-2 ${filterMode === 'top' ? 'text-blue-600 font-semibold' : 'text-gray-500 hover:text-gray-700'}`}
                onClick={() => toggleFilterMode('top')}
              >
                Top
              </span>
              {selectedSources.length > 0 && (
                <span className="ml-3 text-sm text-gray-500">
                  ({selectedSources.join(', ')})
                </span>
              )}
            </div>
          </div>
          <div className="divide-y divide-gray-100 h-[calc(100vh-10rem)] overflow-y-auto">
            <PostsList 
              onPostClick={handlePostClick} 
              selectedSources={selectedSources}
              selectedSubs={selectedSubs}
              filterMode={filterMode}
            />
          </div>
        </div>

        {/* Right Column: Post Content */}
        <div className="w-2/3 bg-white overflow-hidden">
          <PostContent post={selectedPost} />
        </div>
      </div>
      
      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 py-3">
        <div className="w-full px-6 text-center">
          <p className="text-sm text-gray-500">&copy; 2025 Post Reader. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default PostsPage;
