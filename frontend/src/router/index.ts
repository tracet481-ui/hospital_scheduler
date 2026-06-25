import { createRouter, createWebHistory } from 'vue-router'
import AppLayout  from '../layouts/AppLayout.vue'
import ScheduleView from '../views/ScheduleView.vue'
import LoginView  from '../views/LoginView.vue'
import { isAuthenticated } from "../services/authService"



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

            },

          ]

        }

      ]


    }
)



router.beforeEach((to) => {

  if ( to.meta.requireAuth && !isAuthenticated()) {

    return "/login"
    
  }

  if (to.path === "/login" && isAuthenticated()) {

    return "/"

  }

})


export default router



// const routes = [

//   {
//     path: "/",
//     name: "schedule",
//     component: ScheduleView,
//   },
//   {
//     path: "/login",
//     name: "login",
//     component: LoginView,
//   },


// ];



// const router = createRouter({
//   history: createWebHistory(import.meta.env.BASE_URL),
//   routes, // <-- Burada oluşturduğun diziyi kullan
// });

// export default router;

