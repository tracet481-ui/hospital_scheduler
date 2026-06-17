from scheduling.services.cp.scheduler import CPScheduler

from scheduling.services.scoring import calculate_schedule_score




class SimulationEngine:


    def __init__ (
            
        self,
        surgeons,
        rooms,
        anesthesia_teams,
        surgeries,
        planning_day,

    ) :
        

        self.surgeons = surgeons
        self.rooms = rooms
        self.anesthesia_teams = anesthesia_teams
        self.surgeries = surgeries
        self.planning_day = planning_day



    def run (self, iterations = 10 ) :


        best_schedule = None
        best_score = float ("-inf")
        best_details = None


        all_results = []


        for iteration in range(iterations) :


            print(

                f"\n=== Simulation {iteration + 1 } / {iterations} ==="

            )


            scheduler = CPScheduler(

                surgeons = self.surgeons,
                rooms = self.rooms,
                anesthesia_teams = self.anesthesia_teams,
                surgeries = self.surgeries,
                planning_day = self.planning_day,

            )


            schedule = scheduler.generate()

            if not schedule : 
                continue


            score, details = calculate_schedule_score(

                schedule = schedule,
                surgeries = self.surgeries,

            )


            all_results.append ({ 

                "iteration" : iteration + 1,
                "score" : score,
                "details" : details,

            })


            if score > best_score :

                best_score = score
                best_schedule = schedule
                best_details = details


        return (

            best_schedule,
            best_score,
            best_details,
            all_results,

        )
    

