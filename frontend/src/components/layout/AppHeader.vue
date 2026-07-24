<script setup lang="ts">
import { computed } from "vue"
import { useRoute } from "vue-router"

const route = useRoute()

const pageTitle = computed(() => {
  return route.meta.title || "Ameliyathane Planlama Sistemi"
})

const pageDescription = computed(() => {
  return (
    route.meta.description ||
    "Haftalık operasyon planlama ve yönetim sistemi"
  )
})
</script>

<template>
  <header class="app-header">
    <div class="header-title">
      <h1>
        {{ pageTitle }}
      </h1>

      <p>
        {{ pageDescription }}
      </p>
    </div>

    <div class="header-actions">
      <button
        type="button"
        class="header-button"
        aria-label="Bildirimler"
      >
        <i class="mdi mdi-bell-outline"></i>
        <span class="notification-dot"></span>
      </button>

      <div class="user-summary">
        <div class="user-avatar">
          <i class="mdi mdi-account"></i>
        </div>

        <div class="user-details">
          <strong>Yönetici</strong>
          <span>Administrator</span>
        </div>

        <i class="mdi mdi-chevron-down user-chevron"></i>
      </div>
    </div>
  </header>
</template>

<style scoped>
.app-header {
  position: sticky;
  top: 0;
  z-index: 50;

  display: flex;
  align-items: center;
  justify-content: space-between;

  min-height: 86px;
  padding: 16px 34px;

  background: rgb(255 255 255 / 93%);
  border-bottom: 1px solid #e2e8f0;
  backdrop-filter: blur(14px);
}

.header-title h1 {
  margin: 0;

  font-size: 20px;
  font-weight: 750;
  color: #0f172a;
}

.header-title p {
  margin: 6px 0 0;

  font-size: 12px;
  color: #64748b;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 18px;
}

.header-button {
  position: relative;

  display: flex;
  align-items: center;
  justify-content: center;

  width: 42px;
  height: 42px;

  font-size: 21px;
  color: #475569;

  cursor: pointer;

  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;

  transition:
    color 160ms ease,
    border-color 160ms ease,
    background 160ms ease;
}

.header-button:hover {
  color: #0f8f83;
  background: #f0fdfa;
  border-color: #99f6e4;
}

.notification-dot {
  position: absolute;
  top: 7px;
  right: 7px;

  width: 7px;
  height: 7px;

  background: #14b8a6;
  border: 2px solid #ffffff;
  border-radius: 50%;
}

.user-summary {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-avatar {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 42px;
  height: 42px;

  font-size: 21px;
  color: #ffffff;

  background:
    linear-gradient(
      135deg,
      #14b8a6,
      #0f766e
    );

  border-radius: 50%;
}

.user-details {
  display: flex;
  flex-direction: column;
  min-width: 100px;
}

.user-details strong {
  font-size: 13px;
  color: #1e293b;
}

.user-details span {
  margin-top: 3px;

  font-size: 11px;
  color: #94a3b8;
}

.user-chevron {
  font-size: 20px;
  color: #94a3b8;
}

@media (max-width: 650px) {
  .app-header {
    min-height: 76px;
    padding: 14px 20px;
  }

  .header-title p,
  .user-details,
  .user-chevron {
    display: none;
  }
}
</style>