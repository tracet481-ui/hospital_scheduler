<script setup>
import { onMounted, ref } from "vue"
import { useRouter } from "vue-router"
import { getPlans } from "../services/scheduleApi"

const router = useRouter()

const plans = ref([])
const loading = ref(false)
const errorMessage = ref("")

const loadPlans = async () => {
    loading.value = true
    errorMessage.value = ""

    try {
        const response = await getPlans()
        plans.value = response.data
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
                        <th>Algoritma</th>
                        <th>Feasible</th>
                        <th>Tarih</th>
                        <th>Detay</th>
                    </tr>
                </thead>

                <tbody>
                    <tr v-for="plan in plans" :key="plan.id">
                        <td>{{ plan.id }}</td>
                        <td>{{ plan.score }}</td>
                        <td>{{ plan.algorithm_name }}</td>
                        <td>{{ plan.is_feasible ? "Evet" : "Hayır" }}</td>
                        <td>{{ plan.created_at }}</td>
                        <td>
                            <button @click="goDetail(plan.id)">
                                Detay
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>

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

button {
    border: none;
    padding: 8px 12px;
    border-radius: 8px;
    background: #2563eb;
    color: white;
    cursor: pointer;
}

.error {
    color: #dc2626;
}
</style>