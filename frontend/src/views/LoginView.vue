<script setup>

    import { ref } from "vue"
    import { useRouter } from "vue-router"
    // import { login } from "../services/authService"


    const router = useRouter ()

    const username = ref("")
    const password = ref ("")
    const errorMessage = ("")
    const loading = ref (false)


    const handleLogin = async () => {

        loading.value = true

        errorMessage.value = ""



        try {

            await login (username.value , password.value )

            router.push ("/")

        }   catch (error) {

            errorMessage.value = "Kullanıcı adı ve şifre hatalı! "

        }   finally {

            loading.value = false

        }

    }

</script>



<template>

    <div class = "login-page">

        <header class = "hospital-header">

            <div class = "header-content">

                <div class = "logo-circle">+</div>

                    <div>

                        <div class ="ministry">T.C. Sağlık Bakanlığı</div> 

                            <h1>Hastane Yönetim Ssstemi
                            </h1>

                            <h1>Ameliyathane Planlama Ve Yönetim Paneli
                            </h1>

                    </div>                    

            </div>

        </header>


        <main class = "login-wrapper">

            <section class = "intro-panel">

                    <h2>Ameliyathane Planlama Sistemi </h2>

                    <p> Cerrah, ameliyathane, anestezi ekibi ve operasyon taleplerini
          haftalık takvim üzerinde optimize eder. </p>


                    <div class = "info-box">

                        <strong>V2 Scheduler</strong>

                        <span>CP- SAT Simulation Score Basing Planning</span>

                    </div>

            </section>


            <section class = "login-card">

                <div class = "card-title">

                    <h2>Yetkili Personel Girişi</h2>

                    <p>Sisteme erişmek için kullanıcı bilgilerinizle giriş yapınız...</p>

                </div>


                <form @submit.prevent = "handleLogin" >


                        <label>Kullanıcı Adı</label>

                        <input v-model ="username" type = "text" autocomplete="username"/>


                        <label>Şifre</label>

                        <input v-model ="password" type ="password" autocomplete="current-password"/>

                        <button type ="submit" :disabled = "loading" >

                            {{ loading ? "Giriş yapılıyor...." : "Giriş Yap" }}

                        </button>


                        <p v-if = "errorMessage" class ="error-message">

                            {{ errorMessage }}

                        </p>
  
                </form>
                        
            </section>

        </main>

        
        <footer class = "login-footer">

            2026 Hastane Yönetim Sistemi · Ameliyathane Planlama Modülü

        </footer>

    </div>

</template>



<style scoped>
.login-page {
  min-height: 100vh;
  background:
    linear-gradient(rgba(238, 243, 248, 0.92), rgba(238, 243, 248, 0.92)),
    radial-gradient(circle at top right, #b8d8f2, transparent 35%);
}

.hospital-header {
  background: #003b73;
  color: white;
  border-bottom: 6px solid #1f75bb;
}

.header-content {
  max-width: 1180px;
  margin: 0 auto;
  padding: 24px 32px;
  display: flex;
  align-items: center;
  gap: 18px;
}

.logo-circle {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: white;
  color: #003b73;
  display: grid;
  place-items: center;
  font-size: 42px;
  font-weight: 700;
}

.ministry {
  font-size: 13px;
  letter-spacing: 1.4px;
  opacity: 0.9;
  font-weight: 700;
}

h1 {
  margin: 4px 0;
  font-size: 30px;
}

.header-content p {
  margin: 0;
  font-size: 16px;
  opacity: 0.92;
}

.login-wrapper {
  max-width: 1180px;
  margin: 0 auto;
  min-height: calc(100vh - 170px);
  padding: 64px 32px;
  display: grid;
  grid-template-columns: 1.2fr 430px;
  gap: 42px;
  align-items: center;
}

.intro-panel {
  background: white;
  border-radius: 14px;
  padding: 44px;
  box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
  border-left: 7px solid #1f75bb;
}

.intro-panel h2 {
  margin: 0 0 16px;
  color: #003b73;
  font-size: 34px;
}

.intro-panel p {
  margin: 0;
  color: #526173;
  font-size: 17px;
  line-height: 1.7;
}

.info-box {
  margin-top: 32px;
  padding: 18px 20px;
  border-radius: 10px;
  background: #eef6fd;
  border: 1px solid #cfe3f5;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.info-box strong {
  color: #003b73;
}

.info-box span {
  color: #526173;
}

.login-card {
  background: white;
  border-radius: 14px;
  padding: 34px;
  box-shadow: 0 14px 35px rgba(15, 23, 42, 0.13);
  border-top: 7px solid #1f75bb;
}

.card-title h2 {
  margin: 0;
  color: #003b73;
  font-size: 24px;
}

.card-title p {
  margin: 8px 0 28px;
  color: #667085;
  line-height: 1.5;
}

label {
  display: block;
  margin: 16px 0 7px;
  color: #344054;
  font-weight: 700;
  font-size: 14px;
}

input {
  width: 100%;
  padding: 13px 14px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-size: 15px;
}

input:focus {
  outline: none;
  border-color: #1f75bb;
  box-shadow: 0 0 0 3px rgba(31, 117, 187, 0.14);
}

button {
  margin-top: 24px;
  width: 100%;
  padding: 14px;
  background: #003b73;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 800;
  font-size: 15px;
  cursor: pointer;
}

button:hover {
  background: #005792;
}

button:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

.error-message {
  margin-top: 16px;
  padding: 11px 12px;
  background: #fef3f2;
  color: #b42318;
  border-radius: 8px;
  font-weight: 600;
}

.login-footer {
  text-align: center;
  color: #667085;
  padding: 18px;
  font-size: 14px;
}

@media (max-width: 900px) {
  .login-wrapper {
    grid-template-columns: 1fr;
  }

  .intro-panel {
    display: none;
  }
}
</style>