<script setup>
import { computed, onMounted, ref } from "vue"
import { useRoute } from "vue-router"
import { getPlanDetail } from "../services/scheduleApi"

const route = useRoute()

const plan = ref(null)
const loading = ref(false)
const errorMessage = ref("")
const recentPlansDialog = ref(false)

const groupedSchedule = computed(() => {
    if (!plan.value?.items) return []

    const days = [
        "Pazartesi",
        "Salı",
        "Çarşamba",
        "Perşembe",
        "Cuma",
    ]

    return days.map((day, index) => ({
        dayName: day,
        items: plan.value.items.filter(
            (item) => item.day_index === index,
        ),
    }))
})

const loadPlanDetail = async () => {
    loading.value = true
    errorMessage.value = ""

    try {
        const response = await getPlanDetail(String(route.params.id))
        plan.value = response.data

        console.log("Plan detail:", plan.value)
        console.log(
            "Simulation results:",
            plan.value?.simulation_results,
        )
    } catch (error) {
        console.log(error)
        errorMessage.value = "Plan detayı yüklenirken hata oluştu!"
    } finally {
        loading.value = false
    }
}

const scorePercent = computed(() => {
    return Number(plan.value?.success_rate ?? 0)
})

const simulationResults = computed(() => {
    if (!plan.value) return []

    return Array.isArray(plan.value.simulation_results)
        ? plan.value.simulation_results
        : []
})

const getResultPercentage = (result) => {
    const storedPercentage =
        result.success_rate ??
        result.percentage ??
        result.percent

    if (storedPercentage !== undefined && storedPercentage !== null) {
        return Number(storedPercentage)
    }

    // Eski simulation_results kayıtlarında yalnızca score varsa
    // mevcut yüzde hesabıyla uyumluluk için geçici geri dönüş.
    if (result.score !== undefined && result.score !== null) {
        return Math.min(100, Math.max(0, Number(result.score) / 1300))
    }

    return 0
}

const recentPlanPercentages = computed(() => {
    const results = simulationResults.value.slice(0, 10)

    let selectedIndex = results.findIndex(
        (result) => result.is_best === true,
    )

    if (selectedIndex === -1 && plan.value?.score !== undefined) {
        selectedIndex = results.findIndex(
            (result) => Number(result.score) === Number(plan.value.score),
        )
    }

    return results.map((result, index) => ({
        key: `${result.attempt ?? "attempt"}-${result.valid_index ?? index}`,
        percentage: getResultPercentage(result),
        isSelected: index === selectedIndex,
    }))
})

const formatPercentage = (percentage) => {
    const value = Number(percentage)

    if (!Number.isFinite(value)) return "0.0"

    return value.toFixed(1)
}



// raporlama --------------------------------------------- 

const reportDialog = ref(false)

const reportData = computed (() => ({

    violations : [

        {
            code : "DAY_BALANCE",
            title : "Gün dengesi",
            message : "Operasyonlar günlere dengeli dağıtılmadı...",
            loss : 2400
        },

        {
            code : "SURGEON_IDLE",
            title : "Cerrah boşluğu",
            message : "Cerrah programında boş slotlar oluştu",
            loss : 400
        },

        {
            code : "ROOM_IDLE",
            title : "Ameliyathane boşluğu",
            message : "Ameliiyathaneler arası boş süreler oluştu",
            loss : 240
        },

        {
            code : "ANESTHESIA",
            title : "Anestezi dengesi",
            message : "Takımlar eşit yük dağılımına ulaşamadı",
            loss : 50
        }

    ],


    resources : {

        rooms : [

            { name : "OR-1", usage: 92},
            { name : "OR-2", usage: 88},
            { name : "OR-3", usage: 95},
            { name : "OR-4", usage: 81},
            
        ],

        surgeons : [

            { name : "Dr. Ahmet", usage: 87},
            { name : "Dr. Mehmet", usage: 91},
            { name : "Dr. Can", usage: 78},        

        ],

        anesthesia : [

            { name : "TEAM-A", usage: 44},
            { name : "TEAM-B", usage: 44},
            { name : "TEAM-C", usage: 43},
            
        ],

    }

}))

// --------------------------------------------- raporlama



onMounted(loadPlanDetail)
</script>

