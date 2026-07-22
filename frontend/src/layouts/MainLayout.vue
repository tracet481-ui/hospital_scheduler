<script setup lang="ts">
import AppHeader from "../components/layout/AppHeader.vue"
import AppSidebar from "../components/layout/AppSidebar.vue"
</script>

<template>
  <div class="main-layout">
    <AppSidebar />

    <div class="layout-content">
      <AppHeader />

      <main class="page-content">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<style scoped>
.main-layout {
  min-height: 100vh;
  background: #f3f7fa;
}

.layout-content {
  min-height: 100vh;
  margin-left: 78px;
}

.page-content {
  min-height: calc(100vh - 86px);
  padding: 28px 32px 48px;
}

@media (max-width: 760px) {
  .layout-content {
    margin-left: 68px;
  }

  .page-content {
    padding: 20px;
  }
}
</style>