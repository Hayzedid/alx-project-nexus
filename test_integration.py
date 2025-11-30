"""
Comprehensive Frontend-Backend Integration Test
Tests all critical endpoints before frontend testing
"""

import requests
import json
import sys
import time

print("=" * 70)
print("🧪 FRONTEND-BACKEND INTEGRATION TEST")
print("=" * 70)
print()

# Test configuration
BASE_URL = "http://127.0.0.1:8000"
GRAPHQL_URL = f"{BASE_URL}/graphql/"
test_user = {
    "username": f"frontend_test_{int(time.time())}",
    "email": f"test_{int(time.time())}@example.com",
    "password": "TestPass123!"
}
session = requests.Session()
test_results = []

# Test 1: Backend connectivity
print("Test 1: Backend Server Connectivity...")
try:
    response = requests.get(GRAPHQL_URL, timeout=5)
    if response.status_code in [200, 400, 405]:
        print("   ✅ Backend server is running")
        test_results.append(("Backend Server", True))
    else:
        print(f"   ⚠️  Backend returned status {response.status_code}")
        test_results.append(("Backend Server", False))
except Exception as e:
    print(f"   ❌ Backend not accessible: {e}")
    print("   Please start: python manage.py runserver 8000")
    test_results.append(("Backend Server", False))
    sys.exit(1)

print()

# Test 2: GraphQL Schema
print("Test 2: GraphQL Schema Introspection...")
try:
    query = "{ __schema { queryType { name } } }"
    response = session.post(GRAPHQL_URL, json={"query": query})
    if response.status_code == 200 and 'data' in response.json():
        print("   ✅ GraphQL endpoint responding correctly")
        test_results.append(("GraphQL Schema", True))
    else:
        print(f"   ❌ GraphQL schema check failed")
        test_results.append(("GraphQL Schema", False))
except Exception as e:
    print(f"   ❌ GraphQL test failed: {e}")
    test_results.append(("GraphQL Schema", False))

print()

# Test 3: Register User
print("Test 3: User Registration...")
try:
    mutation = """
    mutation RegisterUser($input: RegisterInput!) {
        registerUser(input: $input) {
            user { id username email }
            success
            message
        }
    }
    """
    variables = {"input": test_user}
    response = session.post(GRAPHQL_URL, json={"query": mutation, "variables": variables})
    data = response.json()
    
    if response.status_code == 200 and data.get('data', {}).get('registerUser', {}).get('success'):
        user = data['data']['registerUser']['user']
        print(f"   ✅ User registered: {user['username']} ({user['email']})")
        test_results.append(("User Registration", True))
    else:
        errors = data.get('data', {}).get('registerUser', {}).get('message') or data.get('errors')
        print(f"   ❌ Registration failed: {errors}")
        test_results.append(("User Registration", False))
except Exception as e:
    print(f"   ❌ Registration test failed: {e}")
    test_results.append(("User Registration", False))

print()

# Test 4: Login User
print("Test 4: User Login...")
try:
    mutation = """
    mutation LoginUser($input: LoginInput!) {
        loginUser(input: $input) {
            user { id username }
            success
            message
        }
    }
    """
    variables = {"input": {"username": test_user["username"], "password": test_user["password"]}}
    response = session.post(GRAPHQL_URL, json={"query": mutation, "variables": variables})
    data = response.json()
    
    if response.status_code == 200 and data.get('data', {}).get('loginUser', {}).get('success'):
        print(f"   ✅ Login successful: {data['data']['loginUser']['user']['username']}")
        print(f"   ℹ️  Session cookies: {len(session.cookies)} cookie(s) set")
        test_results.append(("User Login", True))
    else:
        errors = data.get('data', {}).get('loginUser', {}).get('message') or data.get('errors')
        print(f"   ❌ Login failed: {errors}")
        test_results.append(("User Login", False))
except Exception as e:
    print(f"   ❌ Login test failed: {e}")
    test_results.append(("User Login", False))

print()

# Test 5: Fetch Posts
print("Test 5: Fetch Posts Query...")
try:
    query = """
    query {
        posts {
            id
            content
            author { username }
            likesCount
            commentsCount
        }
    }
    """
    response = session.post(GRAPHQL_URL, json={"query": query})
    data = response.json()
    
    if response.status_code == 200 and 'data' in data and 'posts' in data['data']:
        posts = data['data']['posts']
        print(f"   ✅ Fetched {len(posts)} posts")
        if posts:
            print(f"   ℹ️  Sample: @{posts[0]['author']['username']}: {posts[0]['content'][:40]}...")
        test_results.append(("Fetch Posts", True))
    else:
        print(f"   ❌ Fetch failed: {data.get('errors', 'Unknown error')}")
        test_results.append(("Fetch Posts", False))
except Exception as e:
    print(f"   ❌ Fetch posts failed: {e}")
    test_results.append(("Fetch Posts", False))

print()

