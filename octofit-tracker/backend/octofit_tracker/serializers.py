from rest_framework import serializers
from .models import User, Team, Activity, Workout, Leaderboard


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'team', 'bio', 'profile_picture', 'created_at']
        read_only_fields = ['id', 'created_at']


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'members', 'leader', 'created_at']
        read_only_fields = ['id', 'created_at']


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'user_email', 'user_name', 'activity_type', 'distance', 'duration', 'calories_burned', 'date', 'intensity']
        read_only_fields = ['id']


class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['id', 'name', 'description', 'duration_weeks', 'difficulty', 'exercises', 'created_at']
        read_only_fields = ['id', 'created_at']


class LeaderboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaderboard
        fields = ['id', 'user_email', 'user_name', 'team', 'total_activities', 'total_calories_burned', 'total_distance', 'rank', 'updated_at']
        read_only_fields = ['id', 'updated_at']
