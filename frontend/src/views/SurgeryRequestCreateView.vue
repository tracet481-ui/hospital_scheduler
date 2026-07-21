<script setup lang = "ts">

    import { ref, computed, onMounted } from "vue"

    import { 
        
        getPatients,
        getSurgeryTypes,
        getSurgeryRequest,

        type PatientOption,
        type SurgeryTypeOption,
        type SurgeryRequestPayload,
        createSurgeryRequest,
        } from "../services/scheduleApi"
    
    
    const patients = ref<PatientOption[]>([])

    const surgeryTypes = ref<SurgeryTypeOption[]>([])

    const loading = ref(false)

    const errorMessage = ref("")

    const successMessage = ref("")


    
    const form = ref<SurgeryRequestPayload>({

        patient : "" ,
        surgery_type : "" ,
        priority : "medium" ,

    })


    const priorityOptions = [

        {

            title : "Kritik",
            value : "critical",

        },

        {

            title : "Yüksek",
            value : "high",

        },

        {

            title : "Orta",
            value : "medium",

        },

        {

            title : "Düşük",
            value : "low",

        },

    ]


    const selectedOperation = computed (() => {

        return surgeryTypes.value.find(

            item => item.id === form.value.surgery_type

        )

    })


    const loadData = async () => {

        loading.value = true 

        try {

            const patientResponse = await getPatients()

            const surgeryResponse = await getSurgeryTypes ()

            patients.value = patientResponse.data

            surgeryTypes.value = surgeryResponse.data

        }


        catch (error) {

            console.log (error)

            errorMessage.value = "Veriler Yüklenemedi !"

        }


        finally {

            loading.value = false

        }

    }


    const saveRequest = async () => {

        errorMessage.value = ""
        successMessage.value = ""

        console.log("Gönderilecek form:", form.value)



        if (! form.value.patient || !form.value.surgery_type) {

            errorMessage.value = "Hasta ve operasyon türü seçilmelidir..."
            return
        }

        loading.value = true

        try {

            await createSurgeryRequest(form.value)

            successMessage.value = "Ameliyat talebi başarıyla oluşturuldu."

            form.value = {
                patient: "",
                surgery_type: "",
                priority: "medium",
            }

        }

        catch (error: any) {

            console.log(error)
            console.log(error.response)
            console.log(error.response?.data)

            const responseData = error.response?.data


            if (responseData) {

                errorMessage.value = 
                    typeof responseData === "string"
                    ? responseData
                    : JSON.stringify ( responseData )

            }

            else    {

                errorMessage.value = "Kayıt Oluşturulamadı !"

            }

        }

        finally {

            loading.value = false

        }

    }


    onMounted (() => {

        loadData()

    })

    // const submitOperation = async () => {

    //     loading.value = true
    //     successMessage.value = ""
    //     errorMessage.value = ""



    //     try {

    //         await createSurgeryType (form.value)

    //         successMessage.value = "Operasyon başarıyla eklendi."


            
    //         form.value = {

    //             name : "",
    //             duration : "",
    //             compatible_rooms : [],

    //         }

    //     }   catch (error)
        
    //     {

    //         console.log(error.response?.data ?? error)

    //         errorMessage.value = "Operasyon eklenirken hata oluştu! "

    //     }   finally {

    //         loading.value = false

    //     }

    // }

</script> 

<!-- 
<template>


    <main class ="operation-page" >

        <section class = "operation-card" >

            <h1>
                Operasyon Ekle 
            </h1>


            <form @submit.prevent = "submitOperation">

                <label>
                    Operasyon Adı

                    <input 
                        v-model.trim = "form.name"
                        type = "text"
                        required
                        />
                </label>

                <label>

                    Süre (30 dk slot süresi)

                    <input
                        v-model.nnumber = "form.duration"
                        type="number"
                        min="1"
                        max="20"
                        required
                        />
                </label>


                <button
                    type ="submit"
                    :disabled="loading">

                    {{ loading ? "Kaydediliyor..." : "Operasyonu Kaydet" }}

                </button>

            </form>

            <p v-if = "successMessage">
                    {{ successMessage }}
            </p>

            <p v-if = "errorMessage">
                    {{ errorMessage }}
            </p>

        </section>

    </main>

</template> -->


