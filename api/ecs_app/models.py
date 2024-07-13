# models.py

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class UserProfile(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    # Aplicar related_name directamente en los campos de relación
    groups = models.ManyToManyField(Group, related_name='user_profiles_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='user_profiles_permissions')

    def __str__(self):
        return self.username

import socket

class DockerContainer(models.Model):
    name = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    port = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        # Convierte el nombre del host a una dirección IP
        try:
            ip_address = socket.gethostbyname(self.ip_address)
            self.ip_address = ip_address
        except socket.error:
            pass  # Manejar el caso en el que no se pueda resolver el nombre del host

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name