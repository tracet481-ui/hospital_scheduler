<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { login } from "../services/authService"

const router = useRouter()

const username = ref("")
const password = ref("")
const loading = ref(false)
const errorMessage = ref("")

const handleLogin = async () => {
    loading.value = true
    errorMessage.value = ""

    try {
        await login(username.value, password.value)

        router.push("/schedule")
    } catch (error) {
        console.log(error)
        errorMessage.value = "Kullanıcı adı veya şifre hatalı!"
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <main class="login-page">
        <section class="login-card">
            <h1>Hospital Scheduler</h1>
            <p>Yönetim Paneli Girişi</p>

            <form @submit.prevent="handleLogin">
                <input
                    v-model="username"
                    type="text"
                    placeholder="Kullanıcı adı"
                />

                <input
                    v-model="password"
                    type="password"
                    placeholder="Şifre"
                />

                <button type="submit" :disabled="loading">
                    {{ loading ? "Giriş yapılıyor..." : "Giriş Yap" }}
                </button>
            </form>

            <p v-if="errorMessage" class="error">
                {{ errorMessage }}
            </p>
        </section>
    </main>
</template>

<style scoped>
.login-page {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f3f6fb;
}

.login-card {
    width: 380px;
    padding: 32px;
    background: white;
    border-radius: 14px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
}

.login-card h1 {
    margin-bottom: 8px;
}

.login-card p {
    margin-bottom: 20px;
    color: #666;
}

form {
    display: flex;
    flex-direction: column;
    gap: 14px;
}

input {
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 8px;
}

button {
    padding: 12px;
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
    margin-top: 16px;
    color: #dc2626;
}
</style>