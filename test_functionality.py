"""
Comprehensive Functionality Test Script
Tests all backend and frontend functionality
"""

import requests
import json
from datetime import datetime

# Configuration
API_URL = 'http://localhost:8000/graphql/'

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

class TestResult:
    """Track test results"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def add_pass(self, test_name):
        self.passed += 1
        print(f"{Colors.GREEN}✓{Colors.END} {test_name}")
    
    def add_fail(self, test_name, error):
        self.failed += 1
        self.errors.append((test_name, error))
        print(f"{Colors.RED}✗{Colors.END} {test_name}: {error}")
    
    def summary(self):
        total = self.passed + self.failed
        success_rate = (self.passed / total * 100) if total > 0 else 0
        
        print(f"\n{Colors.BOLD}{'=' * 60}{Colors.END}")
        print(f"{Colors.BOLD}TEST SUMMARY{Colors.END}")
        print(f"{'=' * 60}")
        print(f"Total Tests: {total}")
        print(f"{Colors.GREEN}Passed: {self.passed}{Colors.END}")
        print(f"{Colors.RED}Failed: {self.failed}{Colors.END}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if self.errors:
            print(f"\n{Colors.RED}Failed Tests:{Colors.END}")
            for test_name, error in self.errors:
                print(f"  - {test_name}: {error}")
        
        print(f"{'=' * 60}\n")

def graphql_query(query, variables=None):
    """Execute a GraphQL query"""
    try:
        response = requests.post(
            API_URL,
            json={'query': query, 'variables': variables or {}},
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        return response.json()
    except Exception as e:
        return {'errors': [{'message': str(e)}]}

def test_backend_connectivity(results):
    """Test if backend server is running"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}Testing Backend Connectivity{Colors.END}")
    print("-" * 60)
    
    try:
        response = requests.get('http://localhost:8000/graphql/', timeout=5)
        if response.status_code in [200, 405]:  # 405 is expected for GET on POST endpoint
            results.add_pass("Backend server is running")
        else:
            results.add_fail("Backend server connectivity", f"Status code: {response.status_code}")
    except Exception as e:
        results.add_fail("Backend server connectivity", str(e))

def test_query_all_posts(results):
    """Test querying all posts"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}Testing GraphQL Queries{Colors.END}")
    print("-" * 60)
    
    query = '''
        query {
            posts(limit: 10, offset: 0) {
                id
                content
                author {
                    username
                    fullName
                }
                likesCount
                commentsCount
                sharesCount
                createdAt
            }
        }
    '''
    
    result = graphql_query(query)
    
    if 'errors' in result:
        results.add_fail("Query all posts", result['errors'][0]['message'])
    elif 'data' in result and 'posts' in result['data']:
        posts = result['data']['posts']
        results.add_pass(f"Query all posts (found {len(posts)} posts)")
    else:
        results.add_fail("Query all posts", "Unexpected response format")

def test_query_users(results):
    """Test querying users"""
    query = '''
        query {
            users(search: "demo") {
                id
                username
                email
                fullName
                followersCount
                followingCount
                postsCount
            }
        }
    '''
    
    result = graphql_query(query)
    
    if 'errors' in result:
        results.add_fail("Query users", result['errors'][0]['message'])
    elif 'data' in result and 'users' in result['data']:
        users = result['data']['users']
        results.add_pass(f"Query users (found {len(users)} users)")
    else:
        results.add_fail("Query users", "Unexpected response format")

def test_user_registration(results):
    """Test user registration mutation"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}Testing Mutations{Colors.END}")
    print("-" * 60)
    
    mutation = '''
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
    '''
    
    variables = {
        'input': {
            'username': f'testuser_{datetime.now().timestamp()}',
            'email': f'test_{datetime.now().timestamp()}@example.com',
            'password': 'testpass123'
        }
    }
    
    result = graphql_query(mutation, variables)
    
    if 'errors' in result:
        results.add_fail("User registration", result['errors'][0]['message'])
    elif result.get('data', {}).get('registerUser', {}).get('success'):
        results.add_pass("User registration")
    else:
        message = result.get('data', {}).get('registerUser', {}).get('message', 'Unknown error')
        results.add_fail("User registration", message)

