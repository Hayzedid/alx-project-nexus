import { useEffect } from "react";
import { useQuery } from "@apollo/client";
import { motion } from "framer-motion";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import { GET_ME } from "../graphql/queries";
import "./Profile.css";

const Profile = () => {
  const { user, loading: authLoading } = useAuth();
  const navigate = useNavigate();
  const { data, loading } = useQuery(GET_ME, {
    skip: !user,
  });

  useEffect(() => {
    if (!authLoading && !user) {
      navigate("/login");
    }
  }, [user, authLoading, navigate]);

  if (authLoading || loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
      </div>
    );
  }

  if (!user) return null;

  const profileData = data?.me || user;

  return (
    <div className="profile-page">
      <div className="container">
        <motion.div
          className="profile-card"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="profile-header">
            <div className="profile-avatar">
              {profileData.profilePicture ? (
                <img
                  src={profileData.profilePicture}
                  alt={profileData.username}
                />
              ) : (
                <div className="avatar-placeholder">
                  {profileData.username[0].toUpperCase()}
                </div>
              )}
            </div>
            <div className="profile-info">
              <h1 className="profile-name">
                @{profileData.username}
                {profileData.isVerified && (
                  <span className="verified-badge">Verified</span>
                )}
              </h1>
              <p className="profile-email">{profileData.email}</p>
            </div>
          </div>

          {profileData.bio && (
            <div className="profile-bio">
              <p>{profileData.bio}</p>
            </div>
          )}

          <div className="profile-stats">
            <div className="stat">
              <span className="stat-value">{profileData.postsCount || 0}</span>
              <span className="stat-label">Posts</span>
            </div>
            <div className="stat">
              <span className="stat-value">
                {profileData.followersCount || 0}
              </span>
              <span className="stat-label">Followers</span>
            </div>
            <div className="stat">
              <span className="stat-value">
                {profileData.followingCount || 0}
              </span>
              <span className="stat-label">Following</span>
            </div>
          </div>

          <div className="profile-actions">
            <button className="btn btn-primary">Edit Profile</button>
            <button className="btn btn-outline">Settings</button>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Profile;
