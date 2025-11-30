import { useState } from "react";
import { motion } from "framer-motion";
import { useMutation } from "@apollo/client";
import { CREATE_POST, GET_POSTS } from "../graphql/queries";
import { ContentType, PrivacyLevel } from "../types";
import "./CreatePost.css";

interface CreatePostProps {
  onPostCreated?: () => void;
}

const CreatePost = ({ onPostCreated }: CreatePostProps) => {
  const [content, setContent] = useState("");
  const [contentType, setContentType] = useState<ContentType>("text");
  const [privacyLevel, setPrivacyLevel] = useState<PrivacyLevel>("public");
  const [mediaUrl, setMediaUrl] = useState("");
  const [showAdvanced, setShowAdvanced] = useState(false);

  const [createPost, { loading, error }] = useMutation(CREATE_POST, {
    refetchQueries: [{ query: GET_POSTS, variables: { limit: 20, offset: 0 } }],
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!content.trim()) {
      alert("Please enter some content");
      return;
    }

    try {
      const { data } = await createPost({
        variables: {
          input: {
            content,
            contentType,
            privacyLevel,
            mediaUrl: mediaUrl || undefined,
          },
        },
      });

      if (data?.createPost?.success) {
        setContent("");
        setMediaUrl("");
        setShowAdvanced(false);
        onPostCreated?.();
      }
    } catch (err) {
      console.error("Create post error:", err);
    }
  };

  return (
    <motion.div
      className="create-post"
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <h2 className="create-post-title">What's on your mind?</h2>

      <form onSubmit={handleSubmit} className="create-post-form">
        <textarea
          className="post-textarea"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="Share your thoughts..."
          rows={4}
          maxLength={1000}
        />

        <div className="char-count">{content.length}/1000</div>

        <button
          type="button"
          className="toggle-advanced"
          onClick={() => setShowAdvanced(!showAdvanced)}
        >
          {showAdvanced ? "− Hide Options" : "+ More Options"}
        </button>

        {showAdvanced && (
          <motion.div
            className="advanced-options"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
          >
            <div className="form-group">
              <label>Media URL (Optional)</label>
              <input
                type="url"
                value={mediaUrl}
                onChange={(e) => setMediaUrl(e.target.value)}
                placeholder="https://example.com/image.jpg"
                className="form-input"
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Content Type</label>
                <select
                  value={contentType}
                  onChange={(e) =>
                    setContentType(e.target.value as ContentType)
                  }
                  className="form-select"
                  aria-label="Content type"
                  title="Select content type"
                >
                  <option value="text">Text</option>
                  <option value="image">Image</option>
                  <option value="video">Video</option>
                  <option value="mixed">Mixed</option>
                </select>
              </div>

              <div className="form-group">
                <label>Privacy</label>
                <select
                  value={privacyLevel}
                  onChange={(e) =>
                    setPrivacyLevel(
                      e.target.value as "public" | "private" | "followers"
                    )
                  }
                  className="privacy-select"
                  aria-label="Privacy level"
                  title="Select privacy level"
                >
                  <option value="public">🌍 Public</option>
                  <option value="followers">👥 Followers</option>
                  <option value="private">🔒 Private</option>
                </select>
              </div>
            </div>
          </motion.div>
        )}

        {error && <div className="error-message">{error.message}</div>}

        <button
          type="submit"
          className="submit-btn"
          disabled={loading || !content.trim()}
        >
          {loading ? (
            <>
              <span className="loading-spinner"></span>
              Posting...
            </>
          ) : (
            "Post"
          )}
        </button>
      </form>
    </motion.div>
  );
};

export default CreatePost;
