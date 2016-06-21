import datetime
import os
import subprocess
import shutil
import tempfile
import time
from wsgiref.util import FileWrapper
from jinja2 import Environment, PackageLoader

from django.conf import settings
from django.db.models import Max
from django.http import HttpResponse

from rest_framework import viewsets, response, status, views

from mailings.models import Mailing
from mailings.serializers import MailingSerializer

import glaubs


class MailingViewSet(viewsets.ViewSet):
    lookup_field = 'id'
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

    def list(self, request, municipality_id=None):
        mailings = self.queryset.filter(municipality=municipality_id).order_by('-pk')

        if mailings is not None:
            serializer = self.serializer_class(data=mailings, many=True)
            serializer.is_valid()
            return response.Response(serializer.data)

        serializer = self.serializer_class([], many=True)
        serializer.is_valid()
        return response.Response(serializer.data)

    def create(self, request, municipality_id=None):
        data = request.data
        data['municipality'] = municipality_id
        if str(data['to_number']).startswith('+'):
            data['to_number'] = int(data['to_number'][1:]) + int(data['from_number']) - 1

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            mailing = Mailing(**serializer.validated_data)
            mailing.save()

            serializer = self.serializer_class(mailing)
            serializer.data['municipality'] = None

            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response({'status': 'Bad request', 'message': 'Couldnt validate'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, id=None, municipality_id=None):
        data = request.data
        mailing = Mailing.objects.all().get(id=id, municipality=municipality_id)

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():

            old_state = mailing.state

            for key, value in serializer.validated_data.items():
                if key == 'municipality':
                    continue

                if getattr(mailing, key) != value:
                    setattr(mailing, key, value)

            # mark it as received if we have valid_signatures
            if old_state in ('sent', 'called') and mailing.valid_signatures:
                mailing.state = 'received'
                mailing.received_on = datetime.datetime.now()

            mailing.save()

            serializer = self.serializer_class(mailing)
            serializer.data['municipality'] = None

            return response.Response(serializer.data)

        return response.Response({'status': 'Bad request', 'message': 'Couldnt validate'}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, id=None, municipality_id=None):
        mailing = Mailing.objects.all().get(id=id, municipality=municipality_id)
        serializer = self.serializer_class(mailing)
        return response.Response(serializer.data)


class MailingMaxNumber(views.APIView):
    serializer_class = MailingSerializer

    def get(self, request):
        max_number = Mailing.objects.all().aggregate(Max('to_number'));

        return response.Response({'max_number': max_number['to_number__max']})


class MailingSearch(views.APIView):
    serializer_class = MailingSerializer

    def get(self, request):
        query = request.query_params['q']

        try:
            number = int(query)
        except ValueError:
            return response.Response({'status': 'Bad request', 'message': 'q must be an int'}, status=status.HTTP_400_BAD_REQUEST)

        mailings = Mailing.objects.filter(from_number__lte=number, to_number__gte=number)
        print(mailings.query)
        serializer = self.serializer_class(data=mailings, many=True)
        serializer.is_valid()
        return response.Response(serializer.data)


class MailingsRemider(views.APIView):
    serializer_class = MailingSerializer

    def get(self, request):
        state = request.query_params.get('state', 'sent')
        mailings = Mailing.objects.filter(state=state).order_by('-number_of_signatures')
        serializer = self.serializer_class(data=mailings, many=True)
        serializer.is_valid()
        return response.Response(serializer.data)


class MailingsMark(views.APIView):

    def post(self, request, municipality_id):
        print(repr(request.query_params))
        as_ = request.query_params['as']
        state = request.query_params['state']
        mailings = Mailing.objects.filter(state=state, municipality_id=municipality_id)
        if as_ == 'called':
            mailings.update(state=as_, called_on=datetime.datetime.now())
        else:
            mailings.update(state=as_)

        return response.Response({'success': True})


class PDFView(views.APIView):

    def get(self, request):
        municipality_id = request.query_params['municipality_id']
        id = request.query_params['id']
        target_file = self._get_or_create_mailing_pdf(id, municipality_id)

        wrapper = FileWrapper(open(target_file, 'rb'))
        resp = HttpResponse(wrapper, content_type='application/pdf')
        resp['Content-Length'] = os.path.getsize(target_file)
        return resp

    def _get_or_create_mailing_pdf(self, id, municipality_id):
        mailing = Mailing.objects.all().get(id=id, municipality=municipality_id)

        result = self._create_pdf(mailing)

        return result

    def _create_pdf(self, mailing):
        env = Environment(loader=PackageLoader('glaubs', 'tex'))
        template = env.get_template(os.path.join(mailing.municipality.language, 'anschreiben.tex'))
        params = {
            'recipient': mailing.municipality.address.replace('\n', ' \\\\ '),
            'listCount': mailing.to_number - mailing.from_number + 1,
            'listMin': mailing.from_number,
            'listMax': mailing.to_number,
            'sigCount': mailing.number_of_signatures,
            'dueDate': self._get_due_date().strftime('%d.%m.%Y'),
        }
        output = template.render(**params).encode('utf-8')

        target_file = '{}_{}_{}.pdf'.format(mailing.municipality.pk,
                                            mailing.pk,
                                            datetime.datetime.now().isoformat()[:19])
        target = os.path.join(self._get_target_dir(), target_file)

        with tempfile.TemporaryDirectory() as tempdir:
            process = subprocess.Popen(
                ['pdflatex', '-output-directory', tempdir],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                cwd=self._get_cwd()
            )
            process.communicate(output)

            shutil.move(os.path.join(tempdir, 'texput.pdf'), target)

        mailing.state = 'sent'
        mailing.pdf_file = target_file
        mailing.save()

        return target

    def _get_target_dir(self):
        retval = os.path.abspath(os.path.join(os.path.dirname(glaubs.__file__), '..', 'pdfs'))
        return retval

    def _get_cwd(self):
        retval = os.path.abspath(os.path.join(os.path.dirname(glaubs.__file__), 'tex'))
        return retval

    def _get_due_date(self):
        response_days = getattr(settings, "RESPONSE_DAYS", 8)
        retval = (datetime.datetime.now() + datetime.timedelta(days=response_days))
        return retval

