from rest_framework import serializers
from .models import AdamLinkedwith
from .models import Adam


class AdamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adam
        fields = '__all__'


class AdamLinkedwithSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdamLinkedwith
        fields = '__all__'  
