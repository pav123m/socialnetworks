from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from .models import User, FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from datetime import timedelta

class UserSignup(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Extract password from validated data
            password = serializer.validated_data.get('password')

            # Create user object but do not save yet
            user = User.objects.create_user(**serializer.validated_data)

            # Set password using set_password method
            user.set_password(password)
            user.save()

            # Return success response
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Return error response if serializer is not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        # Check if email and password are provided
        if not email or not password:
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Convert email to lowercase
        email = email.lower()
        
        # Retrieve user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Check user's password
        if not user.check_password(password):
            return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Authentication successful
        return Response({"message": "Login successful"}, status=status.HTTP_200_OK)

# Other views remain unchanged


class UserSearch(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        keyword = request.query_params.get('keyword', '').lower()
        if not keyword:
            return Response({"message": "Keyword is required"}, status=status.HTTP_400_BAD_REQUEST)

        users = User.objects.filter(Q(email__icontains=keyword) | Q(username__icontains=keyword))
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(users, request)
        serializer = UserSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class SendFriendRequest(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, to_user_id):
        from_user = request.user
        to_user = User.objects.get(id=to_user_id)

        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
            return Response({"message": "Friend request already sent"}, status=status.HTTP_400_BAD_REQUEST)

        if FriendRequest.objects.filter(from_user=from_user, timestamp__gt=timezone.now() - timedelta(minutes=1)).count() >= 3:
            return Response({"message": "Cannot send more than 3 friend requests within a minute"}, status=status.HTTP_400_BAD_REQUEST)

        friend_request = FriendRequest(from_user=from_user, to_user=to_user)
        friend_request.save()
        return Response({"message": "Friend request sent"}, status=status.HTTP_201_CREATED)

class HandleFriendRequest(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, request_id, action):
        friend_request = FriendRequest.objects.get(id=request_id, to_user=request.user)
        if action == 'accept':
            friend_request.accepted = True
            friend_request.save()
            return Response({"message": "Friend request accepted"}, status=status.HTTP_200_OK)
        elif action == 'reject':
            friend_request.delete()
            return Response({"message": "Friend request rejected"}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

class ListFriends(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        friends = User.objects.filter(sent_requests__to_user=request.user, sent_requests__accepted=True) | \
                  User.objects.filter(received_requests__from_user=request.user, received_requests__accepted=True)
        serializer = UserSerializer(friends, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ListPendingFriendRequests(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pending_requests = FriendRequest.objects.filter(to_user=request.user, accepted=False)
        serializer = FriendRequestSerializer(pending_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
