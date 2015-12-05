from rest_framework import viewsets, serializers
from .models import TokenType, Token, AccessType, Grant

class TokenTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TokenType

class TokenTypeViewSet(viewsets.ModelViewSet):
    serializer_class = TokenTypeSerializer
    queryset = TokenType.objects.all()

class TokenSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Token

class TokenViewSet(viewsets.ModelViewSet):
    serializer_class = TokenSerializer
    queryset = Token.objects.all()

class AccessTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AccessType

class AccessTypeViewSet(viewsets.ModelViewSet):
    serializer_class = AccessTypeSerializer
    queryset = AccessType.objects.all()

class GrantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Grant

class GrantViewSet(viewsets.ModelViewSet):
    serializer_class = GrantSerializer
    queryset = Grant.objects.all()
