<script setup>

import { ref } from "vue";

import { generateSchedule } from "../services/scheduleApi" ;


const loading = ref (false) 

const errorMessage = ref("") 

const scheduleResult = ref(null)



const handleGenerate = async () => {

    loading.value = true;

    errorMessage.value = ""

    scheduleResult.value = null


    try {

        const response = await generateSchedule() 
        scheduleResult.value = response.data
        
    }   catch (error) {

        console.log(error)
        console.log(error.response)
        console.log(error.response?.data)

        errorMessage.value = "Plan oluşturulurken hata oluştu!"

    }   finally {

        loading.value = false;

    }
};


</script>



<template>

    <main>

        <h1>
            Hospital Scheduler
        </h1>


        <button @click="handleGenerate" :disabled = "loading">
            {{  loading ? "Plan oluşturuluyor ... " : " Plan oluştur " }}
        </button>

        <p v-if = "errorMessage">
            {{  errorMessage }}

        </p>


        <section v-if = "scheduleResult">

            <h2>
                Sonuç

            </h2>

            <p>
                <strong>
                    Score : 

                </strong>

                {{ scheduleResult.score }}

            </p>

            <p>
                <strong>
                    Plan ID : 

                </strong>

                {{ scheduleResult.plan_id }}

            </p>


            <div    
                v-for = "day in scheduleResult.weekly_schedule"
                :key = "day.day_index">

                <h3>

                    {{  day.day_name }}

                </h3>            

                <ul>

                    <li v-for = "item in day.items" :key= "item.patient">

                        {{ item.start_time }} - {{ item.end_time }} 
                        |
                        {{ item.patient }}
                        |
                        {{ item.operation }}
                        |
                        {{ item.room }}
                        |
                        {{ item.surgeon }}
                        |
                        {{ item.anesthesia_team }}

                    </li>

                </ul>

            </div>

        </section>

    </main>

</template>