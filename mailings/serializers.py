from rest_framework import serializers

from mailings.models import Mailing


class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing

        fields = (
            'pk', 'sent_on', 'received_on', 'state', 'alert',
            'number_of_signatures', 'valid_signatures', 'invalid_signatures',
            'municipality', 'from_number', 'to_number',
            'created_at', 'updated_at', 'called_on')
        read_only_fields = ('pk', 'created_at', 'updated_at')
