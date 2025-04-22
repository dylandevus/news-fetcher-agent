// A simple cache utility for storing post data

// Type for post data
export interface PostData {
  id: string;
  source?: string;
  sub?: string;
  title: string;
  text: string;
  author?: string;
  upvotes?: number;
  publishedDate?: string;
  url?: string;
  commentUrl?: string;
  commentHtml?: string;
}

// Simple in-memory cache
const postCache: Record<string, PostData> = {};

/**
 * Store a post in the cache
 * @param post The post to cache
 */
export const cachePost = (post: PostData): void => {
  if (post && post.id) {
    postCache[post.id] = { ...post };
  }
};

/**
 * Get a post from the cache by ID
 * @param id The post ID to lookup
 * @returns The cached post or undefined if not found
 */
export const getCachedPost = (id: string): PostData | undefined => {
  return postCache[id];
};

/**
 * Check if a post exists in the cache
 * @param id The post ID to check
 * @returns Boolean indicating if the post is cached
 */
export const isPostCached = (id: string): boolean => {
  return !!postCache[id];
};

/**
 * Store multiple posts in the cache
 * @param posts Array of posts to cache
 */
export const cachePosts = (posts: PostData[]): void => {
  posts.forEach(post => {
    if (post && post.id) {
      postCache[post.id] = { ...post };
    }
  });
};

/**
 * Clear all posts from the cache
 */
export const clearCache = (): void => {
  Object.keys(postCache).forEach(key => {
    delete postCache[key];
  });
};

/**
 * Get cache statistics
 * @returns Object with cache stats
 */
export const getCacheStats = (): { size: number, keys: string[] } => {
  return {
    size: Object.keys(postCache).length,
    keys: Object.keys(postCache)
  };
};
