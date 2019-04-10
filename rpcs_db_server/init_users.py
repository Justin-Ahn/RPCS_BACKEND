from django.contrib.auth.models import User

def init_users():
    wtUser = User(username="wt")
    wtUser.save()

    stmUser = User(username="stm")
    stmUser.save()

    hsUser = User(username="hs")
    hsUser.save()

    caUser = User(username="ca")
    caUser.save()

    gaUser = User(username="ga")
    gaUser.save()

    watchUser = User(username="watch")
    watchUser.save()

    ctUser = User(username="ct")
    ctUser.save()


if __name__=="__main__":
    init_users()