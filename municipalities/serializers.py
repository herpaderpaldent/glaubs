from rest_framework import serializers

from municipalities.models import Municipality


class MunicipalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipality

        fields = ('id', 'name', 'zip_code', 'address', 'phone_number',
                  'main_municipality', 'canton', 'comment',
                  'bfs_number', 'email', 'website', 'language', 'verified')
        read_only_fields = ('id', 'created_at', 'updated_at')
