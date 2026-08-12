<script setup>
import { computed, onMounted, ref } from "vue"
import { useRoute, useRouter, } from "vue-router"
import { getPlanDetail } from "../services/scheduleApi"


import { jsPDF } from "jspdf"
import { autoTable } from "jspdf-autotable"


const route = useRoute()
const router = useRouter()

const plan = ref(null)
const errorMessage = ref("")
const loading = ref(false)
const recentPlansDialog = ref(false)


const exportingPdf = ref(false)







const days = [
        "Pazartesi",
        "Salı",
        "Çarşamba",
        "Perşembe",
        "Cuma",
    ]

// takvim görünümü -----------------------------------------------

const selectedScheduleDay = ref(0)


const slots = []


for (let hour = 8; hour < 18; hour ++) {

    const formattedHour = hour
            .toString()
            .padStart (2, "0")

    slots.push(`${formattedHour} : 00`)
    slots.push(`${formattedHour} : 30`)

}

const normalizeTime = (time) => {

    if (!time) return ""

    return String (time)

        .replace(/\s/g, "")
        .slice(0, 5)

}


const timeToMinutes = (time) => {

    const normalizedTime = normalizeTime(time)

    const [hour, minute] = normalizedTime
            .split (":")
            .map (Number)

    return hour * 60 + minute

}

// seçilen günün operasyonları -------------------------------

const selectedDayOperations = computed(() => {

    if (!plan.value?.items) {

        return []

    }

    return plan.value.items.filter (

        (item) => 
                Number(item.day_index) === 
                Number(selectedScheduleDay.value),

    )

})

//  -------------------------------  seçilen günün operasyonları

// Slot satırları--------------------------------------------------

