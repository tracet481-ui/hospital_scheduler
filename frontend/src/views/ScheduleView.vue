<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { generateSchedule } from "../services/scheduleApi"
import { logout } from "../services/authService"
import { isTemplateExpression } from "typescript"

const router = useRouter()

const loading = ref(false)
const errorMessage = ref("")
const scheduleResult = ref(null)

const handleGenerate = async () => {
    loading.value = true
    errorMessage.value = ""
    scheduleResult.value = null

    try {
        const response = await generateSchedule()
        scheduleResult.value = response.data
    } catch (error) {
        console.log(error)
        errorMessage.value = "Plan oluşturulurken hata oluştu!"
    } finally {
        loading.value = false
    }


    const response = await generateSchedule()

    console.log(response.data)
    console.log(response.data.weekly_schedule)
    console.log(response.data.weekly_schedule[0])

    scheduleResult.value = response.data
}

const handleLogout = () => {
    logout()
    router.push("/login")
}
</script>

<template>
    <main class="schedule-page">
        <header class="page-header">
            <div>
                <h1>Plan Oluştur</h1>
                <p>Haftalık ameliyathane planı üret</p>
            </div>

            <button class="logout-button" @click="handleLogout">
                Çıkış Yap
            </button>
        </header>

        <section class="action-card">
            <button @click="handleGenerate" :disabled="loading">
                {{ loading ? "Plan oluşturuluyor..." : "Plan Oluştur" }}
            </button>

            <p v-if="errorMessage" class="error">
                {{ errorMessage }}
            </p>
        </section>

        <section v-if="scheduleResult" class="result-card">
            <h2>Plan Oluşturuldu</h2>

            <div class="score-box">
                <span>Skor</span>
                <strong>{{ scheduleResult.score }}</strong>
            </div>

            <p>
                Plan ID:
                <strong>{{ scheduleResult.plan_id }}</strong>
            </p>

            <!-- <pre>{{ scheduleResult }}</pre> -->


            <section v-if = "scheduleResult" class ="result-card">

                <h2>Plan Oluşturuldu</h2>


                <div class =" summary-grid ">

                    <div class= "summary-box">

                        <span>

                            Skor

                        </span>

                        <strong>

                            {{ scheduleResult.score }}

                        </strong>

                    </div>


                    <div class="summary-box">
    
                        <span>Plan ID</span>
    
                        <strong>{{ scheduleResult.plan_id }}</strong>

                    </div>



                    <div class = "summary-box" >

                        <span>Durum</span>

                            <strong>

                                {{ scheduleResult.success ? "Başarılı" : "Başarısız" }}

                            </strong>

                    </div>

                </div>

                <h3>

                    Oluşturulan Plan:

                </h3>    


                <table class =" schedule-table ">

                    <thead>

                        <tr>

                            <th>#</th>
                            <th>Gün</th>
                            <th>Başlangıç</th>
                            <th>Bitiş</th>
                            <th>Hasta</th>
                            <th>Ameliyat</th>
                            <th>Doktor</th>
                            <th>Oda</th>
                            <th>Anestezi</th>

                        </tr>

                    </thead>


                    <tbody>

                        <template
                            v-for="day in scheduleResult.weekly_schedule"
                            :key="day.day_index"
                        >
                            <tr
                                v-for="(item, index) in day.items"
                                :key="`${day.day_index}-${index}`"
                            >
                                <td>{{ index + 1 }}</td>
                                <td>{{ day.day_name }}</td>
                                <td>{{ item.start_time }}</td>
                                <td>{{ item.end_time }}</td>
                                <td>{{ item.patient }}</td>
                                <td>{{ item.operation }}</td>
                                <td>{{ item.surgeon }}</td>
                                <td>{{ item.room }}</td>
                                <td>{{ item.anesthesia_team }}</td>
                            </tr>
                        </template>

                    </tbody>

                </table>

            </section>





        </section>
    </main>
</template>

<style scoped>
.schedule-page {
    padding: 32px;
    background: #f8fafc;
    min-height: 100vh;
}

.page-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 24px;
}

.page-header h1 {
    margin: 0;
}

.page-header p {
    margin: 6px 0 0;
    color: #64748b;
}

.logout-button {
    background: #991b1b;
}

.action-card,
.result-card {
    background: white;
    padding: 24px;
    border-radius: 14px;
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.06);
    margin-bottom: 24px;
}

button {
    padding: 12px 18px;
    border: none;
    border-radius: 8px;
    background: #0f766e;
    color: white;
    cursor: pointer;
}

button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.error {
    color: #dc2626;
    margin-top: 16px;
}

.score-box {
    display: inline-flex;
    flex-direction: column;
    gap: 4px;
    padding: 16px 24px;
    background: #ecfdf5;
    border-radius: 12px;
    margin-bottom: 16px;
}

.score-box span {
    color: #64748b;
    font-size: 14px;
}

.score-box strong {
    font-size: 28px;
    color: #047857;
}

pre {
    background: #0f172a;
    color: #e2e8f0;
    padding: 16px;
    border-radius: 10px;
    overflow-x: auto;
}

.summary-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin: 20px 0;
}

.summary-box {
    padding: 16px;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    background: #f8fafc;
}

.summary-box span {
    display: block;
    font-size: 13px;
    color: #64748b;
    margin-bottom: 6px;
}

.summary-box strong {
    font-size: 18px;
    color: #0f172a;
}

.schedule-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 16px;
    font-size: 14px;
}

.schedule-table th,
.schedule-table td {
    border: 1px solid #e2e8f0;
    padding: 10px 12px;
    text-align: left;
}

.schedule-table th {
    background: #f1f5f9;
    color: #334155;
    font-weight: 600;
}

.schedule-table tr:nth-child(even) {
    background: #f8fafc;
}


</style>