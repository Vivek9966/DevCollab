from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Workspace , Membership
from .serializer import WorkspaceSerializer ,AddMemberSerializer
from core.permissions import IsWorkforce

class WorkspaceViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated,IsWorkforce]
    serializer_class =WorkspaceSerializer
    
    def get_queryset(self):
        
        return Workspace.objects.filter(
            members = self.request.user
        )
    
    @action(detail=True,methods=['post'],url_path='add-member')
    def add_member(self,request,pk=None):
        workspace = self.get_object()

        membership = Membership.objects.filter(
            user = request.user
            , workspace=workspace
        ).first()

        if not membership or membership.role != 'admin':
            return Response(
                {
                    'error':'Only admins can add memebers'
                },status=status.HTTP_403_FORBIDDEN
            ) 
        serializer = AddMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_user = serializer.validated_data['user']
        validated_role =serializer.validated_data['role']
        if Membership.objects.filter(user =validated_user, workspace=workspace).exists():
            return Response(
                {
                    'error':'user already a memeber'
                },status=status.HTTP_400_BAD_REQUEST
            )
        Membership.objects.create(
            user=validated_user,
            workspace=workspace,
            role=validated_role
        )
        return Response({
            'message':f'User added succesfully '
        })