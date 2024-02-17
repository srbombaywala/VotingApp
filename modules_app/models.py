import json
import random
from django.db import models
from django.utils import timezone
from collections import Counter
import itertools

class member(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    ppan = models.CharField(max_length = 10)
    picture = models.ImageField(upload_to='user_pics/', blank=True, null=True)
    otp = models.CharField(max_length=6, null=True, default='')
    has_voted = models.BooleanField(default=False)
    otp_generated_at = models.DateTimeField(null=True, blank=True)
    vote_casted = models.TextField(null=True, blank=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def generate_otp(self):
        generated_otp = ''.join(random.choice('0123456789') for _ in range(6))
        # Check if the generated OTP already exists in the database
        while member.objects.filter(otp=generated_otp).exists():
            # If it exists, generate a new one
            generated_otp = ''.join(random.choice('0123456789') for _ in range(6))
        self.otp = generated_otp
        self.otp_generated_at = timezone.now()
        self.save()
        return generated_otp

    def save_vote(self, vote):
        self.vote_casted = json.dumps(vote)
        self.has_voted = True
        self.save()

    @staticmethod
    def get_votes_count():
        # Retrieve all members and their vote_casted arrays
        all_members = member.objects.all()

        # Extract all vote_casted arrays into a list
        all_votes = [json.loads(member_obj.vote_casted) for member_obj in all_members if member_obj.vote_casted]

        # Merge all arrays into a single list
        merged_votes = list(itertools.chain.from_iterable(all_votes))
        # Count the occurrences of each name
        votes_counter = Counter(merged_votes)

        # Convert the Counter to a dictionary for easier handling
        votes_dict = dict(votes_counter)

        return votes_dict