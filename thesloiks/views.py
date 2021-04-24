from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from django.db import transaction
from django.db.models import Q
import io
from .models import Jar, Transaction
from .constants import *
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import ParseError
from .serializers import JarSerializer, TransactionSerializer, ValidationException
import re


def index(request):
    return HttpResponse(msg_welcome)


@csrf_exempt
def jar(request, jar_id=None):
    if request.method == 'GET':
        if jar_id:
            return get_jar_with_id(request, jar_id)
        return get_all_jars(request)
    elif request.method == 'POST':
        return post_new_jar(request)
    return HttpResponse(content=msg_method_now_allowed, status=405)


def post_new_jar(request):
    if request.body:
        stream = io.BytesIO(request.body)
        try:
            new_jar = JSONParser().parse(stream)
        except ParseError:
            return HttpResponse(content=msg_not_json_body, status=400)
        jar_serializer = JarSerializer(data=new_jar)
        try:
            jar_serializer.validate()
            jar_serializer.create()
        except ValidationException as e:
            return HttpResponse(content=e.message, status=e.status_code)
    else:
        return HttpResponse(content=msg_request_without_body, status=400)
    return HttpResponse(content=msg_jar_created, status=200)


def get_jar_with_id(request, jar_id):
    jars_list = Jar.objects.filter(id=jar_id)
    template = loader.get_template('thesloiks/jar.html')
    context = {
        'jars_list': jars_list,
        'single': True,
    }
    return HttpResponse(template.render(context, request))


def get_all_jars(request):
    jars_list = Jar.objects.all()
    template = loader.get_template('thesloiks/jar.html')
    context = {
        'jars_list': jars_list,
        'single': False,
    }
    return HttpResponse(template.render(context, request))


@csrf_exempt
@transaction.atomic
def transaction(request):
    if request.method == 'POST':
        return post_new_transaction(request)
    elif request.method == 'GET':
        return get_transactions(request)
    return HttpResponse(content=msg_method_now_allowed, status=405)


def post_new_transaction(request):
    if request.body:
        stream = io.BytesIO(request.body)
        try:
            new_transaction = JSONParser().parse(stream)
        except ParseError:
            return HttpResponse(content=msg_not_json_body, status=400)
        transaction_serializer = TransactionSerializer(data=new_transaction)
        try:
            transaction_serializer.validate()
            transaction_serializer.create()
            return HttpResponse(content=msg_transaction_created, status=200)
        except ValidationException as e:
            return HttpResponse(content=e.message, status=e.status_code)
    else:
        return HttpResponse(content=msg_request_without_body, status=400)


def get_transactions(request):
    jars_ids = request.GET['jarsIds'] if 'jarsIds' in request.GET else None
    if jars_ids and not re.fullmatch(r'[0-9]+(,[0-9]+)*', jars_ids):
        return HttpResponse(content=msg_wrong_jars_ids, status=400)
    sort_order = request.GET['sortOrder'] if 'sortOrder' in request.GET else None
    sort_by = request.GET['sortBy'] if 'sortBy' in request.GET else None
    if sort_order:
        if not sort_by:
            return HttpResponse(content=msg_missing_sort_by, status=400)
        if sort_order not in ['asc', 'desc']:
            return HttpResponse(content=msg_wrong_sort_order, status=400)
    if sort_by and sort_by not in ['date_created', 'value', 'type', 'title', 'currency']:
        return HttpResponse(content=msg_wrong_sort_by, status=400)
    sort_by = '-' + sort_by if sort_by else '-date_created'
    if sort_order and sort_order == 'asc':
        sort_by = sort_by[1:]
    if jars_ids:
        jars_ids = jars_ids.split(',')
        transactions_list = Transaction.objects.filter(Q(target_jar__in=jars_ids) | Q(source_jar__in=jars_ids)).order_by(sort_by)
    else:
        transactions_list = Transaction.objects.all().order_by(sort_by)
    template = loader.get_template('thesloiks/transaction.html')
    context = {
        'transactions_list': transactions_list
    }
    return HttpResponse(template.render(context, request))
