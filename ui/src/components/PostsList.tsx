import React from "react";
import { useQuery, gql, useApolloClient } from "@apollo/client";
import "../App.css";
import PostListItem from "./PostListItem";
import useKeyNav from "../utils/useKeyNav";
import { cachePost, getCachedPost, isPostCached, cachePosts } from "../utils/cacheUtils";

const GET_POSTS = gql`
  query GetPosts($interweave: Boolean) {
    posts(limit: 300, interweave: $interweave) {
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

const GET_DETAILED_POSTS = gql`
  query GetDetailedPosts($id: String!, $surroundingIds: [String!]!) {
    getDetailedPosts(id: $id, surroundingIds: $surroundingIds) {
      post {
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
      surroundingPosts {
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
  }
`;

const PostsList: React.FC<{ 
  onPostClick: (post: { id: string; title: string; text: string; publishedDate?: string; url?: string; source?: string; sub?: string; commentUrl?: string, commentHtml?: string }) => void;
  selectedSources: string[];
  selectedSubs: string[];
  filterMode?: 'all' | 'top';
}> = ({ onPostClick, selectedSources, selectedSubs, filterMode = 'all' }) => {
  const { loading, error, data } = useQuery(GET_POSTS, {
    variables: {
      interweave: true // Enable interwoven results by default
    }
  });
  const containerRef = React.useRef<HTMLDivElement>(null);

  const sortedPosts = React.useMemo(() => {
    if (!data?.posts) return [];

    const posts = [...data.posts];

    if (filterMode === 'top') {
      const twoDaysAgo = new Date();
      twoDaysAgo.setDate(twoDaysAgo.getDate() - 2);

      const recentPosts = posts.filter(post => {
        return post.publishedDate && new Date(post.publishedDate) >= twoDaysAgo && post.upvotes && post.upvotes > 0;
      });

      const otherPosts = posts.filter(post => {
        return !post.publishedDate || new Date(post.publishedDate) < twoDaysAgo || !post.upvotes;
      });

      recentPosts.sort((a, b) => (b.upvotes || 0) - (a.upvotes || 0));
      otherPosts.sort((a, b) => {
        if (!a.publishedDate) return 1;
        if (!b.publishedDate) return -1;
        return new Date(b.publishedDate).getTime() - new Date(a.publishedDate).getTime();
      });

      return [...recentPosts, ...otherPosts];
    } else {
      return posts.sort((a, b) => {
        if (!a.publishedDate) return 1;
        if (!b.publishedDate) return -1;
        return new Date(b.publishedDate).getTime() - new Date(a.publishedDate).getTime();
      });
    }
  }, [data?.posts, filterMode]);

  let filteredPosts = sortedPosts;

  if (selectedSources.length > 0 && sortedPosts.length > 0) {
    filteredPosts = filteredPosts.filter(post => selectedSources.includes(post.source));
  }

  if (selectedSubs.length > 0 && filteredPosts.length > 0) {
    filteredPosts = filteredPosts.filter(post => post.source !== 'REDDIT' || selectedSubs.includes(post.sub));
  }

  // Use the keyboard navigation hook
  const handlePostSelect = (post: any, isOpeningLink?: boolean) => {
    if (isOpeningLink && post.url) {
      // Open the original URL in a new tab
      window.open(post.url, '_blank');
    } else {
      const currentIndex = filteredPosts.findIndex((p) => p.id === post.id);
      
      // Get unique surrounding IDs (prevent duplicates)
      const idSet = new Set<string>();
      if (filteredPosts[currentIndex - 1]?.id) {
        idSet.add(filteredPosts[currentIndex - 1].id);
      }
      if (filteredPosts[currentIndex + 1]?.id) {
        idSet.add(filteredPosts[currentIndex + 1].id);
      }
      const surroundingIds: string[] = Array.from(idSet);

      fetchDetailedPost(post.id, surroundingIds).then((detailedData) => {
        onPostClick(detailedData.post);
      });
    }
  };

  const client = useApolloClient();

  const { activeItemId: activePostId, handleItemClick } = useKeyNav({
    items: filteredPosts,
    containerRef: containerRef as React.RefObject<HTMLElement>,
    autoSelectOnKeyPress: false,
    onSelect: handlePostSelect,
    getItemId: (item) => item.id,
    deps: [selectedSources, selectedSubs, filterMode, data]
  });

  const fetchDetailedPost = async (postId: string, surroundingIds: string[]) => {
    // Check our simple cache first
    if (isPostCached(postId)) {
      console.log('Using cached data for post:', postId);
      const cachedPost = getCachedPost(postId);
      
      // Check for surrounding posts in our cache
      const cachedSurroundingPosts = surroundingIds
        .map(id => getCachedPost(id))
        .filter(Boolean); // Filter out undefined posts
      
      console.log(`Found ${cachedSurroundingPosts.length} surrounding posts in cache`);
      
      return {
        post: cachedPost,
        surroundingPosts: cachedSurroundingPosts,
      };
    }
    
    // If not in cache, make the network request
    console.log('Fetching from network for post:', postId);
    const { data } = await client.query({
      query: GET_DETAILED_POSTS,
      variables: { id: postId, surroundingIds },
    });
    
    // Store main post in our simple cache
    if (data.getDetailedPosts.post) {
      cachePost(data.getDetailedPosts.post);
    }
    
    // Store surrounding posts in our simple cache
    if (data.getDetailedPosts.surroundingPosts && data.getDetailedPosts.surroundingPosts.length) {
      cachePosts(data.getDetailedPosts.surroundingPosts);
    }

    return {
      post: data.getDetailedPosts.post,
      surroundingPosts: data.getDetailedPosts.surroundingPosts,
    };
  };

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
      {filteredPosts.map((item, index) => (
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
