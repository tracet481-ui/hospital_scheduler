<script setup>
import { computed, onMounted, ref, watch } from "vue"
import { useRouter } from "vue-router"
import { getPlans } from "../services/scheduleApi"

const router = useRouter()

const plans = ref([])
const loading = ref(false)
const errorMessage = ref("")

// -----------------------------------------------------------
// Page ekleme
// -----------------------------------------------------------

const currentPage = ref(1)



const pageSize = ref(20)

const pageSizeOptions = [20, 50, 100, 200]



const totalPages = computed(() => {

    return Math.max(
        1,
        Math.ceil(plans.value.length / pageSize.value)
    )

})




const paginatedPlans = computed(() => {

    const startIndex = (currentPage.value - 1) * pageSize.value
    const endIndex = startIndex + pageSize.value

    return plans.value.slice(startIndex, endIndex)

})





const firstVisibleRecord = computed(() => {

    if (plans.value.length === 0) return 0

    return (currentPage.value - 1) * pageSize.value + 1

})




const lastVisibleRecord = computed(() => {

    return Math.min(

        currentPage.value * pageSize.value,

        plans.value.length

    )

})



const changePageSize = () => {

    currentPage.value = 1

}


// -----------------------------------------------------------
//                                                 Page ekleme
// -----------------------------------------------------------


const loadPlans = async () => {
    loading.value = true
    errorMessage.value = ""

    try {
        const response = await getPlans()
        plans.value = response.data
        currentPage.value = 1
    } catch (error) {
        console.log(error)
        errorMessage.value = "Planlar yüklenirken hata oluştu!"
    } finally {
        loading.value = false
    }
}

const goDetail = (id) => {
    router.push(`/plans/${id}`)
}

const getScorePercent = (score) => {

    if (!score) return 0

    const percent = score / 1300

    return Math.min ( 100, Math.max ( 0, percent ))

}


onMounted(loadPlans)
</script>

<template>
    <main class="page">
        <header class="page-header">
            <h1>Kayıtlı Planlar</h1>
            <p>Veritabanına kaydedilmiş ameliyathane planları</p>
        </header>

        <section class="card">
            <p v-if="loading">Planlar yükleniyor...</p>
            <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

            <table v-if="!loading && plans.length" class="plans-table">
                <thead>
                    <tr>
                        <th>Plan ID</th>
                        <th>Skor</th>
                        <th>Yüzdelik</th>
                        <th>Algoritma</th>
                        <th>Feasible</th>
                        <th>Tarih</th>
                        <th>Detay</th>
                    </tr>
                </thead>

                <tbody>
                    <tr v-for="plan in paginatedPlans" :key="plan.id">
                        <td>{{ plan.id }}</td>
                        <td>{{ plan.score }}</td>

                        <td class = "progress-cell">

                            <div class = "progress-info">

                                <span>
                                    {{ getScorePercent(plan.score).toFixed(2) }}%
                                </span>

                                <v-progress-linear
                                                :model-value = "getScorePercent(plan.score)"
                                                color = "blue"
                                                height = "8"
                                                rounded
                                                >

                                </v-progress-linear>

                            </div>

                        </td>   

                        <td>{{ plan.algorithm_name }}</td>
                        <td>{{ plan.is_feasible ? "Evet" : "Hayır" }}</td>
                        <td>{{ plan.created_at }}</td>
                        <td>
                            <button
                                
                                class = "detail-button"
                                @click="goDetail(plan.id)">
                                
                                Detay

                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>

            

            <div class="page-size">


                <label for="page-size">
                    Sayfa başına
                </label>

                <select
                    id="page-size"
                    v-model.number="pageSize"
                    @change="changePageSize"
                >

                    <option
                        v-for="size in pageSizeOptions"
                        :key="size"
                        :value="size"
                    >
                        {{ size }}
                    </option>

                </select>

                <span>kayıt</span>

            </div>




            <p v-if="!loading && !plans.length">
                Henüz kayıtlı plan yok.
            </p>
        </section>
    </main>
</template>

<style scoped>
.page {
    padding: 28px;
}

.page-header {
    margin-bottom: 20px;
}

.page-header h1 {
    color: #0f172a;
    margin-bottom: 6px;
}

.page-header p {
    color: #64748b;
}

.card {
    background: white;
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 2px 10px rgba(15, 23, 42, 0.08);
}

.plans-table {
    width: 100%;
    border-collapse: collapse;
}

.plans-table th,
.plans-table td {
    border-bottom: 1px solid #e2e8f0;
    padding: 12px;
    text-align: left;
    color: #0f172a;
}

.plans-table th {
    background: #f8fafc;
    font-weight: 700;
}

.detail-button {
    padding: 8px 12px;

    color: white;

    background: #2563eb;
    border: none;
    border-radius: 8px;

    cursor: pointer;
}

.error {
    color: #dc2626;
}


.progress-cell {
    min-width: 190px;
}

.progress-info {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.progress-info span {
    font-size: 13px;
    font-weight: 600;
    color: #15803d;
}


.pagination-wrapper {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;

    margin-top: 20px;
}

.pagination-info {
    margin: 0;

    font-size: 13px;
    color: #64748b;
}

.pagination {
    display: flex;
    align-items: center;
    gap: 6px;
}

.pagination-button {
    display: flex;
    align-items: center;
    justify-content: center;

    min-width: 38px;
    height: 38px;

    padding: 0 10px;

    color: #475569;

    background: #ffffff;
    border: 1px solid #dbe4ee;
    border-radius: 8px;

    cursor: pointer;

    transition: 0.2s;
}

.pagination-button:hover:not(:disabled) {
    color: #ffffff;

    background: #2563eb;
    border-color: #2563eb;
}

.pagination-button.active {
    color: #ffffff;

    background: #2563eb;
    border-color: #2563eb;
}

.pagination-button:disabled {
    cursor: not-allowed;

    opacity: 0.4;
}


</style>