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

        console.log ("Plan detail : " , plan.value)
        console.log (
            "Simulation results : ",
            plan.value?.simulation_results)

    }   catch   (error) {

        console.log(error)

        errorMessage.value = "Plan detayı yüklenirken hata oluştu !"

    }   finally {

        loading.value = false

    }

        // plan.value = response.data

        // console.log ("Plan detail : " , plan.value)
        // console.log (
        //     "Simulation results : ",
        //     plan.value?.simulation_results
        // )

}

//   score görselleştirme   ----------------------------------------------


const scorePercent = computed (() => {

    return Number (plan.value?.success_rate ?? 0) 


    // if (! plan.value?.score) return 0

    // return Math.min(100, Math.round (plan.value.score / 1300 ))

})

const simulationResults = computed(() => {
    if (!plan.value) return []

    return Array.isArray(plan.value.simulation_results)
        ? plan.value.simulation_results
        : []
})



//  ---------------------------------------------- score görselleştirme   


// const scoreCircleStyle = computed (() => {

//     return {

//         background : 'conic-gradient( #2563eb ${scorePercent.value * 3.6} deg, #e5e7eb 0deg)'

//     }

// })


//   score görselleştirme   ----------------------------------------------


// const scorePercent= computed (() => {

//     if (!plan.value?.score) return 0

//     return Math.min (100, Math.round (plan.value.score / 1300 ))

// })


//   score görselleştirme   ---------------------------------------------- 



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

            <!-- <div class ="summary-grid" >

                <div class ="summary-card" >

                    <span >
                        Skor
                    </span>

                    <strong>
                        {{ plan.score }}
                    </strong>

                </div>


     score görselleştirme --------------------------------- -->

                
                <!-- <div v-if ="plan" class = "score-progress-card" > -->

            <!--     <div class ="progress-heading" >

                        <span>
                                Plan Başarı Oranı 
                        </span>

                        <strong >

                            {{ scorePercent }}%

                        </strong>

                    </div>


                    <v-progress-linear
                                    :model-value ="scorePercent"
                                    color = "blue"
                                    height ="20"
                                    rounded
                                    >
 
                    </v-progress-linear>

                </div>

        ----------------------------- score görselleştirme  -->


        <!--  score görselleştirme ----------------------------- -->



<!-- 
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


                <div class="summary-card simulation-card">
                    <span class="card-label">Simülasyon Skorları</span>

                    <div
                        v-if="simulationResults.length > 0"
                        class="simulation-score-list"
                    >
                        <div
                            v-for="result in simulationResults"
                            :key="result.valid_index"
                            class="simulation-score-row"
                            :class="{ best: result.is_best }"
                        >
                            <div class="simulation-plan-name">
                                <span
                                    v-if="result.is_best"
                                    class="best-star"
                                >
                                    ★
                                </span>

                                <span v-else class="star-placeholder"></span>

                                <span>
                                    Plan {{ result.valid_index }}
                                </span>
                            </div>

                            <strong>
                                {{ result.score }}
                            </strong>
                        </div>
                    </div>

                    <span v-else class="empty-result">
                        Simülasyon sonucu bulunamadı.
                    </span>
                </div>

            </div> --> -->
<!-- 
----------------------------------------------------- -->


        <div class="summary-layout">

            <div class="summary-grid">
                <div class="summary-card">
                    <span class="card-label">Skor</span>
                    <strong>{{ plan.score }}</strong>
                </div>

                <div class="summary-card progress-card">
                    <div class="progress-heading">
                        <span class="card-label">Plan Başarı Oranı</span>
                        <strong>{{ scorePercent }}%</strong>
                    </div>

                    <v-progress-linear
                        :model-value="scorePercent"
                        color="blue"
                        height="14"
                        rounded
                    />
                </div>

                <div class="summary-card">
                    <span class="card-label">Algoritma</span>
                    <strong>{{ plan.algorithm_name }}</strong>
                </div>

                <div class="summary-card">
                    <span class="card-label">Feasible</span>
                    <strong>{{ plan.is_feasible ? "Evet" : "Hayır" }}</strong>
                </div>
            </div>

            <div class="summary-card simulation-card">
                <span class="card-label">Simülasyon Skorları</span>

                <div
                    v-if="simulationResults.length"
                    class="simulation-score-list"
                >
                    <div
                        v-for="result in simulationResults"
                        :key="`${result.attempt}-${result.valid_index}`"
                        class="simulation-score-row"
                        :class="{ best: result.is_best }"
                    >
                        <div class="simulation-plan-name">
                            <span v-if="result.is_best" class="best-star">★</span>
                            <span v-else class="star-placeholder"></span>

                            <span>Plan {{ result.valid_index }}</span>
                        </div>

                        <strong>{{ result.score }}</strong>
                    </div>
                </div>
            </div>

        </div>



