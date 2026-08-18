<script setup>
import { computed, onMounted, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { getPlanDetail } from "../services/scheduleApi"

const route = useRoute()
const router = useRouter()

const plan = ref(null)
const loading = ref(false)
const errorMessage = ref("")

const showAllRoomIdle = ref(false)
const showAllSurgeonIdle = ref(false)

const days = [
    "Pazartesi",
    "Salı",
    "Çarşamba",
    "Perşembe",
    "Cuma",
]

// -----------------------------------------------------------------------------
// Plan yükleme
// -----------------------------------------------------------------------------

const loadPlanDetail = async () => {
    loading.value = true
    errorMessage.value = ""

    try {
        const response = await getPlanDetail(
            String(route.params.id),
        )

        plan.value = response.data

        console.log(
            "Simple plan detail:",
            plan.value,
        )

        console.log(
            "Simple score details:",
            plan.value?.score_details,
        )
    } catch (error) {
        console.error(error)

        errorMessage.value =
            "Plan detayı yüklenirken hata oluştu!"
    } finally {
        loading.value = false
    }
}

onMounted(loadPlanDetail)

// -----------------------------------------------------------------------------
// Score details
// -----------------------------------------------------------------------------

const scoreDetails = computed(() => {
    return plan.value?.score_details ?? {}
})

const priorityReport = computed(() => {
    return scoreDetails.value?.priority ?? {
        score: 0,
        details: [],
    }
})

const losses = computed(() => {
    return scoreDetails.value?.losses ?? {}
})

const dayBalance = computed(() => {
    return losses.value?.day_balance ?? {
        loss: 0,
        raw_value: 0,
        details: {
            daily_loads: [],
            min_load: 0,
            max_load: 0,
        },
    }
})

const anesthesiaBalance = computed(() => {
    return losses.value?.anesthesia_balance ?? {
        loss: 0,
        raw_value: 0,
        details: {
            team_loads: {},
            min_load: 0,
            max_load: 0,
        },
    }
})

const roomIdle = computed(() => {
    return losses.value?.room_idle ?? {
        loss: 0,
        raw_value: 0,
        details: [],
    }
})

const surgeonIdle = computed(() => {
    return losses.value?.surgeon_idle ?? {
        loss: 0,
        raw_value: 0,
        details: [],
    }
})

const roomIdleItems = computed(() => {
    return Array.isArray(roomIdle.value?.details)
        ? roomIdle.value.details
        : []
})

const surgeonIdleItems = computed(() => {
    return Array.isArray(surgeonIdle.value?.details)
        ? surgeonIdle.value.details
        : []
})

const dailyLoads = computed(() => {
    const loads =
        dayBalance.value?.details?.daily_loads ?? []

    return days.map((day, index) => ({
        day,
        load: Number(loads[index] ?? 0),
    }))
})

const anesthesiaLoads = computed(() => {
    const loads =
        anesthesiaBalance.value?.details?.team_loads ?? {}

    return Object.entries(loads).map(
        ([team, load]) => ({
            team,
            load: Number(load),
        }),
    )
})

const finalScore = computed(() => {
    return Number(
        scoreDetails.value?.final_score ??
        plan.value?.score ??
        0,
    )
})

const totalLoss = computed(() => {
    return Number(
        scoreDetails.value?.total_losses ?? 0,
    )
})

const scorePercent = computed(() => {
    return Number(
        scoreDetails.value?.success_rate ??
        plan.value?.success_rate ??
        0,
    )
})

const priorityOperationCount = computed(() => {
    return Array.isArray(
        priorityReport.value?.details,
    )
        ? priorityReport.value.details.length
        : 0
})

const priorityScore = computed(() => {
    return Number(
        priorityReport.value?.score ?? 0,
    )
})

const visibleRoomIdleItems = computed(() => {
    if (showAllRoomIdle.value) {
        return roomIdleItems.value
    }

    return roomIdleItems.value.slice(0, 5)
})

const visibleSurgeonIdleItems = computed(() => {
    if (showAllSurgeonIdle.value) {
        return surgeonIdleItems.value
    }

    return surgeonIdleItems.value.slice(0, 5)
})

const getDayName = (dayIndex) => {
    return (
        days[Number(dayIndex)] ??
        `Gün ${dayIndex}`
    )
}

const formatScore = (value) => {
    return new Intl.NumberFormat(
        "tr-TR",
    ).format(Number(value ?? 0))
}

const formatPercentage = (value) => {
    const numberValue = Number(value)

    if (!Number.isFinite(numberValue)) {
        return "0.0"
    }

    return numberValue.toFixed(1)
}

// -----------------------------------------------------------------------------
// Simple rapor mesajları
// -----------------------------------------------------------------------------

const dayBalanceSummary = computed(() => {
    const minLoad = Number(
        dayBalance.value?.details?.min_load ?? 0,
    )

    const maxLoad = Number(
        dayBalance.value?.details?.max_load ?? 0,
    )

    const rawValue = Number(
        dayBalance.value?.raw_value ?? 0,
    )

    const busiest = dailyLoads.value.find(
        (item) => item.load === maxLoad,
    )

    const quietest = dailyLoads.value.find(
        (item) => item.load === minLoad,
    )

    return {
        minLoad,
        maxLoad,
        rawValue,
        busiestDay: busiest?.day ?? "-",
        quietestDay: quietest?.day ?? "-",
    }
})

const anesthesiaSummary = computed(() => {
    const minLoad = Number(
        anesthesiaBalance.value?.details?.min_load ?? 0,
    )

    const maxLoad = Number(
        anesthesiaBalance.value?.details?.max_load ?? 0,
    )

    return {
        minLoad,
        maxLoad,
        difference: Number(
            anesthesiaBalance.value?.raw_value ?? 0,
        ),
    }
})

// -----------------------------------------------------------------------------
// Detaylı rapora geçiş
// -----------------------------------------------------------------------------

const openDetailedReport = () => {
    router.push({
        name: "plan-detail",
        params: {
            id:
                plan.value?.id ??
                route.params.id,
        },
    })
}

// -----------------------------------------------------------------------------
// Haftalık takvim
// -----------------------------------------------------------------------------

const selectedScheduleDay = ref(0)

const slots = []

for (let hour = 8; hour < 18; hour++) {
    const formattedHour = hour
        .toString()
        .padStart(2, "0")

    slots.push(`${formattedHour} : 00`)
    slots.push(`${formattedHour} : 30`)
}

const normalizeTime = (time) => {
    if (!time) return ""

    return String(time)
        .replace(/\s/g, "")
        .slice(0, 5)
}

const timeToMinutes = (time) => {
    const normalizedTime =
        normalizeTime(time)

    const [hour, minute] =
        normalizedTime
            .split(":")
            .map(Number)

    return hour * 60 + minute
}

const selectedDayOperations = computed(() => {
    if (!plan.value?.items) {
        return []
    }

    return plan.value.items.filter(
        (item) =>
            Number(item.day_index) ===
            Number(selectedScheduleDay.value),
    )
})

const planSlotRows = computed(() => {
    return slots.map((slot) => {
        const slotMinute =
            timeToMinutes(slot)

        const operation =
            selectedDayOperations.value.find(
                (item) => {
                    const startMinute =
                        timeToMinutes(
                            item.start_time,
                        )

                    const endMinute =
                        timeToMinutes(
                            item.end_time,
                        )

                    return (
                        slotMinute >=
                            startMinute &&
                        slotMinute <
                            endMinute
                    )
                },
            )

        return {
            slot,
            operation,
        }
    })
})

const getPlanDayCount = (dayIndex) => {
    if (!plan.value?.items) {
        return 0
    }

    return plan.value.items.filter(
        (item) =>
            Number(item.day_index) ===
            Number(dayIndex),
    ).length
}
</script>

<template>
    <main class="page">
        <div class="page-header">
            <div>
                <span class="page-kicker">
                    Plan değerlendirmesi
                </span>

                <h1>
                    Plan Özeti
                </h1>

                <p>
                    Planın temel performansını ve
                    puan kayıplarını hızlıca inceleyin.
                </p>
            </div>

            <button
                v-if="plan"
                type="button"
                class="detail-button"
                @click="openDetailedReport"
            >
                Ayrıntılı Raporu Gör
            </button>
        </div>

        <p
            v-if="loading"
            class="state-message"
        >
            Plan yükleniyor...
        </p>

        <p
            v-else-if="errorMessage"
            class="state-message error"
        >
            {{ errorMessage }}
        </p>

        <template v-else-if="plan">
            <!-- Skor akışı -->

            <section class="score-story">
                <div class="score-story-heading">
                    <div>
                        <span class="section-kicker">
                            Skor özeti
                        </span>

                        <h2>
                            Plan neden bu skoru aldı?
                        </h2>

                        <p>
                            Operasyonların öncelik puanı ile
                            soft constraint kayıplarının
                            final skora etkisi.
                        </p>
                    </div>

                    <span
                        class="feasible-badge"
                        :class="{
                            invalid:
                                !plan.is_feasible,
                        }"
                    >
                        {{
                            plan.is_feasible
                                ? "Geçerli plan"
                                : "Geçersiz plan"
                        }}
                    </span>
                </div>

                <div class="score-equation">
                    <article class="score-node positive">
                        <span>Öncelik puanı</span>

                        <strong>
                            +{{ formatScore(priorityScore) }}
                        </strong>

                        <small>
                            {{ priorityOperationCount }}
                            operasyonun toplam katkısı
                        </small>
                    </article>

                    <div class="equation-symbol">−</div>

                    <article class="score-node negative">
                        <span>Toplam kayıp</span>

                        <strong>
                            {{ formatScore(totalLoss) }}
                        </strong>

                        <small>
                            Soft constraint cezaları
                        </small>
                    </article>

                    <div class="equation-symbol">=</div>

                    <article class="score-node final">
                        <span>Final skor</span>

                        <strong>
                            {{ formatScore(finalScore) }}
                        </strong>

                        <small>
                            Başarı oranı:
                            %{{ formatPercentage(scorePercent) }}
                        </small>
                    </article>
                </div>

                <div class="loss-breakdown-grid">
                    <article class="loss-chip">
                        <span>Gün dengesi</span>
                        <strong>
                            -{{ formatScore(dayBalance.loss) }}
                        </strong>
                        <small>
                            {{ dayBalance.raw_value ?? 0 }} slot fark
                        </small>
                    </article>

                    <article class="loss-chip">
                        <span>Anestezi dengesi</span>
                        <strong>
                            -{{ formatScore(anesthesiaBalance.loss) }}
                        </strong>
                        <small>
                            {{ anesthesiaBalance.raw_value ?? 0 }} slot fark
                        </small>
                    </article>

                    <article class="loss-chip">
                        <span>Oda boşluğu</span>
                        <strong>
                            -{{ formatScore(roomIdle.loss) }}
                        </strong>
                        <small>
                            {{ roomIdle.raw_value ?? 0 }} boş slot
                        </small>
                    </article>

                    <article class="loss-chip">
                        <span>Cerrah boşluğu</span>
                        <strong>
                            -{{ formatScore(surgeonIdle.loss) }}
                        </strong>
                        <small>
                            {{ surgeonIdle.raw_value ?? 0 }} boş slot
                        </small>
                    </article>
                </div>
            </section>

            <!-- Simple rapor -->

            <section class="simple-report">
                <div class="section-heading">
                    <div>
                        <span class="section-kicker">
                            Basit rapor
                        </span>

                        <h2>
                            Kayıplar nerede oluştu?
                        </h2>

                        <p class="section-description">
                            Aşağıdaki açıklamalar doğrudan
                            kayıtlı score_details verisinden
                            üretilir.
                        </p>
                    </div>
                </div>

                <div class="report-grid">
                    <!-- Gün dengesi -->

                    <article class="report-card">
                        <div class="report-card-header">
                            <div>
                                <span class="report-icon">
                                    📅
                                </span>

                                <h3>
                                    Gün Dengesi
                                </h3>
                            </div>

                            <strong class="loss">
                                -{{
                                    formatScore(
                                        dayBalance.loss,
                                    )
                                }}
                            </strong>
                        </div>

                        <p>
                            En yoğun gün
                            <b>
                                {{
                                    dayBalanceSummary
                                        .busiestDay
                                }}
                            </b>
                            ve
                            {{
                                dayBalanceSummary
                                    .maxLoad
                            }}
                            slot yük taşıyor.
                        </p>

                        <p>
                            En sakin gün
                            <b>
                                {{
                                    dayBalanceSummary
                                        .quietestDay
                                }}
                            </b>
                            ve
                            {{
                                dayBalanceSummary
                                    .minLoad
                            }}
                            slot yük taşıyor.
                        </p>

                        <p class="report-conclusion">
                            Günler arasında
                            <b>
                                {{
                                    dayBalanceSummary
                                        .rawValue
                                }}
                                slot
                            </b>
                            fark oluştu. Bu nedenle
                            gün dengesi başlığında
                            <b>
                                {{
                                    formatScore(
                                        dayBalance.loss,
                                    )
                                }}
                                puan
                            </b>
                            kaybedildi.
                        </p>
                    </article>

                    <!-- Anestezi dengesi -->

                    <article class="report-card">
                        <div class="report-card-header">
                            <div>
                                <span class="report-icon">
                                    💉
                                </span>

                                <h3>
                                    Anestezi Dengesi
                                </h3>
                            </div>

                            <strong class="loss">
                                -{{
                                    formatScore(
                                        anesthesiaBalance.loss,
                                    )
                                }}
                            </strong>
                        </div>

                        <p>
                            En düşük takım yükü
                            <b>
                                {{
                                    anesthesiaSummary
                                        .minLoad
                                }}
                                slot
                            </b>,
                            en yüksek takım yükü ise
                            <b>
                                {{
                                    anesthesiaSummary
                                        .maxLoad
                                }}
                                slot
                            </b>.
                        </p>

                        <div
                            v-if="
                                anesthesiaLoads.length
                            "
                            class="compact-loads"
                        >
                            <span
                                v-for="item in anesthesiaLoads"
                                :key="item.team"
                            >
                                {{ item.team }}:
                                <b>{{ item.load }}</b>
                            </span>
                        </div>

                        <p class="report-conclusion">
                            Takımlar arasında
                            <b>
                                {{
                                    anesthesiaSummary
                                        .difference
                                }}
                                slot
                            </b>
                            fark oluştu. Bu nedenle
                            <b>
                                {{
                                    formatScore(
                                        anesthesiaBalance.loss,
                                    )
                                }}
                                puan
                            </b>
                            kaybedildi.
                        </p>
                    </article>
                </div>

                <!-- Oda boşlukları -->

                <article class="detail-report-card">
                    <div class="detail-report-header">
                        <div>
                            <span class="section-kicker">
                                Kaynak kullanımı
                            </span>

                            <h3>
                                Ameliyathane Boşlukları
                            </h3>

                            <p>
                                Operasyonlar arasında
                                oluşan oda boşlukları.
                            </p>
                        </div>

                        <div class="report-total">
                            <span>
                                Toplam ceza
                            </span>

                            <strong>
                                -{{
                                    formatScore(
                                        roomIdle.loss,
                                    )
                                }}
                            </strong>
                        </div>
                    </div>

                    <div
                        v-if="roomIdleItems.length"
                        class="message-list"
                    >
                        <div
                            v-for="(gap, index) in visibleRoomIdleItems"
                            :key="`room-${index}`"
                            class="report-message"
                        >
                            <div class="message-badge room">
                                {{ gap.room }}
                            </div>

                            <div>
                                <strong>
                                    {{
                                        getDayName(
                                            gap.day_index,
                                        )
                                    }}
                                </strong>

                                <p>
                                    <b>
                                        {{
                                            gap.from_patient
                                        }}
                                    </b>
                                    operasyonundan sonra
                                    <b>
                                        {{
                                            gap.to_patient
                                        }}
                                    </b>
                                    operasyonuna kadar
                                    <b>
                                        {{ gap.gap }} slot
                                    </b>
                                    ameliyathane boş
                                    kaldı.
                                </p>
                            </div>
                        </div>

                        <button
                            v-if="roomIdleItems.length > 5"
                            type="button"
                            class="show-more-button"
                            @click="
                                showAllRoomIdle =
                                    !showAllRoomIdle
                            "
                        >
                            {{
                                showAllRoomIdle
                                    ? "Daha az göster"
                                    : `+ ${
                                        roomIdleItems.length - 5
                                    } boşluk daha göster`
                            }}
                        </button>

                        <p class="section-total-note">
                            Toplam
                            <b>
                                {{
                                    roomIdle.raw_value ??
                                    0
                                }}
                                boş slot
                            </b>
                            nedeniyle oda boşluğu
                            başlığında
                            <b>
                                {{
                                    formatScore(
                                        roomIdle.loss,
                                    )
                                }}
                                puan
                            </b>
                            kaybedildi.
                        </p>
                    </div>

                    <p
                        v-else
                        class="empty-message"
                    >
                        Ameliyathaneler arasında
                        cezaya neden olan boşluk
                        bulunmuyor.
                    </p>
                </article>

                <!-- Cerrah boşlukları -->

                <article class="detail-report-card">
                    <div class="detail-report-header">
                        <div>
                            <span class="section-kicker">
                                Personel kullanımı
                            </span>

                            <h3>
                                Cerrah Boşlukları
                            </h3>

                            <p>
                                Aynı cerrahın operasyonları
                                arasında oluşan boşluklar.
                            </p>
                        </div>

                        <div class="report-total">
                            <span>
                                Toplam ceza
                            </span>

                            <strong>
                                -{{
                                    formatScore(
                                        surgeonIdle.loss,
                                    )
                                }}
                            </strong>
                        </div>
                    </div>

                    <div
                        v-if="surgeonIdleItems.length"
                        class="message-list"
                    >
                        <div
                            v-for="(gap, index) in visibleSurgeonIdleItems"
                            :key="`surgeon-${index}`"
                            class="report-message"
                        >
                            <div class="message-badge surgeon">
                                {{ gap.surgeon }}
                            </div>

                            <div>
                                <strong>
                                    {{
                                        getDayName(
                                            gap.day_index,
                                        )
                                    }}
                                </strong>

                                <p>
                                    <b>
                                        {{
                                            gap.from_patient
                                        }}
                                    </b>
                                    operasyonundan sonra
                                    <b>
                                        {{
                                            gap.to_patient
                                        }}
                                    </b>
                                    operasyonuna kadar
                                    <b>
                                        {{ gap.gap }} slot
                                    </b>
                                    boşluk oluştu.
                                </p>
                            </div>
                        </div>

                        <button
                            v-if="surgeonIdleItems.length > 5"
                            type="button"
                            class="show-more-button"
                            @click="
                                showAllSurgeonIdle =
                                    !showAllSurgeonIdle
                            "
                        >
                            {{
                                showAllSurgeonIdle
                                    ? "Daha az göster"
                                    : `+ ${
                                        surgeonIdleItems.length - 5
                                    } boşluk daha göster`
                            }}
                        </button>

                        <p class="section-total-note">
                            Toplam
                            <b>
                                {{
                                    surgeonIdle.raw_value ??
                                    0
                                }}
                                boş slot
                            </b>
                            nedeniyle cerrah boşluğu
                            başlığında
                            <b>
                                {{
                                    formatScore(
                                        surgeonIdle.loss,
                                    )
                                }}
                                puan
                            </b>
                            kaybedildi.
                        </p>
                    </div>

                    <p
                        v-else
                        class="empty-message"
                    >
                        Cerrah operasyonları arasında
                        cezaya neden olan boşluk
                        bulunmuyor.
                    </p>
                </article>
            </section>

            <!-- Haftalık çizelge -->

            <section class="weekly-calendar-card">
                <div class="weekly-calendar-header">
                    <div>
                        <span class="calendar-kicker">
                            Haftalık Ameliyat Takvimi
                        </span>

                        <h2>
                            {{
                                days[
                                    selectedScheduleDay
                                ]
                            }}
                        </h2>

                        <p>
                            Seçilen güne ait
                            operasyonların saat bazlı
                            dağılımı
                        </p>
                    </div>

                    <span class="operation-count">
                        {{
                            getPlanDayCount(
                                selectedScheduleDay,
                            )
                        }}
                        operasyon
                    </span>
                </div>

                <div class="day-tabs">
                    <button
                        v-for="(day, dayIndex) in days"
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
                                getPlanDayCount(
                                    dayIndex,
                                )
                            }}
                        </small>
                    </button>
                </div>

                <div class="plan-calendar-table-wrapper">
                    <table class="plan-calendar-table">
                        <thead>
                            <tr>
                                <th>Saat</th>
                                <th>Hasta</th>
                                <th>Operasyon</th>
                                <th>Doktor</th>
                                <th>Oda</th>
                                <th>Anestezi Ekibi</th>
                                <th>Durum</th>
                            </tr>
                        </thead>

                        <tbody>
                            <tr
                                v-for="row in planSlotRows"
                                :key="row.slot"
                                :class="{
                                    'calendar-filled':
                                        row.operation,
                                }"
                            >
                                <td class="calendar-time-cell">
                                    {{ row.slot }}
                                </td>

                                <template
                                    v-if="row.operation"
                                >
                                    <td>
                                        <strong>
                                            {{
                                                row
                                                    .operation
                                                    .patient
                                            }}
                                        </strong>
                                    </td>

                                    <td>
                                        {{
                                            row
                                                .operation
                                                .operation
                                        }}
                                    </td>

                                    <td>
                                        👨‍⚕️
                                        {{
                                            row
                                                .operation
                                                .surgeon
                                        }}
                                    </td>

                                    <td>
                                        🏥
                                        {{
                                            row
                                                .operation
                                                .room
                                        }}
                                    </td>

                                    <td>
                                        💉
                                        {{
                                            row
                                                .operation
                                                .anesthesia_team
                                        }}
                                    </td>

                                    <td>
                                        <span class="calendar-status">
                                            Planlandı
                                        </span>
                                    </td>
                                </template>

                                <template v-else>
                                    <td
                                        colspan="6"
                                        class="calendar-empty-cell"
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
.page {
    padding: 28px;
}

