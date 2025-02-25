from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class TrackRating(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    album_id=models.CharField(max_length=22) #max id length of the spotify
    track_id=models.CharField(max_length=22) #max track id of the spotify
    score=models.IntegerField()
    comment=models.TextField(blank=True, null=True)

    class Meta:
        unique_together= ('user', 'track_id')# prevent duplicate ratings




    
