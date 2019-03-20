from django.db import models


class Mailing(models.Model):
    from_number = models.IntegerField(null=True)
    to_number = models.IntegerField(null=True)
    sent_on = models.DateTimeField(auto_now_add=True, null=True)
    received_on = models.DateTimeField(null=True)
    state = models.TextField(default='new')
    alert = models.BooleanField(default=False)
    number_of_signatures = models.IntegerField(default=0)
    valid_signatures = models.IntegerField(null=True)
    invalid_signatures = models.IntegerField(null=True)
    pdf_file = models.CharField(max_length=256, null=True)
    called_on = models.DateTimeField(null=True)

    municipality = models.ForeignKey(
        'municipalities.Municipality', on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
