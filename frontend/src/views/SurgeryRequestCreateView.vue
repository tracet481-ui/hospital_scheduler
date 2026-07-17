<script setup>

    import { ref } from "vue"

    import { createSurgeryType } from "../services/scheduleApi"
import { error } from "console"



    const form = ref ({

        name : "",
        duration : 2,
        compatible_rooms : [] ,
        
    })


    const loading = ref (false)

    const successMessage = ref ("")

    const errorMessage = ref ("")




    const submitOperation = async () => {

        loading.value = true
        successMessage.value = ""
        errorMessage.value = ""



        try {

            await createSurgeryType (form.value)

            successMessage.value = "Operasyon başarıyla eklendi."


            
            form.value = {

                name : "",
                duration : "",
                compatible_rooms : [],

            }

        }   catch (error)
        
        {

            console.log(error.response?.data ?? error)

            errorMessage.value = "Operasyon eklenirken hata oluştu! "

        }   finally {

            loading.value = false

        }

    }

</script>


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

</template>