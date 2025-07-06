from rest_framework import serializers
from .models import *

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'
        
        # 'singer'는 URL에서 전달받고 views.py에서 직접 지정해주므로,
        # 클라이언트가 JSON으로 값을 보내지 않아도 되게끔 read_only 처리함
        read_only_fields = ['singer']

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

        # 'song'은 URL 경로에서 전달되며 views.py에서 직접 지정하므로,
        # 사용자가 JSON에서 전달하지 않아도 되도록 read_only 처리함
        read_only_fields = ['created_at', 'song']
