import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q, Count, F, Sum
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from users.models import User
from posts.models import Post, PostMedia
from interactions.models import Like, Comment, Share, Follow, PostView, CommentLike


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = '__all__'

    full_name = graphene.String()
    followers_count = graphene.Int()
    following_count = graphene.Int()
    posts_count = graphene.Int()
    is_following = graphene.Boolean()
    mutual_followers = graphene.List(lambda: UserType)

    def resolve_full_name(self, info):
        return self.full_name

    def resolve_is_following(self, info):
        if not info.context.user.is_authenticated:
            return False
        return Follow.objects.filter(
            follower=info.context.user,
            following=self
        ).exists()

    def resolve_mutual_followers(self, info):
        if not info.context.user.is_authenticated:
            return []
        user_following = Follow.objects.filter(follower=self).values_list('following', flat=True)
        current_user_following = Follow.objects.filter(follower=info.context.user).values_list('following', flat=True)
        mutual_ids = set(user_following) & set(current_user_following)
        return User.objects.filter(id__in=mutual_ids)


class PostMediaType(DjangoObjectType):
    class Meta:
        model = PostMedia
        fields = '__all__'


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = '__all__'

    author = graphene.Field(UserType)
    media_files = graphene.List(PostMediaType)
    is_liked = graphene.Boolean()
    is_shared = graphene.Boolean()
    comments = graphene.List(lambda: CommentType)
    likes_count = graphene.Int()
    comments_count = graphene.Int()
    shares_count = graphene.Int()

    def resolve_author(self, info):
        return self.author

    def resolve_media_files(self, info):
        return self.media_files.all()

    def resolve_is_liked(self, info):
        if not info.context.user.is_authenticated:
            return False
        return Like.objects.filter(user=info.context.user, post=self).exists()

    def resolve_is_shared(self, info):
        if not info.context.user.is_authenticated:
            return False
        return Share.objects.filter(user=info.context.user, post=self).exists()

    def resolve_comments(self, info):
        return self.comments.filter(parent=None).order_by('created_at')

    def resolve_likes_count(self, info):
        return self.likes_count

    def resolve_comments_count(self, info):
        return self.comments_count

    def resolve_shares_count(self, info):
        return self.shares_count


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = '__all__'

    author = graphene.Field(UserType)
    post = graphene.Field(PostType)
    parent = graphene.Field(lambda: CommentType)
    replies = graphene.List(lambda: CommentType)
    is_liked = graphene.Boolean()
    likes_count = graphene.Int()

    def resolve_author(self, info):
        return self.user

    def resolve_post(self, info):
        return self.post

    def resolve_replies(self, info):
        return self.replies.all().order_by('created_at')

    def resolve_is_liked(self, info):
        if not info.context.user.is_authenticated:
            return False
        return CommentLike.objects.filter(user=info.context.user, comment=self).exists()

    def resolve_likes_count(self, info):
        return self.likes_count


class LikeType(DjangoObjectType):
    class Meta:
        model = Like
        fields = '__all__'

    user = graphene.Field(UserType)
    post = graphene.Field(PostType)


class ShareType(DjangoObjectType):
    class Meta:
        model = Share
        fields = '__all__'

    user = graphene.Field(UserType)
    post = graphene.Field(PostType)


class FollowType(DjangoObjectType):
    class Meta:
        model = Follow
        fields = '__all__'

    follower = graphene.Field(UserType)
    following = graphene.Field(UserType)


# Input Types
class PostInput(graphene.InputObjectType):
    content = graphene.String(required=False)
    content_type = graphene.String(required=False)
    privacy_level = graphene.String(required=False)
    media_url = graphene.String(required=False)


class CommentInput(graphene.InputObjectType):
    post_id = graphene.ID(required=True)
    content = graphene.String(required=True)
    parent_id = graphene.ID(required=False)


class UserInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    first_name = graphene.String(required=False)
    last_name = graphene.String(required=False)
    bio = graphene.String(required=False)


class LoginInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    password = graphene.String(required=True)


class RegisterInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    first_name = graphene.String(required=False)
    last_name = graphene.String(required=False)


