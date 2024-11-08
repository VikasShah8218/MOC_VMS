# Third-Party Imports
from rest_framework import serializers

# Local Imports
from .models import VisitorPass
from apps.visitor.models import Visitor
from apps.visitor.serializers import VisitorSerializer
import random
import time 

class VisitorPassSerializer(serializers.ModelSerializer):
    visitor = VisitorSerializer(read_only=True)
    created_by_name = serializers.SerializerMethodField()
    pass_number = serializers.IntegerField(read_only=True)  # Set as read-only

    class Meta:
        model = VisitorPass
        fields = '__all__'

    def create(self, validated_data):
        if 'pass_number' not in validated_data:
            validated_data['pass_number'] = self.generate_unique_pass_number()
        return super().create(validated_data)

    def generate_unique_pass_number(self):
        pass_number = int(f"{int(time.time()) % 100000}{random.randint(100, 999)}")  # Truncate timestamp to last 5 digits
        while VisitorPass.objects.filter(pass_number=pass_number).exists():
            pass_number = int(f"{int(time.time()) % 100000}{random.randint(100, 999)}")
        return pass_number
    
    def get_created_by_name(self, obj):
        return obj.created_by.username if obj.created_by else None


class VisitorPassOverwriteSerializer(VisitorPassSerializer):
    valid_until = serializers.DateTimeField(required=True)
    visitor = serializers.PrimaryKeyRelatedField(
        queryset=Visitor.objects.all(),
        required=True
    )

    class Meta(VisitorPassSerializer.Meta):
        extra_kwargs = {
            'key': {'required': True}
        }

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['visitor'] = VisitorSerializer(instance.visitor).data
        return repr

    def create(self, validated_data):
        validated_data['created_by'] = self.context['created_by']
        return super().create(validated_data)


class CancelPassSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitorPass
        fields = 'is_cancelled'


class TblVisitorVisitDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitorPass
        fields = [
            'id', 
            # 'passNumber',
            # 'barcode' ,
            # 'toMeet', 
            # 'department', 
           
            # 'allowedGates', 
            # 'validFor', 
            # 'authoByWhome', 
            # 'purpose', 
           
            # 'daysImage', 
            # 'passCancelledAt', 
            # 'visitorId',
            # 'vDate'
        ]
