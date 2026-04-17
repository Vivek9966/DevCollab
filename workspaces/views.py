from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Workspace , Membership
from .serializer import WorkspaceSerializer ,AddMemberSerializer
from core.permissions import IsWorkforce,IsWorkforceAdmin
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

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
    @action(detail=True, methods=['delete'], url_path='rem-member',
            permission_classes=[IsAuthenticated, IsWorkforceAdmin])
    def remove_member(self, request, pk=None):
        workspace = self.get_object()

        github_id = request.data.get('github_id')

        if not github_id:
            return Response({'error': 'github_id is required'}, status=400)

        user_to_remove = User.objects.filter(github_id=github_id).first()

        if not user_to_remove:
            return Response({'error': 'User not found'}, status=400)

        membership = Membership.objects.filter(
            user=user_to_remove,
            workspace=workspace
        ).first()

        if not membership:
            return Response({'error': 'User not in this workspace'}, status=400)

        membership.delete()

        return Response({
            'message': f'{user_to_remove} removed from workspace {workspace.name}'
        })