# Queries
class Query(graphene.ObjectType):
    # User queries
    me = graphene.Field(UserType)
    user = graphene.Field(UserType, id=graphene.ID(required=True))
    users = graphene.List(UserType, search=graphene.String())

    # Post queries
    posts = graphene.List(PostType, limit=graphene.Int(), offset=graphene.Int())
    post = graphene.Field(PostType, id=graphene.ID(required=True))
    user_posts = graphene.List(PostType, user_id=graphene.ID(required=True))
    feed = graphene.List(PostType, limit=graphene.Int(), offset=graphene.Int())

    # Interaction queries
    post_likes = graphene.List(LikeType, post_id=graphene.ID(required=True))
    post_comments = graphene.List(CommentType, post_id=graphene.ID(required=True))
    user_followers = graphene.List(UserType, user_id=graphene.ID(required=True))
    user_following = graphene.List(UserType, user_id=graphene.ID(required=True))

    def resolve_me(self, info):
        user = info.context.user
        if user.is_authenticated:
            return user
        return None

    def resolve_user(self, info, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None

    def resolve_users(self, info, search=None):
        queryset = User.objects.all()
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
        return queryset

    def resolve_posts(self, info, limit=20, offset=0):
        return Post.objects.filter(
            privacy_level='public'
        ).select_related('author').order_by('-created_at')[offset:offset+limit]

    def resolve_post(self, info, id):
        try:
            return Post.objects.get(id=id)
        except Post.DoesNotExist:
            return None

    def resolve_user_posts(self, info, user_id):
        user = User.objects.get(id=user_id)
        posts = Post.objects.filter(author=user)
        
        if info.context.user.is_authenticated:
            if info.context.user != user:
                # Show only public posts for other users
                posts = posts.filter(privacy_level='public')
        else:
            # Show only public posts for anonymous users
            posts = posts.filter(privacy_level='public')
            
        return posts.select_related('author').order_by('-created_at')

    def resolve_feed(self, info, limit=20, offset=0):
        if not info.context.user.is_authenticated:
            return []
        
        # Get posts from users that current user follows
        following_users = Follow.objects.filter(
            follower=info.context.user
        ).values_list('following', flat=True)
        
        # Include user's own posts
        following_users = list(following_users) + [info.context.user.id]
        
        return Post.objects.filter(
            author_id__in=following_users
        ).select_related('author').order_by('-created_at')[offset:offset+limit]

    def resolve_post_likes(self, info, post_id):
        return Like.objects.filter(post_id=post_id).select_related('user')

    def resolve_post_comments(self, info, post_id):
        return Comment.objects.filter(
            post_id=post_id, 
            parent=None
        ).select_related('user').order_by('created_at')

    def resolve_user_followers(self, info, user_id):
        follows = Follow.objects.filter(following_id=user_id).select_related('follower')
        return [follow.follower for follow in follows]

    def resolve_user_following(self, info, user_id):
        follows = Follow.objects.filter(follower_id=user_id).select_related('following')
        return [follow.following for follow in follows]


# Mutations
class RegisterUser(graphene.Mutation):
    class Arguments:
        input = RegisterInput(required=True)

    user = graphene.Field(UserType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, input):
        try:
            # Create user with explicit first_name and last_name (default to empty string)
            user = User.objects.create_user(
                username=input.username,
                email=input.email,
                password=input.password,
                first_name=getattr(input, 'first_name', ''),
                last_name=getattr(input, 'last_name', '')
            )
            
            return RegisterUser(user=user, success=True, message="User registered successfully")
        except Exception as e:
            return RegisterUser(success=False, message=str(e))


class LoginUser(graphene.Mutation):
    class Arguments:
        input = LoginInput(required=True)

    user = graphene.Field(UserType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, input):
        # Try authenticating with username first, then email
        user = authenticate(username=input.username, password=input.password)
        if user is None:
            # Try with email if username didn't work
            try:
                user_obj = User.objects.get(username=input.username)
                user = authenticate(username=user_obj.email, password=input.password)
            except User.DoesNotExist:
                pass
        
        if user is not None:
            login(info.context, user)
            return LoginUser(user=user, success=True, message="Login successful")
        return LoginUser(success=False, message="Invalid credentials")


class LogoutUser(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info):
        if info.context.user.is_authenticated:
            logout(info.context)
            return LogoutUser(success=True, message="Logout successful")
        return LogoutUser(success=False, message="No user logged in")


class CreatePost(graphene.Mutation):
    class Arguments:
        input = PostInput(required=True)

    post = graphene.Field(PostType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            return CreatePost(success=False, message="Authentication required")

        post = Post.objects.create(
            author=info.context.user,
            content=input.content or '',
            content_type=input.content_type or 'text',
            privacy_level=input.privacy_level or 'public',
            media_url=input.media_url or ''
        )
        
        # TODO: Implement real-time updates via WebSocket when needed
        # For now, skip the asyncio broadcast to avoid event loop issues
        
        return CreatePost(post=post, success=True, message="Post created successfully")


class LikePost(graphene.Mutation):
    class Arguments:
        post_id = graphene.ID(required=True)

    success = graphene.Boolean()
    message = graphene.String()
    is_liked = graphene.Boolean()

    def mutate(self, info, post_id):
        if not info.context.user.is_authenticated:
            return LikePost(success=False, message="Authentication required", is_liked=False)
        
        try:
            post = Post.objects.get(id=post_id)
            like, created = Like.objects.get_or_create(
                user=info.context.user,
                post=post
            )
            
            if not created:
                # Unlike the post
                like.delete()
                post.likes_count = Like.objects.filter(post=post).count()
                post.save()
                is_liked = False
            else:
                # Like the post
                post.likes_count = Like.objects.filter(post=post).count()
                post.save()
                is_liked = True
                
            return LikePost(success=True, message="Like status updated", is_liked=is_liked)
            
        except Post.DoesNotExist:
            return LikePost(success=False, message="Post not found", is_liked=False)


class CreateComment(graphene.Mutation):
    class Arguments:
        input = CommentInput(required=True)

    comment = graphene.Field(CommentType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            return CreateComment(success=False, message="Authentication required")

        try:
            post = Post.objects.get(id=input.post_id)
            parent = None
            if input.parent_id:
                parent = Comment.objects.get(id=input.parent_id)

            comment = Comment.objects.create(
                user=info.context.user,
                post=post,
                parent=parent,
                content=input.content
            )
            
            post.comments_count += 1
            post.save()
            
            return CreateComment(comment=comment, success=True, message="Comment created")
            
        except Post.DoesNotExist:
            return CreateComment(success=False, message="Post not found")
        except Comment.DoesNotExist:
            return CreateComment(success=False, message="Parent comment not found")


class FollowUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)

    success = graphene.Boolean()
    message = graphene.String()
    is_following = graphene.Boolean()

    def mutate(self, info, user_id):
        if not info.context.user.is_authenticated:
            return FollowUser(success=False, message="Authentication required", is_following=False)

        try:
            user_to_follow = User.objects.get(id=user_id)
            if user_to_follow == info.context.user:
                return FollowUser(success=False, message="Cannot follow yourself", is_following=False)

            follow, created = Follow.objects.get_or_create(
                follower=info.context.user,
                following=user_to_follow
            )
            
            if created:
                # Update follower counts
                info.context.user.following_count += 1
                info.context.user.save()
                user_to_follow.followers_count += 1
                user_to_follow.save()
                
                # Send real-time notification
                from .consumers import send_follow_notification
                import asyncio
                asyncio.create_task(send_follow_notification(
                    user_to_follow.id,
                    {
                        'user_id': info.context.user.id,
                        'username': info.context.user.username,
                        'full_name': info.context.user.get_full_name(),
                        'message': f'{info.context.user.username} started following you',
                        'followers_count': user_to_follow.followers_count
                    }
                ))
                
                return FollowUser(success=True, message="User followed", is_following=True)
            else:
                follow.delete()
                info.context.user.following_count -= 1
                info.context.user.save()
                user_to_follow.followers_count -= 1
                user_to_follow.save()
                
                return FollowUser(success=True, message="User unfollowed", is_following=False)
                
        except User.DoesNotExist:
            return FollowUser(success=False, message="User not found", is_following=False)


class SharePost(graphene.Mutation):
    class Arguments:
        post_id = graphene.ID(required=True)

    success = graphene.Boolean()
    message = graphene.String()
    shares_count = graphene.Int()

    def mutate(self, info, post_id):
        if not info.context.user.is_authenticated:
            return SharePost(success=False, message="Authentication required", shares_count=0)
        
        try:
            post = Post.objects.get(id=post_id)
            
            # Create or get share record
            share, created = Share.objects.get_or_create(
                user=info.context.user,
                post=post
            )
            
            if created:
                # Increment share count
                post.shares_count = Share.objects.filter(post=post).count()
                post.save()
                
                return SharePost(
                    success=True,
                    message="Post shared successfully",
                    shares_count=post.shares_count
                )
            else:
                # Already shared
                return SharePost(
                    success=True,
                    message="Post already shared",
                    shares_count=post.shares_count
                )
            
        except Post.DoesNotExist:
            return SharePost(success=False, message="Post not found", shares_count=0)


class Mutation(graphene.ObjectType):
    # Authentication mutations
    register_user = RegisterUser.Field()
    login_user = LoginUser.Field()
    logout_user = LogoutUser.Field()
    
    # Post and interaction mutations
    create_post = CreatePost.Field()
    like_post = LikePost.Field()
    create_comment = CreateComment.Field()
    share_post = SharePost.Field()
    follow_user = FollowUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
