import { ApolloClient, InMemoryCache } from "@apollo/client";

const client = new ApolloClient({
  uri: "http://localhost:8000/graphql",
  cache: new InMemoryCache({
    typePolicies: {
      PostType: {
        keyFields: ["id"],
      },
      DetailedPostResponse: {
        fields: {
          surroundingPosts: {
            merge(existing, incoming) {
              return incoming; // Always use the latest data
            }
          }
        }
      }
    }
  }),
});

export default client;
