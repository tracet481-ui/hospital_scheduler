<script setup lang="ts">
import { useRouter } from "vue-router"

const router = useRouter()

const menuItems = [
  {
    title: "Plan Oluştur",
    icon: "mdi-calendar-plus-outline",
    route: "/schedule",
  },
  {
    title: "Doktor Takvimleri",
    icon: "mdi-doctor",
    route: "/doctor",
  },
  {
    title: "Kayıtlı Planlar",
    icon: "mdi-clipboard-text-clock-outline",
    route: "/plans",
  },
  {
    title: "Operasyon Yönetimi",
    icon: "mdi-hospital-box-outline",
    route: "/operations",
  },
]

const logout = () => {
  localStorage.removeItem("token")
  router.push("/login")
}
</script>

<template>
  <aside class="app-sidebar">
    <div class="sidebar-top">
      <RouterLink
        to="/schedule"
        class="sidebar-brand"
        aria-label="Ana sayfa"
      >
        <span class="brand-icon">
          <i class="mdi mdi-hospital-building"></i>
        </span>

        <span class="brand-content">
          <strong>HYS</strong>
          <small>Ameliyathane Planlama</small>
        </span>
      </RouterLink>

      <nav class="sidebar-navigation">
        <RouterLink
          v-for="item in menuItems"
          :key="item.route"
          :to="item.route"
          class="sidebar-item"
          :title="item.title"
        >
          <span class="item-icon">
            <i :class="['mdi', item.icon]"></i>
          </span>

          <span class="item-title">
            {{ item.title }}
          </span>
        </RouterLink>
      </nav>
    </div>

    <button
      type="button"
      class="sidebar-item logout-item"
      title="Çıkış Yap"
      @click="logout"
    >
      <span class="item-icon">
        <i class="mdi mdi-logout"></i>
      </span>

      <span class="item-title">
        Çıkış Yap
      </span>
    </button>
  </aside>
</template>

<style scoped>
.app-sidebar {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 100;

  display: flex;
  flex-direction: column;
  justify-content: space-between;

  width: 78px;
  height: 100vh;
  padding: 18px 12px;

  overflow: hidden;

  color: #dbeafe;
  background:
    linear-gradient(
      180deg,
      #0f3f46 0%,
      #0f2f36 48%,
      #0d1f2b 100%
    );

  border-right: 1px solid rgb(255 255 255 / 8%);
  box-shadow: 8px 0 26px rgb(15 23 42 / 10%);

  transition:
    width 220ms ease,
    box-shadow 220ms ease;
}

.app-sidebar:hover {
  width: 250px;
  box-shadow: 14px 0 36px rgb(15 23 42 / 16%);
}

.sidebar-top {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.sidebar-brand,
.sidebar-item {
  display: flex;
  align-items: center;

  width: 100%;
  min-height: 52px;

  text-decoration: none;
  border-radius: 14px;
}

.sidebar-brand {
  gap: 14px;
  color: #ffffff;
}

.brand-icon,
.item-icon {
  display: flex;
  flex: 0 0 52px;
  align-items: center;
  justify-content: center;
}

.brand-icon {
  width: 52px;
  height: 52px;

  font-size: 28px;
  color: #ffffff;

  background:
    linear-gradient(
      135deg,
      #14b8a6,
      #0f8f83
    );

  border-radius: 15px;
  box-shadow: 0 10px 24px rgb(20 184 166 / 26%);
}

.brand-content {
  display: flex;
  flex-direction: column;

  min-width: 160px;

  opacity: 0;
  transform: translateX(-8px);

  transition:
    opacity 150ms ease,
    transform 180ms ease;
}

.app-sidebar:hover .brand-content {
  opacity: 1;
  transform: translateX(0);
}

.brand-content strong {
  font-size: 19px;
  line-height: 1;
  letter-spacing: 0.6px;
}

.brand-content small {
  margin-top: 6px;

  font-size: 11px;
  color: #9ec5c8;
  white-space: nowrap;
}

.sidebar-navigation {
  display: flex;
  flex-direction: column;
  gap: 9px;
}

.sidebar-item {
  position: relative;
  gap: 14px;

  padding: 0;

  font-family: inherit;
  color: #a8c7ca;

  cursor: pointer;

  background: transparent;
  border: 1px solid transparent;

  transition:
    color 160ms ease,
    background 160ms ease,
    border-color 160ms ease,
    transform 160ms ease;
}

.sidebar-item:hover {
  color: #ffffff;
  background: rgb(255 255 255 / 7%);
  transform: translateX(2px);
}

.sidebar-item.router-link-active {
  color: #ffffff;

  background:
    linear-gradient(
      90deg,
      rgb(20 184 166 / 50%),
      rgb(20 184 166 / 18%)
    );

  border-color: rgb(94 234 212 / 14%);
}

.sidebar-item.router-link-active::before {
  position: absolute;
  top: 10px;
  left: -12px;

  width: 4px;
  height: 32px;

  content: "";

  background: #2dd4bf;
  border-radius: 0 5px 5px 0;
}

.item-icon {
  font-size: 23px;
}

.item-title {
  min-width: 160px;

  font-size: 14px;
  font-weight: 600;
  white-space: nowrap;

  opacity: 0;
  transform: translateX(-8px);

  transition:
    opacity 150ms ease,
    transform 180ms ease;
}

.app-sidebar:hover .item-title {
  opacity: 1;
  transform: translateX(0);
}

.logout-item {
  color: #fecaca;
}

.logout-item:hover {
  color: #ffffff;
  background: rgb(185 28 28 / 45%);
}

@media (max-width: 760px) {
  .app-sidebar,
  .app-sidebar:hover {
    width: 68px;
    padding-right: 8px;
    padding-left: 8px;
  }

  .brand-content,
  .item-title,
  .app-sidebar:hover .brand-content,
  .app-sidebar:hover .item-title {
    opacity: 0;
    pointer-events: none;
  }

  .brand-icon,
  .item-icon {
    flex-basis: 50px;
  }
}
</style>