<template>
    <main class="page">
        <div class="page-header">
            <h1>Plan Detayı</h1>

            <div class = "detail-actions">

                <button
                        class = "secondary-button"
                        @click = "recentPlansDialog = true">

                    Son 10 Plan

                </button>

                <button
                        class = "secondary-button"
                        @click = "reportDialog = true">

                    Raporlar

                </button>

            </div>
        </div>

        <p v-if="loading">
            Yükleniyor
        </p>

        <p v-if="errorMessage" class="error">
            {{ errorMessage }}
        </p>

        <section v-if="plan" class="card">
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

            <table class="detail-table">
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
                    <tr
                        v-for="item in plan.items"
                        :key="`${item.day_index}-${item.patient}-${item.start_slot}`"
                    >
                        <td>
                            {{
                                [
                                    "Pazartesi",
                                    "Salı",
                                    "Çarşamba",
                                    "Perşembe",
                                    "Cuma",
                                ][item.day_index]
                            }}
                        </td>
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
            v-for="day in groupedSchedule"
            :key="day.dayName"
            class="day-card"
        >
            <h2>{{ day.dayName }}</h2>

            <div
                v-for="item in day.items"
                :key="`${item.patient}-${item.start_slot}`"
                class="operation-card"
            >
                <div class="time">
                    {{ item.start_time }} - {{ item.end_time }}
                </div>

                <div class="patient">
                    {{ item.patient }}
                </div>

                <div class="operation">
                    {{ item.operation }}
                </div>

                <div>👨‍⚕️ {{ item.surgeon }}</div>
                <div>🏥 {{ item.room }}</div>
                <div>💉 {{ item.anesthesia_team }}</div>
            </div>
        </section>


        <Teleport to ="body" >

            <div
                v-if = "recentPlansDialog"
                class = "dialog-overlay"
                click.self = "recentPlansDialog = false " 
                >

                <div
                    class = "recent-plans-dialog"
                    role = "dialog"
                    aria-model = "true"
                    aria-labelledby = "recent-plans-title">
                
                    <div class ="dialog-header">

                        <h2 id = "recent-plans-title">
                            Son 10 Plan
                        </h2>

                        <button
                                type = "button"
                                class = "dialog-close-button"
                                aria-label = "Pencereyi Kapat"
                                @click = "recentPlansDialog  = False">

                                x

                        </button>

                    </div>

                    <div
                        v-if = "recentPlanPercentages.length"
                        class = "recent-plans-list">
                    
                        <div
                            v-for = "result in recentPlanPercentages"
                            :key = "result.key"
                            class = "recent-plan-row"
                            :class = "{ selected: result.isSelected }" >
                        
                            <strong>
                                %{{ formatPercentage(result.percentage) }}
                            </strong>

                            <span
                            v-if = "result.isSelected"
                                class = "selected-marker">

                                <span class = "selected-check" >
                                    ✓
                                </span>

                                Seçili
                                                                
                            </span>
                        
                        </div>

                    </div>


                    <p v-else class ="empty-result">
                        Simülasyon Sonucu  Bulunamadı!
                    </p>

                </div>

            </div>

        </Teleport>


        <Teleport to = "body">

            <div
                v-if = "reportDialog"
                class = "dialog-overlay"
                @click.self = "reportDialog = false">

                <div class = "report-dialog">

                    <div class = "dialog-header" >

                        <h2>
                            Raporlar
                        </h2>

                        <button
                                class = "dialog-close-button"
                                @click = "reportDialog = false">

                            x

                        </button>

                    </div>

                    <section>

                        <h3>
                            Soft Constrait İhlalleri
                        </h3>

                        <div
                            v-for = "item in reportData.violations"
                            :key = "item.code"
                            class = "report-card">

                            <h4>
                                    {{ item.title }}
                            </h4>

                            <p>
                                    {{ item.message }}
                            </p>

                            <strong>
                                        -{{ item.loss }}
                            </strong>

                        </div>

                    </section>


                    <section>

                        <h3>
                            Ameliyathaneler
                        </h3>

                        <div
                            v-for = "romm in reportData.resources.rooms"
                            :key = "room.name">

                            {{ room.name }}

                            <span>

                                {{ room.usage }} %

                            </span>

                        </div>

                    </section>


                    <section>

                        <h3>
                            Cerrahlar
                        </h3>

                        <div
                            v-for = "doctor in reportData.resources.surgeons"
                            :key = "doctor.name">

                            {{ doctor.name }}

                            <span>
                                    {{ doctor.usage }} %
                            </span>

                        </div>

                    </section>


                    <section>

                        <h3>
                            Anestezi Takımları
                        </h3>

                        <div
                            v-for = "team in reportData.resources.anesthesia"
                            :key= "team.name">
                        
                            {{ team.name }}

                            <span>
                                    {{ team.usage }}
                            </span>

                        </div>

                    </section>

                </div>

            </div>

        </Teleport>



        <!-- <v-dialog
            v-model="recentPlansDialog"
            max-width="420"
        >
            <div class="recent-plans-dialog">
                <div class="dialog-header">
                    <h2>Son 10 Plan</h2>

                    <button
                        type="button"
                        class="dialog-close-button"
                        aria-label="Pencereyi kapat"
                        @click="recentPlansDialog = false"
                    >
                        ×
                    </button>
                </div>

                <div
                    v-if="recentPlanPercentages.length"
                    class="recent-plan-list"
                >
                    <div
                        v-for="result in recentPlanPercentages"
                        :key="result.key"
                        class="recent-plan-row"
                        :class="{ selected: result.isSelected }"
                    >
                        <strong>
                            %{{ formatPercentage(result.percentage) }}
                        </strong>

                        <span
                            v-if="result.isSelected"
                            class="selected-marker"
                        >
                            <span class="selected-check">✓</span>
                            Seçili
                        </span>
                    </div>
                </div>

                <p v-else class="empty-result">
                    Simülasyon sonucu bulunamadı.
                </p>
            </div>
        </v-dialog> -->
    </main>
