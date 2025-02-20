from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Album(models.Model):
    title= models.CharField(max_length=255)
    artist=models.CharField(max_length=255)
    release_date=models.DateField
    image=models.ImageField()

    def __str__(self):
        return self.title

class Track(models.Model):
    # foreign key to refrence the album it belongs to
    album=models.ForeignKey(Album, on_delete=models.CASCADE, related_name="tracks")
    title=models.CharField(max_length=255)
    duration=models.PositiveIntegerField(help_text="Durations in seconds")

    def __str__(self):
        return f"{self.title} - {self.album.title}"

class Rating(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    album= models.ForeignKey(Album, on_delete=models.CASCADE, null=True, blank=True)
    track= models.ForeignKey(Track, on_delete=models.CASCADE, null=True, blank=True)
    rating=models.DecimalField(max_digits=3, decimal_places=1) #1.0 to 5.0
    review=models.TextField(blank=True)
    public=models.BooleanField(default=True)


    def __str__(self):
        return f"{self.user.username} rated {self.album or self.track} - {self.rating}"




    
