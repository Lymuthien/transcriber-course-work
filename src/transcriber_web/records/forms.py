from django import forms
from django.core.validators import MinValueValidator


class AudioUploadForm(forms.Form):
    file = forms.FileField(label="Аудиофайл (до 10 МБ, mp3)")
    language = forms.CharField(
        required=False,
        label="Язык (на английском). Желательно.",
    )
    max_speakers = forms.IntegerField(
        required=False, label="Макс. кол-во спикеров", validators=[MinValueValidator(1)]
    )
    main_theme = forms.CharField(required=False, label="Вспомогательное")
