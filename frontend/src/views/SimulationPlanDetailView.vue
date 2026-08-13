<script setup lang="ts">

import { computed, onMounted, ref } from "vue"
import { useRoute, useRouter } from "vue-router"

import { getSimulationPlanDetail } from "../services/scheduleApi"


const route = useRoute()
const router = useRouter()

const loading = ref(false)
const errorMessage = ref("")

const candidate = ref<any>(null)

const selectedScheduleDay = ref(0)

const DAYS = [
    "Pazartesi",
    "Salı",
    "Çarşamba",
    "Perşembe",
    "Cuma",
]


const slots: string[] = []

for (let hour = 8; hour < 18; hour++) {

    const formattedHour = hour
        .toString()
        .padStart(2, "0")

    slots.push(`${formattedHour}:00`)
    slots.push(`${formattedHour}:30`)
}


const normalizeTime = (time: string) => {

    if (!time) return ""

    return String(time)
        .replace(/\s/g, "")
        .slice(0, 5)

}


const timeToMinutes = (time: string) => {

    const normalized = normalizeTime(time)

    if (!normalized.includes(":")) {
        return 0
    }

    const parts = normalized.split(":")

    const hour = Number(parts[0] ?? 0)
    const minute = Number(parts[1] ?? 0)

    return hour * 60 + minute
}


const loadCandidate = async () => {

    loading.value = true
    errorMessage.value = ""

    try {

        const planId = String(route.params.id)

        const simulationIndex = Number(
            route.params.simulationIndex
        )

        const response =
            await getSimulationPlanDetail(
                planId,
                simulationIndex,
            )

        candidate.value = response.data

        console.log(
            "Candidate plan:",
            response.data
        )

    } catch (error: any) {

        console.error(
            "Aday plan yükleme hatası:",
            error.response?.data ?? error,
        )

        errorMessage.value =
            error.response?.data?.error ??
            "Aday plan yüklenemedi."

    } finally {

        loading.value = false

    }

}


const candidateItems = computed(() => {

    return candidate.value?.items ?? []

})


const selectedDayOperations = computed(() => {

    return candidateItems.value.filter(
        (item: any) =>
            Number(item.day_index) ===
            Number(selectedScheduleDay.value),
    )

})


const getDayCount = (dayIndex: number) => {

    return candidateItems.value.filter(
        (item: any) =>
            Number(item.day_index) ===
            Number(dayIndex),
    ).length

}


const planSlotRows = computed(() => {

    return slots.map((slot) => {

        const slotMinute =
            timeToMinutes(slot)

        const operation =
            selectedDayOperations.value.find(
                (item: any) => {

                    const startMinute =
                        timeToMinutes(
                            item.start_time,
                        )

                    const endMinute =
                        timeToMinutes(
                            item.end_time,
                        )

                    return (
                        slotMinute >= startMinute &&
                        slotMinute < endMinute
                    )
                },
            )

        return {
            slot,
            operation,
        }

    })

})


const goBack = () => {

    router.push({
        name: "plan-detail",
        params: {
            id: route.params.id,
        },
    })

}


const scoreDetails = computed (() => {

    return candidate.value?.score_details ?? {}

})


const losses = computed (() =>  {

    return scoreDetails.value?.losses ?? {}

})






onMounted(() => {

    loadCandidate()

})

</script>


<template>

    <main class="candidate-page">

        <div class="candidate-header">

            <div>

                <button
                    type="button"
                    class="back-button"
                    @click="goBack"
                >
                    ← Plan detayına dön
                </button>

                <span class="page-kicker">
                    Simülasyon sonucu
                </span>

                <h1>
                    Aday Plan
                    #{{ candidate?.valid_index }}
                </h1>

                <p>
                    Bu plan aynı simülasyon
                    çalışmasında değerlendirilen
                    aday çözümlerden biridir.
                </p>

            </div>

            <div
                v-if="candidate"
                class="candidate-status"
                :class="{
                    best:
                        candidate.is_best,
                }"
            >

                {{
                    candidate.is_best
                        ? "★ Seçilen Plan"
                        : "Değerlendirildi"
                }}

            </div>

        </div>


        <p
            v-if="loading"
            class="state-message"
        >
            Aday plan yükleniyor...
        </p>


        <p
            v-else-if="errorMessage"
            class="state-message error"
        >
            {{ errorMessage }}
        </p>


        <template v-else-if="candidate">

            <section class="summary-grid">

                <article class="summary-card">

                    <span>
                        Aday No
                    </span>

                    <strong>
                        {{ candidate.valid_index }}
                    </strong>

                </article>


                <article class="summary-card">

                    <span>
                        Deneme
                    </span>

                    <strong>
                        {{ candidate.attempt }}
                    </strong>

                </article>


                <article class="summary-card">

                    <span>
                        Skor
                    </span>

                    <strong>
                        {{ candidate.score }}
                    </strong>

                </article>


                <article class="summary-card">

                    <span>
                        Operasyon
                    </span>

                    <strong>
                        {{ candidateItems.length }}
                    </strong>

                </article>

            </section>

