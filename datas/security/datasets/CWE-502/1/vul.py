from django.conf.urls import url
import pickle

def deserialize(pickled):
    return pickle.loads(pickled)

urlpatterns = [
    url(r'^(?P<object>.*)$', deserialize)
]