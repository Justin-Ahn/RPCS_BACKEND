from stm.models import Results
from graphene import ObjectType, Node, Schema
from graphene_django.fields import DjangoConnectionField
from graphene_django.types import DjangoObjectType

class ResultsNode(DjangoObjectType):

    class Meta:
        model = Results
        interfaces = (Node, )

class Query(ObjectType):
    category = Node.Field(ResultsNode)
    all_categories = DjangoConnectionField(ResultsNode)

schema = Schema(query=Query)