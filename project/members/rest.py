from rest_framework import viewsets, serializers
import rest_framework_filters as filters
from .models import MemberType, Member, MembershipApplicationTag, MembershipApplication


class MemberTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MemberType

class MemberTypeFilter(filters.FilterSet):
    class Meta:
        model = MemberType
        fields = {
            'label': filters.ALL_LOOKUPS,
        }

class MemberTypeViewSet(viewsets.ModelViewSet):
    serializer_class = MemberTypeSerializer
    queryset = MemberType.objects.all()
    filter_class = MemberTypeFilter



class MembershipApplicationTagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MembershipApplicationTag

class MembershipApplicationTagFilter(filters.FilterSet):
    class Meta:
        model = MembershipApplicationTag
        fields = {
            'label': filters.ALL_LOOKUPS,
        }

class MembershipApplicationTagViewSet(viewsets.ModelViewSet):
    serializer_class = MembershipApplicationTagSerializer
    queryset = MembershipApplicationTag.objects.all()
    filter_class = MembershipApplicationTagFilter



class MemberSerializer(serializers.HyperlinkedModelSerializer):
    credit = serializers.CharField(read_only=True)
    class Meta:
        model = Member
        fields = '__all__'

class MemberFilter(filters.FilterSet):
    # TODO: figure out how to implement the credit < 0 filter here
    class Meta:
        model = Member
        fields = {
            'nick': filters.ALL_LOOKUPS,
            'email': filters.ALL_LOOKUPS,
            'lname': filters.ALL_LOOKUPS,
            'fname': filters.ALL_LOOKUPS,
            'accepted': filters.ALL_LOOKUPS,
            'mtypes': filters.ALL_LOOKUPS,
            'anonymized_id': filters.ALL_LOOKUPS,
            'member_id': filters.ALL_LOOKUPS,
        }

class MemberViewSet(viewsets.ModelViewSet):
    serializer_class = MemberSerializer
    queryset = Member.objects.all()
    filter_class = MemberFilter



class MembershipApplicationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MembershipApplication

class MembershipApplicationFilter(filters.FilterSet):
    class Meta:
        model = MembershipApplication
        fields = {
            'nick': filters.ALL_LOOKUPS,
            'email': filters.ALL_LOOKUPS,
            'lname': filters.ALL_LOOKUPS,
            'fname': filters.ALL_LOOKUPS,
            'received': filters.ALL_LOOKUPS,
            'tags': filters.ALL_LOOKUPS,
        }

class MembershipApplicationSerializerViewSet(viewsets.ModelViewSet):
    serializer_class = MembershipApplicationSerializer
    queryset = MembershipApplication.objects.all()
    filter_class = MembershipApplicationFilter
