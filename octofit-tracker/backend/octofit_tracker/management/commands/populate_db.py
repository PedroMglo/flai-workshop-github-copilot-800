from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from pymongo import MongoClient
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Clear existing data
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        self.stdout.write(self.style.SUCCESS('Cleared existing data'))

        # Marvel superheroes
        marvel_heroes = [
            {'name': 'Iron Man', 'email': 'tony.stark@marvel.com', 'team': 'Team Marvel'},
            {'name': 'Captain America', 'email': 'steve.rogers@marvel.com', 'team': 'Team Marvel'},
            {'name': 'Thor', 'email': 'thor.odinson@marvel.com', 'team': 'Team Marvel'},
            {'name': 'Black Widow', 'email': 'natasha.romanoff@marvel.com', 'team': 'Team Marvel'},
            {'name': 'Hulk', 'email': 'bruce.banner@marvel.com', 'team': 'Team Marvel'},
        ]

        # DC superheroes
        dc_heroes = [
            {'name': 'Batman', 'email': 'bruce.wayne@dc.com', 'team': 'Team DC'},
            {'name': 'Superman', 'email': 'clark.kent@dc.com', 'team': 'Team DC'},
            {'name': 'Wonder Woman', 'email': 'diana.prince@dc.com', 'team': 'Team DC'},
            {'name': 'The Flash', 'email': 'barry.allen@dc.com', 'team': 'Team DC'},
            {'name': 'Aquaman', 'email': 'arthur.curry@dc.com', 'team': 'Team DC'},
        ]

        all_heroes = marvel_heroes + dc_heroes

        # Insert users
        users_data = []
        for hero in all_heroes:
            user_data = {
                'name': hero['name'],
                'email': hero['email'],
                'team': hero['team'],
                'created_at': datetime.now(),
                'bio': f'{hero["name"]} is a superhero',
                'profile_picture': '',
            }
            users_data.append(user_data)

        db.users.insert_many(users_data)
        self.stdout.write(self.style.SUCCESS(f'Created {len(users_data)} users'))

        # Insert teams
        teams_data = [
            {
                'name': 'Team Marvel',
                'description': 'Marvel Superheroes',
                'members': [h['email'] for h in marvel_heroes],
                'created_at': datetime.now(),
                'leader': 'tony.stark@marvel.com',
            },
            {
                'name': 'Team DC',
                'description': 'DC Superheroes',
                'members': [h['email'] for h in dc_heroes],
                'created_at': datetime.now(),
                'leader': 'bruce.wayne@dc.com',
            },
        ]
        db.teams.insert_many(teams_data)
        self.stdout.write(self.style.SUCCESS(f'Created {len(teams_data)} teams'))

        # Insert activities
        activities = []
        activity_types = ['running', 'cycling', 'swimming', 'weight_training', 'yoga']
        for i, hero in enumerate(all_heroes):
            for j in range(random.randint(3, 8)):
                activity = {
                    'user_email': hero['email'],
                    'user_name': hero['name'],
                    'activity_type': random.choice(activity_types),
                    'distance': round(random.uniform(1, 20), 2),
                    'duration': random.randint(15, 120),  # minutes
                    'calories_burned': random.randint(100, 800),
                    'date': datetime.now() - timedelta(days=random.randint(0, 30)),
                    'intensity': random.choice(['low', 'medium', 'high']),
                }
                activities.append(activity)

        db.activities.insert_many(activities)
        self.stdout.write(self.style.SUCCESS(f'Created {len(activities)} activities'))

        # Insert workouts (predefined workout plans)
        workouts = [
            {
                'name': 'Superhero Strength Training',
                'description': 'Build the strength of a superhero',
                'duration_weeks': 12,
                'difficulty': 'hard',
                'exercises': ['push-ups', 'squats', 'deadlifts', 'pull-ups'],
                'created_at': datetime.now(),
            },
            {
                'name': 'Cardio Crusader',
                'description': 'Improve your cardio endurance',
                'duration_weeks': 8,
                'difficulty': 'medium',
                'exercises': ['running', 'cycling', 'swimming'],
                'created_at': datetime.now(),
            },
            {
                'name': 'Flexibility Fortress',
                'description': 'Enhance flexibility and mobility',
                'duration_weeks': 6,
                'difficulty': 'low',
                'exercises': ['yoga', 'stretching', 'pilates'],
                'created_at': datetime.now(),
            },
        ]
        db.workouts.insert_many(workouts)
        self.stdout.write(self.style.SUCCESS(f'Created {len(workouts)} workouts'))

        # Insert leaderboard
        leaderboard = []
        for i, hero in enumerate(all_heroes):
            total_activities = sum(1 for a in activities if a['user_email'] == hero['email'])
            total_calories = sum(a['calories_burned'] for a in activities if a['user_email'] == hero['email'])
            rank_data = {
                'user_email': hero['email'],
                'user_name': hero['name'],
                'team': hero['team'],
                'total_activities': total_activities,
                'total_calories_burned': total_calories,
                'total_distance': round(sum(a['distance'] for a in activities if a['user_email'] == hero['email']), 2),
                'rank': i + 1,
                'updated_at': datetime.now(),
            }
            leaderboard.append(rank_data)

        # Sort by calories burned and update ranks
        leaderboard = sorted(leaderboard, key=lambda x: x['total_calories_burned'], reverse=True)
        for i, entry in enumerate(leaderboard):
            entry['rank'] = i + 1

        db.leaderboard.insert_many(leaderboard)
        self.stdout.write(self.style.SUCCESS(f'Created {len(leaderboard)} leaderboard entries'))

        self.stdout.write(self.style.SUCCESS('Database population completed successfully!'))
