import React from "react";

interface PostContentProps {
  post: {
    id: string;
    source: string;
    sub?: string;
    title: string;
    text: string;
    publishedDate?: string;
    upvotes?: number;
    commentUrl?: string;
    commentHtml?: string;
    url?: string;
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
  const commentsUrl = post.commentUrl || (post.source === 'REDDIT' ? `https://www.reddit.com/r/${post.sub}/comments/${post.id}` : '')

  return (
    <div className="p-8 h-[calc(100vh-10rem)] overflow-y-auto">
      <span className="text-3xl font-bold text-gray-900" 
          dangerouslySetInnerHTML={{ __html: post.title }}></span>
      
      <div className="mt-2 flex items-center text-gray-400 text-sm gap-4">
        {post.publishedDate && (
          <span>{post.publishedDate}</span>
        )}
        
        {post.upvotes !== undefined && (
          <span className="flex items-center">
            <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
              <path d="M2 10.5a1.5 1.5 0 113 0v6a1.5 1.5 0 01-3 0v-6zM6 10.333v5.43a2 2 0 001.106 1.79l.05.025A4 4 0 008.943 18h5.416a2 2 0 001.962-1.608l1.2-6A2 2 0 0015.56 8H12V4a2 2 0 00-2-2 1 1 0 00-1 1v.667a4 4 0 01-.8 2.4L6.8 7.933a4 4 0 00-.8 2.4z"></path>
            </svg>
            {post.upvotes.toLocaleString()}
          </span>
        )}
        
        {commentsUrl && (
          <a 
            href={commentsUrl} 
            target="_blank" 
            rel="noopener noreferrer"
            className="hover:text-blue-500 transition-colors flex items-center"
          >
            <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"></path>
            </svg>
            Comments
          </a>
        )}
      </div>
      
      <div className="prose prose-lg max-w-none mt-6">
        <div 
          // className="text-gray-700 leading-relaxed whitespace-pre-line"
          dangerouslySetInnerHTML={{ 
            __html: (post?.commentHtml ? post?.commentHtml : post?.text)
              .replace(/&quot;/g, '"')
              // .replace(/\n/g, '<br />')
              .replace(/\r/g, '')
              .replace(/\n\n/g, '\n')
          }}
        ></div>
      </div>
    </div>
  );
};

export default PostContent;
