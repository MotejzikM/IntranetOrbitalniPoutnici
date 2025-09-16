from rest_framework import serializers
from .models import Page

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['id', 'title', 'slug', 'content', 'created', 'updated', 'updated_by', 'diskuze_set']
        read_only_fields = ['id', 'created', 'updated']

        extra_kwargs = {
            'title': {'required': True, 'max_length': 200},
            'slug': {'required': True, 'max_length': 200, 'error_messages': {
                'unique': "Tento identifikátor již existuje.",
                'blank': "Identifikátor nesmí být prázdný."
            }},
            'content': {'required': True}
        }

    def create(self, validated_data):
        return Page.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.content = validated_data.get('content', instance.content)
        instance.updated_by = validated_data.get('updated_by', instance.updated_by)
        instance.diskuze_set = validated_data.get('diskuze_set', instance.diskuze_set)
        instance.save()
        return instance