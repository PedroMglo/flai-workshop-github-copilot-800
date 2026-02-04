from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    team = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    profile_picture = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    leader = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'teams'

    def __str__(self):
        return self.name


class Activity(models.Model):
    ACTIVITY_CHOICES = [
        ('running', 'Running'),
        ('cycling', 'Cycling'),
        ('swimming', 'Swimming'),
        ('weight_training', 'Weight Training'),
        ('yoga', 'Yoga'),
    ]

    user_email = models.EmailField()
    user_name = models.CharField(max_length=100)
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_CHOICES)
    distance = models.FloatField(default=0)
    duration = models.IntegerField()  # in minutes
    calories_burned = models.IntegerField()
    date = models.DateTimeField()
    intensity = models.CharField(max_length=20, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])

    class Meta:
        db_table = 'activities'

    def __str__(self):
        return f"{self.user_name} - {self.activity_type}"


class Workout(models.Model):
    DIFFICULTY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    duration_weeks = models.IntegerField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'workouts'

    def __str__(self):
        return self.name


class Leaderboard(models.Model):
    user_email = models.EmailField()
    user_name = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    total_activities = models.IntegerField(default=0)
    total_calories_burned = models.IntegerField(default=0)
    total_distance = models.FloatField(default=0)
    rank = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'leaderboard'
        ordering = ['rank']

    def __str__(self):
        return f"{self.rank}. {self.user_name}"
