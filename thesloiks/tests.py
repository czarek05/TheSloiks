import json
from django.test import TestCase
from .constants import *
from .models import Jar, Transaction


class JarTests(TestCase):

    def test_jar_method_not_allowed(self):
        response = self.client.generic('DELETE', path='/thesloiks/jar/')
        self.assertEqual(response.status_code, 405)
        self.assertTrue(msg_method_now_allowed in str(response.content))

    def test_get_jar_with_id_happy_path(self):
        jar = Jar(balance=0.0, currency='PLN')
        jar.save()
        get_jar_with_id_part_of_content_two = f'<td>{jar.id}</td>'

        response = self.client.generic('GET', path='/thesloiks/jar/1')
        self.assertEqual(response.status_code, 200)
        response_content = str(response.content)
        self.assertTrue(get_jar_with_id_part_of_content_one in response_content)
        self.assertTrue(get_jar_with_id_part_of_content_two in response_content)

    def test_get_all_jars_happy_path(self):
        jar_one = Jar(balance=0.0, currency='PLN')
        jar_one.save()
        jar_two = Jar(balance=0.0, currency='USD')
        jar_two.save()
        get_all_jars_part_of_content_four = f'<td>{jar_one.id}</td>'
        get_all_jars_part_of_content_five = f'<td>{jar_two.id}</td>'

        response = self.client.generic('GET', path='/thesloiks/jar/')
        self.assertEqual(response.status_code, 200)
        response_content = str(response.content)
        self.assertTrue(get_all_jars_part_of_content_one in response_content)
        self.assertTrue(get_all_jars_part_of_content_two in response_content)
        self.assertTrue(get_all_jars_part_of_content_three in response_content)
        self.assertTrue(get_all_jars_part_of_content_four in response_content)
        self.assertTrue(get_all_jars_part_of_content_five in response_content)

    def test_post_new_jar_not_json_body(self):
        response = self.client.generic('POST', path='/thesloiks/jar/', data=not_json_body)
        self.assertEqual(response.status_code, 400)
        self.assertTrue(msg_not_json_body in str(response.content))

    def test_post_new_jar_without_body(self):
        response = self.client.generic('POST', path='/thesloiks/jar/')
        self.assertEqual(response.status_code, 400)
        self.assertTrue(msg_request_without_body in str(response.content))

    def test_post_new_jar_number_of_fields_ne_one(self):
        response = self.client.generic('POST', path='/thesloiks/jar/',
                                       data=json.dumps(post_new_jar_number_of_fields_ne_one),
                                       content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertTrue(msg_jar_wrong_body in str(response.content))

    def test_post_new_jar_missing_currency(self):
        response = self.client.generic('POST', path='/thesloiks/jar/',
                                       data=json.dumps(post_new_jar_missing_currency),
                                       content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertTrue(msg_jar_wrong_body in str(response.content))

    def test_post_new_jar_not_supported_currency(self):
        response = self.client.generic('POST', path='/thesloiks/jar/',
                                       data=json.dumps(post_new_jar_not_supported_currency),
                                       content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertTrue(msg_unsupported_currency in str(response.content))

    def test_post_new_jar_happy_path(self):
        response = self.client.generic('POST', path='/thesloiks/jar/', data=json.dumps(post_new_jar_proper_data),
                                       content_type="application/json")
        all_jars = Jar.objects.all()
        created_jar = all_jars[0]
        self.assertEqual(len(all_jars), 1)
        self.assertEqual(created_jar.currency, 'PLN')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(msg_jar_created in str(response.content))


class TransactionTests(TestCase):

    def test_transaction_method_not_allowed(self):
        response = self.client.generic('DELETE', path='/thesloiks/transaction/')
        self.assertEqual(response.status_code, 405)
        self.assertTrue(msg_method_now_allowed in str(response.content))

    def test_get_transactions_wrong_jars_ids_format(self):
        response = self.client.get(path='/thesloiks/transaction/', data=get_transactions_wrong_jars_ids_format)
        self.assertEqual(response.status_code, 400)
        self.assertTrue(msg_wrong_jars_ids in str(response.content))

    def test_get_transactions_missing_sort_by(self):
        response = self.client.get(path='/thesloiks/transaction/', data=get_transactions_missing_sort_by)
        self.assertEqual(response.status_code, 400)
        self.assertTrue(msg_missing_sort_by in str(response.content))

    def test_get_transactions_wrong_sort_order(self):
        response = self.client.get(path='/thesloiks/transaction/', data=get_transactions_wrong_sort_order)
        self.assertEqual(response.status_code, 400)
        self.assertTrue(msg_wrong_sort_order in str(response.content))

    def test_get_transactions_wrong_sort_by(self):
        response = self.client.get(path='/thesloiks/transaction/', data=get_transactions_wrong_sort_by)
        self.assertEqual(response.status_code, 400)
        self.assertTrue(msg_wrong_sort_by in str(response.content))

    def test_get_transactions_happy_path(self):
        source_jar = Jar(balance=100.0, currency='PLN')
        target_jar = Jar(balance=0.0, currency='PLN')
        source_jar.save()
        target_jar.save()
        post_new_transaction_happy_path['sourceJar'] = source_jar.id
        post_new_transaction_happy_path['targetJar'] = target_jar.id
        jarsIds = str(source_jar.id) + ',' + str(target_jar.id)
        self.client.generic('POST', path='/thesloiks/transaction/', data=json.dumps(post_new_transaction_happy_path),
                            content_type="application/json")
        get_transactions_happy_path['jarsIds'] = jarsIds
        get_transactions_part_of_content_five = f'<td>{source_jar.id}</td>'
        get_transactions_part_of_content_six = f'<td>{target_jar.id}</td>'

        response = self.client.get(path='/thesloiks/transaction/', data=get_transactions_happy_path)
        self.assertEqual(response.status_code, 200)
        response_content = str(response.content)
        self.assertTrue(get_transactions_part_of_content_one in response_content)
        self.assertTrue(get_transactions_part_of_content_two in response_content)
        self.assertTrue(get_transactions_part_of_content_three in response_content)
        self.assertTrue(get_transactions_part_of_content_four in response_content)
        self.assertTrue(get_transactions_part_of_content_five in response_content)
        self.assertTrue(get_transactions_part_of_content_six in response_content)

    def test_post_new_transaction_not_json_body(self):
        response = self.client.generic('POST', path='/thesloiks/transaction/', data=not_json_body)
        self.assertEqual(response.status_code, 400)
        self.assertTrue(msg_not_json_body in str(response.content))

    def test_post_new_transaction_without_body(self):
        response = self.client.generic('POST', path='/thesloiks/transaction/')
        self.assertEqual(response.status_code, 400)
        self.assertTrue(msg_request_without_body in str(response.content))

    def test_post_new_transaction_forbidden_fields(self):
        response = self.client.generic('POST', path='/thesloiks/transaction/',
                                       data=json.dumps(post_new_transaction_forbidden_fields),
                                       content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertTrue(msg_transaction_forbidden_fields in str(response.content))

    def test_post_new_transaction_missing_required_fields(self):
        response = self.client.generic('POST', path='/thesloiks/transaction/',
                                       data=json.dumps(post_new_transaction_missing_required_fields),
                                       content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertTrue(msg_transaction_missing_required_fields in str(response.content))

    def test_post_new_transaction_missing_target_jar_and_source_jar(self):
        response = self.client.generic('POST', path='/thesloiks/transaction/',
                                       data=json.dumps(post_new_transaction_missing_target_jar_and_source_jar),
                                       content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertTrue(msg_transaction_missing_target_jar_and_source_jar in str(response.content))

    def test_post_new_transaction_value_not_a_number(self):
        response = self.client.generic('POST', path='/thesloiks/transaction/',
                                       data=json.dumps(post_new_transaction_value_not_a_number),
                                       content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertTrue(msg_transaction_wrong_value in str(response.content))

    def test_post_new_transaction_value_lt_zero(self):
        response = self.client.generic('POST', path='/thesloiks/transaction/',
                                       data=json.dumps(post_new_transaction_value_lt_zero),
                                       content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertTrue(msg_transaction_wrong_value in str(response.content))

    def test_post_new_transaction_value_too_big(self):
        response = self.client.generic('POST', path='/thesloiks/transaction/',
                                       data=json.dumps(post_new_transaction_value_too_big),
                                       content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertTrue(msg_transaction_wrong_value in str(response.content))

    def test_post_new_transaction_value_three_decimal_places(self):
        response = self.client.generic('POST', path='/thesloiks/transaction/',
                                       data=json.dumps(post_new_transaction_value_three_decimal_places),
                                       content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertTrue(msg_transaction_wrong_value in str(response.content))

    def test_post_new_transaction_unsupported_currency(self):
        response = self.client.generic('POST', path='/thesloiks/transaction/',
                                       data=json.dumps(post_new_transaction_unsupported_currency),
                                       content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertTrue(msg_unsupported_currency in str(response.content))

    def test_post_new_transaction_wrong_target_jar(self):
        response = self.client.generic('POST', path='/thesloiks/transaction/',
                                       data=json.dumps(post_new_transaction_wrong_target_jar),
                                       content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertTrue(msg_transaction_wrong_target_jar in str(response.content))

    def test_post_new_transaction_unexisting_target_jar(self):
        response = self.client.generic('POST', path='/thesloiks/transaction/',
                                       data=json.dumps(post_new_transaction_unexisting_target_jar),
                                       content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertTrue(msg_transaction_target_jar_not_exist in str(response.content))

    def test_post_new_transaction_currencies_conflict_target_jar(self):
        jar = Jar(balance=0.0, currency='USD')
        jar.save()
        post_new_transaction_currencies_conflict_target_jar['targetJar'] = jar.id

        response = self.client.generic('POST', path='/thesloiks/transaction/',
                                       data=json.dumps(post_new_transaction_currencies_conflict_target_jar),
                                       content_type="application/json")
        self.assertEqual(response.status_code, 409)
        self.assertTrue(msg_transaction_currencies_conflict_target_jar in str(response.content))

    def test_post_new_transaction_wrong_source_jar(self):
        response = self.client.generic('POST', path='/thesloiks/transaction/',
                                       data=json.dumps(post_new_transaction_wrong_source_jar),
                                       content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertTrue(msg_transaction_wrong_source_jar in str(response.content))

    def test_post_new_transaction_jars_conflict(self):
        jar = Jar(balance=0.0, currency='PLN')
        jar.save()
        post_new_transaction_jars_conflict['targetJar'] = jar.id
        post_new_transaction_jars_conflict['sourceJar'] = jar.id

        response = self.client.generic('POST', path='/thesloiks/transaction/',
                                       data=json.dumps(post_new_transaction_jars_conflict),
                                       content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertTrue(msg_transaction_jars_conflict in str(response.content))

    def test_post_new_transaction_unexisting_source_jar(self):
        response = self.client.generic('POST', path='/thesloiks/transaction/',
                                       data=json.dumps(post_new_transaction_unexisting_source_jar),
                                       content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertTrue(msg_transaction_source_jar_not_exist in str(response.content))

    def test_post_new_transaction_currencies_conflict_source_jar(self):
        jar = Jar(balance=0.0, currency='USD')
        jar.save()
        post_new_transaction_currencies_conflict_source_jar['sourceJar'] = jar.id

        response = self.client.generic('POST', path='/thesloiks/transaction/',
                                       data=json.dumps(post_new_transaction_currencies_conflict_source_jar),
                                       content_type="application/json")
        self.assertEqual(response.status_code, 409)
        self.assertTrue(msg_transaction_currencies_conflict_source_jar in str(response.content))

    def test_post_new_transaction_insufficient_funds(self):
        jar = Jar(balance=100.0, currency='PLN')
        jar.save()
        post_new_transaction_insufficient_funds['sourceJar'] = jar.id

        response = self.client.generic('POST', path='/thesloiks/transaction/',
                                       data=json.dumps(post_new_transaction_insufficient_funds),
                                       content_type="application/json")
        self.assertEqual(response.status_code, 409)
        self.assertTrue(msg_transaction_insufficient_funds in str(response.content))

    def test_post_new_transaction_too_long_title(self):
        response = self.client.generic('POST', path='/thesloiks/transaction/',
                                       data=json.dumps(post_new_transaction_too_long_title),
                                       content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertTrue(msg_transaction_too_long_title in str(response.content))

    def test_post_new_transaction_happy_path(self):
        source_jar = Jar(balance=100.0, currency='PLN')
        target_jar = Jar(balance=0.0, currency='PLN')
        source_jar.save()
        target_jar.save()
        post_new_transaction_happy_path['sourceJar'] = source_jar.id
        post_new_transaction_happy_path['targetJar'] = target_jar.id

        response = self.client.generic('POST', path='/thesloiks/transaction/',
                                       data=json.dumps(post_new_transaction_happy_path),
                                       content_type="application/json")

        source_jar = Jar.objects.get(pk=source_jar.id)
        target_jar = Jar.objects.get(pk=target_jar.id)
        all_transactions = Transaction.objects.all()
        created_transaction = all_transactions[0]
        self.assertEqual(len(all_transactions), 1)
        self.assertEqual(created_transaction.type, 'TRANSFER')
        self.assertEqual(created_transaction.value, 50)
        self.assertEqual(created_transaction.title, 'Jar operation')
        self.assertEqual(created_transaction.currency, 'PLN')
        self.assertEqual(created_transaction.source_jar.id, source_jar.id)
        self.assertEqual(created_transaction.target_jar.id, target_jar.id)
        self.assertEqual(float(source_jar.balance), 100.0 - post_new_transaction_happy_path['value'])
        self.assertEqual(float(target_jar.balance), 0.0 + post_new_transaction_happy_path['value'])
        self.assertEqual(response.status_code, 200)
        self.assertTrue(msg_transaction_created in str(response.content))