<template>

  <main class="operation-page">

    <section class="operation-card">

      <div class="page-header">

        <div>

          <p class="page-label">
            Operasyon Yönetimi
          </p>

          <h1>
            Yeni Operasyon Oluştur
          </h1>

          <p class="page-description">
            Hasta, operasyon türü ve öncelik bilgilerini seçerek
            yeni bir ameliyat talebi oluşturun.
          </p>

        </div>

      </div>


      <div
        v-if="errorMessage"
        class="message error-message"
      >
        {{ errorMessage }}
      </div>


      <div
        v-if="successMessage"
        class="message success-message"
      >
        {{ successMessage }}
      </div>


      <form
        class="operation-form"
        @submit.prevent="saveRequest"
      >

        <div class="form-group">

          <label for="patient">
            Hasta
          </label>

          <select
            id="patient"
            v-model="form.patient"
            :disabled="loading"
            required
            >
            <option value="" disabled>
                Hasta seçin
            </option>

            <option
                v-for="patient in patients"
                :key="patient.id"
                :value="String(patient.id)"
            >
                {{ patient.code }}
            </option>
          </select>

        </div>


        <div class="form-group">

          <label for="surgery-type">
            Operasyon Türü
          </label>

          <select
            id="surgery-type"
            v-model="form.surgery_type"
            :disabled="loading"
            required
            >
            <option value="" disabled>
                Operasyon türü seçin
            </option>

            <option
                v-for="operation in surgeryTypes"
                :key="operation.id"
                :value="String(operation.id)"
            >
                {{ operation.name }}
            </option>
          </select>

        </div>


        <div class="form-group">

          <label for="priority">
            Öncelik
          </label>

          <select
            id="priority"
            v-model="form.priority"
            :disabled="loading"
            required
          >

            <option
              v-for="priority in priorityOptions"
              :key="priority.value"
              :value="priority.value"
            >
              {{ priority.title }}
            </option>

          </select>

        </div>


        <section
          v-if="selectedOperation"
          class="operation-info"
        >

          <h2>
            Operasyon Bilgileri
          </h2>

          <div class="info-grid">

            <div class="info-item">

              <span class="info-label">
                Operasyon
              </span>

              <strong>
                {{ selectedOperation.name }}
              </strong>

            </div>


            <div class="info-item">

              <span class="info-label">
                Uzmanlık
              </span>

              <strong>
                {{ selectedOperation.specialty_name }}
              </strong>

            </div>


            <div class="info-item">

              <span class="info-label">
                Süre
              </span>

              <strong>
                {{ selectedOperation.duration_slots }} slot
              </strong>

            </div>


            <div class="info-item">

              <span class="info-label">
                Toplam Süre
              </span>

              <strong>
                {{ selectedOperation.duration_slots * 30 }} dakika
              </strong>

            </div>

          </div>

        </section>


        <div class="form-actions">

          <RouterLink
            to="/operations"
            class="cancel-button"
          >
            İptal
          </RouterLink>

          <button
            type="submit"
            class="save-button"
            :disabled="
              loading ||
              !form.patient ||
              !form.surgery_type
            "
          >

            {{
              loading
                ? "Kaydediliyor..."
                : "Operasyonu Kaydet"
            }}

          </button>

        </div>

      </form>

    </section>

  </main>

</template>





<style scoped>

.operation-page {
  min-height: calc(100vh - 70px);
  padding: 48px 24px;
  background: #f3f6fa;
}

.operation-card {
  width: 100%;
  max-width: 760px;
  margin: 0 auto;
  padding: 36px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 18px;
  box-shadow: 0 14px 40px rgba(15, 23, 42, 0.08);
}

.page-header {
  margin-bottom: 30px;
  padding-bottom: 24px;
  border-bottom: 1px solid #e2e8f0;
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
  font-size: 30px;
  font-weight: 700;
}

.page-description {
  max-width: 580px;
  margin: 10px 0 0;
  color: #64748b;
  font-size: 15px;
  line-height: 1.6;
}

.operation-form {
  display: flex;
  flex-direction: column;
  gap: 22px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  color: #334155;
  font-size: 14px;
  font-weight: 600;
}

.form-group select {
  width: 100%;
  height: 48px;
  padding: 0 14px;
  color: #0f172a;
  font-size: 15px;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  outline: none;
  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease;
}

.form-group select:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.12);
}

.form-group select:disabled {
  cursor: not-allowed;
  background: #f1f5f9;
}

.operation-info {
  padding: 24px;
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  border-radius: 14px;
}

.operation-info h2 {
  margin: 0 0 18px;
  color: #1e3a8a;
  font-size: 18px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.info-label {
  color: #64748b;
  font-size: 13px;
}

.info-item strong {
  color: #0f172a;
  font-size: 15px;
}

.message {
  margin-bottom: 22px;
  padding: 14px 16px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
}

.error-message {
  color: #991b1b;
  background: #fef2f2;
  border: 1px solid #fecaca;
}

.success-message {
  color: #166534;
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 12px;
  padding-top: 8px;
}

.cancel-button,
.save-button {
  min-width: 130px;
  padding: 12px 20px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  text-align: center;
  text-decoration: none;
  transition:
    transform 0.2s ease,
    background 0.2s ease;
}

.cancel-button {
  color: #475569;
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
}

.cancel-button:hover {
  background: #e2e8f0;
}

.save-button {
  cursor: pointer;
  color: #ffffff;
  background: #2563eb;
  border: none;
}

.save-button:hover:not(:disabled) {
  background: #1d4ed8;
  transform: translateY(-1px);
}

.save-button:disabled {
  cursor: not-allowed;
  opacity: 0.55;
}

@media (max-width: 640px) {

  .operation-page {
    padding: 24px 14px;
  }

  .operation-card {
    padding: 24px 18px;
  }

  .page-header h1 {
    font-size: 24px;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column-reverse;
  }

  .cancel-button,
  .save-button {
    width: 100%;
  }

}

</style>
