import factory

from .models import File


class FileFactory(factory.DjangoModelFactory):
    name = factory.sequence(lambda n: f'Name {n}')
    other = factory.django.FileField(filename='file.txt')
    image = factory.django.ImageField(filename='image.jpg', width=10, height=10)

    class Meta:
        model = File