def test_database_models(results):
    """Test database models"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}Testing Database Models{Colors.END}")
    print("-" * 60)
    
    # Test if we can query data which means models are working
    queries = [
        ("User Model", '''
            query { users(search: "") { id username } }
        '''),
        ("Post Model", '''
            query { posts(limit: 1) { id content } }
        '''),
    ]
    
    for name, query in queries:
        result = graphql_query(query)
        if 'errors' not in result and 'data' in result:
            results.add_pass(name)
        else:
            error = result.get('errors', [{}])[0].get('message', 'Unknown error')
            results.add_fail(name, error)

def test_interaction_queries(results):
    """Test interaction-related queries"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}Testing Interactions{Colors.END}")
    print("-" * 60)
    
    # First get a post ID
    posts_query = 'query { posts(limit: 1) { id } }'
    posts_result = graphql_query(posts_query)
    
    if 'data' not in posts_result or not posts_result['data']['posts']:
        results.add_fail("Get post for interaction test", "No posts available")
        return
    
    post_id = posts_result['data']['posts'][0]['id']
    
    # Test likes query
    likes_query = f'''
        query {{
            postLikes(postId: "{post_id}") {{
                user {{ username }}
                createdAt
            }}
        }}
    '''
    
    likes_result = graphql_query(likes_query)
    if 'errors' not in likes_result and 'data' in likes_result:
        likes = likes_result['data'].get('postLikes', [])
        results.add_pass(f"Query post likes (found {len(likes)} likes)")
    else:
        results.add_fail("Query post likes", "Failed to query likes")
    
    # Test comments query
    comments_query = f'''
        query {{
            postComments(postId: "{post_id}") {{
                content
                author {{ username }}
            }}
        }}
    '''
    
    comments_result = graphql_query(comments_query)
    if 'errors' not in comments_result and 'data' in comments_result:
        comments = comments_result['data'].get('postComments', [])
        results.add_pass(f"Query post comments (found {len(comments)} comments)")
    else:
        results.add_fail("Query post comments", "Failed to query comments")

def test_follow_queries(results):
    """Test follow-related queries"""
    # First get a user ID
    users_query = 'query { users(search: "") { id } }'
    users_result = graphql_query(users_query)
    
    if 'data' not in users_result or not users_result['data']['users']:
        results.add_fail("Get user for follow test", "No users available")
        return
    
    user_id = users_result['data']['users'][0]['id']
    
    # Test followers query
    followers_query = f'''
        query {{
            userFollowers(userId: "{user_id}") {{
                username
            }}
        }}
    '''
    
    followers_result = graphql_query(followers_query)
    if 'errors' not in followers_result and 'data' in followers_result:
        followers = followers_result['data'].get('userFollowers', [])
        results.add_pass(f"Query user followers (found {len(followers)} followers)")
    else:
        results.add_fail("Query user followers", "Failed to query followers")
    
    # Test following query
    following_query = f'''
        query {{
            userFollowing(userId: "{user_id}") {{
                username
            }}
        }}
    '''
    
    following_result = graphql_query(following_query)
    if 'errors' not in following_result and 'data' in following_result:
        following = following_result['data'].get('userFollowing', [])
        results.add_pass(f"Query user following (found {len(following)} following)")
    else:
        results.add_fail("Query user following", "Failed to query following")

def test_frontend_files(results):
    """Test frontend files existence"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}Testing Frontend{Colors.END}")
    print("-" * 60)
    
    import os
    frontend_path = os.path.join(os.path.dirname(__file__), '..', 'social-media-frontend')
    
    files_to_check = [
        'index.html',
        'package.json',
        'README.md'
    ]
    
    for file in files_to_check:
        file_path = os.path.join(frontend_path, file)
        if os.path.exists(file_path):
            results.add_pass(f"Frontend file exists: {file}")
        else:
            results.add_fail(f"Frontend file exists: {file}", "File not found")

def main():
    """Run all tests"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}SOCIAL MEDIA PLATFORM - COMPREHENSIVE FUNCTIONALITY TEST{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.END}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = TestResult()
    
    # Run all tests
    test_backend_connectivity(results)
    test_query_all_posts(results)
    test_query_users(results)
    test_user_registration(results)
    test_database_models(results)
    test_interaction_queries(results)
    test_follow_queries(results)
    test_frontend_files(results)
    
    # Print summary
    results.summary()
    
    return results.failed == 0

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
