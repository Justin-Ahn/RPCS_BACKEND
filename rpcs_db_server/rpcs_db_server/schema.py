import graphene
from graphene_django import DjangoObjectType

#from stm.models import Results

import stm.schema
import int.schema
import watch.schema
import wt.schema
import ga.schema
import ct.schema
import ca.schema
import hs.schema

#class ResultsType(DjangoObjectType):
#    class Meta:
#        model = Results


class Query(stm.schema.Query, int.schema.Query, watch.schema.Query, wt.schema.Query, ga.schema.Query, ct.schema.Query,
ca.schema.Query, hs.schema.Query, graphene.ObjectType):
    #links = graphene.List(ResultsType)
	pass

    #def resolve_links(self, info, **kwargs):
    #    return Results.objects.all()

class Mutation(stm.schema.Mutation, int.schema.Mutation, watch.schema.Mutation, wt.schema.Mutation, ga.schema.Mutation,
ct.schema.Mutation, ca.schema.Mutation, hs.schema.Mutation, graphene.ObjectType):
	pass

schema = graphene.Schema(query=Query, mutation=Mutation)
