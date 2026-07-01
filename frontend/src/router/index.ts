import { createRouter, createWebHistory } from 'vue-router'
import AppLayout  from '../layouts/AppLayout.vue'
import ScheduleView from '../views/ScheduleView.vue'
import LoginView  from '../views/LoginView.vue'
import { isAuthenticated } from "../services/authService"
import DoctorScheduleView from '@/views/DoctorScheduleView.vue'
import PlanListView from "../views/PlanListView.vue"
import PlanDetailView from "../views/PlanDetailView.vue"



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

              path : "/",
              name : "dashboard",
              component :ScheduleView,

            },

            {

              path : "schedule",
              name : "schedule",
              component : ScheduleView,
              meta : {

                requiresAuth : true,

              }

            },


            {

              path : "/doctor-schedules",
              name : "doctor-schedules",
              component : DoctorScheduleView,
              meta : {

                requiresAuth : true,

              },

            },


            {

              path : "/plans",
              name : "plans",
              component : PlanListView,
              meta : {

                requiresAuth : true

              },

            },

            {

              path : "/plans/:id",
              name : "plan-detail",
              component : PlanDetailView,
              meta : {
                  requiresAuth : true
              },

            },

          ]

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




// const router = createRouter({
//   history: createWebHistory(import.meta.env.BASE_URL),
//   routes, // <-- Burada oluşturduğun diziyi kullan
// });

// export default router;

