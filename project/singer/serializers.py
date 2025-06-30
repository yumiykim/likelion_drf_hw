from rest_framework import serializers
from .models import Singer, Song, Comment

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'

class SingerSerializer(serializers.ModelSerializer):
    songs = serializers.SerializerMethodField()

    class Meta:
        model = Singer
        fields = ['id', 'content', 'debut', 'songs']

    def get_songs(self, obj):
        return SongSerializer(obj.songs.all(), many=True).data


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['created_at', 'song']
