import graphene
from graphene_django import DjangoObjectType

#from stm.models import Results

import stm.schema
import int.schema

#class ResultsType(DjangoObjectType):
#    class Meta:
#        model = Results


class Query(stm.schema.Query, int.schema.Query, graphene.ObjectType):
    #links = graphene.List(ResultsType)
	pass

    #def resolve_links(self, info, **kwargs):
    #    return Results.objects.all()

class Mutation(stm.schema.Mutation, int.schema.Mutation, graphene.ObjectType):
	pass

schema = graphene.Schema(query=Query, mutation=Mutation)
