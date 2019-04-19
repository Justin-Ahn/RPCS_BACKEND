import graphene
from graphene_django import DjangoObjectType

from .models import Wandering, Phys_measure, Phys_params, Phys_incidents, Sleep_trend
from .models import Incident_summary
from django.db.models import Q

class WanderingType(DjangoObjectType):
	class Meta:
		model = Wandering

class PhysMeasureType(DjangoObjectType):
    class Meta:
        model = Phys_measure

class PhysParamsType(DjangoObjectType):
    class Meta:
        model = Phys_params

class PhysIncidentsType(DjangoObjectType):
    class Meta:
        model = Phys_incidents

class SleepTrendType(DjangoObjectType):
    class Meta:
        model = Sleep_trend

class IncidentSummaryType(DjangoObjectType):
    class Meta:
        model = Incident_summary

class CreateWandering(graphene.Mutation):
    patient_id = graphene.Int()
    caregiver_id = graphene.Int()
    isWandering = graphene.Boolean()
    alerted = graphene.Boolean()

    class Arguments:
        patient_id = graphene.Int()
        caregiver_id = graphene.Int()
        isWandering = graphene.Boolean()
        alerted = graphene.Boolean()

    def mutate(self, info, patient_id, caregiver_id, isWandering, alerted):
        user = info.context.user or None

        wd = Wandering(patient_id=patient_id, caregiver_id=caregiver_id,
            isWandering=isWandering, alerted=alerted)
        wd.save()

        return CreateWandering(
            patient_id = wd.patient_id, 
            caregiver_id = wd.caregiver_id,
            isWandering = wd.isWandering, 
            alerted = wd.alerted
        )

class CreatePhysMeasure(graphene.Mutation):
    patient_id = graphene.Int()
    age = graphene.Int()
    gender = graphene.String()
    stage = graphene.String()
    weight = graphene.Float()
    body_fat = graphene.Float()
    skinny_fat = graphene.Float()
    bp_low = graphene.Int()
    bp_high = graphene.Int()
    pr_low = graphene.Int()
    pr_high = graphene.Int()
    rr_low = graphene.Int()
    rr_high = graphene.Int()

    class Arguments:
        patient_id = graphene.Int()
        age = graphene.Int()
        gender = graphene.String()
        stage = graphene.String()
        weight = graphene.Float()
        body_fat = graphene.Float()
        skinny_fat = graphene.Float()
        bp_low = graphene.Int()
        bp_high = graphene.Int()
        pr_low = graphene.Int()
        pr_high = graphene.Int()
        rr_low = graphene.Int()
        rr_high = graphene.Int()

    def mutate(self, info, patient_id, age, gender, stage, weight, body_fat,
        skinny_fat, bp_low, bp_high, pr_low, pr_high, rr_low, rr_high):
        user = info.context.user or None

        pm = Phys_measure(patient_id=patient_id, age=age, gender=gender,
            stage=stage, weight=weight, body_fat=body_fat, 
            skinny_fat=skinny_fat, bp_low=bp_low, bp_high=bp_high,
            pr_low=pr_low, pr_high=pr_high, rr_low=rr_low, rr_high=rr_high)
        pm.save()

        return CreatePhysMeasure(
            patient_id = pm.patient_id, 
            age = pm.age, 
            gender = pm.gender,
            stage = pm.stage, 
            weight = pm.weight, 
            body_fat = pm.body_fat, 
            skinny_fat = pm.skinny_fat, 
            bp_low = pm.bp_low, 
            bp_high = pm.bp_high,
            pr_low = pm.pr_low, 
            pr_high = pm.pr_high, 
            rr_low = pm.rr_low, 
            rr_high = pm.rr_high
        )

