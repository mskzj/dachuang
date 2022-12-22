from haystack import indexes
from .models import Question
from account.models import User,Userinfo

class QuestionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    author = indexes.CharField(model_attr='user')
    question_date = indexes.DateTimeField(model_attr='question_date')
    question_type = indexes.CharField(model_attr='question_type')

    def get_model(self):
        return Question

    def index_queryset(self, using=None):
        return self.get_model().objects.all().order_by('-question_date')