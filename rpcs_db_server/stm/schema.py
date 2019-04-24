import graphene
from graphene_django import DjangoObjectType

from .models import Results
from django.db.models import Q

class StmType(DjangoObjectType):
	class Meta:
		model = Results

class CreateResults(graphene.Mutation):
	#results = graphene.Field(StmType)
	patient_name = graphene.String()
	patient_id = graphene.Int()
	scaled_rating1 = graphene.Int()	
	scaled_rating2 = graphene.Int()	
	test_results = graphene.String()

	class Arguments:
		patient_name = graphene.String()
		patient_id = graphene.Int()
		scaled_rating1 = graphene.Int()	
		scaled_rating2 = graphene.Int()	
		test_results = graphene.String()
		
	def mutate(self, info, patient_name, patient_id, scaled_rating1,
		scaled_rating2, test_results):
		user = info.context.user or None
		
		res = Results(patient_name=patient_name, patient_id=patient_id,
			scaled_rating1=scaled_rating1, scaled_rating2=scaled_rating2,
			test_results=test_results)
		res.save()

		return CreateResults(
			patient_name = res.patient_name,
			patient_id = res.patient_id,
			scaled_rating1 = res.scaled_rating1,
			scaled_rating2 = res.scaled_rating2,
			test_results = res.test_results
		)

class Query(graphene.ObjectType):
	results = graphene.List(StmType, id = graphene.Int())
	
	def resolve_results(self, info, id=-1, **kwargs):
		if id>=0:
			filter = (
				Q(patient_id=id)
			)
			return Results.objects.filter(filter)

		return Results.objects.all()

class Mutation(graphene.ObjectType):
	create_results = CreateResults.Field()
