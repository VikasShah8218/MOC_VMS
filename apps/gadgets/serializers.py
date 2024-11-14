from rest_framework import serializers
from .models import AdamLinkedwith
from .models import Adam


class AdamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adam
        fields = '__all__'


class AdamLinkedwithCreateSerializer(serializers.ModelSerializer):
    # adam = serializers.PrimaryKeyRelatedField(queryset=Adam.objects.all(), required=True)
    class Meta:
        model = AdamLinkedwith
        fields = '__all__'




class AdamLinkedwithReadSerializer(serializers.ModelSerializer):
    adam = AdamSerializer(read_only=True)
    class Meta:
        model = AdamLinkedwith
        fields = '__all__'  

