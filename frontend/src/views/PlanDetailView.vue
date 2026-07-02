<script setup>

import { computed, onMounted, ref } from "vue"
import { useRoute } from "vue-router"
import { getPlanDetail } from "../services/scheduleApi"    


const route = useRoute()

const plan = ref(null)
const loading = ref(false)
const errorMessage = ref ("")


const groupedSchedule = computed (() => {

    if (!plan.value?.items)

        return []

    
        const days = [

            "Pazartesi",
            "Salı",
            "Çarşamba",
            "Perşembe",
            "Cuma",

        ]


        return days.map((day, index)  =>  ({

            dayName : day,

            items : plan.value.items.filter (

                item  =>  item.day_index === index

            )


        }))

})


const loadPlanDetail = async () => {

    loading.value = true
    errorMessage.value = ""


    try {

        const response = await getPlanDetail(route.params.id)
        plan.value = response.data

    }   catch   (error) {

        console.log(error)

        errorMessage.value = "Plan detayı yüklenirken hata oluştu !"

    }   finally {

        loading.value = false

    }

}


onMounted (loadPlanDetail)

</script>



<template>

    <main class ="page" >

        <h1>
            Plan Detayı
        </h1>

        <p v-if="loading">
            Yükleniyor
        </p>

        <p v-if="errorMessage"  class = "error">
            {{ errorMessage }}
        </p>


        <section v-if ="plan" class="card" >

            <h2>
                Skor: {{ plan.score }}
            </h2>

            <!-- <pre>
                {{ plan }}
            </pre> -->

            <div class ="summary-grid" >

                <div class ="summary-card" >

                    <span >
                        Skor
                    </span>

                    <strong>
                        {{ plan.score }}
                    </strong>

                </div>


                <div class = "summary-card" >

                    <span>
                        Algoritma
                    </span>

                    <strong>
                        {{ plan.algorithm_name }}
                    </strong>

                </div>

                <div class ="summary-card">

                    <span>
                        Feasible
                    </span>

                    <strong>
                        {{ plan.is_feasible ? "Evet" : "Hayır" }}
                    </strong>

                </div>

            </div>


            <table class ="detail-table" >

                <thead>
                    <tr>
                        <th>Gün</th>
                        <th>Başlangıç</th>
                        <th>Bitiş</th>
                        <th>Hasta</th>
                        <th>Operasyon</th>
                        <th>Doktor</th>
                        <th>Oda</th>
                        <th>Anestezi</th>
                    </tr>
                </thead>


                <tbody>

                    <tr v-for ="item in plan.items" :key="'${item.day_index}-${item.patient}'">
                        <td>{{ 
                                [
                                    "Pazartesi",
                                    "Salı",
                                    "Çarşamba",
                                    "Perşembe",
                                    "Cuma",
                                ][item.day_index]
                            }}</td>
                        <td>{{ item.start_time }}</td>
                        <td>{{ item.end_time }}</td>
                        <td>{{ item.patient }}</td>
                        <td>{{ item.operation }}</td>
                        <td>{{ item.surgeon }}</td>
                        <td>{{ item.room }}</td>
                        <td>{{ item.anesthesia_team }}</td>
                    </tr>

                </tbody>

            </table>

        </section>


        <section
                v-for ="day in groupedSchedule"
                :key = "day.dayName"
                class ="day-card">

            
            <h2>
                {{ day.dayName }}
            </h2>

            <div
                v-for ="item in day.items"
                :key = "'${item.patient} - ${item.start_slot}'"
                class = "operation-card">

                <div class = "time" >

                    {{ item.start_time }} -
                    {{ item.end_time }}

                </div>

                <div class = "patient" >

                    {{ item.patient }}

                </div>

                <div class ="operation">

                    {{ item.operation }}

                </div>

                <div>

                    👨‍⚕️ {{ item.surgeon }}

                </div>


                <div>

                    🏥 {{ item.room }}


                </div>

                <div>

                    💉 {{ item.anesthesia_team }}

                </div>

            </div>

        </section>

    </main>

</template>



<style scoped>
.page {
    padding: 28px;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 14px;
}

.error {
    color: #dc2626;
}


.summary-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 24px;
}

.summary-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 16px;
}

.summary-card span {
    display: block;
    color: #64748b;
    font-size: 13px;
}

.summary-card strong {
    color: #0f172a;
    font-size: 22px;
}

.detail-table {
    width: 100%;
    border-collapse: collapse;
}

.detail-table th,
.detail-table td {
    padding: 12px;
    border-bottom: 1px solid #e2e8f0;
    text-align: left;
    color: #0f172a;
}

.detail-table th {
    background: #f1f5f9;
    font-weight: 700;
}


.day-card{
    background:white;
    padding:20px;
    border-radius:14px;
    margin-bottom:30px;
    box-shadow:0 2px 10px rgba(0,0,0,.08);
}

.day-card h2{
    margin-bottom:20px;
    color:#0f172a;
    border-bottom:2px solid #e2e8f0;
    padding-bottom:10px;
}

.operation-card{
    background:#f8fafc;
    padding:16px;
    border-radius:10px;
    margin-bottom:12px;

    display:grid;
    grid-template-columns:
        120px
        80px
        220px
        170px
        100px
        120px;

    align-items:center;
}

.time{
    font-weight:bold;
    color:#2563eb;
}

.patient{
    font-weight:bold;
}

.operation{
    color:#0f172a;
}


</style>