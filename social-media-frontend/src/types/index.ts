// User Types
export interface User {
  id: string;
  username: string;
  email: string;
  bio?: string;
  profilePicture?: string;
  followersCount: number;
  followingCount: number;
  postsCount: number;
  isVerified: boolean;
  createdAt: string;
}

export interface AuthUser {
  id: string;
  username: string;
  email: string;
}

// Post Types
export interface Post {
  id: string;
  content: string;
  contentType: ContentType;
  privacyLevel: PrivacyLevel;
  mediaUrl?: string;
  likesCount: number;
  commentsCount: number;
  sharesCount: number;
  createdAt: string;
  author: {
    id: string;
    username: string;
    profilePicture?: string;
  };
}

export type ContentType = 'text' | 'image' | 'video' | 'mixed';
export type PrivacyLevel = 'public' | 'followers' | 'private';

// Comment Types
export interface Comment {
  id: string;
  content: string;
  createdAt: string;
  user: {
    id: string;
    username: string;
    profilePicture?: string;
  };
  parent?: {
    id: string;
  };
}

// Input Types
export interface RegisterInput {
  username: string;
  email: string;
  password: string;
  firstName?: string;
  lastName?: string;
}

export interface LoginInput {
  username: string;
  password: string;
}

export interface PostInput {
  content: string;
  contentType?: ContentType;
  privacyLevel?: PrivacyLevel;
  mediaUrl?: string;
}

export interface CommentInput {
  postId: string;
  content: string;
  parentId?: string;
}

// Response Types
export interface MutationResponse {
  success: boolean;
  message: string;
}

export interface RegisterResponse extends MutationResponse {
  user?: AuthUser;
}

export interface LoginResponse extends MutationResponse {
  user?: AuthUser;
}

export interface CreatePostResponse extends MutationResponse {
  post?: Post;
}

export interface LikePostResponse extends MutationResponse {
  isLiked: boolean;
}

export interface CreateCommentResponse extends MutationResponse {
  comment?: Comment;
}
