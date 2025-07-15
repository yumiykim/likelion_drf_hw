from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *

'''
def parse_tags_from_text(text):
    return [word[1:] for word in text.split() if word.startswith("#")]
'''

# Singer 리스트 & 생성
@api_view(['GET', 'POST'])
def singer_list_create(request):
    if request.method == 'GET':
        singers = Singer.objects.all()
        serializer = SingerSerializer(singers, many=True)
        return Response(data=serializer.data)

    elif request.method == 'POST':
        serializer = SingerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            singer = serializer.save()

            content = request.data.get('content', '')
            tags = [word[1:] for word in content.split(' ') if word.startswith('#')]
            for t in tags:
                try:
                    tag = get_object_or_404(Tag, name=t)
                except:
                    tag = Tag(name=t)
                    tag.save()
                singer.tags.add(tag)

            singer.save()
            return Response(data=SingerSerializer(singer).data)

# Singer 상세조회, 수정, 삭제
@api_view(['GET', 'PATCH', 'DELETE'])
def singer_detail_update_delete(request, singer_id):
    singer = get_object_or_404(Singer, id=singer_id)

    if request.method == 'GET':
        serializer = SingerSerializer(singer)
        return Response(data=serializer.data)

    elif request.method == 'PATCH':
        serializer = SingerSerializer(instance=singer, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            updated_singer = serializer.save()

            updated_singer.tags.clear()
            content = request.data.get('content', '')
            tags = [word[1:] for word in content.split(' ') if word.startswith('#')]
            for t in tags:
                try:
                    tag = get_object_or_404(Tag, name=t)
                except:
                    tag = Tag(name=t)
                    tag.save()
                updated_singer.tags.add(tag)

            updated_singer.save()
            return Response(data=SingerSerializer(updated_singer).data)

    elif request.method == 'DELETE':
        singer.delete()
        return Response({'deleted_singer': singer_id})
    

@api_view(['POST'])
def singer_add_images(request, singer_id):
    singer = get_object_or_404(Singer, id=singer_id)
    images = request.FILES.getlist('images')  # 다중이미지
    created_images = []

    for img in images:
        img_obj = SingerImage.objects.create(singer=singer, image=img)
        created_images.append(img_obj)

    serializer = SingerImageSerializer(created_images, many=True)
    return Response(serializer.data)


# Song 생성
@api_view(['POST'])
def song_create(request, singer_id):
    singer = get_object_or_404(Singer, id=singer_id)
    serializer = SongSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(singer=singer)
        return Response(data=serializer.data)

# Comment 읽기 & 생성
@api_view(['GET', 'POST'])
def comment_read_create(request, song_id):
    song = get_object_or_404(Song, id=song_id)

    if request.method == 'GET':
        comments = Comment.objects.filter(song=song)
        serializer = CommentSerializer(comments, many=True)
        return Response(data=serializer.data)

    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(song=song)
            return Response(data=serializer.data)

# 태그 검색
@api_view(['GET'])
def find_tag(request, tags_name):
    tag = get_object_or_404(Tag, name=tags_name)
    singers = Singer.objects.filter(tags__in=[tag])
    serializer = SingerSerializer(singers, many=True)
    return Response(data=serializer.data)

