import { gql } from "@apollo/client";

// User Fragments
export const USER_FRAGMENT = gql`
  fragment UserFields on UserType {
    id
    username
    email
    bio
    profilePicture
    followersCount
    followingCount
    postsCount
    isVerified
    createdAt
  }
`;

// Post Fragments
export const POST_FRAGMENT = gql`
  fragment PostFields on PostType {
    id
    content
    contentType
    privacyLevel
    mediaUrl
    likesCount
    commentsCount
    sharesCount
    createdAt
    author {
      id
      username
      profilePicture
    }
  }
`;

// Comment Fragment
export const COMMENT_FRAGMENT = gql`
  fragment CommentFields on CommentType {
    id
    content
    createdAt
    user {
      id
      username
      profilePicture
    }
    parent {
      id
    }
  }
`;

// ===================== QUERIES =====================

export const GET_POSTS = gql`
  ${POST_FRAGMENT}
  query GetPosts($limit: Int, $offset: Int) {
    posts(limit: $limit, offset: $offset) {
      ...PostFields
    }
  }
`;

export const GET_FEED = gql`
  ${POST_FRAGMENT}
  query GetFeed($limit: Int, $offset: Int) {
    feed(limit: $limit, offset: $offset) {
      ...PostFields
    }
  }
`;

export const GET_POST = gql`
  ${POST_FRAGMENT}
  ${COMMENT_FRAGMENT}
  query GetPost($id: ID!) {
    post(id: $id) {
      ...PostFields
      comments {
        ...CommentFields
      }
    }
  }
`;

export const GET_ME = gql`
  ${USER_FRAGMENT}
  query GetMe {
    me {
      ...UserFields
    }
  }
`;

export const GET_POST_COMMENTS = gql`
  ${COMMENT_FRAGMENT}
  query GetPostComments($postId: ID!) {
    postComments(postId: $postId) {
      ...CommentFields
    }
  }
`;

// ===================== MUTATIONS =====================

export const REGISTER_USER = gql`
  mutation RegisterUser($input: RegisterInput!) {
    registerUser(input: $input) {
      user {
        id
        username
        email
      }
      success
      message
    }
  }
`;

export const LOGIN_USER = gql`
  mutation LoginUser($input: LoginInput!) {
    loginUser(input: $input) {
      user {
        id
        username
        email
      }
      success
      message
    }
  }
`;

export const LOGOUT_USER = gql`
  mutation LogoutUser {
    logoutUser {
      success
      message
    }
  }
`;

export const CREATE_POST = gql`
  ${POST_FRAGMENT}
  mutation CreatePost($input: PostInput!) {
    createPost(input: $input) {
      post {
        ...PostFields
      }
      success
      message
    }
  }
`;

export const LIKE_POST = gql`
  mutation LikePost($postId: ID!) {
    likePost(postId: $postId) {
      success
      message
      isLiked
    }
  }
`;

export const CREATE_COMMENT = gql`
  ${COMMENT_FRAGMENT}
  mutation CreateComment($input: CommentInput!) {
    createComment(input: $input) {
      comment {
        ...CommentFields
      }
      success
      message
    }
  }
`;

export const SHARE_POST = gql`
  mutation SharePost($postId: ID!) {
    sharePost(postId: $postId) {
      success
      message
      sharesCount
    }
  }
`;
