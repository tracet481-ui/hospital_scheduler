import { createApp } from "vue"
import App from "./App.vue"
import router from "./router"

import "vuetify/styles"
import "@mdi/font/css/materialdesignicons.css"

import { createVuetify } from "vuetify"
import { VProgressLinear } from "vuetify/components"

import "./assets/main.css"

const vuetify = createVuetify({
    components: {
        VProgressLinear,
    },
})

createApp(App)
    .use(router)
    .use(vuetify)
    .mount("#app")
