msg_welcome = 'Welcome at the TheSloiks index.'
msg_method_now_allowed = 'Method Not Allowed.'
msg_request_without_body = 'Request without body. Please provide proper JSON body.'
msg_not_json_body = 'Wrong body. Please provide proper JSON body.'
msg_wrong_jars_ids = 'Param jarsIds must contain comma separated numbers. For example jarsIds=1,11,233'
msg_missing_sort_by = 'Param sortOrder provided, while param sortBy not. Please provide param sortBy or do not ' \
                      'provide param sortOrder.'
msg_wrong_sort_by = 'Param sortBy must be equal to a one value from list: date_created, value, type, title or currency'
msg_wrong_sort_order = 'Param sortOrder must be equal to: asc or desc'
msg_jar_created = 'New jar created successfully.'
msg_transaction_created = 'New transaction created successfully.'
msg_jar_wrong_body = 'Wrong body. Please provide proper JSON body. Request body must only contain one field: currency.'
msg_unsupported_currency = 'Provided currency is not supported. Please choose one from PLN, EUR, USD.'
msg_transaction_forbidden_fields = 'Wrong body. Please provide proper JSON body. Request body may only contain ' \
                                  'fields: targetJar, sourceJar, value, title and currency.'
msg_transaction_missing_required_fields = 'Wrong body. Please provide proper JSON body. ' \
                                          'Request body must contain fields: value and currency.'
msg_transaction_not_unique_fields = 'Wrong body. Please provide proper JSON body. Request body fields must be unique'
msg_transaction_missing_target_jar_and_source_jar = 'Wrong body. Please provide proper JSON body. Request body' \
                                                   ' must contain both or one from fields: targetJar, sourceJar.'
msg_transaction_wrong_value = 'Wrong value. Please provide proper JSON value. Value must be a positive, less than' \
                              ' 5200000000000000 number and has up to two decimal places.'
msg_transaction_wrong_target_jar = 'Wrong targetJar. Please provide proper targetJar. Field targetJar must be a ' \
                                   'positive integer.'
msg_transaction_target_jar_not_exist = 'Provided targetJar does not exist.'
msg_transaction_currencies_conflict_target_jar = 'Currencies of targetJar and transaction must be the same.'
msg_transaction_wrong_source_jar = 'Wrong sourceJar. Please provide proper sourceJar. Field sourceJar must be a ' \
                                   'positive integer.'
msg_transaction_jars_conflict = 'Wrong sourceJar or targetJar. Please provide proper sourceJar and targetJar. Fields' \
                                ' sourceJar and targetJar must be different.'
msg_transaction_source_jar_not_exist = 'Provided sourceJar does not exist.'
msg_transaction_currencies_conflict_source_jar = 'Currencies of source_jar and transaction must be the same.'
msg_transaction_insufficient_funds = 'Insufficient funds in sourceJar.'
msg_transaction_too_long_title = 'Title is too long. Please provide proper title. Field title must be text and' \
                                  ' up to 250 characters.'

# tests
not_json_body = 'aaa'
get_jar_with_id_part_of_content_one = '<h1 style="text">Requsted Jar:</h1>'
get_all_jars_part_of_content_one = '<h1 style="text">List of all Jars:</h1>'
get_all_jars_part_of_content_two = '<td>PLN</td>'
get_all_jars_part_of_content_three = '<td>USD</td>'
post_new_jar_proper_data = {'currency': 'PLN'}
post_new_jar_number_of_fields_ne_one = {'currency': 'PLN', 'unneededField': 1}
post_new_jar_missing_currency = {'unneededField': 1}
post_new_jar_not_supported_currency = {'currency': 'GBP'}


get_transactions_wrong_jars_ids_format = {'jarsIds': '[1, 2, 8]'}
get_transactions_missing_sort_by = {'jarsIds': '11,2,8', 'sortOrder': 'desc'}
get_transactions_wrong_sort_order = {'jarsIds': '11,2,8', 'sortBy': 'balance', 'sortOrder': 'aaa'}
get_transactions_wrong_sort_by = {'jarsIds': '11,2,8', 'sortBy': 'aaa', 'sortOrder': 'desc'}
get_transactions_happy_path = {'sortBy': 'type', 'sortOrder': 'asc'}
get_transactions_part_of_content_one = '<h1 style="text">Requsted Transactions:</h1>'
get_transactions_part_of_content_two = '<td>TRANSFER</td>'
get_transactions_part_of_content_three = '<td>50.00</td>'
get_transactions_part_of_content_four = '<th>From Jar</th>'
post_new_transaction_forbidden_fields = {'unneededField': 1, 'nextUnneededField': 2}
post_new_transaction_missing_required_fields = {'value': 100, 'targetJar': 1, 'sourceJar': 2, 'title': 'aaa'}
post_new_transaction_missing_target_jar_and_source_jar = {'value': 100, 'currency': 'PLN', 'title': 'aaa'}
post_new_transaction_value_not_a_number = {'value': 'aaa', 'currency': 'PLN', 'targetJar': 1, 'title': 'aaa'}
post_new_transaction_value_lt_zero = {'value': -1, 'currency': 'PLN', 'targetJar': 1, 'title': 'aaa'}
post_new_transaction_value_too_big = {'value': 999999999999999999999, 'currency': 'PLN', 'targetJar': 1, 'title': 'aaa'}
post_new_transaction_value_three_decimal_places = {'value': 1.999, 'currency': 'PLN', 'targetJar': 1, 'title': 'aaa'}
post_new_transaction_unsupported_currency = {'value': 1, 'currency': 'GBP', 'targetJar': 1, 'title': 'aaa'}
post_new_transaction_wrong_target_jar = {'value': 1, 'currency': 'PLN', 'targetJar': -1}
post_new_transaction_unexisting_target_jar = {'value': 1, 'currency': 'PLN', 'targetJar': 1}
post_new_transaction_currencies_conflict_target_jar = {'value': 1, 'currency': 'PLN'}
post_new_transaction_wrong_source_jar = {'value': 1, 'currency': 'PLN', 'sourceJar': -1}
post_new_transaction_jars_conflict = {'value': 1, 'currency': 'PLN', 'sourceJar': 1, 'targetJar': 1}
post_new_transaction_unexisting_source_jar = {'value': 1, 'currency': 'PLN', 'sourceJar': 1}
post_new_transaction_currencies_conflict_source_jar = {'value': 1, 'currency': 'PLN'}
post_new_transaction_insufficient_funds = {'value': 1000, 'currency': 'PLN'}
post_new_transaction_too_long_title = {'value': 1, 'currency': 'PLN', 'sourceJar': 1, 'title': 1000*'a'}
post_new_transaction_happy_path = {'currency': 'PLN', 'value': 50.0}




