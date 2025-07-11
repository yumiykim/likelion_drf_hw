from rest_framework import serializers
from .models import *

class SongSerializer(serializers.ModelSerializer):
    singer = serializers.CharField(source='singer.name', read_only=True)

    class Meta:
        model = Song
        fields = '__all__'


class SingerSerializer(serializers.ModelSerializer):
    songs = serializers.SerializerMethodField()

    class Meta:
        model = Singer
        fields = ['id', 'name', 'content', 'debut', 'songs']

    def get_songs(self, obj):
        return SongSerializer(obj.songs.all(), many=True).data


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

        # 'song'은 URL 경로에서 전달되며 views.py에서 직접 지정하므로,
        # 사용자가 JSON에서 전달하지 않아도 되도록 read_only 처리함
        read_only_fields = ['created_at', 'song']
