
from django.conf.urls import url
import json

def deserialize(pickled):
    return json.loads(pickled)

urlpatterns = [
    url(r'^(?P<object>.*)$', deserialize)
]