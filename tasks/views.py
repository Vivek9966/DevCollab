from django.shortcuts import render
from rest_framework import settings
from .models import Task
from .serializers import TaskSerializer
from rest_framework import  status
from core.permissions import IsWorkforce
from rest_framework.permissions import  IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from  workspaces.models import Membership
class TaskViewset(ModelViewSet):
    permission_classes=[IsWorkforce,IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(
            project__workspace__members=self.request.user
        )
    def perform_create(self, serializer):

        project_id = self.kwargs.get('project_pk')
        user = self.request.user

        membership = Membership.objects.filter(
            user=user, workspace__project__id = project_id
        ).first()

        if not membership or membership.role == 'Viewer':
            raise PermissionError('Viewers can\'t create tasks')

        serializer.save(
            project_id=project_id,
            created_by = self.request.user
        )
        
    @action(detail=True,methods=['post'])
    def change_status(self,request,pk = None):
        task=self.get_object()
        
        user = self.request.user

        membership = Membership.objects.filter(
            user=user, workspace__project__id = project_id
        ).first()

        if not membership or membership.role == 'Viewer':
            raise PermissionError('Viewers can\'t change task status')
        
        new_status = request.data.get('status')
        if new_status not in dict(Task.STATUS_CHOICES):
            return Response({'error': 'Invalid status'},status=400)
        task.status = new_status
        task.save()
        return Response({

            'status': 'Status updated'
        })