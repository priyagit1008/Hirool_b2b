# django imports
from rest_framework import serializers

# app level imports
from .models import Client, Job


class ClientCreateRequestSerializer(serializers.Serializer):
    """
    ClientCreateRequestSerializer
    """
    name = serializers.CharField(required=True)
    web_link = serializers.CharField(required=False)
    headquarter = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    category = serializers.CharField(required=True)
    business_type = serializers.CharField(required=True)
    # status = serializers.CharField(required=False)
    profile_desc = serializers.CharField(required=False)
    aggrement_doc = serializers.CharField(required=True)
    extra = serializers.JSONField(required=False)

    # password = serializers.CharField(required=True, min_length=5)
    class Meta:
        model = Client
        fields = (
            'name', 'web_link', 'headquarter', 'address', 'category',
            'business_type', 'status', 'profile_desc', 'aggrement_doc',
            'extra'
        )

    def create(self, validated_data):
        client = Client.objects.create(**validated_data)

        # user.set_password(validated_data['password'])
        client.save()

        return client


class ClientListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        # Tuple of serialized model fields (see link [2])
        # fields = ( "id", "username", "password", )
        fields = (
            'id', 'name', 'web_link', 'headquarter', 'address', 'category',
            'business_type', 'status', 'profile_desc', 'aggrement_doc',
            'extra'
        )
        # write_only_fields = ('password',)
        # read_only_fields = ('id',)


class JobCreateRequestSerializer(serializers.Serializer):
    """
    ClientCreateRequestSerializer
    """
    client_id = serializers.CharField(required=True)
    job_title = serializers.CharField(required=True)
    jd_url = serializers.CharField(required=False)
    tech_skills = serializers.JSONField(required=False)
    location = serializers.CharField(required=True)
    job_type = serializers.CharField(required=True)
    min_exp = serializers.IntegerField(required=True)
    max_exp = serializers.IntegerField(required=True)
    min_relevant_exp = serializers.IntegerField(required=True)
    max_notice = serializers.IntegerField(required=True)
    # status = serializers.CharField(required=False)
    min_ctc = serializers.FloatField(required=False)
    max_ctc = serializers.FloatField(required=False)

    expiring_on = serializers.DateTimeField(required=False)
    jd_extra = serializers.JSONField(required=False)

    # password = serializers.CharField(required=True, min_length=5)
    class Meta:
        model = Job
        fields = (
            'client_id', 'job_title', 'jd_url', 'tech_skills', 'location', 'job_type',
            'min_exp', 'max_exp', 'min_relevant_exp', 'max_notice', 'min_ctc', 'max_ctc',
            'expiring_days', 'jd_extra'
        )

    def create(self, validated_data):
        job_obj = Job.objects.create(**validated_data)
        # client_obj = Client.objects.get(validated_data['client'])
        # job_obj.client = client_obj
        print(job_obj)
        job_obj.save()
        return job_obj


class JobListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        # Tuple of serialized model fields (see link [2])
        # fields = ( "id", "username", "password", )
        fields = (
            'id', 'client_id', 'job_title', 'jd_url', 'tech_skills', 'location', 'job_type',
            'min_exp', 'max_exp', 'min_relevant_exp', 'max_notice', 'min_ctc', 'max_ctc',
            'expiring_days', 'jd_extra'
        )
        # write_only_fields = ('password',)
        read_only_fields = ('id',)
