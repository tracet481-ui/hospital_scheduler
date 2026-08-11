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
                    v-for = "item in menuItems"
                    :key = "item.route"
                    :to ="item.route"
                    class = "sidebar-item"
                    :aria-label = "item.title"  >
                
            <span class = "item-icon">
                        <i :class = "['mdi', item.icon]"></i>                
            </span>

            <span class = "sidebar-tooltip">
                        {{ item.title }}
            </span>
                    
        </RouterLink>



      </nav>
    </div>

    <button
      type="button"
      class="sidebar-item logout-item"
      aria-label ="Çıkış Yap"
      @click="logout"
    >
      <span class="item-icon">
        <i class="mdi mdi-logout"></i>
      </span>

      <span class="sidebar-tooltip">
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
      #ffffff 0%,
      #ffffff 48%,
      #ffffff 100%
    );

  border-right: 1px solid rgb(255 255 255 / 8%);
  box-shadow: 8px 0 26px rgb(15 23 42 / 10%);

  transition:
    width 220ms ease,
    box-shadow 220ms ease;
}

/* .app-sidebar:hover {
  width: 250px;
  box-shadow: 14px 0 36px rgb(15 23 42 / 16%);
} */

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

  width: 46px;
  height: 46px;

  font-size: 23px;
  border-radius: 13px;

  transition:
    color 160ms ease,
    background 160ms ease,
    box-shadow 160ms ease;
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

/* .app-sidebar:hover .brand-content {
  opacity: 1;
  transform: translateX(0);
} */

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


.sidebar-item.router-link-active .item-icon {
  color: #ffffff;
  background: linear-gradient(135deg, #14b8a6, #0f8f83);
  box-shadow: 0 8px 18px rgb(20 184 166 / 28%);
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


.logout-item {
  color: #0a0000;
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

  /* .brand-content,
  .item-title, */
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

.sidebar-tooltip {
  position: absolute;
  top: 50%;
  left: calc(100% + 14px);
  z-index: 300;

  padding: 8px 11px;

  font-size: 12px;
  font-weight: 600;
  color: #ffffff;
  white-space: nowrap;

  pointer-events: none;

  background: #111827;
  border: 1px solid rgb(255 255 255 / 8%);
  border-radius: 8px;
  box-shadow: 0 8px 20px rgb(15 23 42 / 22%);

  opacity: 0;
  transform: translate(-6px, -50%);

  transition:
    opacity 140ms ease,
    transform 140ms ease;
}

.sidebar-tooltip::before {
  position: absolute;
  top: 50%;
  left: -5px;

  width: 10px;
  height: 10px;

  content: "";

  background: #111827;
  transform: translateY(-50%) rotate(45deg);
}

.sidebar-item:hover .sidebar-tooltip {
  opacity: 1;
  transform: translate(0, -50%);
}

.sidebar-item:hover .item-icon {
  color: #5eead4;
  background: rgb(20 184 166 / 12%);
}

.app-sidebar {
  width: 78px;
  overflow: visible;
}

</style>