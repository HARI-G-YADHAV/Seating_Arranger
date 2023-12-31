# authentication/views.py

from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login


User = get_user_model()

@csrf_exempt
def sign_up(request):
    if request.method == 'POST':
        try:
            # Retrieve the JSON data from the request body
            data = json.loads(request.body)
        except json.JSONDecodeError as e:
            # Return an error response if the JSON data is invalid
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        email = data.get('email')
        password1 = data.get('password1')
        username = data.get('username')
        password2 = data.get('password2')
        if password1 != password2:
            return JsonResponse({'success': False, 'message': 'Password incorrect'}, status=400)
        if not email or not password1 or not username:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        try:
            user = User.objects.create_user(email=email, password=password1, username=username)
            return JsonResponse({'message': 'User created successfully', 'user_id': user.id}, status=201)
        except IntegrityError as e:
            return JsonResponse({'success': False, 'message': 'Username already exists'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def sign_in(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        if not username or not password:
            return JsonResponse({'message': 'Missing email or password'}, status=400)

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            is_admin = user.is_superuser
            is_staff = user.is_staff
            if user.is_staff:
                message = ''
            else:
                message = 'user is not verified.'
            return JsonResponse({'token': token.key, 'user_id': user.id, 'message': message,'is_admin': is_admin,'is_staff': is_staff}, status=200)
        else:
            return JsonResponse({'message': 'Invalid email or password'}, status=401)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