<!-- 
            10 plan detyı ------------------------------------------- -->


            <section class = "analysis-card">

                <div class = "analysis-header">

                    <div>

                        <span class = "page-kicker">
                            Plan değerlendirmesi
                        </span>

                        <h2>
                            Skor kırılımı
                        </h2>

                    </div>


                    <span
                        v-if = "candidate.is_best"
                        class = "best-badge">
                            ★ Seçilen Plan                       
                    </span>

                </div>


                <div class = "analysis-grid">

                    <article class = "analysis-item">

                        <span>
                            Güç dengesi
                        </span>


                        <strong>
                            {{ losses.day_balance?.loss ?? 0 }}
                        </strong>

                    </article>


                    <article class = "analysis-item" >

                        <span>
                            Anestezi dengesi
                        </span>

                        <strong>
                            {{ losses.anesthesia_balance?.loss ?? 0 }}
                        </strong>

                    </article>


                    <article class = "analysis-item">

                        <span>
                            Oda boşluğu
                        </span>

                        <strong>
                            {{ losses.room_idle?.loss ?? 0 }}
                        </strong>

                    </article>


                    <article class = "analysis-item">

                        <span>
                            Doktor dengesi
                        </span>

                        <strong>
                            {{ losses.surgeon_idle?.loss ?? 0 }}
                        </strong>

                    </article>

                </div>

            </section>

<!-- 
             ------------------------------------------- 10 plan detyı-->

            
             <article class = "summary-card" >

                <span>
                    Başarı oranı
                </span>

                <strong>
                    %{{ candidate.success_rate }}
                </strong>

             </article>






            <section class="weekly-calendar-card">

                <div class="weekly-calendar-header">

                    <div>

                        <span class="calendar-kicker">
                            Haftalık ameliyat takvimi
                        </span>

                        <h2>
                            {{
                                DAYS[
                                    selectedScheduleDay
                                ]
                            }}
                        </h2>

                        <p>
                            Aday planın seçilen güne
                            ait operasyon dağılımı
                        </p>

                    </div>

                    <span class="operation-count">

                        {{
                            getDayCount(
                                selectedScheduleDay
                            )
                        }}

                        operasyon

                    </span>

                </div>


                <div class="day-tabs">

                    <button
                        v-for="(day, dayIndex) in DAYS"
                        :key="day"
                        type="button"
                        class="day-tab"
                        :class="{
                            active:
                                selectedScheduleDay ===
                                dayIndex,
                        }"
                        @click="
                            selectedScheduleDay =
                                dayIndex
                        "
                    >

                        <span>
                            {{ day }}
                        </span>

                        <small>
                            {{
                                getDayCount(
                                    dayIndex
                                )
                            }}
                        </small>

                    </button>

                </div>


                <div class="calendar-wrapper">

                    <table class="calendar-table">

                        <thead>

                            <tr>

                                <th>Saat</th>
                                <th>Hasta</th>
                                <th>Operasyon</th>
                                <th>Doktor</th>
                                <th>Oda</th>
                                <th>Anestezi</th>

                            </tr>

                        </thead>


                        <tbody>

                            <tr
                                v-for="row in planSlotRows"
                                :key="row.slot"
                                :class="{
                                    filled:
                                        row.operation,
                                }"
                            >

                                <td class="time-cell">
                                    {{ row.slot }}
                                </td>


                                <template
                                    v-if="row.operation"
                                >

                                    <td>
                                        <strong>
                                            {{
                                                row.operation
                                                    .patient
                                            }}
                                        </strong>
                                    </td>

                                    <td>
                                        {{
                                            row.operation
                                                .operation
                                        }}
                                    </td>

                                    <td>
                                        {{
                                            row.operation
                                                .surgeon
                                        }}
                                    </td>

                                    <td>
                                        {{
                                            row.operation
                                                .room
                                        }}
                                    </td>

                                    <td>
                                        {{
                                            row.operation
                                                .anesthesia_team
                                        }}
                                    </td>

                                </template>


                                <template v-else>

                                    <td
                                        colspan="5"
                                        class="empty-slot"
                                    ></td>

                                </template>

                            </tr>

                        </tbody>

                    </table>

                </div>

            </section>

        </template>

    </main>

