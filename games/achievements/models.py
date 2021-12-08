from django.db.models import Model, CharField, URLField, TextField, ImageField, BooleanField, ForeignKey, CASCADE, \
    SlugField
from django.utils.text import slugify


class Game(Model):
    name = CharField(max_length=128)

    def __str__(self):
        return self.name


class Achievement(Model):
    completed = BooleanField(default=False)
    name = CharField(max_length=128)
    game = ForeignKey(Game, on_delete=CASCADE)
    image = ImageField(blank=True, null=True)
    link = URLField(null=True, blank=True)
    description = TextField(null=True, blank=True)
    slug = SlugField(max_length=128, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# Create your models here.
