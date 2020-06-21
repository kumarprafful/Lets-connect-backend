from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import Contacts, Invites
from users.serializers import ContactSerializer, UserSerializer, InvitesSerializer

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def fetch_contact_list(request):
    try:
        user = request.user
        contacts = Contacts.objects.get(user=request.user)
        serializer = ContactSerializer(contacts)
        return Response({'status':'success', 'data': serializer.data}, status=200)
    except Exception as e:
        return Response({'status':'error', 'message':str(e)}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def update_customer_info(request):
    try:
        user = request.user
        data = JSONParser().parse(request)
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({'status':'error', 'message': serializer.errors}, status=400)
        return Response({'status':'success'}, status=200)
    except Exception as e:
        return Response({'status':'error', 'message':str(e)}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def invite_friends(request):
    try:
        data = JSONParser().parse(request)
        emails = data.get('emails')
        valid_invites = 0
        message = ''
        invalid_emails = []
        for email in emails:
            try:
                validate_email(email)
                if email == request.user.email:
                    message = 'Trying to talk to yourself. I don\'t think we are there yet!'
                    continue
                try:
                    user = User.objects.get(email=email)
                    Invites.objects.get_or_create(invited_by=request.user, invited_user=user)
                    valid_invites += 1
                    print('send mail and notification to {email}')
                    # send mail and notification
                except:
                    Invites.objects.get_or_create(invited_by=request.user, invited_email=email)
                    valid_invites += 1
                    print('send mail to {email}')
                    # send mail
            except ValidationError:
                invalid_emails.append(email)
        return Response({
                    'invalid_emails': invalid_emails,
                    'valid_invites': valid_invites,
                    'message': message
                    }, status=200)
    except Exception as e:
        return Response({'status':'error', 'message':str(e)}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_invites(request):
    try:
        invites = Invites.objects.filter(invited_user=request.user, active=True).order_by('-created_at')
        serializer = InvitesSerializer(invites, many=True)
        return Response({'status': 'success', 'data':serializer.data}, status=200)
    except Exception as e:
        return Response({'status':'error', 'message':str(e)}, status=400)
        

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def invite_action(request):
    try:
        data = JSONParser().parse(request)
        invite = Invites.objects.get(id=data.get('invite_id'), invited_user=request.user)
        action = data.get('action')
        invite.active = False
        if action:
            invite.accepted = True
            invited_by = invite.invited_by
            contact_invited_by = Contacts.objects.get(user=invited_by)
            contact_invited_by.contacts.add(request.user)
            contact = Contacts.objects.get(user=request.user)
            contact.contacts.add(invited_by)
        else:
            # lets think about blocking the user
            invite.decline = False
        invite.save()
        return Response({'status': 'success'}, status=200)
    except Exception as e:
        return Response({'status':'error', 'message':str(e)}, status=400)