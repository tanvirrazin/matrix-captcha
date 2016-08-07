from __future__ import unicode_literals

from django.db import models


STATUS_CHOICES = (
    ('w', 'White Listed'),
    ('b', 'Black Listed'),
)

class ClientIP(models.Model):
    ip_address = models.GenericIPAddressField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    def __unicode__(self):
        return self.ip_address

