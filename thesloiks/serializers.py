from .models import Jar, Transaction
from django.utils import timezone
from .constants import *


class ValidationException(Exception):

    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code


class JarSerializer():
    supported_currencies = ['PLN', 'EUR', 'USD']

    def __init__(self, data):
        self.data = data

    def validate(self):
        data = self.data
        currency = data['currency'] if 'currency' in data else None
        if len(data) != 1:
            raise ValidationException(msg_jar_wrong_body, 400)
        if not currency:
            raise ValidationException(msg_jar_wrong_body, 400)
        if currency not in JarSerializer.supported_currencies:
            raise ValidationException(msg_unsupported_currency, 400)
        return True

    def create(self):
        self.data['balance'] = 0.0
        db_new_jar = Jar.objects.create(**self.data)
        return db_new_jar


class TransactionSerializer():
    required_fields = ['value', 'currency']
    all_fields = ['targetJar', 'value', 'currency', 'title', 'sourceJar']
    supported_currencies = ['PLN', 'EUR', 'USD']
    # approximated value of all money in the world (PLN)
    max_value = 5200000000000000

    def __init__(self, data):
        self.data = data

    def validate(self):
        data = self.data
        if not all([data_field in TransactionSerializer.all_fields for data_field in data]):
            raise ValidationException(msg_transaction_forbidden_fields, 400)
        if not all([required_field in data for required_field in TransactionSerializer.required_fields]):
            raise ValidationException(msg_transaction_missing_required_fields, 400)
        data_fields = list(data.keys())
        if len(data_fields) != len(set(data_fields)):
            raise ValidationException(msg_transaction_not_unique_fields, 400)
        if 'targetJar' not in data and 'sourceJar' not in data:
            raise ValidationException(msg_transaction_missing_target_jar_and_source_jar, 400)
        value = data['value']
        currency = data['currency']
        if not (isinstance(value, float) or isinstance(value,
                                                       int)) or value > TransactionSerializer.max_value or value <= 0.0:
            raise ValidationException(msg_transaction_wrong_value, 400)
        str_value = str(value)
        if '.' in str_value and len(str_value[str_value.rfind('.')+1:]) > 2:
            raise ValidationException(msg_transaction_wrong_value, 400)
        if currency not in TransactionSerializer.supported_currencies:
            raise ValidationException(msg_unsupported_currency, 400)
        title = data['title'] if 'title' in data else None
        if title and (not isinstance(title, str) or len(title) > 250):
            raise ValidationException(msg_transaction_too_long_title, 400)
        target_jar = data['targetJar'] if 'targetJar' in data else None
        if target_jar:
            if not isinstance(target_jar, int) or target_jar < 1:
                raise ValidationException(msg_transaction_wrong_target_jar, 400)
            db_target_jar_query = Jar.objects.filter(id=target_jar)
            if not db_target_jar_query:
                raise ValidationException(msg_transaction_target_jar_not_exist, 404)
            if db_target_jar_query[0].currency != currency:
                raise ValidationException(msg_transaction_currencies_conflict_target_jar, 409)
        source_jar = data['sourceJar'] if 'sourceJar' in data else None
        if source_jar:
            if not isinstance(source_jar, int) or source_jar < 1:
                raise ValidationException(msg_transaction_wrong_source_jar, 400)
            if target_jar and source_jar == target_jar:
                raise ValidationException(msg_transaction_jars_conflict, 400)
            db_source_jar_query = Jar.objects.filter(id=source_jar)
            if not db_source_jar_query:
                raise ValidationException(msg_transaction_source_jar_not_exist, 404)
            db_source_jar = db_source_jar_query[0]
            if db_source_jar.currency != currency:
                raise ValidationException(msg_transaction_currencies_conflict_source_jar, 409)
            if db_source_jar.balance < value:
                raise ValidationException(msg_transaction_insufficient_funds, 409)
        return True

    def create(self):
        db_new_transaction = Transaction(date_created=timezone.now(), value=self.data['value'],
                                         currency=self.data['currency'])
        db_new_transaction.title = self.data['title'] if 'title' in self.data else 'Jar operation'
        if 'targetJar' in self.data and 'sourceJar' in self.data:
            db_new_transaction.type = 'TRANSFER'
        else:
            db_new_transaction.type = 'WITHDRAW' if 'sourceJar' in self.data else 'DEPOSIT'
        if 'targetJar' in self.data:
            db_target_jar = Jar.objects.get(pk=self.data['targetJar'])
            db_target_jar.balance = float(db_target_jar.balance) + self.data['value']
            db_new_transaction.target_jar = db_target_jar
            db_target_jar.save()
        if 'sourceJar' in self.data:
            db_source_jar = Jar.objects.get(pk=self.data['sourceJar'])
            db_source_jar.balance = float(db_source_jar.balance) - self.data['value']
            db_new_transaction.source_jar = db_source_jar
            db_source_jar.save()
        db_new_transaction.save()
        return db_new_transaction
