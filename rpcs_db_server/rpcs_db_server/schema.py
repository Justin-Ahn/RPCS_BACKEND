import graphene
from graphene_django import DjangoObjectType

from stm.models import Results


class ResultsType(DjangoObjectType):
    class Meta:
        model = Results


class Query(graphene.ObjectType):
    links = graphene.List(ResultsType)

    def resolve_links(self, info, **kwargs):
        return Results.objects.all()