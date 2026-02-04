from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Team, Activity, Workout, Leaderboard
from .serializers import UserSerializer, TeamSerializer, ActivitySerializer, WorkoutSerializer, LeaderboardSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'email'

    @action(detail=False, methods=['get'])
    def by_team(self, request):
        team = request.query_params.get('team')
        if not team:
            return Response({'error': 'team parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        users = User.objects.filter(team=team)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        team = self.get_object()
        users = User.objects.filter(email__in=team.members)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    @action(detail=False, methods=['get'])
    def by_user(self, request):
        user_email = request.query_params.get('email')
        if not user_email:
            return Response({'error': 'email parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        activities = Activity.objects.filter(user_email=user_email).order_by('-date')
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_type(self, request):
        activity_type = request.query_params.get('type')
        if not activity_type:
            return Response({'error': 'type parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        activities = Activity.objects.filter(activity_type=activity_type).order_by('-date')
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)


class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer

    @action(detail=False, methods=['get'])
    def by_difficulty(self, request):
        difficulty = request.query_params.get('difficulty')
        if not difficulty:
            return Response({'error': 'difficulty parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        workouts = Workout.objects.filter(difficulty=difficulty)
        serializer = self.get_serializer(workouts, many=True)
        return Response(serializer.data)


class LeaderboardViewSet(viewsets.ModelViewSet):
    queryset = Leaderboard.objects.all().order_by('rank')
    serializer_class = LeaderboardSerializer

    @action(detail=False, methods=['get'])
    def top_10(self, request):
        leaderboard = Leaderboard.objects.all().order_by('rank')[:10]
        serializer = self.get_serializer(leaderboard, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_team(self, request):
        team = request.query_params.get('team')
        if not team:
            return Response({'error': 'team parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        leaderboard = Leaderboard.objects.filter(team=team).order_by('rank')
        serializer = self.get_serializer(leaderboard, many=True)
        return Response(serializer.data)
