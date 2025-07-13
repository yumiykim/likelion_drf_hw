from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Singer, Song, Comment, Tag
from .serializers import SingerSerializer, SongSerializer, CommentSerializer, TagSerializer


def parse_tags_from_text(text):
    return [word[1:] for word in text.split() if word.startswith("#")]

@api_view(['GET', 'POST'])
def singer_list(request):
    if request.method == 'GET':
        tag_name = request.GET.get('tag')
        if tag_name:
            singers = Singer.objects.filter(tags__name=tag_name)
        else:
            singers = Singer.objects.all()
        serializer = SingerSerializer(singers, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        content_text = request.data.get('content', '')
        tag_names = parse_tags_from_text(content_text)

        serializer = SingerSerializer(data=request.data)
        if serializer.is_valid():
            singer = serializer.save()
            for tag_name in tag_names:
                tag_obj, _ = Tag.objects.get_or_create(name=tag_name)
                singer.tags.add(tag_obj)
            return Response(SingerSerializer(singer).data)
        return Response(serializer.errors)

@api_view(['GET', 'PATCH', 'DELETE'])
def singer_detail(request, pk):
    try:
        singer = Singer.objects.get(pk=pk)
    except Singer.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)

    if request.method == 'GET':
        return Response(SingerSerializer(singer).data)

    elif request.method == 'PATCH':
        content_text = request.data.get('content', '')
        tag_names = parse_tags_from_text(content_text)

        serializer = SingerSerializer(singer, data=request.data, partial=True)
        if serializer.is_valid():
            updated_singer = serializer.save()
            updated_singer.tags.clear()
            for tag_name in tag_names:
                tag_obj, _ = Tag.objects.get_or_create(name=tag_name)
                updated_singer.tags.add(tag_obj)
            return Response(SingerSerializer(updated_singer).data)
        return Response(serializer.errors)

    elif request.method == 'DELETE':
        singer.delete()
        return Response({'id': pk, 'deleted': True})

@api_view(['POST'])
def song_create(request, singer_id):
    try:
        singer = Singer.objects.get(pk=singer_id)
    except Singer.DoesNotExist:
        return Response({'error': 'Singer not found'}, status=404)

    serializer = SongSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(singer=singer)
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['POST'])
def comment_create(request, song_id):
    try:
        song = Song.objects.get(pk=song_id)
    except Song.DoesNotExist:
        return Response({'error': 'Song not found'}, status=404)

    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(song=song)
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['GET'])
def comment_list(request, song_id):
    comments = Comment.objects.filter(song__id=song_id)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


