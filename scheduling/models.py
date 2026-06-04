from django.db import models

# Create your models here.


class BaseModel (models.Model) :

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class Specialty (BaseModel) :
    name = models.CharField(max_length = 100, unique = True)


    def __str__ (self):
        return self.name
    

class Surgeon (BaseModel) :
    name = models.CharField(max_length = 100 )
    specialty = models.ForeignKey(
        Specialty,
        on_delete = models.PROTECT,
        related_name = "surgeons" 
    )

    off_day = models.CharField(max_length = 20 )

    def __str__(self) :
        return self.name
    

class OperatingRoom ( BaseModel ) :
    name = models.CharField(max_length= 50, unique = True )
    room_type = models.ForeignKey (
        Specialty,
        on_delete = models.PROTECT,
        related_name= "rooms",
        null= True,
        blank = True,

    ) 
    is_hybrid = models.BooleanField (default = False )

    def __str__ (self) :
        return self.name
    


class AnesthesiaTeam (BaseModel) :

    name = models.CharField(max_length = 50, unique = True )

    def __str__ (self) :
        return  self.name
    


class Patient ( BaseModel ) :

    code = models.CharField (max_length = 20, unique = True )

    def __str__ (self) : 
        return self.code
    

class SurgeryType (BaseModel) :
    name = models.CharField (max_length= 100, unique= True)
    required_specialty = models. ForeignKey(
        Specialty,
        on_delete= models.PROTECT,
        related_name = "surgery_types",
        
    )

    competible_rooms = models.ManyToManyField(
        OperatingRoom,
        related_name = "competible_surgery_types",
        blank = True,

    )

    def __str__ (self) :
        return self.name
    

class SurgeryRequest ( BaseModel ):
    PRIORITY_CHOICES = [
        ("critical", "Kritik"),
        ("high", "Yüksek"),
        ("medium", "Orta"),
        ("low", "Düşük"),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete = models.CASCADE,
        related_name = "surgery_requests", 

    )

    surgery_type = models.ForeignKey(
        SurgeryType,
        on_delete = models.PROTECT,
        related_name="requests",
    )

    duration = models.PositiveIntegerField()
    priority = models.CharField (max_length= 20, choices= PRIORITY_CHOICES)

    def __str__(self) :
        return f"{self.patient.code} - {self.surgery_type.name}"
    


class SchedulePlan(BaseModel):
    ALGORITHM_CHOICES = [
        ("backtracking", "Backtacking"),
        ("cp", "Constraint Programming"),


    ]


    planning_day = models.CharField(max_length=20)
    algorithm_name = models.CharField(max_length= 30, choices=ALGORITHM_CHOICES)
    score = models.IntegerField(default=0)
    is_feasible = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.algorithm_name} - {self.planning_day} - {self.score} "
    


class ScheduleItem(BaseModel) :
    plan = models.ForeignKey(
        SchedulePlan,
        on_delete= models.CASCADE,
        related_name= "items",

    )

    surgery_request = models.ForeignKey(
        SurgeryRequest,
        on_delete= models.CASCADE,
        related_name = "schedule_items",

    )

    surgeon = models.ForeignKey(
        Surgeon,
        on_delete = models.PROTECT,
        related_name = "schedule_items",

    )


    room = models.ForeignKey(
        OperatingRoom,
        on_delete= models.PROTECT,
        related_name = "schedule_items",

    )


    anesthesia_team = models.ForeignKey(
        AnesthesiaTeam,
        on_delete = models.PROTECT,
        related_name= "schedule_items",


    )

    start_slot = models.PositiveIntegerField() 
    end_slot =models.PositiveIntegerField()

    def __str__(self) :
        return f"{self.surgery_request} | {self.start_slot} - {self.end_slot}"
    

