from .serializers import AudioFileSerializerFull, AudioFileSerializer
from .models import AudioFile

from rest_framework import viewsets
from rest_framework.views import APIView
from django.http.response import JsonResponse
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
import mimetypes
from django.http import HttpResponse
import mutagen
from mutagen.wave import WAVE
import json
from decimal import *


@api_view(['POST', 'DELETE'])
def audio_post(request):
    if request.method == 'POST':
        audio_serializer = AudioFileSerializerFull(data=request.data)
        if audio_serializer.is_valid():
            audio_serializer.save()
            voice = WAVE("media/{}".format(request.data['audio_file']))
            voice_info = voice.info
            audio_metadata = {'duration': voice_info.length, 'bitrate': voice_info.bitrate,
             'channels': voice_info.channels, 'sample_rate': voice_info.sample_rate,
              'sample_size': voice_info.bits_per_sample}
              
            AudioFile.objects.filter(file_id=audio_serializer.data['file_id']).update(duration=audio_metadata['duration'])
            AudioFile.objects.filter(file_id=audio_serializer.data['file_id']).update(bitrate=audio_metadata['bitrate'])
            AudioFile.objects.filter(file_id=audio_serializer.data['file_id']).update(channels=audio_metadata['channels'])
            AudioFile.objects.filter(file_id=audio_serializer.data['file_id']).update(sample_rate=audio_metadata['sample_rate'])
            AudioFile.objects.filter(file_id=audio_serializer.data['file_id']).update(sample_size=audio_metadata['sample_size'])

            audio_file_data = audio_serializer.data
            audio_file_data.update(audio_metadata)
            return JsonResponse(audio_file_data, status=status.HTTP_201_CREATED)
            
        return JsonResponse(audio_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = AudioFile.objects.all().delete()
        return JsonResponse({'messsage': '{} Audio files were deleted successfully'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)

    else:
        return JsonResponse({'message': 'Please use the POST/DELETE(all) method with this API!'})

@api_view(['GET'])
def audio_list(request):
    if request.method == 'GET':
        if request.GET.get('name', '') != '':
            name = request.GET.get('name','')
            try:
                audio_file = AudioFile.objects.filter(name=name)
                audio_serializer = AudioFileSerializer(audio_file, many=True)
                return JsonResponse(audio_serializer.data, safe=False)
            except:
                return JsonResponse({'message': 'The audio file does not exist with that name'})
        elif request.GET.get('audio_file', '') != '':
            audio_file_name = request.GET.get('audio_file', '')
            try:
                audio_file = AudioFile.objects.filter(audio_file__endswith=audio_file_name)
                audio_serializer = AudioFileSerializer(audio_file, many=True)
                return JsonResponse(audio_serializer.data, safe=False)
            except:
                return JsonResponse({'message': 'The audio file does not exist with that file name'})
        elif request.GET.get('duration', '') != '':
            duration = int(request.GET.get('duration','0'))
            try:
                audio_file = AudioFile.objects.filter(duration=duration)
                audio_serializer = AudioFileSerializer(audio_file, many=True)
                return JsonResponse(audio_serializer.data, safe=False)
            except:
                return JsonResponse({'message': 'The audio file does not exist with that duration'})
        elif request.GET.get('max_duration', '') != '':
            max_duration = float(request.GET.get('max_duration','0'))
            audio_file = AudioFile.objects.all()
            audio_serializer = AudioFileSerializer(audio_file, many=True)
            audio_serializer_filtered = []
            for audio in audio_serializer.data:
                if float(audio['duration']) <= float(max_duration):
                    audio_serializer_filtered.append(audio)
            return JsonResponse(audio_serializer_filtered, safe=False)
        elif request.GET.get('min_duration', '') != '':
            min_duration = float(request.GET.get('min_duration','0'))
            audio_file = AudioFile.objects.all()
            audio_serializer = AudioFileSerializer(audio_file, many=True)
            audio_serializer_filtered = []
            for audio in audio_serializer.data:
                if float(audio['duration']) >= float(min_duration):
                    audio_serializer_filtered.append(audio)
            return JsonResponse(audio_serializer_filtered, safe=False)
        else:
            audio_files = AudioFile.objects.all()
            audio_serializer = AudioFileSerializer(audio_files, many=True)
            return JsonResponse(audio_serializer.data, safe=False)
    else:
        return JsonResponse({'message': 'Please use the GET method with this API!'})

@api_view(['GET'])
def download_file(request):
    if request.method == 'GET':
        file_name = request.GET.get('file_name', '')

        if file_name != '':
            try:
                # audio_file = AudioFile.objects.get(file_name=name)
                # audio_serializer = AudioFileSerializer(audio_file)
                # file = './media/{}'.format(audio_serializer.data.audio_file)
                file = 'media/{}'.format(file_name)
                fl = open(file, 'rb')
                mime_type, _ = mimetypes.guess_type(file)
                response = HttpResponse(fl, content_type=mime_type)
                response['Content-Disposition'] = "attachment; filename=%s" % file_name
                return response

            except:
                return JsonResponse({'message': 'Name not found in database'})

        else:
            return JsonResponse({'message': 'Please provide a name to search for'})

    else:
        return JsonResponse({'message': 'Please use the GET method with this API!'})

@api_view(['GET'])
def audio_info(request):
    if request.method == 'GET':
        if request.GET.get('name', '') != '':
            name = request.GET.get('name','')
            try:
                audio_file = AudioFile.objects.filter(name=name)
                audio_serializer = AudioFileSerializerFull(audio_file, many=True)
                return JsonResponse(audio_serializer.data, safe=False)
            except:
                return JsonResponse({'message': 'The audio file does not exist with that name'})
        elif request.GET.get('audio_file', '') != '':
            audio_file_name = request.GET.get('audio_file', '')
            try:
                audio_file = AudioFile.objects.filter(audio_file__endswith=audio_file_name)
                audio_serializer = AudioFileSerializerFull(audio_file, many=True)
                return JsonResponse(audio_serializer.data, safe=False)
            except:
                return JsonResponse({'message': 'The audio file does not exist with that file name'})
        elif request.GET.get('duration', '') != '':
            duration = int(request.GET.get('duration','0'))
            try:
                audio_file = AudioFile.objects.filter(duration=duration)
                audio_serializer = AudioFileSerializerFull(audio_file, many=True)
                return JsonResponse(audio_serializer.data, safe=False)
            except:
                return JsonResponse({'message': 'The audio file does not exist with that duration'})
        elif request.GET.get('max_duration', '') != '':
            max_duration = float(request.GET.get('max_duration','0'))
            audio_file = AudioFile.objects.all()
            audio_serializer = AudioFileSerializerFull(audio_file, many=True)
            audio_serializer_filtered = []
            for audio in audio_serializer.data:
                if float(audio['duration']) <= float(max_duration):
                    audio_serializer_filtered.append(audio)
            return JsonResponse(audio_serializer_filtered, safe=False)
        elif request.GET.get('min_duration', '') != '':
            min_duration = float(request.GET.get('min_duration','0'))
            audio_file = AudioFile.objects.all()
            audio_serializer = AudioFileSerializerFull(audio_file, many=True)
            audio_serializer_filtered = []
            for audio in audio_serializer.data:
                if float(audio['duration']) >= float(min_duration):
                    audio_serializer_filtered.append(audio)
            return JsonResponse(audio_serializer_filtered, safe=False)
        else:
            audio_files = AudioFile.objects.all()
            audio_serializer = AudioFileSerializerFull(audio_files, many=True)
            return JsonResponse(audio_serializer.data, safe=False)
    else:
        return JsonResponse({'message': 'Please use the GET method with this API!'})
