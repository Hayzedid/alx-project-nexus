import { useState } from "react";
import { useQuery } from "@apollo/client";
import { motion, AnimatePresence } from "framer-motion";
import { GET_POST_COMMENTS } from "../graphql/queries";
import { Comment } from "../types";
import "./CommentSection.css";

interface CommentSectionProps {
  postId: string;
  onAddComment: (content: string) => void;
}

const CommentSection = ({ postId, onAddComment }: CommentSectionProps) => {
  const [commentText, setCommentText] = useState("");
  const { data, loading } = useQuery(GET_POST_COMMENTS, {
    variables: { postId },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (commentText.trim()) {
      onAddComment(commentText);
      setCommentText("");
    }
  };

  const comments: Comment[] = data?.postComments || [];

  return (
    <motion.div
      className="comment-section"
      initial={{ opacity: 0, height: 0 }}
      animate={{ opacity: 1, height: "auto" }}
      exit={{ opacity: 0, height: 0 }}
      transition={{ duration: 0.3 }}
    >
      <form onSubmit={handleSubmit} className="comment-form">
        <input
          type="text"
          value={commentText}
          onChange={(e) => setCommentText(e.target.value)}
          placeholder="Write a comment..."
          className="comment-input"
        />
        <button
          type="submit"
          className="comment-submit"
          disabled={!commentText.trim()}
        >
          Post
        </button>
      </form>

      <div className="comments-list">
        {loading ? (
          <div className="loading-comments">Loading comments...</div>
        ) : comments.length === 0 ? (
          <div className="no-comments">
            No comments yet. Be the first to comment!
          </div>
        ) : (
          <AnimatePresence>
            {comments.map((comment) => (
              <motion.div
                key={comment.id}
                className="comment"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                transition={{ duration: 0.2 }}
              >
                <div className="comment-avatar">
                  {comment.user.profilePicture ? (
                    <img
                      src={comment.user.profilePicture}
                      alt={comment.user.username}
                    />
                  ) : (
                    <div className="avatar-placeholder">
                      {comment.user.username[0].toUpperCase()}
                    </div>
                  )}
                </div>
                <div className="comment-content">
                  <div className="comment-header">
                    <span className="comment-author">
                      @{comment.user.username}
                    </span>
                    <span className="comment-time">
                      {new Date(comment.createdAt).toLocaleDateString()}
                    </span>
                  </div>
                  <p className="comment-text">{comment.content}</p>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
        )}
      </div>
    </motion.div>
  );
};

export default CommentSection;
