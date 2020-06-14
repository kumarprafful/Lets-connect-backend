from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@login_required
def index(request):
    return render(request, 'chat/index.html')

@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def add_contact(request):
    try:
        data = JSONParser.parse(request)
        friend = User.objects.get(email=data.get('friend'))
        contacts, _ = Contact.objects.get_or_create(user=request.user)
        contacts.contacts.add(friend)
        contacts.save()
        Room.objects.get_or_create(first_user=request.user, second_user=friend)
        return Response({'status':'success', 'data': 'Added'})
    except Exception as e:
        return Response({'status':'error', 'message':str(e)})

