<!-- <template>
  <RouterView />
</template> -->

<!-- <script setup>
</script>

<style>
html,
body,
#app {
  width: 100%;
  min-height: 100vh;
  margin: 0;
}
</style> -->

<script setup >

  import { RouterLink, RouterView } from "vue-router"

</script>

<template>

  <nav class = "navbar">

    <RouterLink to ="/schedule">Plan Oluştur</RouterLink>

    <RouterLink to ="/doctor-schedules">Doktor Takvimleri</RouterLink>

    <RouterLink to ="/plans">Kayıtlı Planlar</RouterLink>

  </nav>

  <RouterView />

</template>


<style scoped>

  .navbar {
      display: flex;
      gap: 16px;
      padding: 16px 28px;
      background: #0f172a;
  }

  .navbar a {
      color: #e2e8f0;
      text-decoration: none;
      padding: 10px 14px;
      border-radius: 8px;
  }

  .navbar a:hover,
  .navbar a.router-link-active {
      background: #1e293b;
      color: white;
  }


</style>


