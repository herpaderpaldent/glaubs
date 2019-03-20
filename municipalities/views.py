from django.db.models import Q

from rest_framework import viewsets, response, status
from rest_framework.views import APIView

from municipalities.models import Municipality
from municipalities.serializers import MunicipalitySerializer


class MunicipalityViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Municipality.objects.all()
    serializer_class = MunicipalitySerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            Municipality.objects.create(**serializer.validated_data)

            return response.Response(
                serializer.validated_data, status=status.HTTP_201_CREATED)

        return response.Response({
            'status': 'Bad request',
            'message': 'Couldnt validate'
        }, status=status.HTTP_400_BAD_REQUEST)


class SearchMunicipality(APIView):

    serializer_class = MunicipalitySerializer

    def get(self, request):
        q = request.query_params['q']
        zip_code = None
        name = None
        try:
            zip_code = int(q)
        except ValueError:
            name = q

        try:
            municipalities = []
            if zip_code is not None:
                municipalities = \
                    Municipality.objects.filter(zip_code=zip_code)
            elif name is not None:
                municipalities = \
                    Municipality.objects.filter(Q(name__startswith=name))

            # prioritize main municipalities
            municipalities = municipalities.order_by('-main_municipality')

            serializer = \
                self.serializer_class(data=municipalities[:50], many=True)
            serializer.is_valid()
            return response.Response(serializer.data)
        except Municipality.DoesNotExist:
            serializer = self.serializer_class(data=[], many=True)
            serializer.is_valid()
            return response.Response(serializer.data)


class PrimaryMunicipality(APIView):

    serializer_class = MunicipalitySerializer

    def get(self, request):
        id = request.query_params['id']
        selected = Municipality.objects.get(id=id)
        same_bfs_number = \
            Municipality.objects.filter(bfs_number=selected.bfs_number)
        primary = selected
        for m in same_bfs_number:
            if m.main_municipality:
                primary = m
                break

        serializer = self.serializer_class(primary)
        return response.Response(serializer.data)


class RelatedMunicipalities(APIView):

    def get(self, request):
        id = request.query_params['id']
        selected = Municipality.objects.get(id=id)
        same_bfs_number = \
            Municipality.objects.filter(bfs_number=selected.bfs_number)
        result = []
        for m in same_bfs_number:
            result.append({
                'zip_code': m.zip_code,
                'name': m.name,
                'id': m.id,
                'primary': m.main_municipality
            })

        return response.Response(result)
