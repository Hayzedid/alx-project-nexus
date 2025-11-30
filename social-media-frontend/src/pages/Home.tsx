import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { useAuth } from "../context/AuthContext";
import "./Home.css";

const Home = () => {
  const { user } = useAuth();

  return (
    <div className="home-page">
      <div className="container">
        <motion.div
          className="hero-section"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <h1 className="hero-title">
            Welcome to <span className="gradient-text">SocialFeed</span>
          </h1>
          <p className="hero-subtitle">
            Connect, Share, and Engage with your community in real-time
          </p>

          <div className="hero-features">
            <div className="feature">
              <h3>Real-time Updates</h3>
              <p>See posts and interactions as they happen</p>
            </div>
            <div className="feature">
              <h3>Rich Interactions</h3>
              <p>Like, comment, and share with ease</p>
            </div>
            <div className="feature">
              <h3>Beautiful UI</h3>
              <p>Smooth animations and modern design</p>
            </div>
          </div>

          <div className="hero-cta">
            {user ? (
              <Link to="/feed" className="cta-btn primary">
                Go to Feed
              </Link>
            ) : (
              <>
                <Link to="/register" className="cta-btn primary">
                  Get Started
                </Link>
                <Link to="/login" className="cta-btn secondary">
                  Sign In
                </Link>
              </>
            )}
          </div>
        </motion.div>

        <motion.div
          className="tech-stack"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3, duration: 0.6 }}
        >
          <h2>Built with Modern Technologies</h2>
          <div className="tech-badges">
            <span className="tech-badge">React</span>
            <span className="tech-badge">TypeScript</span>
            <span className="tech-badge">GraphQL</span>
            <span className="tech-badge">Apollo Client</span>
            <span className="tech-badge">Framer Motion</span>
            <span className="tech-badge">React Router</span>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Home;