</template>

<style scoped>
.page {
    padding: 28px;
}

.page-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    margin-bottom: 20px;
}

.page-header h1 {
    margin: 0;
    color: #0f172a;
}

.recent-plans-button {
    padding: 10px 16px;
    border: 0;
    border-radius: 10px;
    background: #2563eb;
    color: #ffffff;
    font-size: 14px;
    font-weight: 700;
    cursor: pointer;
    transition:
        transform 0.18s ease,
        background 0.18s ease;
}

.recent-plans-button:hover {
    background: #1d4ed8;
    transform: translateY(-1px);
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
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 16px;
    margin-bottom: 24px;
}

.summary-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 14px;
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

.progress-heading {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
}

.progress-heading strong {
    color: #2563eb;
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

.day-card {
    margin-bottom: 30px;
    padding: 20px;
    background: white;
    border-radius: 14px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
}

.day-card h2 {
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 2px solid #e2e8f0;
    color: #0f172a;
}

.operation-card {
    display: grid;
    grid-template-columns: 120px 80px 220px 170px 100px 120px;
    align-items: center;
    margin-bottom: 12px;
    padding: 16px;
    background: #f8fafc;
    border-radius: 10px;
}

.time {
    color: #2563eb;
    font-weight: bold;
}

.patient {
    font-weight: bold;
}

.operation {
    color: #0f172a;
}

.dialog-overlay {
    position: fixed;
    inset: 0;
    z-index: 9999;

    display: flex;
    align-items: center;
    justify-content: center;

    padding: 20px;
    background: rgba(15, 23, 42, 0.55);
    backdrop-filter: blur(3px);
}

.recent-plans-dialog {
    width: 100%;
    max-width: 420px;
    max-height: calc(100vh - 40px);
    overflow-y: auto;

    padding: 22px;
    background: #ffffff;
    border-radius: 16px;
    box-shadow:
        0 20px 25px rgba(15, 23, 42, 0.15),
        0 8px 10px rgba(15, 23, 42, 0.08);
}

.dialog-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    margin-bottom: 18px;
}

.dialog-header h2 {
    margin: 0;
    color: #0f172a;
    font-size: 21px;
}

.dialog-close-button {
    display: grid;
    width: 34px;
    height: 34px;
    padding: 0;
    border: 0;
    border-radius: 9px;
    background: #f1f5f9;
    color: #475569;
    font-size: 24px;
    line-height: 1;
    place-items: center;
    cursor: pointer;
}

.dialog-close-button:hover {
    background: #e2e8f0;
    color: #0f172a;
}

.recent-plan-list {
    display: flex;
    flex-direction: column;
    gap: 9px;
}

.recent-plan-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    min-height: 48px;
    padding: 11px 14px;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    background: #f8fafc;
}

.recent-plan-row strong {
    color: #0f172a;
    font-size: 18px;
}

.recent-plan-row.selected {
    border-color: #14b8a6;
    background: #f0fdfa;
    box-shadow: 0 0 0 1px rgba(20, 184, 166, 0.1);
}

.selected-marker {
    display: flex;
    align-items: center;
    gap: 6px;
    color: #0f766e;
    font-size: 12px;
    font-weight: 700;
}

.selected-check {
    display: grid;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: #14b8a6;
    color: #ffffff;
    font-size: 13px;
    place-items: center;
}

.empty-result {
    margin: 0;
    padding: 18px;
    border-radius: 10px;
    background: #f8fafc;
    color: #64748b;
    text-align: center;
}

@media (max-width: 980px) {
    .summary-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .detail-table {
        display: block;
        overflow-x: auto;
    }
}

@media (max-width: 640px) {
    .page {
        padding: 18px;
    }

    .page-header {
        align-items: flex-start;
        flex-direction: column;
    }

    .summary-grid {
        grid-template-columns: 1fr;
    }
}
</style>
