from django.contrib.auth.models import User
from wt.models import Patient as wtPatient, Caregiver, Safezone
from stm.models import Results
from hs.models import Event as hsEvent
from ca.models import Wandering, Phys_measure, Phy_params
from ga.models import Logical, Semantic, Procedual, Episodic
from watch.models import Patient as watchPatient, Event as watchEvent
from ct.models import Profile, Incident, Trend

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

def addPerms(user, perms):
    for i in range(4):
        user.user_permissions.add(perms[i])
        user.save()

wtUser = User(username="wt")
wtPatientCt = ContentType.objects.get_for_model(wtPatient)
wtPatientPerms = Permission.objects.filter(content_type=wtPatientCt)
wtUser.save()
addPerms(wtUser, wtPatientPerms)

caregiverCt = ContentType.objects.get_for_model(Caregiver)
wtCaregiverPerms = Permission.objects.filter(content_type=caregiverCt)
for i in range(4):
    wtUser.user_permissions.add(wtCaregiverPerms[i])
    wtUser.save()
safezoneCt = ContentType.objects.get_for_model(Safezone)
wtSafezonePerms = Permission.objects.filter(content_type=safezonePerms)
for i in range(4):
    wtUser.user_permissions.add(wtSafezonePerms[i])
    wtUser.save()
wtUser.save()


stmUser = User(username="stm")
stmResultsCt = ContentType.objects.get_for_model(Results)
stmResultsPerms = Permission.objects.filter(content_type=stmResultsPerms)
stmUser.save()
for i in 

    # hsUser = User(username="hs")
    # hsUser.save()

    # caUser = User(username="ca")
    # caUser.save()

    # gaUser = User(username="ga")
    # gaUser.save()

    # watchUser = User(username="watch")
    # watchUser.save()

    # ctUser = User(username="ct")
    # ctUser.save()


# if __name__=="__main__":
#     init_users()