import { createRouter, createWebHistory } from "vue-router" ;

import ScheduleView from "../views/ScheduleView.vue";


const router = createRouter ({

    history : createWebHistory(),
    routes : [{

        path : "/",
        component : ScheduleView,


    },],

});

export default router ;