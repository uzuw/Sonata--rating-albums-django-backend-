# immediately after creating a model in models.py we make its resppective serializer to serialize the data inform of api

from rest_framework import serializers

from .models import TrackRating

class TrackRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model= TrackRating
        fields= ['id','user','albumn_id','track_id','score','comment']
        red_only_fields=['id','user'] #prevents the user from manually setting the user and id 


#for user form
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', "date_joined", "is_active"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user