const planSlotRows = computed(() => {

    return slots.map((slot) => {

        const slotMinute = timeToMinutes(slot)

        const operation = selectedDayOperations.value.find(

            (item) => {

                const startMinute = timeToMinutes(

                    item.start_time,

                )

                const endMinute = timeToMinutes(

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

// --------------------------------------------------Slot satırları

// Gün başına operasyon sayısı -----------------------------------------

const getPlanDayCount = (dayIndex) => {

    if (!plan.value?.items) {

        return 0

    }


    return plan.value.items.filter(

        (item) => 
                Number(item.day_index) ===
                Number(dayIndex)

    ).length

}

// ----------------------------------------- Gün başına operasyon sayısı



//  -----------------------------------------------  takvim görünümü


const groupedSchedule = computed(() => {
    if (!plan.value?.items) return []

    

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
            "SIMULATION RESULTS:",
            plan.value?.simulation_results
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
        return Math.min(100, Math.max(0, Number(result.score) / 1800 ))
    }

    return 0
}




    

const recentPlanPercentages = computed(() => {

    const results =
        plan.value?.simulation_results ?? []

    if (!results.length) {
        return []
    }

    return results.slice(0, 10).map((result, index) => {

        return {

            key:
                result.valid_index ??
                result.attempt ??
                index,

            valid_index:
                result.valid_index,

            success_rate:
                Number( result.success_rate ?? 0),

            isSelected:
                result.is_best === true,

        }

    })

})






const formatPercentage = (percentage) => {
    const value = Number(percentage)

    if (!Number.isFinite(value)) return "0.0"

    return value.toFixed(1)
}


// raporlama --------------------------------------------- 



// Rapor ekranı --------------------------------------------------------------


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

const priorityItems = computed(() => {
    return Array.isArray(priorityReport.value?.details)
        ? priorityReport.value.details
        : []
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
    const loads = dayBalance.value?.details?.daily_loads ?? []

    return days.map((day, index) => ({
        day,
        load: Number(loads[index] ?? 0),
    }))
})

const anesthesiaLoads = computed(() => {
    const loads =
        anesthesiaBalance.value?.details?.team_loads ?? {}

    return Object.entries(loads).map(([team, load]) => ({
        team,
        load: Number(load),
    }))
})

const totalLoss = computed(() => {
    return Number(scoreDetails.value?.total_losses ?? 0)
})

const finalScore = computed(() => {
    return Number(
        scoreDetails.value?.final_score ??
        plan.value?.score ??
        0,
    )
})

const getDayName = (dayIndex) => {
    return days[dayIndex] ?? `Gün ${dayIndex}`
}

const formatScore = (value) => {
    return new Intl.NumberFormat("tr-TR").format(
        Number(value ?? 0),
    )
}



// --------------------------------------------------------- rapor ekranı 

// export --------------------------------------------------------------


const getRawValue = (report) => {

    return Number(

        report?.raw_value ??
        report?.["raw_value"] ??
// ------------        report?.["raw value"] ??
// ----------       
        
        0,

    )

}



const formatPdfDate =  (value) =>{

    if(!value) return "-"

    const date = new Date(value)

    if (Number.isNaN(date.getTime())) {

        return String(value)

    }

    return new Intl.DateTimeFormat("tr-TR", {
        
        dateStyle: "long",

        timeStyle: "short",

    }).format(date)

}


const normalizePdfText = (value) => {

    if (value === undefined || value === null) {

    }

    return String(value) 

        .replaceAll("ı", "i")
        .replaceAll("İ", "I")
        .replaceAll("ş", "s")
        .replaceAll("Ş", "S")
        .replaceAll("ğ", "g")
        .replaceAll("Ğ", "G")
        .replaceAll("ü", "u")
        .replaceAll("Ü", "u")
        .replaceAll("ö", "o")
        .replaceAll("Ö", "O")
        .replaceAll("ç", "c")
        .replaceAll("Ç", "C")    

}


const createPdfFileName = () => {

    const planId = String(plan.value?.id ?? "plan")
        .slice(0,8)

    
    return `ameliyat-planı-raporu-${planId}.pdf`


}


const addPdfSectionTitle = (doc, title, y) => {

    const pageHeight = doc.internal.pageSize.getHeight()

    if (y > pageHeight - 25 ){

        doc.addPage()
        y = 20

    }


    doc.setFontSize(14)
    doc.setFont("helvetica", "bold")
    doc.text(normalizePdfText(title), 14, y)


    doc.setDrawColor( 210, 220, 235)
    doc.line ( 14, y + 3 , 196, y + 3 )

    return y + 10

}


// sayfa numarası -----------------------------------------------


const addPdfPageNumbers = (doc) => {

    const pageCount = doc.getNumberOfPages()

    for ( let pageNumber = 1; pageNumber <= pageCount; pageNumber++ ) {

        doc.setPage(pageNumber)


        const pageWidth = doc.internal.pageSize.getWidth()
        const pageHeight = doc.internal.pageSize.getHeight()


        doc.setFontSize(8)
        doc.setTextColor (120, 130, 145)

        doc.text(

            `${pageNumber} / ${pageCount}`,
            pageWidth - 14,
            pageHeight - 8, 

            {
                align : "right",
            },

        )

        doc.text (

            "Hospital Scheduler",
            14,
            pageHeight - 8,

        )

    }


    doc.setTextColor(0,0,0)


}



//  ----------------------------------------------- sayfa numarası




const exportPlanPdf = async () => {

    if(!plan.value || exportingPdf.value) {

        return

    }   


    exportingPdf.value = true

    try {

        const doc = new jsPDF({

            orientation: "portrait",
            unit : "mm",
            format : "a4",

        })

        const tableTheme = {

            styles : {

                font : "helvetica",
                FontSize : 8,
                cellPadding: 2.6,
                overflow : "linebreak",
                valign : "middle",

            },

            headStyles : {

                fillColor : [30, 64, 175],
                textColor : [255,255,255],
                fontStyle : "bold",

            },

            alternateRowStyles : {

                fllColor : [240, 250, 252,],    

            },

            margin : {

                left : 14,
                right : 14,
            },

        }


        // pdf başlığı


        doc.setFillColor (15, 23, 42)
        doc.rect( 0, 0, 210, 42, "F")

        doc.setTextColor (255, 255, 255)
        doc.setFont ("helvetica", "bold")
        doc.setFontSize(20)

        doc.text(
            "Hospital Scheduler",
            14,
            17,
        )


        doc.setFontSize(12)
        doc.setFont("helvetica", "normal")

        doc.text ( 
            "Haftalik Ameliyat Plan Raporu",
            14,
            27,
        )

        doc.setFontSize(8)


        doc.text(
            `Olusturulma: ${normalizePdfText(
                formatPdfDate(plan.value.created_at),
            )}`,
            14,
            35,
        )

        doc.setTextColor( 15, 23, 42 )

        // plan bilgileri 

        let currentY = 52

        currentY = addPdfSectionTitle(

            doc,
            "Plan Bilgileri",
            currentY,

        )


        autoTable( doc, {

            ...tableTheme,
            startY : currentY,
            theme : "grid",


            head : [[

                "Alan",
                "Deger",

            ]],


            body : [
                [
                    "Plan ID",
                    normalizePdfText(plan.value.id),
                ],

                [
                    "Algoritma",
                    normalizePdfText(plan.value.algorithm_name),
                ],

                [
                    "Durum",
                    plan.value.is_feasible
                                ? "Geçerli plan"
                                : "Geçersiz plan",
                ],

                [
                    "Olusturma tarihi",
                    normalizePdfText(
                                    formatPdfDate(plan.value.created_at),
                    )
                ],
            ],


            columnStyles : {

                0: {
                    cellWidth : 55,
                    fontStyle : "bold",
                },

            },

        })

        currentY = doc.lastAutoTable.finalY + 10


        // Genel PErformans


        currentY =  addPdfSectionTitle (

            doc,
            "Genel Performans",
            currentY,

        )


        autoTable ( doc, {

            ...tableTheme,
            startY : currentY,
            theme : "grid",


            head : [
                [
                    "Metrik",
                    "Deger",
                    "Aciklama",
                ]
            ],


            body : [
                [
                    "Final Skor",
                    formatScore(finalScore.value),
                    "Öncelik puani eksi toplam kayip"
                ],

                [
                    "Öncelik Puani",
                    formatScore(priorityReport.value.score),
                    `${priorityItems.value.length} operasyon`,
                ],

                [
                    "Toplam Kayip",
                    `-${formatScore(totalLoss.value)}`,
                    "Soft constrait cezalari",
                ],

                [
                    "Basari Orani",
                    `%${formatPercentage(scorePercent.value)}`,
                    "Plan performans göstergesi",
                ],
            ],

        })


        currentY = doc.lastAutoTable.finalY + 10


        // Soft Constrait Özeti



        currentY = addPdfSectionTitle(

            doc,
            "Soft Constrait Ozeti",
            currentY,

        )

        autoTable ( doc, {

            ...tableTheme,
            startY : currentY,
            theme : "grid",


            head : [
                [
                    "Constrait",
                    "Ham Deger",
                    "Puan kaybi",
                ]
            ],


            body : [
                [
                    "Gun dengesi",
                    `${getRawValue(dayBalance.value)} slot`,
                    `-${formatScore(dayBalance.value.loss)}`,

                ],

                [
                    "Anestezi dengesi",
                    `${getRawValue(anesthesiaBalance.value)} slot`,
                    `-${formatScore(anesthesiaBalance.value.loss)}`,

                ],

                [
                    "Oda bosluklari",
                    `${getRawValue(roomIdle.value)} slot`,
                    `-${formatScore(roomIdle.value.loss)}`,
                ],

                [
                    "Cerrah bosluklari",
                    `${getRawValue(surgeonIdle.value)} slot`,
                    `-${formatScore(surgeonIdle.value.loss)}`,

                ],

            ],

        })

        currentY = doc.lastAutoTable.finalY + 10


        // Gün YÜkleri


        currentY = addPdfSectionTitle(

            doc,
            "Gun Yukleri",
            currentY,

        )


        autoTable ( doc, {

            ...tableTheme,
            startY : currentY,
            theme : "striped",


            head : [
                [
                    "Gun",
                    "Toplam yuk",
                ]
            ],

            body : dailyLoads.value.map((item) => [

                normalizePdfText(item.day),
                `${item.load} slot`,

            ]),

        })


        currentY = doc.lastAutoTable.finalY + 10,



        // Anestezi Yükleri


        currentY = addPdfSectionTitle(
            doc,
            "Anestezi Takim Yükleri",
            currentY,
        )


        autoTable ( doc, {

            ...tableTheme,
            startY : currentY,
            theme : "striped",



            head : [
                [
                    "Takim",
                    "Toplam Yuk",
                ]
            ],


            body : anesthesiaLoads.value.map((item) => [

                normalizePdfText(item.team),
                `${item.load} slot`,

            ]),

        })



        // Oda Boşlukları


        doc.addPage()

        currentY = addPdfSectionTitle(
            doc,
            "Oda Bosluklari",
            20,
        )


        autoTable(doc, {

            ...tableTheme,
            startY : currentY,
            theme : "striped",


            head : [
                [
                    "Gun",
                    "Oda",
                    "Onceki hasta",
                    "Sonraki hasta",
                    "Bosluk",
                ]
            ],


            body : roomIdleItems.value.length
                ? roomIdleItems.value.map((gap) => [

                    normalizePdfText(
                        getDayName(gap.day_index),
                    ),

                    normalizePdfText(gap.room),
                    normalizePdfText(gap.from_patient),
                    normalizePdfText(gap.to_patient),
                    `${gap.gap} slot`,
                ])
                :
                [
                    [
                        "Oda boslugu bulunmuyor",
                        "",
                        "",
                        "",
                        "",
                    ]
                ],

        })


        // cerrah boslukları


        currentY = doc.lastAutoTable.finalY + 10


        currentY = addPdfSectionTitle(

            doc,
            "Cerrah Bosluklari",
            currentY,

        )

        autoTable( doc, {

                ...tableTheme,
                startY : currentY,
                theme : "striped",


                head : [
                    [
                        "Gun",
                        "Cerrah",
                        "Onceki hasta",
                        "Sonraki hasta",
                        "Bosluk",
                    ]
                ],

                body : surgeonIdleItems.value.length
                    ? surgeonIdleItems.value.map((gap) => [

                        normalizePdfText(
                            getDayName(gap.day_index),
                        ),

                        normalizePdfText(gap.surgeon),
                        normalizePdfText(gap.from_patient),
                        normalizePdfText(gap.to_patient),
                        `${gap.gap} slot`,

                    ])
                    :
                    [
                        [
                            "Cerrah boslugu  bulunmuyor",
                            "",
                            "",
                            "",
                            "",
                        ]
                    ],

        }),


         /*
         * ÖNCELİK RAPORU
         */

        doc.addPage()

        currentY = addPdfSectionTitle(
            doc,
            "Operasyon Oncelik Puanlari",
            20,
        )

        autoTable(doc, {
            ...tableTheme,
            startY: currentY,
            theme: "striped",

            head: [[
                "Hasta",
                "Operasyon",
                "Oncelik",
                "Gun",
                "Baslangic",
                "Puan",
            ]],

            body: priorityItems.value.map((item) => [
                normalizePdfText(item.patient),
                normalizePdfText(item.operation),
                normalizePdfText(item.priority),
                normalizePdfText(
                    getDayName(item.day_index),
                ),
                String(item.start_slot ?? "-"),
                formatScore(item.score),
            ]),

            columnStyles: {
                0: {
                    cellWidth: 18,
                },
                1: {
                    cellWidth: 50,
                },
                2: {
                    cellWidth: 24,
                },
                3: {
                    cellWidth: 25,
                },
                4: {
                    cellWidth: 22,
                },
                5: {
                    cellWidth: 24,
                    halign: "right",
                },
            },
        })

        /*
         * HAFTALIK AMELİYAT PLANI
         */

        doc.addPage()

        currentY = addPdfSectionTitle(
            doc,
            "Haftalik Ameliyat Plani",
            20,
        )

        autoTable(doc, {
            ...tableTheme,
            startY: currentY,
            theme: "striped",

            head: [[
                "Gun",
                "Saat",
                "Hasta",
                "Operasyon",
                "Cerrah",
                "Oda",
                "Anestezi",
            ]],

            body: Array.isArray(plan.value.items)
                ? plan.value.items.map((item) => [
                    normalizePdfText(
                        getDayName(item.day_index),
                    ),
                    `${normalizePdfText(item.start_time)} - ${normalizePdfText(
                        item.end_time,
                    )}`,
                    normalizePdfText(item.patient),
                    normalizePdfText(item.operation),
                    normalizePdfText(item.surgeon),
                    normalizePdfText(item.room),
                    normalizePdfText(item.anesthesia_team),
                ])
                : [],

            styles: {
                ...tableTheme.styles,
                fontSize: 7,
            },

            columnStyles: {
                0: {
                    cellWidth: 22,
                },
                1: {
                    cellWidth: 27,
                },
                2: {
                    cellWidth: 15,
                },
                3: {
                    cellWidth: 43,
                },
                4: {
                    cellWidth: 30,
                },
                5: {
                    cellWidth: 17,
                },
                6: {
                    cellWidth: 25,
                },
            },
        })

        addPdfPageNumbers(doc)

        doc.save(createPdfFileName())
    } catch (error) {
        console.error("PDF export error:", error)
        errorMessage.value =
            "PDF oluşturulurken bir hata oluştu."
    } finally {
        exportingPdf.value = false
    }
}




//  -------------------------------------------------------------- export




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

// 10 plan detail view -------------------------------------------

const openSimulationPlan = (result) => {

    recentPlansDialog.value = false

    router.push  (
        {
            name : "simulation-plan-detail",
            params : {

                id : plan.value.id,
                simulationIndex : 
                        result.valid_index,

            },
        }
    )

}



//  ------------------------------------------  10 plan detail view


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
                
                <p></p>


                    <button
                        type="button"
                        class="export-button"
                        :disabled="!plan || loading || exportingPdf"
                        @click="exportPlanPdf"
                    >
                        <span class="export-icon">
                            ↓
                        </span>

                        {{
                            exportingPdf
                                ? "PDF Hazırlanıyor..."
                                : "PDF Olarak Dışa Aktar"
                        }}
                    </button>

            </div>
        </div>

        <p v-if="loading">
            Yükleniyor
        </p>

        <p v-if="errorMessage" class="error">
            {{ errorMessage }}
        </p>
<!-- 
        rapor ekranı temp ----------------------------------------------- -->



        <section
            v-if="plan && scoreDetails.final_score !== undefined"
            class="report-section"
        >
            <div class="section-heading">
                <div>
                    <span class="section-eyebrow">Performans analizi</span>
                    <h2>Plan Raporu</h2>
                </div>

                <span class="report-status">
                    {{ plan.is_feasible ? "Geçerli plan" : "Geçersiz plan" }}
                </span>
            </div>

            <div class="score-dashboard">
                <article class="metric-card metric-card-primary">
                    <span class="metric-label">Final skor</span>
                    <strong>{{ formatScore(finalScore) }}</strong>
                    <small>Öncelik puanı eksi toplam kayıp</small>
                </article>

                <article class="metric-card">
                    <span class="metric-label">Öncelik puanı</span>
                    <strong>
                        {{ formatScore(priorityReport.score) }}
                    </strong>
                    <small>
                        {{ priorityItems.length }} operasyon
                    </small>
                </article>

                <article class="metric-card metric-card-danger">
                    <span class="metric-label">Toplam kayıp</span>
                    <strong>
                        -{{ formatScore(totalLoss) }}
                    </strong>
                    <small>Soft constraint cezaları</small>
                </article>

                <article class="metric-card">
                    <span class="metric-label">Başarı oranı</span>
                    <strong>%{{ scorePercent }}</strong>
                    <small>Plan performans göstergesi</small>
                </article>
            </div>

            <div class="penalty-grid">
                <article class="penalty-card">
                    <div class="penalty-card-header">
                        <span>Gün dengesi</span>
                        <strong>
                            -{{ formatScore(dayBalance.loss) }}
                        </strong>
                    </div>

                    <p>
                        Günler arasındaki yük farkı:
                        <b>{{ dayBalance.raw_value ?? dayBalance["raw_value"] ?? 0 }}</b>
                <!-- ------------------        <b>{{ dayBalance.raw_value ?? dayBalance["raw value"] ?? 0 }}</b>
----------------               -->        
                         slot 
                    </p>
                </article>

                <article class="penalty-card">
                    <div class="penalty-card-header">
                        <span>Anestezi dengesi</span>
                        <strong>
                            -{{ formatScore(anesthesiaBalance.loss) }}
                        </strong>
                    </div>

                    <p>
                        Takımlar arasındaki yük farkı:
                        <b>
                            {{
                                anesthesiaBalance.raw_value ??
                                anesthesiaBalance["raw_value"] ??
//              -------------                   anesthesiaBalance["raw value"] ??
// -------------                         
                                0
                            }}
                        </b>
                        slot
                    </p>
                </article>

                <article class="penalty-card">
                    <div class="penalty-card-header">
                        <span>Oda boşlukları</span>
                        <strong>
                            -{{ formatScore(roomIdle.loss) }}
                        </strong>
                    </div>

                    <p>
                        Toplam
                        <b>
                            {{
                                roomIdle.raw_value ??
                                roomIdle["raw_value"] ??
//         -------------                        roomIdle["raw value"] ??
// --------                                
                                0
                            }}
                        </b>
                        boş slot
                    </p>
                </article>

                <article class="penalty-card">
                    <div class="penalty-card-header">
                        <span>Cerrah boşlukları</span>
                        <strong>
                            -{{ formatScore(surgeonIdle.loss) }}
                        </strong>
                    </div>

                    <p>
                        Toplam
                        <b>
                            {{
                                surgeonIdle.raw_value ??
                                surgeonIdle["raw_value"] ??
                                
//               -------                  surgeonIdle["raw value"] ??
// -------------

                                0
                            }}
                        </b>
                        boş slot
                    </p>
                </article>
            </div>

            <div class="report-two-column">
                <article class="report-panel">
                    <div class="panel-heading">
                        <div>
                            <span class="panel-kicker">Haftalık dağılım</span>
                            <h3>Gün yükleri</h3>
                        </div>

                        <span>
                            Min {{ dayBalance.details?.min_load ?? 0 }}
                            ·
                            Maks {{ dayBalance.details?.max_load ?? 0 }}
                        </span>
                    </div>

                    <div class="load-list">
                        <div
                            v-for="item in dailyLoads"
                            :key="item.day"
                            class="load-row"
                        >
                            <span>{{ item.day }}</span>

                            <div class="load-track">
                                <div
                                    class="load-fill"
                                    :style="{
                                        width: `${
                                            dayBalance.details?.max_load
                                                ? (
                                                    item.load /
                                                    dayBalance.details.max_load
                                                ) * 100
                                                : 0
                                        }%`,
                                    }"
                                ></div>
                            </div>

                            <strong>{{ item.load }}</strong>
                        </div>
                    </div>
                </article>

                <article class="report-panel">
                    <div class="panel-heading">
                        <div>
                            <span class="panel-kicker">Kaynak dağılımı</span>
                            <h3>Anestezi yükleri</h3>
                        </div>

                        <span>
                            Min {{ anesthesiaBalance.details?.min_load ?? 0 }}
                            ·
                            Maks {{ anesthesiaBalance.details?.max_load ?? 0 }}
                        </span>
                    </div>

                    <div class="team-grid">
                        <div
                            v-for="item in anesthesiaLoads"
                            :key="item.team"
                            class="team-load-card"
                        >
                            <span>{{ item.team }}</span>
                            <strong>{{ item.load }}</strong>
                            <small>slot</small>
                        </div>
                    </div>
                </article>
            </div>

            <article class="report-panel">
                <div class="panel-heading">
                    <div>
                        <span class="panel-kicker">Kaynak kaybı</span>
                        <h3>Oda boşlukları</h3>
                    </div>

                    <span>{{ roomIdleItems.length }} kayıt</span>
                </div>

                <div class="table-wrapper">
                    <table class="report-table">
                        <thead>
                            <tr>
                                <th>Gün</th>
                                <th>Oda</th>
                                <th>Önceki hasta</th>
                                <th>Sonraki hasta</th>
                                <th>Boşluk</th>
                            </tr>
                        </thead>

                        <tbody>
                            <tr
                                v-for="(gap, index) in roomIdleItems"
                                :key="`room-${index}`"
                            >
                                <td>{{ getDayName(gap.day_index) }}</td>
                                <td>
                                    <span class="resource-badge">
                                        {{ gap.room }}
                                    </span>
                                </td>
                                <td>{{ gap.from_patient }}</td>
                                <td>{{ gap.to_patient }}</td>
                                <td>
                                    <span class="gap-badge">
                                        {{ gap.gap }} slot
                                    </span>
                                </td>
                            </tr>

                            <tr v-if="!roomIdleItems.length">
                                <td colspan="5" class="empty-table">
                                    Oda boşluğu bulunmuyor.
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </article>

            <article class="report-panel">
                <div class="panel-heading">
                    <div>
                        <span class="panel-kicker">Personel kaybı</span>
                        <h3>Cerrah boşlukları</h3>
                    </div>

                    <span>{{ surgeonIdleItems.length }} kayıt</span>
                </div>

                <div class="table-wrapper">
                    <table class="report-table">
                        <thead>
                            <tr>
                                <th>Gün</th>
                                <th>Cerrah</th>
                                <th>Önceki hasta</th>
                                <th>Sonraki hasta</th>
                                <th>Boşluk</th>
                            </tr>
                        </thead>

                        <tbody>
                            <tr
                                v-for="(gap, index) in surgeonIdleItems"
                                :key="`surgeon-${index}`"
                            >
                                <td>{{ getDayName(gap.day_index) }}</td>
                                <td>
                                    <span class="resource-badge surgeon">
                                        {{ gap.surgeon }}
                                    </span>
                                </td>
                                <td>{{ gap.from_patient }}</td>
                                <td>{{ gap.to_patient }}</td>
                                <td>
                                    <span class="gap-badge">
                                        {{ gap.gap }} slot
                                    </span>
                                </td>
                            </tr>

                            <tr v-if="!surgeonIdleItems.length">
                                <td colspan="5" class="empty-table">
                                    Cerrah boşluğu bulunmuyor.
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </article>

            <article class="report-panel">
                <div class="panel-heading">
                    <div>
                        <span class="panel-kicker">Operasyon katkısı</span>
                        <h3>Öncelik puanları</h3>
                    </div>

                    <span>{{ priorityItems.length }} operasyon</span>
                </div>

                <div class="table-wrapper priority-table-wrapper">
                    <table class="report-table">
                        <thead>
                            <tr>
                                <th>Hasta</th>
                                <th>Operasyon</th>
                                <th>Öncelik</th>
                                <th>Gün</th>
                                <th>Başlangıç slotu</th>
                                <th>Puan</th>
                            </tr>
                        </thead>

                        <tbody>
                            <tr
                                v-for="item in priorityItems"
                                :key="item.patient"
                            >
                                <td>
                                    <strong>{{ item.patient }}</strong>
                                </td>
                                <td>{{ item.operation }}</td>
                                <td>
                                    <span
                                        class="priority-badge"
                                        :class="{
                                            critical: item.priority === 'Kritik',
                                            high: item.priority === 'Yüksek',
                                            medium: item.priority === 'Orta',
                                            low: item.priority === 'Düşük',
                                        }"
                                    >
                                        {{ item.priority }}
                                    </span>
                                </td>
                                <td>{{ getDayName(item.day_index) }}</td>
                                <td>{{ item.start_slot }}</td>
                                <td class="score-cell">
                                    {{ formatScore(item.score) }}
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </article>
        </section>
<!-- 
        ------------------------------------------------   rapor ekranı temp -->





        <section v-if="plan" class="card">
            <div class="summary-grid">
                <div class="summary-card">
                    <span class="card-label">Skor</span>
                    <strong>{{ plan.score }}</strong>
                </div>
<!-- 
                Plan success rate ----------------------------------------- -->

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

<!--                 
                 ----------------------------------------- Plan success rate -->
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

        <!-- <section
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
        </section> -->

        <section class = "weekly-calendar-card">

            <div class = "weekly-calendar-header">

                <div>

                    <span class = "calendar-kicker">
                        Haftalık Ameliyat Takvimi
                    </span>

                    <h2>
                        {{ days[selectedScheduleDay] }}
                    </h2>

                    <p>
                        Seçilen güne ait operasyonların saat bazlı dağılımı
                    </p>

                </div>

                <span class = "operation-count">

                    {{ getPlanDayCount(selectedScheduleDay) }}

                </span>

            </div>

            <div class = "day-tabs">

                <button
                        v-for = "(day, dayIndex) in days"
                        :key = "day"
                        type = "button"
                        class = "day-tab"
                        :class = "{
                            active :
                                selectedScheduleDay === dayIndex,
                        }"
                        @click = "selectedScheduleDay = dayIndex">
                    
                        <span>
                            {{ day }}
                        </span>

                        <small>
                            {{ getPlanDayCount(dayIndex) }}
                        </small>
                
                </button>>

            </div>


            <div class = "plan-calendar-table-wrapper">

                <table class = "plan-calendar-table">

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
                            v-for = "row in planSlotRows"
                            :key = "row.slot"
                            :class = "{
                                'calendar-filled' :
                                    row.operation,
                            }">

                                <td
                                    class = "calendar-time-cell">
                                    
                                    {{ row.slot }}

                                </td>

                                <template
                                        v-if = "row.operation">

                                    <td>
                                        <strong>
                                            {{ row.operation.patient }}
                                        </strong>
                                    </td>

                                    <td>
                                        {{ row.operation.operation }}
                                    </td>

                                    <td>
                                        👨‍⚕️ {{ row.operation.surgeon }}
                                    </td>

                                    <td>
                                        🏥 {{ row.operation.room }}
                                    </td>

                                    <td>
                                        💉
                                        {{
                                            row.operation
                                                .anesthesia_team
                                        }}
                                    </td>

                                    <td>
                                        <span
                                            class = "calendar-status">
                                            Planlandı
                                        </span>
                                    </td>

                                </template>

                                <template v-else >

                                    <td
                                        colspan = "6"
                                        class = "calendar-empty-cell">
                                    </td>

                                </template>

                        </tr>

                    </tbody>

                </table>

            </div>

        </section>


        <Teleport to ="body" >

            <div
                v-if = "recentPlansDialog"
                class = "dialog-overlay"
                @click.self = "recentPlansDialog = false " 
                >

                <div
                    class = "recent-plans-dialog"
                    role = "dialog"
                    aria-model = "true"
                    aria-labelledby = "recent-plans-title">
                
                    <div class ="dialog-header">

                        <h2 id = "recent-plans-title">
                            Değerlendirilen 10 Plan
                        </h2>

                        <button
                                type = "button"
                                class = "dialog-close-button"
                                aria-label = "Pencereyi Kapat"
                                @click = "recentPlansDialog  = false">

                                x

                        </button>

                    </div>

                    <div
                        v-if = "recentPlanPercentages.length"
                        class = "recent-plans-list">

                        <button
                                v-for = "result in recentPlanPercentages"
                                :key = "result.key"
                                type = "button"
                                class = "recent-plan-row"
                                :class = "{selected: result.isSelected}"
                                @click = "openSimulationPlan(result)">


                                <div class = "recent-plan-main">

                                    <span class = "candidate-name">

                                        Plan {{ result.valid_index }}

                                    </span>

                                    <strong>

                                        %{{ formatPercentage(result.success_rate) }}

                                    </strong>

                                </div>

                                <span
                                    v-if = "result.isSelected"
                                    class = "selected-marker">
                                
                                    <span class = "selected-check">
                                        ✓
                                    </span>

                                    Seçili
                                
                                </span>

                                <span
                                    v-else
                                    class = "candidate-arrow">
                                
                                    ›
                                
                                </span>

                        </button>
                    


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


/* 
Plan success rate ----------------------------------------- */

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


/* 
----------------------------------------- Plan success rate */

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

/* .recent-plan-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    min-height: 48px;
    padding: 11px 14px;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    background: #f8fafc;
} */

.recent-plan-row {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;

    padding: 14px 16px;

    border: 1px solid #e2e8f0;
    border-radius: 12px;

    background: #ffffff;
    color: inherit;

    font: inherit;
    text-align: left;

    cursor: pointer;

    transition:
        transform 0.18s ease,
        border-color 0.18s ease,
        background 0.18s ease;
}

.recent-plan-row:hover {
    transform: translateY(-1px);
    border-color: #93c5fd;
    background: #f8fafc;
}

.recent-plan-row strong {
    color: #0f172a;
    font-size: 18px;
}

/* .recent-plan-row.selected {
    border-color: #14b8a6;
    background: #f0fdfa;
    box-shadow: 0 0 0 1px rgba(20, 184, 166, 0.1);
} */

.recent-plan-row.selected {
    border-color: #86efac;
    background: #f0fdf4;
}

.recent-plan-main {
    display: flex;
    align-items: center;
    gap: 14px;
}


.candidate-name {
    color: #64748b;
    font-size: 13px;
    font-weight: 700;
}

.candidate-arrow {
    color: #94a3b8;
    font-size: 24px;
    line-height: 1;
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


/* 
rapor ekran css ---------------------------------------------------- */

.report-section {
    display: flex;
    flex-direction: column;
    gap: 22px;
    margin-top: 28px;
}

.section-heading {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 20px;
}

.section-heading h2 {
    margin: 4px 0 0;
    color: #0f172a;
    font-size: 28px;
}

.section-eyebrow,
.panel-kicker {
    color: #2563eb;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.report-status {
    padding: 8px 12px;
    border: 1px solid #bbf7d0;
    border-radius: 999px;
    background: #f0fdf4;
    color: #15803d;
    font-size: 13px;
    font-weight: 800;
}

.score-dashboard {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 16px;
}

.metric-card {
    display: flex;
    min-height: 136px;
    flex-direction: column;
    justify-content: space-between;
    padding: 20px;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    background:
        linear-gradient(145deg, #ffffff, #f8fafc);
    box-shadow: 0 10px 28px rgba(15, 23, 42, 0.06);
}

.metric-card-primary {
    border-color: #bfdbfe;
    background:
        linear-gradient(145deg, #eff6ff, #ffffff);
}

.metric-card-danger {
    border-color: #fecaca;
    background:
        linear-gradient(145deg, #fff1f2, #ffffff);
}

.metric-label {
    color: #64748b;
    font-size: 13px;
    font-weight: 700;
}

.metric-card strong {
    color: #0f172a;
    font-size: 30px;
    line-height: 1;
}

.metric-card-danger strong {
    color: #dc2626;
}

.metric-card-primary strong {
    color: #1d4ed8;
}

.metric-card small {
    color: #94a3b8;
    font-size: 12px;
}

.penalty-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 14px;
}

.penalty-card {
    padding: 17px;
    border: 1px solid #e2e8f0;
    border-radius: 15px;
    background: #ffffff;
}

.penalty-card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
}

.penalty-card-header span {
    color: #334155;
    font-size: 14px;
    font-weight: 800;
}

.penalty-card-header strong {
    color: #dc2626;
    font-size: 18px;
}

.penalty-card p {
    margin: 12px 0 0;
    color: #64748b;
    font-size: 13px;
}

.report-two-column {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 18px;
}

.report-panel {
    padding: 22px;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    background: #ffffff;
    box-shadow: 0 12px 32px rgba(15, 23, 42, 0.05);
}

.panel-heading {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 18px;
    margin-bottom: 20px;
}

.panel-heading h3 {
    margin: 4px 0 0;
    color: #0f172a;
    font-size: 20px;
}

.panel-heading > span {
    padding: 6px 10px;
    border-radius: 999px;
    background: #f1f5f9;
    color: #475569;
    font-size: 12px;
    font-weight: 700;
}

.load-list {
    display: flex;
    flex-direction: column;
    gap: 14px;
}

.load-row {
    display: grid;
    grid-template-columns: 92px minmax(100px, 1fr) 36px;
    align-items: center;
    gap: 12px;
}

.load-row span {
    color: #475569;
    font-size: 13px;
    font-weight: 700;
}

.load-row strong {
    color: #0f172a;
    text-align: right;
}

.load-track {
    height: 10px;
    overflow: hidden;
    border-radius: 999px;
    background: #e2e8f0;
}

.load-fill {
    height: 100%;
    border-radius: inherit;
    background:
        linear-gradient(90deg, #2563eb, #60a5fa);
}

.team-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 12px;
}

.team-load-card {
    display: flex;
    min-height: 120px;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border: 1px solid #dbeafe;
    border-radius: 14px;
    background: #eff6ff;
}

.team-load-card span {
    color: #475569;
    font-size: 13px;
    font-weight: 700;
}

.team-load-card strong {
    margin-top: 6px;
    color: #1d4ed8;
    font-size: 30px;
}

.team-load-card small {
    color: #64748b;
}

.table-wrapper {
    overflow-x: auto;
    border: 1px solid #e2e8f0;
    border-radius: 13px;
}

.report-table {
    width: 100%;
    border-collapse: collapse;
    min-width: 700px;
}

.report-table th {
    padding: 13px 15px;
    background: #f8fafc;
    color: #475569;
    font-size: 12px;
    font-weight: 800;
    text-align: left;
    text-transform: uppercase;
}

.report-table td {
    padding: 14px 15px;
    border-top: 1px solid #e2e8f0;
    color: #334155;
    font-size: 14px;
}

.report-table tbody tr:hover {
    background: #f8fafc;
}

.resource-badge,
.gap-badge,
.priority-badge {
    display: inline-flex;
    align-items: center;
    padding: 5px 9px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 800;
}

.resource-badge {
    background: #eff6ff;
    color: #1d4ed8;
}

.resource-badge.surgeon {
    background: #f5f3ff;
    color: #6d28d9;
}

.gap-badge {
    background: #fff7ed;
    color: #c2410c;
}

.priority-badge.critical {
    background: #fee2e2;
    color: #b91c1c;
}

.priority-badge.high {
    background: #ffedd5;
    color: #c2410c;
}

.priority-badge.medium {
    background: #fef9c3;
    color: #a16207;
}

.priority-badge.low {
    background: #dcfce7;
    color: #15803d;
}

.score-cell {
    color: #15803d !important;
    font-weight: 800;
}

.empty-table {
    padding: 28px !important;
    color: #94a3b8 !important;
    text-align: center !important;
}

.priority-table-wrapper {
    max-height: 520px;
    overflow: auto;
}

@media (max-width: 1100px) {
    .score-dashboard,
    .penalty-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}

@media (max-width: 800px) {
    .report-two-column {
        grid-template-columns: 1fr;
    }

    .team-grid {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 640px) {
    .score-dashboard,
    .penalty-grid {
        grid-template-columns: 1fr;
    }

    .section-heading {
        align-items: flex-start;
        flex-direction: column;
    }
}



.detail-actions {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
}

.export-button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 9px;
    min-height: 42px;
    padding: 10px 17px;
    border: 0;
    border-radius: 11px;
    background: #1d4ed8;
    color: #ffffff;
    font-size: 14px;
    font-weight: 800;
    cursor: pointer;
    box-shadow: 0 8px 20px rgba(29, 78, 216, 0.2);
    transition:
        transform 0.18s ease,
        background 0.18s ease,
        box-shadow 0.18s ease;
}

.export-button:hover:not(:disabled) {
    transform: translateY(-1px);
    background: #1e40af;
    box-shadow: 0 11px 24px rgba(29, 78, 216, 0.26);
}

.export-button:active:not(:disabled) {
    transform: translateY(0);
}

.export-button:disabled {
    cursor: not-allowed;
    opacity: 0.6;
    box-shadow: none;
}

.export-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 22px;
    height: 22px;
    border-radius: 7px;
    background: rgba(255, 255, 255, 0.16);
    font-size: 16px;
    line-height: 1;
}

.secondary-button {

    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 9px;
    min-height: 42px;
    padding: 10px 17px;
    border: 0;
    border-radius: 11px;
    background: #1d4ed8;
    color: #ffffff;
    font-size: 14px;
    font-weight: 800;
    cursor: pointer;
    box-shadow: 0 8px 20px rgba(29, 78, 216, 0.2);
    transition:
        transform 0.18s ease,
        background 0.18s ease,
        box-shadow 0.18s ease;

}

@media (max-width: 640px) {
    .page-header {
        align-items: flex-start;
        flex-direction: column;
    }

    .detail-actions {
        width: 100%;
    }

    .export-button {
        flex: 1;
    }
}

/* 
-------------------------------------------------- rapor ekran css */
/* 
plan detail tablo -------------------------------------------------- */

.weekly-calendar-card {
    margin-top: 26px;
    padding: 24px;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    background: #ffffff;
    box-shadow: 0 10px 28px rgba(15, 23, 42, 0.08);
}

.weekly-calendar-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    margin-bottom: 20px;
}

.calendar-kicker {
    display: block;
    margin-bottom: 5px;
    color: #2563eb;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.weekly-calendar-header h2 {
    margin: 0;
    color: #172554;
    font-size: 24px;
}

.weekly-calendar-header p {
    margin: 5px 0 0;
    color: #64748b;
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
    transition:
        transform 0.18s ease,
        border-color 0.18s ease,
        background 0.18s ease;
}

.day-tab:hover {
    transform: translateY(-1px);
    border-color: #93c5fd;
    background: #eff6ff;
}

.day-tab.active {
    border-color: #2563eb;
    background: #2563eb;
    color: #ffffff;
    box-shadow: 0 8px 18px rgba(37, 99, 235, 0.22);
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

@media (max-width: 800px) {
    .weekly-calendar-header {
        align-items: flex-start;
        flex-direction: column;
    }

    .day-tabs {
        grid-template-columns: 1fr;
    }

    .day-tab {
        width: 100%;
    }
}
/* 
------------------------------------------------- plan detail tablo */



</style>
