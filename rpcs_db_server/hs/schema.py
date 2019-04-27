import graphene
from graphene_django import DjangoObjectType

from .models import Events, Sensors
from django.db.models import Q

class EventsType(DjangoObjectType):
    class Meta:
        model = Events

class SensorsType(DjangoObjectType):
    class Meta:
        model = Sensors

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

    def mutate(self, info, event_type, sensor_id, sensor_type, timestamp, data, 
        event_id):
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

class CreateSensors(graphene.Mutation):
    location = graphene.String()
    sensor_type = graphene.String()
    patient_id = graphene.Int()
    sensor_id = graphene.ID()

    class Arguments:
        location = graphene.String()
        sensor_type = graphene.String()
        patient_id = graphene.Int()
        sensor_id = graphene.ID()

    def mutate(self, info, location, sensor_type, patient_id, sensor_id):
        user = info.context.user or None

        sensors = Sensors(location=location, sensor_type=sensor_type,
            patient_id=patient_id, sensor_id=sensor_id)
        sensors.save()

        return CreateSensors(
            location = sensors.location,
            sensor_type = sensors.sensor_type,
            patient_id = sensors.patient_id,
            sensor_id = sensors.sensor_id)

class Query(graphene.ObjectType):
    events = graphene.List(EventsType, id = graphene.Int(),
        filter_date = graphene.Boolean(),
        start_date = graphene.types.datetime.DateTime(),
        end_date = graphene.types.datetime.DateTime())

    sensors = graphene.List(SensorsType, id = graphene.Int())
    
    def resolve_events(self, info, id=-1, filter_date=False, start_date=None, 
        end_date=None, **kwargs):
        if id >= 0:
            if filter_date:
                filter = (
                    Q(event_id=id) & Q(timestamp__range=(start_date,end_date))
                )
            else:
                filter = (
                    Q(event_id=id)
                )
            return Events.objects.filter(filter)

        return Events.objects.all()

    def resolve_sensors(self, info, id=-1, **kwargs):
        if id >= 0:
            filter = (
                Q(patient_id=id)
            )
            return Sensors.objects.filter(filter)
        return Sensors.objects.all()

class Mutation(graphene.ObjectType):
    create_events = CreateEvents.Field()
    create_sensors = CreateSensors.Field()
