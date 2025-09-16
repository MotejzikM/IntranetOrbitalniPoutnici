from rest_framework import serializers
from .models import Zprava, Diskuze

class ZpravaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zprava
        fields = ['id', 'nazev', 'obsah', 'datum_vytvoreni', 'autor']
        read_only_fields = ['datum_vytvoreni', 'autor']

        extra_kwargs = {
            'nazev': {'required': True, 'max_length': 200},
            'obsah': {'required': True}
        }

class DiskuzeSerializer(serializers.ModelSerializer):
    zpravy = ZpravaSerializer(many=True, required=False)

    class Meta:
        model = Diskuze
        fields = ['id', 'nazev', 'popis', 'datum_zahajeni', 'updated', 'zpravy']
        read_only_fields = ['datum_zahajeni', 'updated']

        extra_kwargs = {
            'nazev': {'required': True, 'max_length': 200},
            'popis': {'required': False}
        }

    def create(self, validated_data):
        zpravy_data = validated_data.pop('zpravy', [])
        diskuze = Diskuze.objects.create(**validated_data)
        for zprava_data in zpravy_data:
            Zprava.objects.create(diskuze=diskuze, **zprava_data)
        return diskuze

    def update(self, instance, validated_data):
        instance.nazev = validated_data.get('nazev', instance.nazev)
        instance.popis = validated_data.get('popis', instance.popis)
        instance.save()
        
        # Update messages if provided
        zpravy_data = validated_data.get('zpravy', [])
        if zpravy_data:
            for zprava_data in zpravy_data:
                Zprava.objects.update_or_create(
                    id=zprava_data.get('id'),
                    defaults=zprava_data
                )
        
        return instance