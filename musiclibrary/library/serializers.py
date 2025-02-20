# immediately after creating a model in models.py we make its resppective serializer to serialize the data inform of api

from rest_framework import serializers

from .models import Album, Track, Rating

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model=Album
        fields='__all__'

class TrackSerializer(serializers.ModelSerializer):
      class Meta:
           model=Track
           field="__all__"
        
class RatingSerializer(serializers.ModelSerializer):
     class Meta:
          model=Rating
          field="__all_"
    


