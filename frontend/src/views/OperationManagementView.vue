<script setup lang ="ts">

    import { onMounted, ref } from 'vue'

    import {

        getSurgeryRequest,
        type SurgeryRequestResponse,

    }   from "../services/scheduleApi"


    
    const operations = ref<SurgeryRequestResponse[]>([])

    const loading = ref(false)

    const errorMessage  = ref("")




    const loadOperations = async () => {

        loading.value = true

        errorMessage.value = ""



        try {

            const response = await getSurgeryRequest()

            console.log ("Operation response :", response.data)

            operations.value = Array.isArray(response.data)
                  ? response.data
                  : response.data.results ?? []

        }

        catch   (error) {

            console.log (error)

            errorMessage.value = "Operasyonlar yüklenemedi !"

        }

        finally {

            loading.value = false

        }

    }


    const getPriorityLabel = (priority : string) => {

        const labels : Record <string, string> = {

            critical : "Kritik",

            high : "Yüksek",

            medium : "Orta",

            low : "Düşük",

        }

        return labels [priority] ?? priority 
 
    }


    const getPriorityClass = (priority : string) => {

        return 'priority-${priority}'

    }


    onMounted (()   =>  {

        loadOperations()

    })

</script>



<template>


    <main class ="operations-page" >

        <section class ="operation-container" >

            <header class = "page-header" >

                <div>

                    <p class ="page-level">
                        
                        Hastane Yönetimi
                    </p>

                    <h1>
                        Operasyon Yönetimi
                    </h1>

                    <p class ="page-description">
                        
                        Sistemde kayıtlı ameliyat taleplerini görüntüleyin
            ve yeni operasyon talepleri oluşturun.
                    </p>

                </div>


                <RouterLink
                        to="/operations/new"
                        class ="create-button" >
                    
                    +Yeni Operasyon    
                </RouterLink>

            </header>


            <div
                v-if ="errorMessage"
                class = "message error-message">

                {{ errorMessage }}

            </div>


            <div
                v-if ="loading"
                class ="status-card" >
            
                Operasyonlar yükleniyor...

            </div>


            <div
                v-else-if ="operations.length === 0"
                class = "empty-state" >
            
                <h2>
                    Henüz operasyon bulunamıyor
                </h2>

                <p>
                    Sisteme ilk ameliyat talebini ekleyebilirsiniz...
                </p>


                <RouterLink
                    to = "/operations/new"
                    class ="empty-create-button" >
                
                    Operasyon oluştur

                </RouterLink>

            </div>


            <div
                v-else 
                class = "tabler-wrapper" >
            
                <table class = "operations-table">

                    <thead>

                        <tr>

                            <th>
                                Hasta
                            </th>

                            <th>
                                Operasyon
                            </th>

                            <th>
                                Öncelik
                            </th>

                            <th>
                                İşlemler
                            </th>

                        </tr>

                    </thead>


                    <tbody>

                        <tr
                            v-for ="operation in operations"
                            :key = "operation.id" >
                        
                            <td>

                                <strong>
                                    {{ operation.patient_name }}
                                </strong>

                            </td>


                            <td>
                                {{ operation.surgery_name }}
                            </td>

                            <td>

                                <span
                                    class = "priority-badge"
                                    :class ="getPriorityClass(operation.priority)">

                                    {{ getPriorityLabel(operation.priority) }}

                                </span>

                            </td>

                            <td>

                                <div class ="action-buttons">

                                    <button
                                        type = "button"
                                        class = "edit-button"
                                        disabled>

                                        Düzenle

                                    </button>


                                    <button
                                        type = "button"
                                        class = "delete-button"
                                        disabled >
                                    
                                        Sil

                                    </button>

                                </div>

                            </td>

                        </tr>

                    </tbody>

                </table>
            
            </div>

        </section>

    </main>

</template>







<style scoped>

.operations-page {
  min-height: calc(100vh - 70px);
  padding: 48px 24px;
  background: #f3f6fa;
}

.operations-container {
  width: 100%;
  max-width: 1100px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 24px;
  margin-bottom: 28px;
}

.page-label {
  margin: 0 0 8px;
  color: #2563eb;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.page-header h1 {
  margin: 0;
  color: #0f172a;
  font-size: 32px;
}

.page-description {
  max-width: 620px;
  margin: 10px 0 0;
  color: #64748b;
  line-height: 1.6;
}

.create-button,
.empty-create-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 12px 20px;
  color: #ffffff;
  font-size: 14px;
  font-weight: 700;
  text-decoration: none;
  white-space: nowrap;
  background: #2563eb;
  border-radius: 10px;
  transition:
    background 0.2s ease,
    transform 0.2s ease;
}

.create-button:hover,
.empty-create-button:hover {
  background: #1d4ed8;
  transform: translateY(-1px);
}

.table-wrapper {
  overflow-x: auto;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  box-shadow: 0 12px 35px rgba(15, 23, 42, 0.07);
}

.operations-table {
  width: 100%;
  border-collapse: collapse;
}

.operations-table th,
.operations-table td {
  padding: 18px 20px;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
}

.operations-table th {
  color: #475569;
  font-size: 13px;
  font-weight: 700;
  background: #f8fafc;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.operations-table td {
  color: #334155;
  font-size: 14px;
}

.operations-table tbody tr:last-child td {
  border-bottom: none;
}

.operations-table tbody tr:hover {
  background: #f8fafc;
}

.priority-badge {
  display: inline-flex;
  padding: 6px 10px;
  font-size: 12px;
  font-weight: 700;
  border-radius: 999px;
}

.priority-critical {
  color: #991b1b;
  background: #fee2e2;
}

.priority-high {
  color: #9a3412;
  background: #ffedd5;
}

.priority-medium {
  color: #854d0e;
  background: #fef9c3;
}

.priority-low {
  color: #166534;
  background: #dcfce7;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.edit-button,
.delete-button {
  padding: 8px 12px;
  font-size: 13px;
  font-weight: 600;
  border-radius: 8px;
}

.edit-button {
  color: #1d4ed8;
  background: #eff6ff;
  border: 1px solid #bfdbfe;
}

.delete-button {
  color: #b91c1c;
  background: #fef2f2;
  border: 1px solid #fecaca;
}

.edit-button:disabled,
.delete-button:disabled {
  cursor: not-allowed;
  opacity: 0.55;
}

.status-card,
.empty-state {
  padding: 48px 24px;
  color: #475569;
  text-align: center;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
}

.empty-state h2 {
  margin: 0;
  color: #0f172a;
  font-size: 22px;
}

.empty-state p {
  margin: 10px 0 22px;
  color: #64748b;
}

.message {
  margin-bottom: 22px;
  padding: 14px 16px;
  border-radius: 10px;
}

.error-message {
  color: #991b1b;
  background: #fef2f2;
  border: 1px solid #fecaca;
}

@media (max-width: 700px) {

  .operations-page {
    padding: 28px 14px;
  }

  .page-header {
    flex-direction: column;
  }

  .create-button {
    width: 100%;
  }

  .operations-table th,
  .operations-table td {
    padding: 14px;
  }

}

</style>








