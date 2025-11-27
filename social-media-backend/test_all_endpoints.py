"""
Comprehensive endpoint testing for Social Media Backend
Tests all GraphQL mutations and queries
"""

import requests
import json
import time
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"
GRAPHQL_URL = f"{BASE_URL}/graphql/"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

class EndpointTester:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        self.user_id = None
        self.post_id = None
        self.comment_id = None
        self.timestamp = str(int(time.time()))
        
    def print_test(self, name: str, status: str, message: str = ""):
        """Print formatted test result"""
        if status == "PASS":
            print(f"{Colors.GREEN}✓{Colors.END} {name}: {Colors.GREEN}PASSED{Colors.END}")
        elif status == "FAIL":
            print(f"{Colors.RED}✗{Colors.END} {name}: {Colors.RED}FAILED{Colors.END}")
            if message:
                print(f"  {Colors.YELLOW}Error: {message}{Colors.END}")
        else:
            print(f"{Colors.BLUE}ℹ{Colors.END} {name}: {Colors.BLUE}{status}{Colors.END}")
        
        self.test_results.append({
            "name": name,
            "status": status,
            "message": message
        })
    
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
    
    def test_1_register_user(self):
        """Test user registration"""
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
                "username": f"testuser_{self.timestamp}",
                "email": f"test_{self.timestamp}@example.com",
                "password": "TestPass123!"
            }
        }
        
        result = self.execute_graphql(mutation, variables)
        
        if "errors" in result:
            self.print_test("User Registration", "FAIL", result["errors"][0]["message"])
            return False
        
        data = result.get("data", {}).get("registerUser", {})
        if data.get("success"):
            self.user_id = data["user"]["id"]
            self.print_test("User Registration", "PASS")
            return True
        else:
            self.print_test("User Registration", "FAIL", data.get("message", "Unknown error"))
            return False
    
    def test_2_login_user(self):
        """Test user login"""
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
                "username": f"testuser_{self.timestamp}",
                "password": "TestPass123!"
            }
        }
        
        result = self.execute_graphql(mutation, variables)
        
        if "errors" in result:
            self.print_test("User Login", "FAIL", result["errors"][0]["message"])
            return False
        
        data = result.get("data", {}).get("loginUser", {})
        if data.get("success"):
            self.print_test("User Login", "PASS")
            return True
        else:
            self.print_test("User Login", "FAIL", data.get("message", "Unknown error"))
            return False
    
    def test_3_get_current_user(self):
        """Test getting current user info"""
        query = """
        query {
            me {
                id
                username
                email
                firstName
                lastName
            }
        }
        """
        
        result = self.execute_graphql(query)
        
        if "errors" in result:
            self.print_test("Get Current User", "FAIL", result["errors"][0]["message"])
            return False
        
        data = result.get("data", {}).get("me")
        if data and data.get("username"):
            self.print_test("Get Current User", "PASS")
            return True
        else:
            self.print_test("Get Current User", "FAIL", "No user data returned")
            return False
    
    def test_4_create_post(self):
        """Test creating a post"""
        mutation = """
        mutation CreatePost($input: PostInput!) {
            createPost(input: $input) {
                success
                message
                post {
                    id
                    content
                    mediaUrl
                    author {
                        username
                    }
                }
            }
        }
        """
        variables = {
            "input": {
                "content": "This is a comprehensive test post for endpoint testing! 🚀",
                "mediaUrl": "https://example.com/test-image.jpg"
            }
        }
        
        result = self.execute_graphql(mutation, variables)
        
        if "errors" in result:
            self.print_test("Create Post", "FAIL", result["errors"][0]["message"])
            return False
        
        data = result.get("data", {}).get("createPost", {})
        if data.get("success"):
            self.post_id = data["post"]["id"]
            self.print_test("Create Post", "PASS")
            return True
        else:
            self.print_test("Create Post", "FAIL", data.get("message", "Unknown error"))
            return False
    
    def test_5_get_all_posts(self):
        """Test getting all posts"""
        query = """
        query {
            posts {
                id
                content
                mediaUrl
                author {
                    username
                }
                likesCount
                commentsCount
            }
        }
        """
        
        result = self.execute_graphql(query)
        
        if "errors" in result:
            self.print_test("Get All Posts", "FAIL", result["errors"][0]["message"])
            return False
        
        data = result.get("data", {}).get("posts", [])
        if isinstance(data, list) and len(data) > 0:
            self.print_test("Get All Posts", "PASS")
            return True
        else:
            self.print_test("Get All Posts", "FAIL", "No posts returned")
            return False
    
    def test_6_get_feed(self):
        """Test getting personalized feed"""
        query = """
        query GetFeed($offset: Int, $limit: Int) {
            feed(offset: $offset, limit: $limit) {
                id
                content
                author {
                    username
                }
                createdAt
            }
        }
        """
        variables = {"offset": 0, "limit": 10}
        
        result = self.execute_graphql(query, variables)
        
        if "errors" in result:
            self.print_test("Get Feed", "FAIL", result["errors"][0]["message"])
            return False
        
        data = result.get("data", {}).get("feed", [])
        if isinstance(data, list):
            self.print_test("Get Feed", "PASS")
            return True
        else:
            self.print_test("Get Feed", "FAIL", "Invalid feed data")
            return False
    
    def test_7_like_post(self):
        """Test liking a post"""
        if not self.post_id:
            self.print_test("Like Post", "SKIP", "No post ID available")
            return False
        
        mutation = """
        mutation LikePost($postId: ID!) {
            likePost(postId: $postId) {
                success
                message
                isLiked
            }
        }
        """
        variables = {"postId": self.post_id}
        
        result = self.execute_graphql(mutation, variables)
        
        if "errors" in result:
            self.print_test("Like Post", "FAIL", result["errors"][0]["message"])
            return False
        
        data = result.get("data", {}).get("likePost", {})
        if data.get("success"):
            self.print_test("Like Post", "PASS")
            return True
        else:
            self.print_test("Like Post", "FAIL", data.get("message", "Unknown error"))
            return False
    
    def test_8_create_comment(self):
        """Test creating a comment"""
        if not self.post_id:
            self.print_test("Create Comment", "SKIP", "No post ID available")
            return False
        
        mutation = """
        mutation CreateComment($input: CommentInput!) {
            createComment(input: $input) {
                success
                message
                comment {
                    id
                    content
                    author {
                        username
                    }
                }
            }
        }
        """
        variables = {
            "input": {
                "postId": self.post_id,
                "content": "This is a test comment for endpoint testing! 💬"
            }
        }
        
        result = self.execute_graphql(mutation, variables)
        
        if "errors" in result:
            self.print_test("Create Comment", "FAIL", result["errors"][0]["message"])
            return False
        
        data = result.get("data", {}).get("createComment", {})
        if data.get("success"):
            self.comment_id = data["comment"]["id"]
            self.print_test("Create Comment", "PASS")
            return True
        else:
            self.print_test("Create Comment", "FAIL", data.get("message", "Unknown error"))
            return False
    
    def test_9_get_post_comments(self):
        """Test getting comments for a post"""
        if not self.post_id:
            self.print_test("Get Post Comments", "SKIP", "No post ID available")
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
            }
        }
        """
        variables = {"postId": self.post_id}
        
        result = self.execute_graphql(query, variables)
        
        if "errors" in result:
            self.print_test("Get Post Comments", "FAIL", result["errors"][0]["message"])
            return False
        
        data = result.get("data", {}).get("postComments", [])
        if isinstance(data, list) and len(data) > 0:
            self.print_test("Get Post Comments", "PASS")
            return True
        else:
            self.print_test("Get Post Comments", "FAIL", "No comments returned")
            return False
    
    def test_10_create_reply(self):
        """Test creating a reply to a comment"""
        if not self.post_id or not self.comment_id:
            self.print_test("Create Reply", "SKIP", "No post/comment ID available")
            return False
        
        mutation = """
        mutation CreateComment($input: CommentInput!) {
            createComment(input: $input) {
                success
                message
                comment {
                    id
                    content
                    parent {
                        id
                    }
                }
            }
        }
        """
        variables = {
            "input": {
                "postId": self.post_id,
                "content": "This is a test reply! 💭",
                "parentId": self.comment_id
            }
        }
        
        result = self.execute_graphql(mutation, variables)
        
        if "errors" in result:
            self.print_test("Create Reply", "FAIL", result["errors"][0]["message"])
            return False
        
        data = result.get("data", {}).get("createComment", {})
        if data.get("success"):
            self.print_test("Create Reply", "PASS")
            return True
        else:
            self.print_test("Create Reply", "FAIL", data.get("message", "Unknown error"))
            return False
    
    def test_11_unlike_post(self):
        """Test unliking a post"""
        if not self.post_id:
            self.print_test("Unlike Post", "SKIP", "No post ID available")
            return False
        
        mutation = """
        mutation LikePost($postId: ID!) {
            likePost(postId: $postId) {
                success
                message
                isLiked
            }
        }
        """
        variables = {"postId": self.post_id}
        
        result = self.execute_graphql(mutation, variables)
        
        if "errors" in result:
            self.print_test("Unlike Post", "FAIL", result["errors"][0]["message"])
            return False
        
        data = result.get("data", {}).get("likePost", {})
        if data.get("success"):
            self.print_test("Unlike Post", "PASS")
            return True
        else:
            self.print_test("Unlike Post", "FAIL", data.get("message", "Unknown error"))
            return False
    
    def test_12_logout(self):
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
            self.print_test("User Logout", "FAIL", result["errors"][0]["message"])
            return False
        
        data = result.get("data", {}).get("logoutUser", {})
        if data.get("success"):
            self.print_test("User Logout", "PASS")
            return True
        else:
            self.print_test("User Logout", "FAIL", data.get("message", "Unknown error"))
            return False
    
    def run_all_tests(self):
        """Run all endpoint tests"""
        print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
        print(f"{Colors.BLUE}Starting Comprehensive Endpoint Testing{Colors.END}")
        print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")
        
        # Run tests in sequence
        tests = [
            self.test_1_register_user,
            self.test_2_login_user,
            self.test_3_get_current_user,
            self.test_4_create_post,
            self.test_5_get_all_posts,
            self.test_6_get_feed,
            self.test_7_like_post,
            self.test_8_create_comment,
            self.test_9_get_post_comments,
            self.test_10_create_reply,
            self.test_11_unlike_post,
            self.test_12_logout
        ]
        
        for test in tests:
            test()
            print()
        
        # Print summary
        passed = sum(1 for r in self.test_results if r["status"] == "PASS")
        failed = sum(1 for r in self.test_results if r["status"] == "FAIL")
        skipped = sum(1 for r in self.test_results if r["status"] == "SKIP")
        
        print(f"{Colors.BLUE}{'='*60}{Colors.END}")
        print(f"{Colors.BLUE}Test Summary{Colors.END}")
        print(f"{Colors.BLUE}{'='*60}{Colors.END}")
        print(f"{Colors.GREEN}Passed: {passed}{Colors.END}")
        print(f"{Colors.RED}Failed: {failed}{Colors.END}")
        print(f"{Colors.YELLOW}Skipped: {skipped}{Colors.END}")
        print(f"Total: {len(self.test_results)}")
        print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")
        
        if failed == 0:
            print(f"{Colors.GREEN}✓ All tests passed successfully!{Colors.END}\n")
        else:
            print(f"{Colors.RED}✗ Some tests failed. Please review the errors above.{Colors.END}\n")

if __name__ == "__main__":
    tester = EndpointTester()
    tester.run_all_tests()
