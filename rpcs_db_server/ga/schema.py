import graphene
from graphene_django import DjangoObjectType

from .models import Logical, Semantic, Procedural, Episodic
from django.db.models import Q

class LogicalType(DjangoObjectType):
	class Meta:
		model = Logical

class SemanticType(DjangoObjectType):
    class Meta:
        model = Semantic

class ProceduralType(DjangoObjectType):
    class Meta:
        model = Procedural

class EpisodicType(DjangoObjectType):
    class Meta:
        model = Episodic

class CreateLogical(graphene.Mutation):
    patient_id = graphene.Int()
    logical_score = graphene.Int()
    timestamp = graphene.types.datetime.DateTime()
    game_id = graphene.Int()

    class Arguments:
        patient_id = graphene.Int()
        logical_score = graphene.Int()
        timestamp = graphene.types.datetime.DateTime()
        game_id = graphene.Int()

    def mutate(self, info, patient_id, logical_score, timestamp, game_id):
        user = info.context.user or None

        logical = Logical(patient_id=patient_id, logical_score=logical_score,
            timestamp=timestamp, game_id=game_id)
        logical.save()

        return CreateLogical(
            patient_id = logical.patient_id,
            logical_score = logical.logical_score,
            timestamp = logical.timestamp,
            game_id = logical.game_id
        )

class CreateSemantic(graphene.Mutation):
    patient_id = graphene.Int()
    semantic_score = graphene.Int()
    timestamp = graphene.types.datetime.DateTime()

    class Arguments:
        patient_id = graphene.Int()
        semantic_score = graphene.Int()
        timestamp = graphene.types.datetime.DateTime()

    def mutate(self, info, patient_id, semantic_score, timestamp):
        user = info.context.user or None
        sm = Semantic(patient_id=patient_id, semantic_score=semantic_score,
            timestamp=timestamp)
        sm.save()

        return CreateSemantic(
            patient_id = sm.patient_id,
            semantic_score = sm.semantic_score,
            timestamp = sm.timestamp
        )

class CreateProcedural(graphene.Mutation):
    patient_id = graphene.Int()
    procedural_score = graphene.Int()
    timestamp = graphene.types.datetime.DateTime()

    class Arguments:
        patient_id = graphene.Int()
        procedural_score = graphene.Int()
        timestamp = graphene.types.datetime.DateTime()

    def mutate(self, info, patient_id, procedural_score, timestamp):
        user = info.context.user or None
        pr = Procedural(patient_id=patient_id, 
            procedural_score=procedural_score, timestamp=timestamp)
        pr.save()

        return CreateProcedural(
            patient_id = pr.patient_id,
            procedural_score = pr.procedural_score,
            timestamp = pr.timestamp
        )

class CreateEpisodic(graphene.Mutation):
    patient_id = graphene.Int()
    episodic_score = graphene.Int()
    timestamp = graphene.types.datetime.DateTime()
    question = graphene.String()
    answer_choices = graphene.String()
    patient_answer = graphene.String()
    correct_answer = graphene.String()

    class Arguments:
        patient_id = graphene.Int()
        episodic_score = graphene.Int()
        timestamp = graphene.types.datetime.DateTime()
        question = graphene.String()
        answer_choices = graphene.String()
        patient_answer = graphene.String()
        correct_answer = graphene.String()

    def mutate(self, info, patient_id, episodic_score, timestamp, question,
        answer_choices, patient_answer, correct_answer):
        user = info.context.user or None
        ep = Episodic(patient_id=patient_id, episodic_score=episodic_score,
            timestamp=timestamp, question=question, 
            answer_choices=answer_choices, patient_answer=patient_answer,
            correct_answer=correct_answer)
        ep.save()

        return CreateEpisodic(
            patient_id = ep.patient_id,
            episodic_score = ep.episodic_score,
            timestamp = ep.timestamp,
            question = ep.question,
            answer_choices = ep.answer_choices,
            patient_answer = ep.patient_answer,
            correct_answer = ep.correct_answer
        )

class Query(graphene.ObjectType):
    logical = graphene.List(LogicalType, id = graphene.Int())
    semantic = graphene.List(SemanticType, id = graphene.Int())
    procedural = graphene.List(ProceduralType, id = graphene.Int())
    episodic = graphene.List(EpisodicType, id = graphene.Int())
	
    def resolve_logical(self, info, id=-1, **kwargs):
        if id>=0:
            filter = (
                Q(patient_id=id)
            )
            return Logical.objects.filter(filter)
        return Logical.objects.all()

    def resolve_semantic(self, info, id=-1, **kwargs):
        if id >= 0:
            filter = (
                Q(patient_id=id)
            )
            return Semantic.objects.filter(filter)
        return Semantic.objects.all()
    
    def resolve_procedural(self, info, id=-1, **kwargs):
        if id >= 0:
            filter = (
                Q(patient_id=id)
            )
            return Procedural.objects.filter(filter)
        return Procedural.objects.all()

    def resolve_episodic(self, info, id=-1, **kwargs):
        if id >= 0:
            filter = (
                Q(patient_id=id)
            )
            return Episodic.objects.filter(filter)
        return Episodic.objects.all()

class Mutation(graphene.ObjectType):
    create_logical = CreateLogical.Field()
    create_semantic = CreateSemantic.Field()
    create_procedural = CreateProcedural.Field()
    create_episodic = CreateEpisodic.Field()
