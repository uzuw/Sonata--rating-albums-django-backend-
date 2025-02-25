# immediately after creating a model in models.py we make its resppective serializer to serialize the data inform of api

from rest_framework import serializers

from .models import TrackRating

class TrackRatingSerialilzer(serializers.ModelSerializer):
    class Meta:
        model= TrackRating
        fields= ['id','user','albumn_id','track_id','score','comment']
        red_only_fields=['id','user'] #prevents the user from manually setting the user and id 

        
