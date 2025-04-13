import React from "react";
import { useQuery, gql } from "@apollo/client";
import "../App.css";
import PostListItem from "./PostListItem";

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
    }
  }
`;

const PostsList: React.FC<{ 
  onPostClick: (post: { id: string; title: string; text: string; publishedDate?: string; url?: string; source?: string; sub?: string; commentUrl?: string }) => void;
  selectedSources: string[];
}> = ({ onPostClick, selectedSources }) => {
  const { loading, error, data } = useQuery(GET_POSTS);
  const [activePostId, setActivePostId] = React.useState<string | null>(null);
  const [activeIndex, setActiveIndex] = React.useState<number>(-1);
  const containerRef = React.useRef<HTMLDivElement>(null);

  // Handle keyboard navigation with window.addEventListener
  React.useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (!data?.posts) return;
      
      // Filter posts as we do in the component
      const sortedPosts = [...data.posts].sort((a, b) => {
        if (!a.publishedDate) return 1;
        if (!b.publishedDate) return -1;
        return new Date(b.publishedDate).getTime() - new Date(a.publishedDate).getTime();
      });
      
      const filteredPosts = selectedSources.length > 0
        ? sortedPosts.filter(post => selectedSources.includes(post.source))
        : sortedPosts;
      
      // Get current active index
      let currentIndex = activeIndex;
      
      switch (e.key) {
        case 'ArrowUp':
          e.preventDefault();
          // Move to previous post
          currentIndex = Math.max(0, currentIndex - 1);
          setActiveIndex(currentIndex);
          setActivePostId(filteredPosts[currentIndex]?.id || null);
          break;
        case 'ArrowDown':
          e.preventDefault();
          // Move to next post
          currentIndex = Math.min(filteredPosts.length - 1, currentIndex + 1);
          setActiveIndex(currentIndex);
          setActivePostId(filteredPosts[currentIndex]?.id || null);
          break;
        case 'Enter':
          // Handle Enter key - select current post
          if (currentIndex >= 0 && currentIndex < filteredPosts.length) {
            const post = filteredPosts[currentIndex];
            if (e.metaKey && post.url) {
              // Meta+Enter opens the original URL in a new tab
              window.open(post.url, '_blank');
            } else {
              // Regular Enter selects the post
              onPostClick({ 
              id: post.id || "", 
              title: post.title, 
              text: post.text,
              publishedDate: post.publishedDate,
              url: post.url,
              source: post.source,
              sub: post.sub,
              commentUrl: post.commentUrl
              });
            }
          }
          break;
      }
      
      // Scroll the active item into view if needed
      if (currentIndex >= 0) {
        const activeElement = containerRef.current?.querySelector(`[data-index="${currentIndex}"]`);
        activeElement?.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [data, activeIndex, selectedSources, onPostClick]);

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

  // Sort posts by date, latest first
  const sortedPosts = [...data.posts].sort((a, b) => {
    if (!a.publishedDate) return 1;
    if (!b.publishedDate) return -1;
    return new Date(b.publishedDate).getTime() - new Date(a.publishedDate).getTime();
  });

  // Filter posts by selected sources if any are selected
  const filteredPosts = selectedSources.length > 0
    ? sortedPosts.filter(post => selectedSources.includes(post.source))
    : sortedPosts;

  return (
    <div ref={containerRef} tabIndex={0}>
      {filteredPosts.map((item: { id: string; source: string; sub: string; title: string; text: string; publishedDate?: string; url?: string; commentUrl?: string }, index: number) => (
        <div key={index} data-index={index}>
          <PostListItem
            post={item}
            onClick={(post) => {
              setActivePostId(post.id ?? '');
              setActiveIndex(index);
              onPostClick({ ...post, id: post.id || "" });
            }}
            isActive={activePostId === item.id}
          />
        </div>
      ))}
    </div>
  );
};

export default PostsList;
