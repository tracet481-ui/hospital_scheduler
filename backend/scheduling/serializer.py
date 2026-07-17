from rest_framework import serializers

from .models import SurgeryRequest, Patient, SurgeryType

## operasyon ekleme -----------------------


class SurgeryRequestSerializer(serializers.ModelSerializer) : 


    patient_name = serializers.CharField(

        source = "patient.code",
        read_only = True,
        
    )

    surgery_name = serializers.CharField(

        source = "surgery_type.name",
        read_only = True,

    )

    
    class Meta :

        model = SurgeryRequest

        fields = [

            "id",

            "patient",
            "patient_name",

            "surgery_type",
            "surgery_name",

            "priority",

        ]

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


    class Meta :

        model = SurgeryType

        fields = [

            "id",
            "name",
            "duration_slots",
            "specialty_name",

        ]


## ------------------------------ SurgeryType Serializer 



## -----------------------   operasyon ekleme 