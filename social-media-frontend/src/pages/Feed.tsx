import { useState, useEffect } from 'react';
import { useQuery } from '@apollo/client';
import { motion } from 'framer-motion';
import { useInView } from 'react-intersection-observer';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { GET_POSTS } from '../graphql/queries';
import { Post } from '../types';
import CreatePost from '../components/CreatePost';
import PostCard from '../components/PostCard';
import './Feed.css';

const Feed = () => {
  const { user, loading: authLoading } = useAuth();
  const navigate = useNavigate();
  const [posts, setPosts] = useState<Post[]>([]);
  const [offset, setOffset] = useState(0);
  const [hasMore, setHasMore] = useState(true);

  const { data, loading, error, fetchMore } = useQuery(GET_POSTS, {
    variables: { limit: 10, offset: 0 },
  });

  const { ref, inView } = useInView({
    threshold: 0.5,
  });

  useEffect(() => {
    if (!authLoading && !user) {
      navigate('/login');
    }
  }, [user, authLoading, navigate]);

  useEffect(() => {
    if (data?.posts) {
      setPosts(data.posts);
    }
  }, [data]);

  useEffect(() => {
    if (inView && hasMore && !loading) {
      loadMore();
    }
  }, [inView, hasMore, loading]);

  const loadMore = async () => {
    try {
      const { data: newData } = await fetchMore({
        variables: {
          offset: offset + 10,
          limit: 10,
        },
      });

      if (newData?.posts && newData.posts.length > 0) {
        setPosts((prev) => [...prev, ...newData.posts]);
        setOffset((prev) => prev + 10);
      } else {
        setHasMore(false);
      }
    } catch (err) {
      console.error('Error loading more posts:', err);
    }
  };

  const handlePostCreated = () => {
    setOffset(0);
    setHasMore(true);
  };

  if (authLoading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <div className="feed-page">
      <div className="container">
        <div className="feed-header">
          <h1 className="gradient-text">Your Feed</h1>
          <p className="feed-subtitle">Stay connected with the latest updates</p>
        </div>

        <CreatePost onPostCreated={handlePostCreated} />

        <div className="posts-container">
          {loading && posts.length === 0 ? (
            <div className="loading-container">
              <div className="loading-spinner"></div>
              <p>Loading posts...</p>
            </div>
          ) : error ? (
            <div className="error-message">
              Error loading posts: {error.message}
            </div>
          ) : posts.length === 0 ? (
            <motion.div
              className="no-posts"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
            >
              <span className="no-posts-icon">📝</span>
              <h3>No posts yet</h3>
              <p>Be the first to share something!</p>
            </motion.div>
          ) : (
            <>
              {posts.map((post, index) => (
                <PostCard key={`${post.id}-${index}`} post={post} onUpdate={handlePostCreated} />
              ))}

              {hasMore && (
                <div ref={ref} className="load-more-trigger">
                  {loading && (
                    <div className="loading-container">
                      <div className="loading-spinner"></div>
                      <p>Loading more posts...</p>
                    </div>
                  )}
                </div>
              )}

              {!hasMore && posts.length > 0 && (
                <div className="end-of-feed">
                  <p>You've reached the end! 🎉</p>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default Feed;
