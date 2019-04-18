"""rpcs_db_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rpcs_db_server import views
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from django.contrib.auth.mixins import LoginRequiredMixin
from rpcs_db_server import schema

class PrivateGraphQLView(LoginRequiredMixin, GraphQLView):
    pass

urlpatterns = [
    path('admin/', admin.site.urls),
    path('wt/', include("wt.urls")),
    path('stm/', include("stm.urls")),
    path('hs/', include("hs.urls")),
    path('ca/', include("ca.urls")),
    path('ga/', include("ga.urls")),
    path('watch/', include("watch.urls")),
    path('ct/', include("ct.urls")),
    path('int/', include("int.urls")),
    path('health', views.health),
    path('auth', views.auth),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
