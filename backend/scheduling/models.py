from django.db import models
import uuid

# Create your models here.


class BaseModel (models.Model) :
    #TO DO: id oluşturulacak uuid türünde 
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     abstract = True


    id = models.UUIDField(
        primary_key= True,
        default= uuid.uuid4,
        editable= False,
    )

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now= True )


    class Meta:
        abstract = True

    




class Specialty(BaseModel):
    """
    Doktorun yetkinliğini tutar.
    """
    name = models.CharField(max_length = 100, unique = True)


    def __str__ (self):
        return self.name
    

class Surgeon(BaseModel):
    """
    Cerrahları tutar.
    """
    name = models.CharField(max_length = 100, verbose_name="Cerrahın İsmi" )
    specialty = models.ForeignKey(
        Specialty,
        on_delete = models.PROTECT,
        related_name = "surgeons", 
        verbose_name="Cerrahın yetkinliği"
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
    name = models.CharField (max_length= 100, )
    required_specialty = models. ForeignKey(
        Specialty,
        on_delete= models.PROTECT,
        related_name = "surgery_types",
        
    )

    duration_slots = models.PositiveIntegerField()

    compatible_rooms = models.ManyToManyField(
        OperatingRoom,
        related_name = "compatible_surgery_types",
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

    # duration = models.PositiveIntegerField()
    priority = models.CharField (max_length= 20, choices= PRIORITY_CHOICES)

    def __str__(self) :
        return f"{self.patient.code} - {self.surgery_type.name}"
    


class SchedulePlan(BaseModel):
    ALGORITHM_CHOICES = [
        ("backtracking", "Backtacking"),
        ("cp", "Constraint Programming"),
    ]

    ## score sayfası --------
    id = models.UUIDField(

        primary_key = True,
        default = uuid.uuid4,
        editable = False,

    )

    
    ## --------   score sayfası 


    planning_day = models.CharField(max_length=20)
    algorithm_name = models.CharField(max_length= 30, choices=ALGORITHM_CHOICES)
    score = models.IntegerField(default=0)
    is_feasible = models.BooleanField(default=True)


    priority_score = models.IntegerField(default = 0)
    day_balance_penalty = models.IntegerField(default = 0)
    anesthesia_balance_penalty = models.IntegerField(default = 0)
    room_idle_penalty = models.IntegerField(default = 0)
    surgeon_idle_penalty = models.IntegerField(default = 0)
    success_rate = models.IntegerField(default = 0)


        ##   detail sayfasında son plan kayıtlarını göster 


    simulation_results = models.JSONField(

    default = list ,
    blank = True,
    )

    def __str__(self):
        return f"{self.algorithm_name} - {self.planning_day} - {self.score} "
    






    # simulation_results = [
    #     {

    #         "attempt" : result["attempt"],
    #         "valid_index" : result["valid_index"],
    #         "score" : result["score"],
    #         "is_best" : result ["score"] == best_score,

    #     }

    #     for result  in all_results
    # ]

    ##   detail sayfasında son plan kayıtlarını göster 








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
    



    day_index = models.PositiveIntegerField(
        default = 0
        )