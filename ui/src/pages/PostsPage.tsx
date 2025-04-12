import React, { useState } from "react";
import PostsList from "../components/PostsList";
import Header from "../components/Header";

const PostsPage: React.FC = () => {
  const [selectedPost, setSelectedPost] = useState<{
    title: string;
    text: string;
  } | null>(null);

  const handlePostClick = (post: { title: string; text: string }) => {
    setSelectedPost(post);
  };

  return (
    <div className="flex flex-col w-full h-screen overflow-hidden">
      <Header />
      
      {/* Main content */}
      <div className="flex flex-1 w-full">
        {/* Left Column: Posts List */}
        <div className="w-1/3 bg-white border-r border-gray-200 overflow-hidden">
          <div className="p-4 border-b border-gray-200 bg-gray-50 sticky top-0 z-10">
            <h2 className="text-lg font-medium text-gray-800">Headlines</h2>
          </div>
          <div className="divide-y divide-gray-100 h-[calc(100vh-10rem)] overflow-y-auto">
            <PostsList onPostClick={handlePostClick} />
          </div>
        </div>

        {/* Right Column: Post Content */}
        <div className="w-2/3 bg-white overflow-hidden">
          {selectedPost ? (
            <div className="p-8 h-[calc(100vh-10rem)] overflow-y-auto">
              <span className="text-3xl font-bold text-gray-900" 
                  dangerouslySetInnerHTML={{ __html: selectedPost.title }}></span>
              <div className="prose prose-lg max-w-none mt-6">
                <div 
                  className="text-gray-700 leading-relaxed whitespace-pre-line"
                  dangerouslySetInnerHTML={{ 
                    __html: (selectedPost?.text ?? '')
                      .replace(/&quot;/g, '"')
                      .replace(/\n/g, '<br />')
                      .replace(/\r/g, '')
                  }}
                ></div>
              </div>
            </div>
          ) : (
            <div className="flex items-center justify-center h-[calc(100vh-10rem)] p-6 text-gray-400 bg-gray-50">
              <div className="text-center">
                <svg className="w-12 h-12 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"></path>
                </svg>
                <p className="text-lg font-medium">No article selected</p>
                <p className="mt-1 text-sm">Select an article from the list to read</p>
              </div>
            </div>
          )}
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
