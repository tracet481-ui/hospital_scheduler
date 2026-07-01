<script setup>

    import { routerKey, useRouter } from "vue-router"
    import { logout } from "../services/authService"


    const router = useRouter() ;

    const handleLogout = () => {

        logout ()

        router.push("/Login")

    }

</script>



<template>

    <div class = "app-layout">

        <aside class = "slidebar">

            <div class = "sidebar-brand">

                <div class ="brand-icon">

                    <h2>HYS</h2>

                    <p>Planlama Paneli</p>

                </div>

            </div>


            <!-- <nav class ="sidebar-nav">

                <RouterLink to ="/">Dashboard</RouterLink>
                <RouterLink to ="/schedule">Plan Oluştur</RouterLink>
                <RouterLink to ="/plans">Plan Listesi</RouterLink>


            </nav> -->

            <!-- <nav class="navbar">

                <div class="logo">
                    Hospital Scheduler
                </div>

                <div class="nav-links">
                    <RouterLink to="/schedule">
                        Plan Oluştur
                    </RouterLink>

                    <RouterLink to="/doctor-schedules">
                        Doktor Takvimleri
                    </RouterLink>

                    <RouterLink to="/plans">
                        Kayıtlı Planlar
                    </RouterLink>
                </div>

                <button @click="logout">
                    Çıkış
                </button>

            </nav> -->

            <button class ="logout-button" @click="handleLogout">

                Çıkış Yap

            </button>

        </aside>


        <div class = "main-area">

             <header class = "main-header">

                <div>

                    <h1>Ameliyathane Planlama Sistemi</h1>

                    <p>Hastane Yönetim Sistemi</p>

                </div>

            </header>


            <main class ="content-area">

                <RouterView />

            </main>

        </div>

    </div>

</template>



<style scoped>
.app-layout {
  min-height: 100vh;
  display: flex;
  background: #eef3f8;
}

.sidebar {
  width: 270px;
  background: #676e75;
  color: rgb(6, 0, 0);
  display: flex;
  flex-direction: column;
  padding: 24px 18px;
}

.sidebar-brand {
  display: flex;
  gap: 13px;
  align-items: center;
  padding-bottom: 24px;
  border-bottom: 1px solid rgba(255,255,255,0.2);
}

.brand-icon {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: white;
  color: #003b73;
  display: grid;
  place-items: center;
  font-size: 28px;
  font-weight: 800;
}

.sidebar-brand h2 {
  margin: 0;
}

.sidebar-brand p {
  margin: 3px 0 0;
  opacity: 0.85;
  font-size: 13px;
}

.sidebar-nav {
  margin-top: 28px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.sidebar-nav a {
  color: rgb(63, 2, 2);
  text-decoration: none;
  padding: 12px 14px;
  border-radius: 8px;
  opacity: 0.9;
}

.sidebar-nav a.router-link-active,
.sidebar-nav a:hover {
  background: rgba(255,255,255,0.14);
}

.logout-button {
  margin-top: auto;
  background: #ffffff;
  color: #003b73;
  border: none;
  border-radius: 8px;
  padding: 12px;
  font-weight: 800;
  cursor: pointer;
}

.main-area {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.main-header {
  background: rgb(255, 255, 255);
  border-bottom: 1px solid #d9e3ee;
  padding: 24px 34px;
}

.main-header h1 {
  margin: 0;
  color: #003b73;
  font-size: 24px;
}

.main-header p {
  margin: 5px 0 0;
  color: #667085;
}

.content-area {
  padding: 32px;
}
</style>