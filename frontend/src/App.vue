<script setup >

  import { RouterLink, RouterView } from "vue-router"

  import { computed } from "vue"
  import { useRoute, useRouter } from "vue-router"


  import MainLayout from "@/layouts/MainLayout.vue"




  const route = useRoute()
  const router = useRouter()

  const isLoginPage = computed(() => {
                      return route.path === "/login"})



</script>

<template>

  <RouterView v-if="isLoginPage" />

  <MainLayout v-else />





</template>



 <style scoped>
* {
  box-sizing: border-box;
}

.app-layout {
  display: flex;
  min-height: 100vh;
  background: #f1f5f9;
}

/* SIDEBAR */

.sidebar {
  position: fixed;
  top: 0;
  left: 0;

  display: flex;
  flex-direction: column;

  width: 270px;
  height: 100vh;

  padding: 24px 18px;

  color: #e2e8f0;
  background:
    linear-gradient(
      180deg,
      #0f172a 0%,
      #111c32 55%,
      #0b1220 100%
    );

  border-right: 1px solid rgb(255 255 255 / 7%);
  box-shadow: 8px 0 30px rgb(15 23 42 / 10%);

  z-index: 100;
}

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 14px;

  padding: 4px 8px 18px;
}

.brand-icon {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 48px;
  height: 48px;

  flex-shrink: 0;

  font-size: 27px;
  color: #ffffff;

  background: linear-gradient(135deg, #0f766e, #14b8a6);
  border-radius: 14px;
  box-shadow: 0 8px 22px rgb(20 184 166 / 25%);
}

.brand-text {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.brand-text strong {
  font-size: 22px;
  line-height: 1.1;
  color: #ffffff;
  letter-spacing: 0.5px;
}

.brand-text span {
  margin-top: 5px;

  font-size: 11px;
  line-height: 1.35;
  color: #94a3b8;
}

.sidebar-divider {
  height: 1px;
  margin-bottom: 24px;
  background: rgb(148 163 184 / 13%);
}

.sidebar-navigation {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 8px;
}

.menu-label {
  margin: 0 12px 8px;

  font-size: 10px;
  font-weight: 700;
  color: #64748b;

  letter-spacing: 1.4px;
}

.sidebar-link {
  position: relative;

  display: flex;
  align-items: center;
  gap: 14px;

  min-height: 48px;
  padding: 0 15px;

  color: #aebbd0;
  text-decoration: none;

  border: 1px solid transparent;
  border-radius: 12px;

  transition:
    color 160ms ease,
    background 160ms ease,
    border-color 160ms ease,
    transform 160ms ease;
}

.sidebar-link i {
  width: 23px;

  font-size: 22px;
  text-align: center;
}

.sidebar-link span {
  font-size: 14px;
  font-weight: 500;
}

.sidebar-link:hover {
  color: #ffffff;
  background: rgb(255 255 255 / 6%);
  transform: translateX(2px);
}

.sidebar-link.router-link-active {
  color: #ffffff;

  background:
    linear-gradient(
      90deg,
      rgb(15 118 110 / 90%),
      rgb(15 118 110 / 55%)
    );

  border-color: rgb(45 212 191 / 15%);
  box-shadow: 0 8px 20px rgb(15 118 110 / 17%);
}

.sidebar-link.router-link-active::before {
  position: absolute;
  top: 11px;
  left: -18px;

  width: 4px;
  height: 26px;

  content: "";

  background: #2dd4bf;
  border-radius: 0 6px 6px 0;
}

/* SIDEBAR ALT KISMI */

.sidebar-footer {
  padding-top: 18px;
  border-top: 1px solid rgb(148 163 184 / 13%);
}

.user-card {
  display: flex;
  align-items: center;
  gap: 11px;

  padding: 11px;
  margin-bottom: 10px;

  background: rgb(255 255 255 / 4%);
  border: 1px solid rgb(255 255 255 / 5%);
  border-radius: 12px;
}

.user-avatar,
.header-avatar {
  display: flex;
  align-items: center;
  justify-content: center;

  flex-shrink: 0;

  color: #ccfbf1;
  background: #0f766e;
  border-radius: 50%;
}

.user-avatar {
  width: 36px;
  height: 36px;
  font-size: 19px;
}

.user-info {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.user-info strong {
  font-size: 13px;
  color: #f8fafc;
}

.user-info span {
  margin-top: 3px;

  overflow: hidden;

  font-size: 10px;
  color: #64748b;

  text-overflow: ellipsis;
  white-space: nowrap;
}

.logout-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;

  width: 100%;
  min-height: 43px;

  font-family: inherit;
  font-size: 13px;
  font-weight: 600;
  color: #fecaca;

  cursor: pointer;

  background: rgb(239 68 68 / 7%);
  border: 1px solid rgb(239 68 68 / 12%);
  border-radius: 11px;

  transition:
    color 160ms ease,
    background 160ms ease,
    border-color 160ms ease;
}

.logout-button i {
  font-size: 19px;
}

.logout-button:hover {
  color: #ffffff;
  background: #b91c1c;
  border-color: #b91c1c;
}

/* ANA ALAN */

.main-area {
  width: calc(100% - 270px);
  min-height: 100vh;
  margin-left: 270px;
}

.top-header {
  position: sticky;
  top: 0;

  display: flex;
  align-items: center;
  justify-content: space-between;

  min-height: 86px;
  padding: 18px 34px;

  background: rgb(255 255 255 / 94%);
  border-bottom: 1px solid #e2e8f0;
  backdrop-filter: blur(12px);

  z-index: 50;
}

.top-header h1 {
  margin: 0;

  font-size: 20px;
  font-weight: 700;
  color: #0f172a;
}

.top-header p {
  margin: 6px 0 0;

  font-size: 12px;
  color: #64748b;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 18px;
}

.notification-button {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 42px;
  height: 42px;

  font-size: 21px;
  color: #475569;

  cursor: pointer;

  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;

  transition:
    color 160ms ease,
    background 160ms ease;
}

.notification-button:hover {
  color: #0f766e;
  background: #f0fdfa;
}

.header-user {
  display: flex;
  align-items: center;
  gap: 10px;
}

.header-avatar {
  width: 40px;
  height: 40px;
  font-size: 20px;
}

.header-user > div:last-child {
  display: flex;
  flex-direction: column;
}

.header-user strong {
  font-size: 13px;
  color: #1e293b;
}

.header-user span {
  margin-top: 2px;

  font-size: 11px;
  color: #94a3b8;
}

.page-content {
  min-height: calc(100vh - 86px);
  padding: 30px 34px 50px;
}

/* RESPONSIVE */

@media (max-width: 900px) {
  .sidebar {
    width: 82px;
    padding-right: 12px;
    padding-left: 12px;
  }

  .brand-text,
  .sidebar-link span,
  .menu-label,
  .user-info,
  .logout-button span {
    display: none;
  }

  .sidebar-brand,
  .sidebar-link {
    justify-content: center;
  }

  .sidebar-link {
    padding: 0;
  }

  .sidebar-link.router-link-active::before {
    left: -12px;
  }

  .user-card {
    justify-content: center;
    padding: 8px;
  }

  .logout-button {
    padding: 0;
  }

  .main-area {
    width: calc(100% - 82px);
    margin-left: 82px;
  }
}

@media (max-width: 650px) {
  .top-header {
    padding: 16px 20px;
  }

  .top-header p,
  .header-user > div:last-child {
    display: none;
  }

  .page-content {
    padding: 20px;
  }
}
</style>