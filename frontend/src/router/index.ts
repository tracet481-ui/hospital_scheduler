import { createRouter, createWebHistory } from 'vue-router'
import AppLayout  from '../layouts/AppLayout.vue'
import ScheduleView from '../views/ScheduleView.vue'
import LoginView  from '../views/LoginView.vue'
import { isAuthenticated } from "../services/authService"
import DoctorScheduleView from '@/views/DoctorScheduleView.vue'
import PlanListView from "../views/PlanListView.vue"
import PlanDetailView from "../views/PlanDetailView.vue"
import OperationManagementView from "../views/OperationManagementView.vue"
import SurgeryRequestCreateView from '../views/SurgeryRequestCreateView.vue'



const router = createRouter({

  history : createWebHistory(import.meta.env.BASE_URL),
  routes : [

        {

          path : "/login",
          name : "login",
          component : LoginView,

        },

        {

          path : "/",
          component : AppLayout,
          meta : { requiresAuth : true },
          children : [

              {
                path: "/schedule",
                name: "schedule",
                component: ScheduleView,
                meta: {
                  requiresAuth: true,
                  title: "Plan Oluştur",
                  description: "Yeni haftalık ameliyathane planı oluşturun",
                },
              },
              {
                path: "/doctor",
                name: "doctor",
                component: DoctorScheduleView,
                meta: {
                  requiresAuth: true,
                  title: "Doktor Takvimleri",
                  description: "Doktorların haftalık operasyon takvimlerini görüntüleyin",
                },
              },
              {
                path: "/plans",
                name: "plans",
                component: PlanListView,
                meta: {
                  requiresAuth: true,
                  title: "Kayıtlı Planlar",
                  description: "Daha önce oluşturulan planları inceleyin",
                },
              },

              {
                path: "/plans/:id",
                name: "plan-detail",
                component: PlanDetailView,
                meta: {
                  requiresAuth: true,
                  title: "Plan Detayı",
                  description: "Seçilen ameliyathane planının ayrıntılarını görüntüleyin",
                },
              },

              {
                path: "/operations",
                name: "operations",
                component: OperationManagementView,
                meta: {
                  requiresAuth: true,
                  title: "Operasyon Yönetimi",
                  description: "Operasyon taleplerini görüntüleyin ve yönetin",
                },
              },


              {

                path : "/operations/new",
                name : "operation-create",
                component : SurgeryRequestCreateView,
                meta: {
                  requiresAuth :true,
                  title : "Operasyon Kaydı",
                  description : "Operasyon düzenleyin",
                },

              },


              {
                path : "/plans/:id/simulations/:simulationIndex",
                name : "simulation-plan-detail",
                component : () => 
                  import("../views/SimulationPlanDetailView.vue"),

                meta : {
                      requiresAuth : true,
                      title : "Seçili Plan Özeti",
                      description : "Seçili planın özeti",
                },
              },

              {
                path : "/plans/:id/simple",
                name : "simple-plan-detail",
                component : () => 
                  import ("../views/SimplePlanDetailView.vue"),

                meta : {

                  requiresAuth : true,
                  title : "Plan Özeti",
                  description : "Planın özet değerlendirmesini görüntüleyin",

                },
              },



          ],

        }

      ]


    }
)



router.beforeEach ((to) => {

  if ( to.meta.requiresAuth && !isAuthenticated()) {

    return  "/login" 
    
  }

  else if (to.path === "/login" && isAuthenticated()) {

    return "/schedule"

  }

})


export default router






