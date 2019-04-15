import graphene
from graphene_django import DjangoObjectType

from stm.models import Results


class ResultsType(DjangoObjectType):
    class Meta:
        model = Results


class Query(graphene.ObjectType):
    links = graphene.List(LinkType)

    def resolve_links(self, info, **kwargs):
        return Link.objects.all()