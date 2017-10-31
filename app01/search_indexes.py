import datetime
from haystack import indexes
from app01.models import BBS

class BBSIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='author')
    created_at = indexes.DateTimeField(model_attr='created_at')

    def get_model(self):
        return BBS

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(created_at__lte=datetime.datetime.now())

