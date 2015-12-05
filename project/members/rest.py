from rest_framework import viewsets, serializers
from .models import MemberType, Member, MembershipApplicationTag, MembershipApplication

class MemberTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MemberType

class MemberTypeViewSet(viewsets.ModelViewSet):
    serializer_class = MemberTypeSerializer
    queryset = MemberType.objects.all()

class MembershipApplicationTagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MembershipApplicationTag

class MembershipApplicationTagViewSet(viewsets.ModelViewSet):
    serializer_class = MembershipApplicationTagSerializer
    queryset = MembershipApplicationTag.objects.all()

class MemberSerializer(serializers.HyperlinkedModelSerializer):
    credit = serializers.CharField(read_only=True)
    class Meta:
        model = Member
        fields = '__all__'

class MemberViewSet(viewsets.ModelViewSet):
    serializer_class = MemberSerializer
    queryset = Member.objects.all()

class MembershipApplicationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MembershipApplication

class MembershipApplicationSerializerViewSet(viewsets.ModelViewSet):
    serializer_class = MembershipApplicationSerializer
    queryset = MembershipApplication.objects.all()
