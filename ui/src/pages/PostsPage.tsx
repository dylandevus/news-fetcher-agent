import React, { useState } from "react";
import PostsList from "../components/PostsList";
import PostContent from "../components/PostContent";
import Header from "../components/Header";

const PostsPage: React.FC = () => {
  const [selectedPost, setSelectedPost] = useState<{
    title: string;
    text: string;
    published_date?: string;
  } | null>(null);

  const handlePostClick = (post: { title: string; text: string; published_date?: string }) => {
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
