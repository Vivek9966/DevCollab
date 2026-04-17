from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsWorkforce
from rest_framework import status
from django.conf import settings
from rest_framework.response import Response
from .models import Projects
from .serializers import ProjectSerializer
from  workspaces.models import Membership
class ProjectViewset(ModelViewSet):
    permission_classes = [IsAuthenticated,IsWorkforce]
    serializer_class = ProjectSerializer
    def get_queryset(self):
        return Projects.objects.filter(
            workspace__members = self.request.user
        )
    def perform_create(self, serializer):
        workspace_id = self.kwargs.get('workspace_pk')
        user =self.request.user
        membership  = Membership.objects.filter(
            user=user,workspace_id = workspace_id 
        ).first()

        if not membership or membership.role =='viewer':
            raise PermissionError('Viewers can\'t create Projects')

        serializer.save(
            workspace_id=workspace_id,
            created_by =self.request.user
        )
        