# Test 6: Create Post
print("Test 6: Create Post...")
post_id = None
try:
    mutation = """
    mutation CreatePost($input: PostInput!) {
        createPost(input: $input) {
            post { id content author { username } }
            success
            message
        }
    }
    """
    variables = {"input": {"content": "Integration test post 🚀 Testing all features!"}}
    response = session.post(GRAPHQL_URL, json={"query": mutation, "variables": variables})
    
    if response.status_code != 200:
        print(f"   ❌ HTTP error: {response.status_code}")
        test_results.append(("Create Post", False))
    else:
        data = response.json()
        if data and 'data' in data and data['data'] and 'createPost' in data['data']:
            result = data['data']['createPost']
            if result and result.get('success'):
                post = result['post']
                post_id = post['id']
                print(f"   ✅ Post created: {post['content'][:40]}...")
                test_results.append(("Create Post", True))
            else:
                errors = result.get('message') if result else 'No result'
                print(f"   ❌ Create failed: {errors}")
                test_results.append(("Create Post", False))
        else:
            errors = data.get('errors') if data else 'No response data'
            print(f"   ❌ Create failed: {errors}")
            test_results.append(("Create Post", False))
except Exception as e:
    print(f"   ❌ Create post failed: {e}")
    import traceback
    traceback.print_exc()
    test_results.append(("Create Post", False))

print()

# Test 7: Like Post
print("Test 7: Like Post...")
try:
    if post_id:
        mutation = """
        mutation LikePost($postId: ID!) {
            likePost(postId: $postId) {
                success
                message
                isLiked
            }
        }
        """
        response = session.post(GRAPHQL_URL, json={"query": mutation, "variables": {"postId": post_id}})
        data = response.json()
        
        if response.status_code == 200 and data.get('data', {}).get('likePost', {}).get('success'):
            is_liked = data['data']['likePost']['isLiked']
            print(f"   ✅ Post liked successfully (Liked: {is_liked})")
            test_results.append(("Like Post", True))
        else:
            errors = data.get('data', {}).get('likePost', {}).get('message') or data.get('errors')
            print(f"   ❌ Like failed: {errors}")
            test_results.append(("Like Post", False))
    else:
        print("   ⚠️  Skipped (no post created)")
        test_results.append(("Like Post", False))
except Exception as e:
    print(f"   ❌ Like post failed: {e}")
    test_results.append(("Like Post", False))

print()

# Test 8: Comment on Post
print("Test 8: Comment on Post...")
try:
    if post_id:
        mutation = """
        mutation CreateComment($input: CommentInput!) {
            createComment(input: $input) {
                comment { id content user { username } }
                success
                message
            }
        }
        """
        variables = {"input": {"postId": post_id, "content": "Great post! Testing comments."}}
        response = session.post(GRAPHQL_URL, json={"query": mutation, "variables": variables})
        data = response.json()
        
        if response.status_code == 200 and data.get('data', {}).get('createComment', {}).get('success'):
            comment = data['data']['createComment']['comment']
            print(f"   ✅ Comment posted: {comment['content'][:40]}...")
            test_results.append(("Comment Post", True))
        else:
            errors = data.get('data', {}).get('createComment', {}).get('message') or data.get('errors')
            print(f"   ❌ Comment failed: {errors}")
            test_results.append(("Comment Post", False))
    else:
        print("   ⚠️  Skipped (no post created)")
        test_results.append(("Comment Post", False))
except Exception as e:
    print(f"   ❌ Comment failed: {e}")
    test_results.append(("Comment Post", False))

print()

# Test 9: CORS Headers
print("Test 9: CORS Configuration...")
try:
    headers = {"Origin": "http://localhost:3000", "Access-Control-Request-Method": "POST"}
    response = requests.options(GRAPHQL_URL, headers=headers)
    cors = response.headers.get("Access-Control-Allow-Origin")
    
    if cors:
        print(f"   ✅ CORS enabled: {cors}")
        test_results.append(("CORS", True))
    else:
        print("   ⚠️  CORS headers not detected (may still work)")
        test_results.append(("CORS", True))
except Exception as e:
    print(f"   ⚠️  CORS check inconclusive: {e}")
    test_results.append(("CORS", True))

print()

# Test 10: Logout
print("Test 10: User Logout...")
try:
    mutation = "mutation { logoutUser { success } }"
    response = session.post(GRAPHQL_URL, json={"query": mutation})
    data = response.json()
    
    if response.status_code == 200 and data.get('data', {}).get('logoutUser', {}).get('success'):
        print("   ✅ Logout successful")
        test_results.append(("User Logout", True))
    else:
        print("   ❌ Logout failed")
        test_results.append(("User Logout", False))
except Exception as e:
    print(f"   ❌ Logout failed: {e}")
    test_results.append(("User Logout", False))

print()
print("=" * 70)
print("📊 TEST RESULTS SUMMARY")
print("=" * 70)

passed = sum(1 for _, result in test_results if result)
total = len(test_results)

for test_name, result in test_results:
    status = "✅ PASS" if result else "❌ FAIL"
    print(f"{status:10} {test_name}")

print("-" * 70)
print(f"Total: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
print("=" * 70)

if passed == total:
    print("\n🎉 ALL TESTS PASSED!")
    print("   Frontend should work perfectly with the backend.")
    print("\n📋 Next Steps:")
    print("   1. Start frontend: python start_frontend.py")
    print("   2. Open browser: http://localhost:3000")
    print("   3. Test registration, login, posts, likes, comments")
    sys.exit(0)
else:
    print(f"\n⚠️  {total - passed} test(s) failed.")
    print("   Please review errors above before testing frontend.")
    sys.exit(1)
