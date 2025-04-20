import React from "react";
import { useQuery, gql } from "@apollo/client";
import "../App.css";
import PostListItem from "./PostListItem";
import useKeyNav from "../utils/useKeyNav";

const GET_POSTS = gql`
  query GetPosts {
    posts {
      id
      source
      sub
      title
      text
      upvotes
      publishedDate
      url
      commentUrl
      commentHtml
    }
  }
`;

const PostsList: React.FC<{ 
  onPostClick: (post: { id: string; title: string; text: string; publishedDate?: string; url?: string; source?: string; sub?: string; commentUrl?: string, commentHtml?: string }) => void;
  selectedSources: string[];
  selectedSubs: string[];
}> = ({ onPostClick, selectedSources, selectedSubs }) => {
  const { loading, error, data } = useQuery(GET_POSTS);
  const containerRef = React.useRef<HTMLDivElement>(null);

  // Sort posts by date, latest first
  const sortedPosts = data?.posts ? [...data.posts].sort((a, b) => {
    if (!a.publishedDate) return 1;
    if (!b.publishedDate) return -1;
    return new Date(b.publishedDate).getTime() - new Date(a.publishedDate).getTime();
  }) : [];

  // Filter posts by selected sources and subs if any are selected
  let filteredPosts = sortedPosts;
  
  // Filter by sources if any sources are selected
  if (selectedSources.length > 0 && sortedPosts.length > 0) {
    filteredPosts = filteredPosts.filter(post => selectedSources.includes(post.source));
  }
  
  // Filter by subreddits if any subs are selected
  if (selectedSubs.length > 0 && filteredPosts.length > 0) {
    filteredPosts = filteredPosts.filter(post => 
      // Only apply sub filtering for Reddit posts
      post.source !== 'REDDIT' || selectedSubs.includes(post.sub)
    );
  }

  // Use the keyboard navigation hook
  const handlePostSelect = (post: any, isOpeningLink?: boolean) => {
    if (isOpeningLink && post.url) {
      // Open the original URL in a new tab
      window.open(post.url, '_blank');
    } else {
      // Regular selection of the post
      onPostClick({
        id: post.id || "",
        title: post.title,
        text: post.text,
        publishedDate: post.publishedDate,
        url: post.url,
        source: post.source,
        sub: post.sub,
        commentUrl: post.commentUrl,
        commentHtml: post.commentHtml
      });
    }
  };

  const { activeItemId: activePostId, handleItemClick } = useKeyNav({
    items: filteredPosts,
    containerRef: containerRef as React.RefObject<HTMLElement>,
    autoSelectOnKeyPress: false,
    onSelect: handlePostSelect,
    getItemId: (item) => item.id,
    deps: [selectedSources, data]
  });

  if (loading) return (
    <div className="flex justify-center items-center p-8">
      <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
    </div>
  );
  
  if (error) return (
    <div className="p-4 text-red-500 bg-red-50 rounded-md m-4">
      <p className="font-medium">Error loading posts</p>
      <p className="text-sm">{error.message}</p>
    </div>
  );

  return (
    <div ref={containerRef} tabIndex={0}>
      {filteredPosts.map((item: { id: string; source: string; sub: string; title: string; text: string; publishedDate?: string; url?: string; commentUrl?: string, commentHtml?: string }, index: number) => (
        <div key={index} data-index={index}>
          <PostListItem
            post={item}
            onClick={(post) => handleItemClick(post, index)}
            isActive={activePostId === item.id}
          />
        </div>
      ))}
    </div>
  );
};

export default PostsList;