.page-header,
.score-story-heading,
.section-heading,
.weekly-calendar-header,
.detail-report-header {
    display: flex;
    justify-content: space-between;
    gap: 20px;
}

.page-header,
.score-story-heading,
.weekly-calendar-header {
    align-items: flex-start;
}

.page-header {
    margin-bottom: 24px;
}

.page-header h1,
.score-story-heading h2,
.section-heading h2,
.weekly-calendar-header h2,
.detail-report-header h3 {
    color: #0f172a;
}

.page-header h1 {
    margin: 4px 0 8px;
    font-size: 32px;
}

.page-header p,
.score-story-heading p,
.section-description,
.weekly-calendar-header p,
.detail-report-header p,
.report-card p,
.report-message p {
    color: #64748b;
    line-height: 1.6;
}

.page-header p,
.score-story-heading p,
.section-description,
.weekly-calendar-header p,
.detail-report-header p {
    margin: 0;
}

.page-kicker,
.section-kicker,
.calendar-kicker {
    display: block;
    color: #2563eb;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.detail-button {
    min-height: 44px;
    padding: 10px 18px;
    border: 0;
    border-radius: 11px;
    background: #1d4ed8;
    color: #fff;
    font-size: 14px;
    font-weight: 800;
    cursor: pointer;
}

