from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('jar/', views.jar, name='jar'),
    path('jar/<int:jar_id>', views.jar, name='jar_with_id'),
    path('transaction/', views.transaction, name='transaction'),
]


'''
API
GET /thesloiks/jar wyswietla wszystkie sloiki (id, balance, currency)
GET /thesloiks/jar/1 wyswietla sloik o id 1
POST /thesloiks/jar JSON (stworzenie sloika)

POST /thesloiks/transaction JSON (włożenie, wyjęcie, transfer środków)
GET /thesloiks/transaction?jarId=1 przejrzenie historii operacji w sloiku
GET /thesloiks/transaction?jarId=1&sortBy=balance&sortOrder=desc przejrzenie posortowanej historii operacji w sloiku
GET /thesloiks/transaction przejrzenie historii wszystkich operacji
GET /thesloiks/transaction?jarId=1,2 przejrzenie historii wszystkich operacji filtrowanej
'''