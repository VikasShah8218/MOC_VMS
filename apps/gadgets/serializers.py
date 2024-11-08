# Local Imports
from .models import Adam

# Third-Party Imports
from rest_framework import serializers
from apps.accounts.serializers import UserDetailsSerializer

class AdamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adam
        fields = '__all__'
