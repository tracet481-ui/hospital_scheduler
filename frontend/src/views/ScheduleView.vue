<script setup>

import { ref } from "vue";

import { generateSchedule } from "../services/scheduleApi" ;


const loading = ref (false) ;

const schedule = ref(null) ;



const handleGenerate = async () => {

    loading.value = true;


    try {

        const response = await generateSchedule() ;
        schedule.value = response.data;
        
    }   catch (error) {

        console.error(error) ;

    }   finally {

        loading.value = false;

    }
};


</script>



<template>

    <div>

        <h1>
            Hospital Scheduler
        </h1>


        <button @click="handleGenerate">
            Plan oluştur
        </button>


        <div v-if = "loading">
            plan oluşturuluyor...
        </div>


        <pre v-if = "schedule">
            {{ schedule }}
        </pre>

    </div>

</template>