.detail-button:hover {
    background: #1e40af;
}

.state-message {
    padding: 18px;
    border-radius: 12px;
    background: #f8fafc;
    color: #475569;
}

.state-message.error {
    color: #dc2626;
}

.feasible-badge {
    padding: 8px 12px;
    border: 1px solid #bbf7d0;
    border-radius: 999px;
    background: #f0fdf4;
    color: #15803d;
    font-size: 13px;
    font-weight: 800;
    white-space: nowrap;
}

.feasible-badge.invalid {
    border-color: #fecaca;
    background: #fff1f2;
    color: #dc2626;
}

/* Score story */

.score-story {
    margin-bottom: 28px;
    padding: 24px;
    border: 1px solid #dbeafe;
    border-radius: 20px;
    background: #fff;
    box-shadow: 0 12px 32px rgba(15, 23, 42, 0.06);
}

.score-story-heading {
    margin-bottom: 22px;
}

.score-story-heading h2 {
    margin: 4px 0 7px;
    font-size: 26px;
}

.score-equation {
    display: grid;
    grid-template-columns:
        minmax(0, 1fr)
        auto
        minmax(0, 1fr)
        auto
        minmax(0, 1fr);
    align-items: stretch;
    gap: 14px;
}

.score-node {
    display: flex;
    min-height: 132px;
    flex-direction: column;
    justify-content: center;
    padding: 20px;
    border-radius: 16px;
    text-align: center;
}

