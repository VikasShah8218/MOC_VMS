# Third-Party Imports
from rest_framework import serializers

# Local Imports
from .models import Visitor


class VisitorBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = ['id', 
                  'first_name', 
                  'last_name', 
                  'visitor_type', 
                  'address',
                  'phone', 
                  'image', 
                  'gov_id_type', 
                  'gov_id_no', 
                  'is_blacklisted', 
                  'is_pass_created',
                  'created_on', 
                  'created_by', 
                  'updated_on', 
                  'updated_by',
                  'is_deleted',
                  'other',
                  ]


class VisitorSerializer(VisitorBaseSerializer):
    def create(self, validated_data):
        validated_data['created_by'] = self.context['created_by']
        return super().create(validated_data)


class UpdateVisitorSerializer(VisitorBaseSerializer):
    gov_id_no = serializers.CharField(max_length=255, read_only=True)

    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['updated_by']
        return super().update(instance, validated_data)
