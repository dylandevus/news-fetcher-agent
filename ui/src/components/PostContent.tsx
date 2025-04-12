import React from "react";

interface PostContentProps {
  post: {
    title: string;
    text: string;
    publishedDate?: string;
  } | null;
}

const PostContent: React.FC<PostContentProps> = ({ post }) => {
  if (!post) {
    return (
      <div className="flex items-center justify-center h-[calc(100vh-10rem)] p-6 text-gray-400 bg-gray-50">
        <div className="text-center">
          <svg className="w-12 h-12 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"></path>
          </svg>
          <p className="text-lg font-medium">No article selected</p>
          <p className="mt-1 text-sm">Select an article from the list to read</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8 h-[calc(100vh-10rem)] overflow-y-auto">
      <span className="text-3xl font-bold text-gray-900" 
          dangerouslySetInnerHTML={{ __html: post.title }}></span>
      
      {post.publishedDate && (
        <div className="mt-2 text-gray-400 text-sm">
          {post.publishedDate}
        </div>
      )}
      
      <div className="prose prose-lg max-w-none mt-6">
        <div 
          className="text-gray-700 leading-relaxed whitespace-pre-line"
          dangerouslySetInnerHTML={{ 
            __html: (post?.text ?? '')
              .replace(/&quot;/g, '"')
              .replace(/\n/g, '<br />')
              .replace(/\r/g, '')
          }}
        ></div>
      </div>
    </div>
  );
};

export default PostContent;