.score-node span {
    margin-bottom: 8px;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

.score-node strong {
    font-size: 30px;
}

.score-node small {
    margin-top: 7px;
    line-height: 1.5;
}

.score-node.positive {
    border: 1px solid #bbf7d0;
    background: #f0fdf4;
    color: #166534;
}

.score-node.negative {
    border: 1px solid #fecaca;
    background: #fff1f2;
    color: #b91c1c;
}

.score-node.final {
    border: 1px solid #bfdbfe;
    background: #eff6ff;
    color: #1d4ed8;
}

.equation-symbol {
    display: flex;
    align-items: center;
    justify-content: center;
    color: #64748b;
    font-size: 30px;
    font-weight: 900;
}

.loss-breakdown-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 12px;
    margin-top: 16px;
}

.loss-chip {
    display: flex;
    flex-direction: column;
    gap: 5px;
    padding: 14px;
    border: 1px solid #e2e8f0;
    border-radius: 13px;
    background: #f8fafc;
}

.loss-chip span {
    color: #475569;
    font-size: 12px;
    font-weight: 800;
}

.loss-chip strong {
    color: #dc2626;
    font-size: 18px;
}

.loss-chip small {
    color: #94a3b8;
}

/* Simple report */

.simple-report {
    display: flex;
    flex-direction: column;
    gap: 18px;
}