</template>


<style scoped>

.candidate-page {
    display: flex;
    flex-direction: column;
    gap: 24px;
}

.candidate-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 20px;
}

.back-button {
    margin-bottom: 14px;
    padding: 0;
    border: 0;
    background: transparent;
    color: #2563eb;
    font-size: 14px;
    font-weight: 700;
    cursor: pointer;
}

.page-kicker,
.calendar-kicker {
    display: block;
    color: #2563eb;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.candidate-header h1 {
    margin: 5px 0 7px;
    color: #0f172a;
}

.candidate-header p {
    margin: 0;
    color: #64748b;
}

.candidate-status {
    padding: 9px 14px;
    border-radius: 999px;
    background: #f1f5f9;
    color: #475569;
    font-size: 13px;
    font-weight: 800;
}

.candidate-status.best {
    background: #f0fdf4;
    color: #15803d;
}

.summary-grid {
    display: grid;
    grid-template-columns:
        repeat(4, minmax(0, 1fr));
    gap: 14px;
}

.summary-card {
    display: flex;
    min-height: 110px;
    flex-direction: column;
    justify-content: space-between;
    padding: 18px;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    background: #ffffff;
    box-shadow:
        0 8px 24px
        rgba(15, 23, 42, 0.05);
}

.summary-card span {
    color: #64748b;
    font-size: 13px;
    font-weight: 700;
}

.summary-card strong {
    color: #0f172a;
    font-size: 26px;
}

.weekly-calendar-card {
    padding: 24px;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    background: #ffffff;
    box-shadow:
        0 10px 28px
        rgba(15, 23, 42, 0.07);
}

.weekly-calendar-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
    margin-bottom: 20px;
}

.weekly-calendar-header h2 {
    margin: 5px 0;
    color: #172554;
}

.weekly-calendar-header p {
    margin: 0;
    color: #64748b;
    font-size: 14px;
}

.operation-count {
    padding: 8px 13px;
    border-radius: 999px;
    background: #eff6ff;
    color: #1d4ed8;
    font-size: 13px;
    font-weight: 800;
}

.day-tabs {
    display: grid;
    grid-template-columns:
        repeat(5, minmax(0, 1fr));
    gap: 10px;
    margin-bottom: 18px;
}

.day-tab {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
    padding: 11px 13px;
    border: 1px solid #dbe3ef;
    border-radius: 10px;
    background: #f8fafc;
    color: #334155;
    font-weight: 700;
    cursor: pointer;
}

.day-tab.active {
    border-color: #2563eb;
    background: #2563eb;
    color: white;
}

.day-tab small {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 24px;
    height: 24px;
    border-radius: 50%;
    background:
        rgba(148, 163, 184, 0.18);
}

.day-tab.active small {
    background:
        rgba(255, 255, 255, 0.2);
}

.calendar-wrapper {
    overflow-x: auto;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
}

.calendar-table {
    width: 100%;
    min-width: 850px;
    border-collapse: collapse;
}

.calendar-table th {
    padding: 12px 14px;
    background: #f8fafc;
    color: #475569;
    font-size: 12px;
    font-weight: 800;
    text-align: left;
    text-transform: uppercase;
}

.calendar-table td {
    height: 44px;
    padding: 9px 14px;
    border-top: 1px solid #e5edf5;
    color: #334155;
    font-size: 14px;
}

.calendar-table tr.filled {
    background: #f5f3ff;
}

.time-cell {
    width: 85px;
    background: #fbfdff;
    color: #1e40af !important;
    font-weight: 800;
}

.empty-slot {
    height: 38px;
}

.state-message {
    padding: 16px;
    border-radius: 12px;
    background: #f8fafc;
    color: #475569;
}

.state-message.error {
    background: #fff1f2;
    color: #be123c;
}

@media (max-width: 900px) {

    .summary-grid {
        grid-template-columns:
            repeat(2, minmax(0, 1fr));
    }

    .day-tabs {
        grid-template-columns:
            1fr;
    }

}

</style>