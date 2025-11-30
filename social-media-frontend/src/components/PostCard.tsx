import { useState } from "react";
import { motion } from "framer-motion";
import { useMutation } from "@apollo/client";
import {
  LIKE_POST,
  CREATE_COMMENT,
  SHARE_POST,
  GET_POST_COMMENTS,
} from "../graphql/queries";
import { Post } from "../types";
import { useAuth } from "../context/AuthContext";
import CommentSection from "./CommentSection";
import "./PostCard.css";

interface PostCardProps {
  post: Post;
  onUpdate?: () => void;
}

const PostCard = ({ post, onUpdate }: PostCardProps) => {
  const { user } = useAuth();
  const [showComments, setShowComments] = useState(false);
  const [isLiked, setIsLiked] = useState(false);
  const [likesCount, setLikesCount] = useState(post.likesCount);
  const [commentsCount, setCommentsCount] = useState(post.commentsCount);
  const [sharesCount, setSharesCount] = useState(post.sharesCount);
  const [showShareSuccess, setShowShareSuccess] = useState(false);

  const [likePost, { loading: liking }] = useMutation(LIKE_POST);
  const [createComment] = useMutation(CREATE_COMMENT);
  const [sharePost, { loading: sharing }] = useMutation(SHARE_POST);

  const handleLike = async () => {
    if (!user) {
      alert("Please login to like posts");
      return;
    }

    try {
      const { data } = await likePost({ variables: { postId: post.id } });
      if (data?.likePost?.success) {
        setIsLiked(data.likePost.isLiked);
        setLikesCount((prev) => (data.likePost.isLiked ? prev + 1 : prev - 1));
      }
    } catch (error) {
      console.error("Like error:", error);
    }
  };

  const handleComment = async (content: string) => {
    if (!user) {
      alert("Please login to comment");
      return;
    }

    try {
      const { data } = await createComment({
        variables: { input: { postId: post.id, content } },
        refetchQueries: [
          { query: GET_POST_COMMENTS, variables: { postId: post.id } },
        ],
      });

      if (data?.createComment?.success) {
        setCommentsCount((prev) => prev + 1);
        onUpdate?.();
      }
    } catch (error) {
      console.error("Comment error:", error);
    }
  };

  const handleShare = async () => {
    if (!user) {
      alert("Please login to share posts");
      return;
    }

    const postUrl = `${window.location.origin}/post/${post.id}`;

    // Try native Web Share API first (works on mobile and some desktop browsers)
    if (navigator.share) {
      try {
        await navigator.share({
          title: `Post by @${post.author.username}`,
          text:
            post.content.substring(0, 100) +
            (post.content.length > 100 ? "..." : ""),
          url: postUrl,
        });

        // Track share in backend
        const { data } = await sharePost({ variables: { postId: post.id } });
        if (data?.sharePost?.success) {
          setSharesCount(data.sharePost.sharesCount);
        }
      } catch (error) {
        // User cancelled share or error occurred
        console.log("Share cancelled or failed:", error);
      }
    } else {
      // Fallback: Copy to clipboard
      try {
        await navigator.clipboard.writeText(postUrl);
        setShowShareSuccess(true);
        setTimeout(() => setShowShareSuccess(false), 2000);

        // Track share in backend
        const { data } = await sharePost({ variables: { postId: post.id } });
        if (data?.sharePost?.success) {
          setSharesCount(data.sharePost.sharesCount);
        }
      } catch (error) {
        console.error("Share error:", error);
        alert("Failed to copy link");
      }
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHours / 24);

    if (diffMins < 1) return "Just now";
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    return date.toLocaleDateString();
  };

  return (
    <motion.div
      className="post-card"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className="post-header">
        <div className="post-author">
          <div className="author-avatar">
            {post.author.profilePicture ? (
              <img
                src={post.author.profilePicture}
                alt={post.author.username}
              />
            ) : (
              <div className="avatar-placeholder">
                {post.author.username[0].toUpperCase()}
              </div>
            )}
          </div>
          <div className="author-info">
            <h4 className="author-name">@{post.author.username}</h4>
            <span className="post-time">{formatDate(post.createdAt)}</span>
          </div>
        </div>
      </div>

      <div className="post-content">
        <p>{post.content}</p>
        {post.mediaUrl && (
          <div className="post-media">
            {post.contentType === "image" || post.contentType === "mixed" ? (
              <img src={post.mediaUrl} alt="Post media" />
            ) : post.contentType === "video" ? (
              <video src={post.mediaUrl} controls />
            ) : null}
          </div>
        )}
      </div>

      <div className="post-actions">
        <motion.button
          className={`action-btn like-btn ${isLiked ? "liked" : ""}`}
          onClick={handleLike}
          disabled={liking}
          whileTap={{ scale: 0.9 }}
          whileHover={{ scale: 1.1 }}
        >
          <span className="icon">{isLiked ? "♥" : "♡"}</span>
          <span className="count">{likesCount}</span>
        </motion.button>

        <motion.button
          className="action-btn comment-btn"
          onClick={() => setShowComments(!showComments)}
          whileTap={{ scale: 0.9 }}
          whileHover={{ scale: 1.05 }}
        >
          <span className="count">{commentsCount} Comments</span>
        </motion.button>

        <motion.button
          className="action-btn share-btn"
          onClick={handleShare}
          disabled={sharing}
          whileTap={{ scale: 0.9 }}
          whileHover={{ scale: 1.05 }}
        >
          <span className="count">Share ({sharesCount})</span>
        </motion.button>

        {showShareSuccess && (
          <motion.div
            className="share-success"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
          >
            Link copied to clipboard!
          </motion.div>
        )}
      </div>

      {showComments && (
        <CommentSection postId={post.id} onAddComment={handleComment} />
      )}
    </motion.div>
  );
};

export default PostCard;
