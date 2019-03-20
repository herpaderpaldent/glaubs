from django.db import models


class Municipality(models.Model):
    name = models.CharField(max_length=100, null=True)
    zip_code = models.IntegerField()
    bfs_number = models.IntegerField(null=True)
    main_municipality = models.BooleanField(default=False)
    address = models.TextField(null=True, blank=True)
    phone_number = models.TextField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    political_municipality = models.ForeignKey(
        'self', null=True, on_delete=models.PROTECT)
    language = models.CharField(max_length=10, default='de')
    canton = models.CharField(max_length=2, null=True)
    website = models.TextField(null=True, blank=True)
    email = models.TextField(null=True, blank=True)
    verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