class CreatePhysParams(graphene.Mutation):
    patient_id = graphene.Int()
    coef_bp = graphene.Float()
    coef_pr = graphene.Float()
    coef_rr = graphene.Float()
    bias_logit = graphene.Float()
    ar = graphene.Float()

    class Arguments:
        patient_id = graphene.Int()
        coef_bp = graphene.Float()
        coef_pr = graphene.Float()
        coef_rr = graphene.Float()
        bias_logit = graphene.Float()
        ar = graphene.Float()

    def mutate(self, info, patient_id, coef_bp, coef_pr, coef_rr, 
        bias_logit, ar):
        user = info.context.user or None

        pp = Phys_params(patient_id=patient_id, coef_bp=coef_bp, 
            coef_pr=coef_pr, coef_rr=coef_rr, bias_logit=bias_logit,
            ar=ar)
        pp.save()

        return CreatePhysParams(
            patient_id = pp.patient_id,
            coef_bp = pp.coef_bp,
            coef_pr = pp.coef_pr,
            coef_rr = pp.coef_rr,
            bias_logit = pp.bias_logit,
            ar = pp.ar
        )

class CreatePhysIncidents(graphene.Mutation):
    patient_id = graphene.Int()
    incident_id = graphene.Int()
    timestamp = graphene.types.datetime.DateTime()
    pulse_rate = graphene.Float()
    respiratory_rate = graphene.Float()
    blood_pressure = graphene.Float()
    incident_type = graphene.String()
    recording = graphene.String()

    class Arguments:
        patient_id = graphene.Int()
        incident_id = graphene.Int()
        timestamp = graphene.types.datetime.DateTime()
        pulse_rate = graphene.Float()
        respiratory_rate = graphene.Float()
        blood_pressure = graphene.Float()
        incident_type = graphene.String()
        recording = graphene.String()

    def mutate(self, info, pt_id, inc_id, ts, prate, rrate, bp, inc_type, rec):
        user = info.context.user or None

        pi = Phys_incidents(patient_id=pt_id, incident_id=inc_id,
            timestamp=ts, pulse_rate=pr, respiratory_rate=rr, 
            blood_pressure=bp, incident_type=inc_type, recording=rec)
        pi.save()

        return CreatePhysicalIncidents(
            patient_id = pi.patient_id, 
            incident_id = pi.incident_id,
            timestamp = pi.timestamp, 
            pulse_rate = pi.pulse_rate, 
            respiratory_rate = pi.respiratory_rate, 
            blood_pressure = pi.blood_pressure, 
            incident_type = pi.incident_type, 
            recording = pi.recording
        )

class CreateSleepTrend(graphene.Mutation):
    patient_id = graphene.Int()
    date = graphene.types.datetime.Date()
    hours_slept = graphene.Float()
    hours_deep_sleep = graphene.Float()
    hours_light_sleep = graphene.Float()
    hours_in_bed = graphene.Float()
    num_wake_up = graphene.Int()
    num_get_out_of_bed = graphene.Int()
    num_go_to_bathroom = graphene.Int()

    class Arguments:
        patient_id = graphene.Int()
        date = graphene.types.datetime.Date()
        hours_slept = graphene.Float()
        hours_deep_sleep = graphene.Float()
        hours_light_sleep = graphene.Float()
        hours_in_bed = graphene.Float()
        num_wake_up = graphene.Int()
        num_get_out_of_bed = graphene.Int()
        num_go_to_bathroom = graphene.Int()

    def mutate(self, info, patient_id, date, hours_slept, hours_deep_sleep,
        hours_light_sleep, hours_in_bed, num_wake_up, num_get_out_of_bed,
        num_go_to_bathroom):
        user = info.context.user or None
        
        st = Sleep_trend(patient_id=patient_id, date=date, 
            hours_slept=hours_slept, hours_deep_sleep=hours_deep_sleep,
            hours_light_sleep=hours_light_sleep, hours_in_bed=hours_in_bed,
            num_wake_up=num_wake_up, num_get_out_of_bed=num_get_out_of_bed,
            num_go_to_bathroom=num_go_to_bathroom)
        st.save()

        return CreateSleepTrend(
            patient_id = st.patient_id, 
            date = st.date, 
            hours_slept = st.hours_slept, 
            hours_deep_sleep = st.hours_deep_sleep,
            hours_light_sleep = st.hours_light_sleep, 
            hours_in_bed = st.hours_in_bed,
            num_wake_up = st.num_wake_up, 
            num_get_out_of_bed = st.num_get_out_of_bed,
            num_go_to_bathroom = st.num_go_to_bathroom
        )

