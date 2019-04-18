from django.contrib.auth.models import User

# Technically this file shouldn't be a part of the git repo...
groups = ["ca", "ct", "ga", "hs", "stm", "watch", "wt", "int", "cg_doc", "readonly"]
for user in groups:
    new_user = User.objects.create_user(user + "_user", password='rpcs_' + user + '2019')
    new_user.save()


"""from wt.models import Patient as wtPatient, Caregiver, Safezone
from stm.models import Results
from ga.models import Logical, Semantic, Procedual, Episodic
from ct.models import Profile, Incident, Trend"""

"""def addPerms(user, model):
    ct = ContentType.objects.get_for_model(model)
    perms = Permission.objects.filter(content_type=ct)
    for i in range(4):
        user.user_permissions.add(perms[i])
        user.save()

wtUser = User(username="wt")
wtUser.save()
addPerms(wtUser, wtPatient)

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
addPerms(stmUser, stmResultsPerms)

hsUser = User(username="hs")
hsEventCt = ContentType.objects.get_for_model(hsEvent)
hsEventPerms = Permission.objects.filter(content_type=hsEventCt)
hsUser.save()

caUser = User(username="ca")
# from ca.models import Wandering, Phys_measure, Phy_params
caWanderingCt = ContentType.objects.get_for_model(Wandering)
caWanderingPerms = Permission.objects.filter(content_type=caWanderingCt)
caUser.save()"""


    # gaUser = User(username="ga")
    # gaUser.save()

    # watchUser = User(username="watch")
    # watchUser.save()

    # ctUser = User(username="ct")
    # ctUser.save()


# if __name__=="__main__":
#     init_users()
