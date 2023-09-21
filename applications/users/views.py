from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

from firebase_admin import auth

from django.shortcuts import render
from django.views.generic import TemplateView

from .serializers import LoginSocialSerializer
from .models import User

#esta solo es un ejemplo de logue con google
class Login(TemplateView):
    template_name = "users/login.html"

#vista que recibe un token
class GoogleLogin(APIView):
    serializer_class = LoginSocialSerializer

    #desencriptando token
    @csrf_exempt
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        #verificando informacion
        #si la informacion enviada no cumple con los campos especificados en el serializador
        #manda un error
        serializer.is_valid(raise_exception=True)

        #recuperando campo que viene del serializador ya verificado
        token = serializer.data.get('token')

        #desencriptando token desde firebase
        # se instala pip install firebase-admin

        #auth provide del paquete firebase_admin 
        decoded_toke = auth.verify_id_token(token)
        #extrayendo datos del token desencriptado
        email = decoded_toke['email']
        name = decoded_toke['name']
        avatar = decoded_toke['picture']
        verified = decoded_toke['email_verified']


        #creado usuario en bd local una vez verificado el acceso en google
        usuario, created = User.objects.get_or_create(
            email = email,
            defaults = {
                'full_name': name,
                'email': email,
                'is_active': True
            }
        )

        #crear token interno 
        if created:
            token = Token.objects.create(user=usuario)
        else:
            token = Token.objects.get(user=usuario)
 

        userGet = {
            'id': usuario.id,
            'email': usuario.email,
            'name': usuario.full_name,
        }

        return Response(
            {                
                'user': userGet,
                'token': token.key,
            }
        )


