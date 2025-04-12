import React from "react";
import { formatRelativeDate } from "../utils/dateUtils";

interface PostListItemProps {
  post: {
    source?: string;
    sub?: string;
    title: string;
    text: string;
    upvotes?: number;
    publishedDate?: string;
    url?: string;
  };
  onClick: (post: { source: string; sub: string; title: string; text: string; upvotes?: number, publishedDate?: string; url?: string; }) => void;
}

const PostListItem: React.FC<PostListItemProps> = ({ post, onClick }) => {
  const handleClick = (event: React.MouseEvent) => {
    // If Cmd key (Mac) or Ctrl key (Windows) is pressed and URL exists
    if ((event.metaKey || event.ctrlKey) && post.url) {
      // Open URL in new tab
      window.open(post.url, '_blank');
      // Prevent default click behavior
      event.preventDefault();
    } else {
      // Normal click behavior - show post details
      onClick(post);
    }
  };

  const handleExternalLinkClick = (event: React.MouseEvent) => {
    if (post.url) {
      window.open(post.url, '_blank');
      event.stopPropagation(); // Prevent the row click event
    }
  }

  return (
    <div
      className="p-4 hover:bg-blue-50 transition-colors duration-200 cursor-pointer relative"
      onClick={handleClick}
    >
      {/* Top section with title and external link icon */}
      <div className="flex justify-between items-start">
        <h3 className="font-semibold text-gray-800 hover:text-blue-600 transition-colors pr-2 flex-grow">
          {post.title}
        </h3>
        {post.url && (
          <button 
            onClick={handleExternalLinkClick}
            className="ml-2 text-gray-400 hover:text-blue-500 focus:outline-none flex-shrink-0"
            title="Open original link"
            aria-label="Open original link"
            style={{ backgroundColor: 'transparent', padding: '2px' }}
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
            </svg>
          </button>
        )}
      </div>
      
      {/* Post text content */}
      <p className="text-gray-500 text-sm mt-1 mb-1 line-clamp-2">{post.text}</p>
      
      {/* Footer row with sub and date */}
      <div className="flex items-center mt-2 text-xs text-gray-500">
        <span>{post.source || ''}</span>
        <span className="ml-3">{post.sub || ''}</span>
        <span className="ml-3">{post.publishedDate && formatRelativeDate(post.publishedDate)}</span>
        <span className="ml-3">{post.upvotes || ''} likes</span>
      </div>
    </div>
  );
};

export default PostListItem;
