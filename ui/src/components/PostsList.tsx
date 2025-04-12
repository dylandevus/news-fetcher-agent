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
}> = ({ onPostClick }) => {
  const { loading, error, data } = useQuery(GET_POSTS);
  const [activePostId, setActivePostId] = React.useState<string | null>(null);

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

  return (
    <>
      {sortedPosts.map((item: { id: string; source: string; sub: string; title: string; text: string; publishedDate?: string; url?: string; commentUrl?: string }, index: number) => (
        <PostListItem
          key={index}
          post={item}
          onClick={(post) => {
            setActivePostId(post.id ?? '');
            onPostClick({ ...post, id: post.id || "" })
          }}
          isActive={activePostId === item.id}
        />
      ))}
    </>
  );
};

export default PostsList;
