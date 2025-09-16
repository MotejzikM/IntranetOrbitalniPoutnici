from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'date', 'description', 'location', 'showToTimeline', 'participants']
        read_only_fields = ['id']

        extra_kwargs = {
            'title': {'required': True, 'max_length': 200},
            'date': {'required': True},
            'description': {'required': False, 'allow_blank': True},
            'location': {'required': False, 'allow_blank': True},
            'showToTimeline': {'required': False}
        }

    def create(self, validated_data):
        return Event.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.date = validated_data.get('date', instance.date)
        instance.description = validated_data.get('description', instance.description)
        instance.location = validated_data.get('location', instance.location)
        instance.showToTimeline = validated_data.get('showToTimeline', instance.showToTimeline)
        instance.save()
        return instance