import React from "react";
import { useQuery, gql } from "@apollo/client";
import "../App.css";

const GET_POSTS = gql`
  query GetPosts {
    posts {
      title
      text
    }
  }
`;

const PostsList: React.FC<{ onPostClick: (post: { title: string; text: string }) => void }> = ({ onPostClick }) => {
  const { loading, error, data } = useQuery(GET_POSTS);

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
    <>
      {data.posts.map((item: { title: string; text: string }, index: number) => (
        <div
          key={index}
          className="p-4 hover:bg-blue-50 transition-colors duration-200 cursor-pointer"
          onClick={() => onPostClick(item)}
        >
          <h3 className="font-medium text-gray-800 hover:text-blue-600 transition-colors">{item.title}</h3>
          <p className="text-gray-500 text-sm mt-1 line-clamp-2">{item.text}</p>
        </div>
      ))}
    </>
  );
};

export default PostsList;