class CreateIncidentSummary(graphene.Mutation):
    patient_id = graphene.Int()
    date = graphene.types.datetime.Date()
    num_hallucinations = graphene.Int()
    num_ltm_lapse = graphene.Int()
    num_stm_lapse = graphene.Int()
    num_injury = graphene.Int()
    num_wandering = graphene.Int()

    class Arguments:
        patient_id = graphene.Int()
        date = graphene.types.datetime.Date()
        num_hallucinations = graphene.Int()
        num_ltm_lapse = graphene.Int()
        num_stm_lapse = graphene.Int()
        num_injury = graphene.Int()
        num_wandering = graphene.Int()

    def mutate(self, info, patient_id, date, num_hallucinations, num_ltm_lapse,
        num_stm_lapse, num_injury, num_wandering):
        user = info.context.user or None

        isum = Incident_summary(patient_id=patient_id, 
            num_hallucinations=num_hallucinations,
            num_ltm_lapse=num_ltm_lapse, num_stm_lapse=num_stm_lapse,
            num_injury=num_injury, num_wandering=num_wandering)
        isum.save()

        return CreateIncidentSumary(
            patient_id = isum.patient_id, 
            num_hallucinations = isum.num_hallucinations,
            num_ltm_lapse = isum.num_ltm_lapse, 
            num_stm_lapse = isum.num_stm_lapse,
            num_injury = isum.num_injury, 
            num_wandering = isum.num_wandering
        )

class Query(graphene.ObjectType):
    wandering = graphene.List(WanderingType, id=graphene.Int())
    phys_measure = graphene.List(PhysMeasureType, id = graphene.Int())
    phys_params = graphene.List(PhysParamsType, id = graphene.Int())
    phys_incidents = graphene.List(PhysIncidentsType, id = graphene.Int())
    sleep_trend = graphene.List(SleepTrendType, id = graphene.Int())
    incident_summary = graphene.List(IncidentSummaryType, id = graphene.Int())

    def resolve_wandering(self, info, id=-1, **kwargs):
        if id >= 0:
            filter = (
                Q(patient_id=id)
            )
            return Wandering.objects.filter(filter)
        return Wandering.objects.all()
	
    def resolve_phys_measure(self, info, id=-1, **kwargs):
        if id >= 0:
            filter = (
                Q(patient_id=id)
            )
            return Phys_measure.objects.filter(filter)
        return Phys_measure.objects.all()
	
    def resolve_phys_params(self, info, id=-1, **kwargs):
        if id >= 0:
            filter = (
                Q(patient_id=id)
            )
            return Phys_params.objects.filter(filter)
        return Phys_params.objects.all()
    
    def resolve_phys_incidents(self, info, id=-1, **kwargs):
        if id >= 0:
            filter = (
                Q(patient_id=id)
            )
            return Phys_incidents.objects.filter(filter)
        return Phys_incidents.objects.all()

    def resolve_sleep_trend(self, info, id=-1, **kwargs):
        if id >= 0:
            filter = (
                Q(patient_id=id)
            )
            return Sleep_trend.objects.filter(filter)
        return Sleep_trend.objects.all()

    def resolve_incident_summary(self, info, id=-1, **kwargs):
        if id >= 0:
            filter = (
                Q(patient_id=id)
            )
            return Incident_summary.objects.filter(filter)
        return Incident_summaryobjects.all()

class Mutation(graphene.ObjectType):
    create_wandering = CreateWandering.Field()
    create_phys_measure = CreatePhysMeasure.Field()
    create_phys_params = CreatePhysParams.Field()
    create_phys_incidents = CreatePhysIncidents.Field()
    create_sleep_trend = CreateSleepTrend.Field()
    create_incident_summary = CreateIncidentSummary.Field()
