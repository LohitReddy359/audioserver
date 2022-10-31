from rest_framework import serializers

from .models import AudioFile

class AudioFileSerializerFull(serializers.ModelSerializer):
    class Meta:
        model = AudioFile
        fields = ('file_id','name','audio_file', 'duration', 'bitrate', 'channels', 'sample_rate', 'sample_size')


class AudioFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioFile
        fields = ('file_id','name','audio_file', 'duration')
