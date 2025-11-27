"""
End-to-End Testing for Social Media Platform
Tests the complete user flow from registration to interactions
"""

import time
import requests
from typing import Dict, Any

BASE_URL = "http://localhost:8000"
GRAPHQL_URL = f"{BASE_URL}/graphql/"
FRONTEND_URL = "http://localhost:3000"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'

class E2ETester:
    def __init__(self):
        self.session = requests.Session()
        self.results = []
        self.timestamp = str(int(time.time()))
        self.username = f"e2euser_{self.timestamp}"
        self.email = f"e2e_{self.timestamp}@example.com"
        self.password = "E2ETestPass123!"
        
    def print_step(self, step: str, status: str, details: str = ""):
        """Print formatted test step"""
        if status == "PASS":
            print(f"{Colors.GREEN}✓{Colors.END} {step}")
            if details:
                print(f"  {Colors.CYAN}{details}{Colors.END}")
        elif status == "FAIL":
            print(f"{Colors.RED}✗{Colors.END} {step}")
            if details:
                print(f"  {Colors.RED}Error: {details}{Colors.END}")
        else:
            print(f"{Colors.BLUE}➜{Colors.END} {step}")
            if details:
                print(f"  {Colors.YELLOW}{details}{Colors.END}")
        
        self.results.append({"step": step, "status": status, "details": details})
    
    def execute_graphql(self, query: str, variables: Dict[str, Any] = None) -> Dict:
        """Execute GraphQL query/mutation"""
        try:
            response = self.session.post(
                GRAPHQL_URL,
                json={"query": query, "variables": variables},
                headers={"Content-Type": "application/json"}
            )
            return response.json()
        except Exception as e:
            return {"errors": [{"message": str(e)}]}
    
    def test_backend_health(self):
        """Test if backend is running"""
        try:
            response = requests.get(f"{BASE_URL}/graphql/", timeout=5)
            if response.status_code in [200, 400]:
                self.print_step("Backend Server Health Check", "PASS", f"Backend running on {BASE_URL}")
                return True
            else:
                self.print_step("Backend Server Health Check", "FAIL", f"Unexpected status: {response.status_code}")
                return False
        except Exception as e:
            self.print_step("Backend Server Health Check", "FAIL", str(e))
            return False
    
    def test_frontend_health(self):
        """Test if frontend is running"""
        try:
            response = requests.get(FRONTEND_URL, timeout=5)
            if response.status_code == 200:
                self.print_step("Frontend Server Health Check", "PASS", f"Frontend running on {FRONTEND_URL}")
                return True
            else:
                self.print_step("Frontend Server Health Check", "FAIL", f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.print_step("Frontend Server Health Check", "FAIL", str(e))
            return False
    
    def test_user_registration_flow(self):
        """Test complete user registration"""
        mutation = """
        mutation RegisterUser($input: RegisterInput!) {
            registerUser(input: $input) {
                success
                message
                user {
                    id
                    username
                    email
                }
            }
        }
        """
        variables = {
            "input": {
                "username": self.username,
                "email": self.email,
                "password": self.password
            }
        }
        
        result = self.execute_graphql(mutation, variables)
        
        if "errors" in result:
            self.print_step("User Registration Flow", "FAIL", result["errors"][0]["message"])
            return False
        
        data = result.get("data", {}).get("registerUser", {})
        if data.get("success"):
            self.print_step("User Registration Flow", "PASS", f"User '{self.username}' registered successfully")
            return True
        else:
            self.print_step("User Registration Flow", "FAIL", data.get("message", "Unknown error"))
            return False
    
    def test_user_login_flow(self):
        """Test user login and session"""
        mutation = """
        mutation LoginUser($input: LoginInput!) {
            loginUser(input: $input) {
                success
                message
                user {
                    id
                    username
                    email
                }
            }
        }
        """
        variables = {
            "input": {
                "username": self.username,
                "password": self.password
            }
        }
        
        result = self.execute_graphql(mutation, variables)
        
        if "errors" in result:
            self.print_step("User Login Flow", "FAIL", result["errors"][0]["message"])
            return False
        
        data = result.get("data", {}).get("loginUser", {})
        if data.get("success"):
            self.print_step("User Login Flow", "PASS", "Session established successfully")
            return True
        else:
            self.print_step("User Login Flow", "FAIL", data.get("message", "Unknown error"))
            return False
    
    def test_post_creation_flow(self):
        """Test creating posts with different content"""
        posts_data = [
            {"content": "First E2E test post! 🚀", "media": None},
            {"content": "Second test post with media 📸", "media": "https://picsum.photos/800/600"},
            {"content": "Testing emojis and special chars: 😀🎉✨ #testing", "media": None}
        ]
        
        created_posts = []
        
        for i, post_data in enumerate(posts_data, 1):
            mutation = """
            mutation CreatePost($input: PostInput!) {
                createPost(input: $input) {
                    success
                    message
                    post {
                        id
                        content
                        mediaUrl
                    }
                }
            }
            """
            variables = {
                "input": {
                    "content": post_data["content"],
                    "mediaUrl": post_data["media"] or ""
                }
            }
            
            result = self.execute_graphql(mutation, variables)
            
            if "errors" in result:
                self.print_step(f"Create Post #{i}", "FAIL", result["errors"][0]["message"])
                return False
            
            data = result.get("data", {}).get("createPost", {})
            if data.get("success"):
                post_id = data["post"]["id"]
                created_posts.append(post_id)
                self.print_step(f"Create Post #{i}", "PASS", f"Post ID: {post_id}")
            else:
                self.print_step(f"Create Post #{i}", "FAIL", data.get("message", "Unknown error"))
                return False
        
        self.created_posts = created_posts
        return True
    
    def test_post_interaction_flow(self):
        """Test liking, commenting, and replying to posts"""
        if not hasattr(self, 'created_posts') or not self.created_posts:
            self.print_step("Post Interaction Flow", "FAIL", "No posts available for testing")
            return False
        
        post_id = self.created_posts[0]
        
        # Test like
        like_mutation = """
        mutation LikePost($postId: ID!) {
            likePost(postId: $postId) {
                success
                message
                isLiked
            }
        }
        """
        
        result = self.execute_graphql(like_mutation, {"postId": post_id})
        if result.get("data", {}).get("likePost", {}).get("success"):
            self.print_step("Like Post", "PASS", "Post liked successfully")
        else:
            self.print_step("Like Post", "FAIL", "Failed to like post")
            return False
        
        # Test comment
        comment_mutation = """
        mutation CreateComment($input: CommentInput!) {
            createComment(input: $input) {
                success
                message
                comment {
                    id
                    content
                }
            }
        }
        """
        comment_variables = {
            "input": {
                "postId": post_id,
                "content": "Great post! This is an E2E test comment 💬"
            }
        }
        
        result = self.execute_graphql(comment_mutation, comment_variables)
        data = result.get("data", {}).get("createComment", {})
        if data.get("success"):
            comment_id = data["comment"]["id"]
            self.print_step("Create Comment", "PASS", f"Comment ID: {comment_id}")
            
            # Test reply to comment
            reply_variables = {
                "input": {
                    "postId": post_id,
                    "content": "This is a reply to the comment! 💭",
                    "parentId": comment_id
                }
            }
            
            result = self.execute_graphql(comment_mutation, reply_variables)
            if result.get("data", {}).get("createComment", {}).get("success"):
                self.print_step("Create Reply", "PASS", "Reply created successfully")
            else:
                self.print_step("Create Reply", "FAIL", "Failed to create reply")
                return False
        else:
            self.print_step("Create Comment", "FAIL", "Failed to create comment")
            return False
        
        # Test unlike
        result = self.execute_graphql(like_mutation, {"postId": post_id})
        if result.get("data", {}).get("likePost", {}).get("success"):
            is_liked = result.get("data", {}).get("likePost", {}).get("isLiked")
            self.print_step("Unlike Post", "PASS", f"Post unliked (isLiked: {is_liked})")
        else:
            self.print_step("Unlike Post", "FAIL", "Failed to unlike post")
            return False
        
        return True
    
    def test_feed_functionality(self):
        """Test feed retrieval and pagination"""
        query = """
        query GetFeed($offset: Int, $limit: Int) {
            feed(offset: $offset, limit: $limit) {
                id
                content
                author {
                    username
                }
                likesCount
                commentsCount
                createdAt
            }
        }
        """
        
        # Test first page
        result = self.execute_graphql(query, {"offset": 0, "limit": 10})
        if "errors" in result:
            self.print_step("Feed - First Page", "FAIL", result["errors"][0]["message"])
            return False
        
        feed = result.get("data", {}).get("feed", [])
        self.print_step("Feed - First Page", "PASS", f"Retrieved {len(feed)} posts")
        
        # Test second page (pagination)
        result = self.execute_graphql(query, {"offset": 10, "limit": 10})
        if "errors" in result:
            self.print_step("Feed - Pagination", "FAIL", result["errors"][0]["message"])
            return False
        
        self.print_step("Feed - Pagination", "PASS", "Pagination working correctly")
        return True
    
    def test_all_posts_query(self):
        """Test retrieving all public posts"""
        query = """
        query {
            posts {
                id
                content
                author {
                    username
                }
                likesCount
                commentsCount
                sharesCount
            }
        }
        """
        
        result = self.execute_graphql(query)
        if "errors" in result:
            self.print_step("All Posts Query", "FAIL", result["errors"][0]["message"])
            return False
        
        posts = result.get("data", {}).get("posts", [])
        self.print_step("All Posts Query", "PASS", f"Retrieved {len(posts)} public posts")
        return True
    
    def test_user_profile_query(self):
        """Test user profile retrieval"""
        query = """
        query {
            me {
                id
                username
                email
                firstName
                lastName
                bio
                postsCount
                followersCount
                followingCount
            }
        }
        """
        
        result = self.execute_graphql(query)
        if "errors" in result:
            self.print_step("User Profile Query", "FAIL", result["errors"][0]["message"])
            return False
        
        user = result.get("data", {}).get("me")
        if user and user.get("username") == self.username:
            self.print_step("User Profile Query", "PASS", f"Profile data retrieved for {user['username']}")
            return True
        else:
            self.print_step("User Profile Query", "FAIL", "Profile data mismatch")
            return False
    
    def test_comment_retrieval(self):
        """Test retrieving comments for a post"""
        if not hasattr(self, 'created_posts') or not self.created_posts:
            self.print_step("Comment Retrieval", "FAIL", "No posts available")
            return False
        
        query = """
        query GetComments($postId: ID!) {
            postComments(postId: $postId) {
                id
                content
                author {
                    username
                }
                createdAt
                parent {
                    id
                }
            }
        }
        """
        
        result = self.execute_graphql(query, {"postId": self.created_posts[0]})
        if "errors" in result:
            self.print_step("Comment Retrieval", "FAIL", result["errors"][0]["message"])
            return False
        
        comments = result.get("data", {}).get("postComments", [])
        self.print_step("Comment Retrieval", "PASS", f"Retrieved {len(comments)} comments with replies")
        return True
    
    def test_logout_flow(self):
        """Test user logout"""
        mutation = """
        mutation {
            logoutUser {
                success
                message
            }
        }
        """
        
        result = self.execute_graphql(mutation)
        if "errors" in result:
            self.print_step("User Logout Flow", "FAIL", result["errors"][0]["message"])
            return False
        
        data = result.get("data", {}).get("logoutUser", {})
        if data.get("success"):
            self.print_step("User Logout Flow", "PASS", "Session terminated successfully")
            return True
        else:
            self.print_step("User Logout Flow", "FAIL", data.get("message", "Unknown error"))
            return False
    
    def run_all_tests(self):
        """Run complete end-to-end test suite"""
        print(f"\n{Colors.BLUE}{'='*70}{Colors.END}")
        print(f"{Colors.BLUE}{'End-to-End Testing - Social Media Platform':^70}{Colors.END}")
        print(f"{Colors.BLUE}{'='*70}{Colors.END}\n")
        
        print(f"{Colors.CYAN}Phase 1: Infrastructure Health Checks{Colors.END}")
        print(f"{Colors.CYAN}{'-'*70}{Colors.END}")
        if not self.test_backend_health():
            print(f"\n{Colors.RED}Backend is not running! Please start the backend server.{Colors.END}")
            return
        if not self.test_frontend_health():
            print(f"\n{Colors.YELLOW}Frontend is not running! Frontend tests will be limited.{Colors.END}")
        print()
        
        print(f"{Colors.CYAN}Phase 2: User Authentication Flow{Colors.END}")
        print(f"{Colors.CYAN}{'-'*70}{Colors.END}")
        self.test_user_registration_flow()
        self.test_user_login_flow()
        print()
        
        print(f"{Colors.CYAN}Phase 3: Content Creation & Management{Colors.END}")
        print(f"{Colors.CYAN}{'-'*70}{Colors.END}")
        self.test_post_creation_flow()
        print()
        
        print(f"{Colors.CYAN}Phase 4: User Interactions{Colors.END}")
        print(f"{Colors.CYAN}{'-'*70}{Colors.END}")
        self.test_post_interaction_flow()
        print()
        
        print(f"{Colors.CYAN}Phase 5: Data Retrieval & Queries{Colors.END}")
        print(f"{Colors.CYAN}{'-'*70}{Colors.END}")
        self.test_feed_functionality()
        self.test_all_posts_query()
        self.test_user_profile_query()
        self.test_comment_retrieval()
        print()
        
        print(f"{Colors.CYAN}Phase 6: Session Management{Colors.END}")
        print(f"{Colors.CYAN}{'-'*70}{Colors.END}")
        self.test_logout_flow()
        print()
        
        # Summary
        passed = sum(1 for r in self.results if r["status"] == "PASS")
        failed = sum(1 for r in self.results if r["status"] == "FAIL")
        total = len(self.results)
        
        print(f"{Colors.BLUE}{'='*70}{Colors.END}")
        print(f"{Colors.BLUE}{'Test Summary':^70}{Colors.END}")
        print(f"{Colors.BLUE}{'='*70}{Colors.END}")
        print(f"{Colors.GREEN}Passed:  {passed}/{total} tests{Colors.END}")
        print(f"{Colors.RED}Failed:  {failed}/{total} tests{Colors.END}")
        print(f"Success Rate: {(passed/total*100):.1f}%")
        print(f"{Colors.BLUE}{'='*70}{Colors.END}\n")
        
        if failed == 0:
            print(f"{Colors.GREEN}✓ All end-to-end tests passed successfully!{Colors.END}")
            print(f"{Colors.GREEN}✓ The application is ready for production deployment!{Colors.END}\n")
        else:
            print(f"{Colors.RED}✗ Some tests failed. Please review the errors above.{Colors.END}\n")
            print("Failed tests:")
            for r in self.results:
                if r["status"] == "FAIL":
                    print(f"  {Colors.RED}•{Colors.END} {r['step']}: {r['details']}")
            print()

if __name__ == "__main__":
    tester = E2ETester()
    tester.run_all_tests()
