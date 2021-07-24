from inonet.users.api.serializers import UserSerializer
from .models import Comment
from rest_framework import serializers


class CommentSerializer(serializers.HyperlinkedModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'user',
            'post',
            'text',
            'answered_to',
            'date_time'
        ]
    
    