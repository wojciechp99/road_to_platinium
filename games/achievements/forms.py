from django.forms import ModelForm
from .models import Achievement


class AchievementForm(ModelForm):
    class Meta:
        model = Achievement
        fields = '__all__'
        exclude = ['slug']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
