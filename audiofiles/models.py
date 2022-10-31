from django.db import models

class AudioFile(models.Model):
    file_id = models.AutoField(primary_key=True)
    name = models.CharField(null=True, blank=True, default="", max_length=100)
    audio_file = models.FileField(null=False)
    duration = models.DecimalField(null=False, default=0, decimal_places=2, max_digits=10)
    bitrate = models.IntegerField(null=False, default=0)
    channels = models.IntegerField(null=False, default=0)
    sample_rate = models.IntegerField(null=False, default=0)
    sample_size = models.IntegerField(null=False, default=0)

    def __str__(self):
        return self.name