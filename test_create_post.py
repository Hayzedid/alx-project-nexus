import requests

s = requests.Session()

# Login
login_query = """
mutation {
    loginUser(input: {username: "user_1", password: "password123"}) {
        success
        message
    }
}
"""
result = s.post('http://127.0.0.1:8000/graphql/', json={'query': login_query})
print("Login:", result.json())

# Create post
post_query = """
mutation {
    createPost(input: {content: "Test post from script"}) {
        success
        message
        post { id content }
    }
}
"""
result = s.post('http://127.0.0.1:8000/graphql/', json={'query': post_query})
print("Post:", result.json())
