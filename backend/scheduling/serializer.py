from rest_framework import serializers

from django.db import transaction

from .models import SurgeryRequest, Patient, SurgeryType

## operasyon ekleme -----------------------


class SurgeryRequestSerializer(serializers.ModelSerializer) : 


    patient_code = serializers.CharField(

        write_only = True,

        max_length = 20,

    )



    patient_name = serializers.CharField(

        source = "patient.code",
        read_only = True,
        
    )

    surgery_name = serializers.CharField(

        source = "surgery_type.name",
        read_only = True,

    )


    priority_display = serializers.CharField(

        source = "get_priority_display",

        read_only = True,

    )

    
    class Meta :

        model = SurgeryRequest

        fields = [

            "id",

            "patient_name",
            "patient_code",

            "surgery_type",
            "surgery_name",

            "priority",
            "priority_display",

        ]

        read_only_fields = [

            "priority",
            "priority_display",

        ]

    def validate_patient_code (self, value) :

        cleaned_code = value.strip().upper()

        if not cleaned_code :

            raise serializers.ValidationError(
                "Hasta kodu boş bırakılamaz."
            )

        if Patient.objects.filter (code = cleaned_code ).exists() :

            raise serializers.ValidationError(
                "Bu hasta kodu zaten kullannılmış."
            )

        return cleaned_code


    @transaction.atomic

    def create (self, validated_data) :


        patient_code = validated_data.pop("patient_code")
        surgery_type = validated_data ["surgery_type"]


        patient = Patient.objects.create(

            code = patient_code,

        )

        return SurgeryRequest.objects.create(

            patient = patient,
            surgery_type = surgery_type,
            priority = surgery_type.priority,

        )




## 1. Patient Serializer -----------------------------

class PatientSerializer (serializers.ModelSerializer) :

    class Meta :

        model = Patient
        fields = [

            "id",
            "code",

        ]



## ----------------------------- 1. Patient Serializer 

## SurgeryType Serializer ------------------------------

class SurgeryTypeSerializer(serializers.ModelSerializer) :

    specialty_name = serializers.CharField(

        source = "required_specialty.name",
        read_only = True,

    )


    priority_display = serializers.CharField(

    source = "get_priority_display",

    read_only = True,

    )


    class Meta :

        model = SurgeryType

        fields = [

            "id",
            "name",
            "duration_slots",
            "required_specialty",
            "specialty_name",
            "priority",
            "priority_display",

        ]

        read_only_fields = [
            "priority",
            "priority_display",
        ]


## ------------------------------ SurgeryType Serializer 



## -----------------------   operasyon ekleme 