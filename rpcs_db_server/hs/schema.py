import graphene
from graphene_django import DjangoObjectType

from .models import Events
from django.db.models import Q

class EventsType(DjangoObjectType):
	class Meta:
		model = Events

class CreateEvents(graphene.Mutation):
    event_type = graphene.String()
    sensor_id = graphene.ID()
    sensor_type = graphene.String()
    timestamp = graphene.types.datetime.DateTime()
    data = graphene.String()
    event_id = graphene.Int()

    class Arguments:
        event_type = graphene.String()
        sensor_id = graphene.ID()
        sensor_type = graphene.String()
        timestamp = graphene.types.datetime.DateTime()
        data = graphene.String()
        event_id = graphene.Int()

    def mutate(self, info, event_type, sensor_id, sensor_type, timestamp, data, event_id):
        user = info.context.user or None

        events = Events(event_type=event_type, sensor_id=sensor_id, 
            sensor_type=sensor_type, timestamp=timestamp, data=data, event_id=event_id)
        events.save()

        return CreateEvents(
            event_type = events.event_type,
            sensor_id = events.sensor_id,
            sensor_type = events.sensor_type,
            timestamp = events.timestamp,
            data = events.data,
            event_id = events.event_id)

class Query(graphene.ObjectType):
	events = graphene.List(EventsType, id = graphene.Int())
	
	def resolve_results(self, info, id=-1, **kwargs):
		if id>=0:
			filter = (
				Q(event_id=id)
			)
			return Events.objects.filter(filter)

		return Events.objects.all()

class Mutation(graphene.ObjectType):
	create_events = CreateEvents.Field()
