from django.db import models
from stdimage.models import StdImageField

# SIGNALS
from django.db.models import signals
from django.template.defaultfilters import slugify

from paho.mqtt import publish
from .encodings import generate_encodings, save_encoding, delete_encoding


class Base(models.Model):
    created = models.DateField('Data de criação', auto_now_add=True)
    modified = models.DateField('Data de atualização', auto_now=True)
    
    class Meta:
        abstract = True


class Owner(Base):
    name = models.CharField('Nome', max_length=100, null=True, blank=True)
    cpf = models.CharField('CPF', max_length=11, unique=True, null=False, default='00000000000')
    password = models.CharField('Senha', max_length=50, null=False, blank=False, default='123456')
    first_access = models.BooleanField('Primeiro acesso', default=True, null=False, blank=False)
    chat_id = models.CharField('Chat ID', max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class Guest(Base):
    name = models.CharField('Nome', max_length=100, null=False, blank=False)
    cpf = models.CharField('CPF', max_length=11, unique=True, null=False)
    nickname = models.CharField('Apelido', max_length=100, null=True, blank=True)
    relationship = models.CharField('Parentesco', max_length=100, null=True, blank=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, null=False, blank=False, default='1')

    def __str__(self):
        return self.name 


class Photo(Base):
    file = StdImageField('Foto', upload_to='photo', variations={'thumb': {'width': 480, 'height': 480, 'crop': True}}, null=False, blank=False)
    slug = models.SlugField('Slug', max_length=100, blank=True, editable=False)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, null=True, blank=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.slug


class Access(models.Model):
    date = models.DateField('Data de acesso', auto_now_add=True)
    hour = models.TimeField('Hora de acesso', auto_now_add=True)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, null=False, blank=False)
    
    def __str__(self):
        return f"Acesso de {self.guest.name} em {self.data} às {self.hora} - Proprietário: {self.guest.owner.name}"

    
def photo_pre_save(signal, instance, sender, **kwargs):
    instance.slug = slugify(instance.file)

signals.pre_save.connect(photo_pre_save, sender=Photo)


def photo_post_save(sender, instance, created, **kwargs):
    if created:
        path = "media/photo/"
        file_name = str(instance.file.name).replace("photo/", "")
        encodings = generate_encodings(path + str(file_name))
        if instance.guest:
            filename = f"{instance.guest.cpf}--{str(file_name)}"
            topic = f"ssmai/encodings/{instance.guest.owner.cpf}"
            message = f"ADDED {filename}"
        else:
            filename = f"{instance.owner.cpf}--{str(file_name)}"
            topic = f"ssmai/encodings/{instance.cpf}"
        message = f"ADDED {filename}"
        save_encoding(path, filename, encodings)
        publish.single(topic, message, hostname="localhost")

signals.post_save.connect(photo_post_save, sender=Photo)


def photo_pre_delete(sender, instance, **kwargs):
    path = "media/encoding/"
    file_name = str(instance.file.name).replace("photo/", "")
    if instance.guest:
        filename = f"{instance.guest.cpf}--{str(file_name)}"
        topic = f"ssmai/encodings/{instance.guest.owner.cpf}"
        message = f"DELETE {instance.guest.cpf}--{file_name}"
    else:
        filename = f"{instance.owner.cpf}--{str(file_name)}"
        topic = f"ssmai/encodings/{instance.cpf}"
        message = f"DELETE {instance.owner.cpf}--{file_name}"
    publish.single(topic, message, hostname="localhost")
    delete_encoding(path, filename)

signals.pre_delete.connect(photo_pre_delete, sender=Photo)