<!-- 
            -------------------------------------------- -->


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
/* 
-----------------------------------------------

.summary-grid {
    display: grid;
    grid-template-columns: 220px 220px 220px 1fr;
    gap: 16px;
    margin-bottom: 24px;
}

----------------------------------------------- */

.summary-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 8px;
    
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

/* 
.score-section {
    display: flex;
    align-items: center;
    gap: 24px;
    margin: 24px 0;
    padding: 24px;
    background: white;
    border-radius: 18px;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
}

.score-circle {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.score-inner {
    width: 110px;
    height: 110px;
    border-radius: 50%;
    background: white;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.score-inner strong {
    font-size: 28px;
    color: #0f172a;
}

.score-inner span {
    font-size: 14px;
    color: #64748b;
}

.score-info {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.score-info span {
    color: #64748b;
    font-size: 14px;
}

.score-info strong {
    font-size: 32px;
    color: #0f172a;
}
 */



.score-card {
    background: white;
    padding: 24px;
    border-radius: 18px;
    margin-bottom: 24px;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
}

.score-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
}

.score-title {
    margin: 0;
    color: #64748b;
    font-size: 14px;
}

.score-header h2 {
    margin: 4px 0 0;
    color: #0f172a;
    font-size: 32px;
}

.score-percent {
    font-size: 28px;
    color: #2563eb;
}


.score-progress-card {
    margin-bottom: 24px;
    padding: 22px;
    background: white;
    border-radius: 16px;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
}

.progress-heading {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
}

.progress-heading span {
    color: #64748b;
    font-size: 14px;
}

.progress-heading strong {
    color: #2563eb;
    font-size: 22px;
}
/* 
----------------------------------------

.simulation-card {
    grid-column: 4;
    grid-row: 1 / span 2;
}

----------------------------------------- */

.simulation-section {
    margin-top: 24px;
    padding: 24px;
    background: white;
    border-radius: 16px;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
    
}

.simulation-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    margin-bottom: 20px;
}

.simulation-header h2 {
    margin: 0;
    color: #0f172a;
}

.simulation-header p {
    margin: 6px 0 0;
    color: #64748b;
}

.best-score-box {
    display: flex;
    flex-direction: column;
    min-width: 150px;
    padding: 14px 18px;
    background: #eff6ff;
    border-radius: 12px;
}

.best-score-box span {
    color: #64748b;
    font-size: 13px;
}

.best-score-box strong {
    color: #2563eb;
    font-size: 24px;
}

.simulation-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
    
}

.simulation-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 16px;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
}

.simulation-item.best {
    border-color: #2563eb;
    background: #eff6ff;
}

.result-left,
.result-right {
    display: flex;
    align-items: center;
    gap: 10px;
}

.result-left div {
    display: flex;
    flex-direction: column;
}

.result-left small {
    color: #94a3b8;
    font-size: 12px;
}

.best-marker {
    color: #f59e0b;
    font-size: 20px;
}

.best-label {
    padding: 4px 8px;
    color: #1d4ed8;
    background: #dbeafe;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;
}

.result-right strong {
    color: #0f172a;
}


/* ----------------------------------------------------- */

.summary-layout {
    display: grid;
    grid-template-columns: minmax(0, 2fr) minmax(280px, 1fr);
    gap: 16px;
    align-items: stretch;
}

.summary-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 16px;
}

.simulation-card {
    height: 100%;
    min-width: 0;
}

.simulation-score-list {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 8px;
    margin-top: 12px;
}

.simulation-score-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    padding: 8px 10px;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    background: #f8fafc;
}

.simulation-score-row.best {
    border-color: #3b82f6;
    background: #eff6ff;
}

.simulation-plan-name {
    display: flex;
    align-items: center;
    gap: 5px;
    font-size: 12px;
}

.simulation-score-row strong {
    font-size: 12px;
}

.best-star {
    color: #f59e0b;
}

.star-placeholder {
    display: inline-block;
    width: 12px;
}




/* ----------------------------------------------------- */


</style>