.section-heading {
    align-items: flex-end;
}

.section-heading h2 {
    margin: 4px 0 5px;
    font-size: 26px;
}

.report-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 18px;
}

.report-card,
.detail-report-card {
    padding: 22px;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    background: #fff;
    box-shadow: 0 10px 28px rgba(15, 23, 42, 0.05);
}

.report-card-header,
.detail-report-header {
    display: flex;
    justify-content: space-between;
    gap: 16px;
}

.report-card-header {
    align-items: center;
    margin-bottom: 17px;
}

.report-card-header > div {
    display: flex;
    align-items: center;
    gap: 10px;
}

.report-card-header h3,
.detail-report-header h3 {
    margin: 0;
}

.detail-report-header {
    align-items: flex-start;
    margin-bottom: 18px;
}

.detail-report-header h3 {
    margin-top: 4px;
}

.detail-report-header p {
    margin-top: 6px;
}

.report-icon {
    font-size: 20px;
}

.loss {
    color: #dc2626;
    font-size: 20px;
}

.report-conclusion {
    margin-top: 18px;
    padding-top: 14px;
    border-top: 1px solid #e2e8f0;
}

.compact-loads {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.compact-loads span {
    padding: 6px 9px;
    border-radius: 999px;
    background: #eff6ff;
    color: #475569;
    font-size: 12px;
}

.report-total {
    min-width: 130px;
    padding: 12px 15px;
    border-radius: 13px;
    background: #fff1f2;
    text-align: right;
}

.report-total span {
    display: block;
    margin-bottom: 4px;
    color: #64748b;
    font-size: 11px;
    font-weight: 700;
}

.report-total strong {
    color: #dc2626;
    font-size: 20px;
}

.message-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.report-message {
    display: grid;
    grid-template-columns: 150px minmax(0, 1fr);
    gap: 16px;
    padding: 15px;
    border: 1px solid #e2e8f0;
    border-radius: 13px;
    background: #f8fafc;
}

.report-message p {
    margin: 5px 0 0;
}

.message-badge {
    align-self: start;
    justify-self: start;
    padding: 6px 10px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 800;
}

.message-badge.room {
    background: #eff6ff;
    color: #1d4ed8;
}

.message-badge.surgeon {
    background: #f5f3ff;
    color: #6d28d9;
}

.show-more-button {
    align-self: flex-start;
    margin-top: 4px;
    padding: 8px 12px;
    border: 1px solid #cbd5e1;
    border-radius: 9px;
    background: #fff;
    color: #334155;
    font-weight: 800;
    cursor: pointer;
}

.show-more-button:hover {
    border-color: #93c5fd;
    background: #eff6ff;
    color: #1d4ed8;
}

.section-total-note {
    margin: 8px 0 0;
    padding: 15px;
    border-radius: 12px;
    background: #fff7ed;
    color: #9a3412;
    line-height: 1.6;
}

.empty-message {
    margin: 0;
    padding: 16px;
    border-radius: 12px;
    background: #f0fdf4;
    color: #15803d;
}

/* Weekly schedule */

.weekly-calendar-card {
    margin-top: 28px;
    padding: 24px;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    background: #fff;
    box-shadow: 0 10px 28px rgba(15, 23, 42, 0.08);
}

.weekly-calendar-header {
    align-items: center;
    margin-bottom: 20px;
}

.weekly-calendar-header h2 {
    margin: 5px 0 0;
    color: #172554;
    font-size: 24px;
}

.weekly-calendar-header p {
    margin-top: 5px;
    font-size: 14px;
}

.operation-count {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 100px;
    padding: 9px 14px;
    border-radius: 999px;
    background: #eff6ff;
    color: #1d4ed8;
    font-size: 13px;
    font-weight: 800;
}

.day-tabs {
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    gap: 10px;
    margin-bottom: 18px;
}

.day-tab {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    padding: 12px 14px;
    border: 1px solid #dbe3ef;
    border-radius: 11px;
    background: #f8fafc;
    color: #334155;
    font-weight: 700;
    cursor: pointer;
}

.day-tab:hover {
    border-color: #93c5fd;
    background: #eff6ff;
}

.day-tab.active {
    border-color: #2563eb;
    background: #2563eb;
    color: #fff;
}

.day-tab small {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 25px;
    height: 25px;
    border-radius: 50%;
    background: rgba(148, 163, 184, 0.18);
    font-size: 12px;
    font-weight: 800;
}

.day-tab.active small {
    background: rgba(255, 255, 255, 0.2);
}

.plan-calendar-table-wrapper {
    overflow-x: auto;
    border: 1px solid #e2e8f0;
    border-radius: 13px;
}

.plan-calendar-table {
    width: 100%;
    min-width: 900px;
    border-collapse: collapse;
}

.plan-calendar-table th {
    padding: 13px 14px;
    background: #f8fafc;
    color: #334155;
    font-size: 12px;
    font-weight: 800;
    text-align: left;
    text-transform: uppercase;
}

.plan-calendar-table td {
    height: 45px;
    padding: 9px 14px;
    border-top: 1px solid #e5edf5;
    color: #334155;
    font-size: 14px;
    text-align: left;
}

.calendar-time-cell {
    width: 90px;
    background: #fbfdff;
    color: #1e40af !important;
    font-weight: 800;
}

.calendar-filled {
    background: #f3e8ff;
}

.calendar-filled:hover {
    background: #ede9fe;
}

.calendar-empty-cell {
    height: 34px;
}

.calendar-status {
    display: inline-flex;
    align-items: center;
    padding: 5px 10px;
    border-radius: 999px;
    background: #e9d5ff;
    color: #6d28d9;
    font-size: 12px;
    font-weight: 800;
}

@media (max-width: 1000px) {
    .score-equation {
        grid-template-columns: 1fr;
    }

    .equation-symbol {
        min-height: 24px;
    }

    .loss-breakdown-grid,
    .report-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}

@media (max-width: 800px) {
    .weekly-calendar-header,
    .detail-report-header {
        align-items: flex-start;
        flex-direction: column;
    }

    .day-tabs,
    .report-grid {
        grid-template-columns: 1fr;
    }

    .report-message {
        grid-template-columns: 1fr;
    }

    .report-total {
        text-align: left;
    }
}

@media (max-width: 640px) {
    .page {
        padding: 18px;
    }

    .page-header,
    .score-story-heading,
    .section-heading {
        align-items: flex-start;
        flex-direction: column;
    }

    .loss-breakdown-grid {
        grid-template-columns: 1fr;
    }

    .detail-button {
        width: 100%;
    }
}
</style>
