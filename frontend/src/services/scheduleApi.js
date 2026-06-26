import axios from "axios"

import { getToken } from "./authService"

const api = axios.create ({

    baseURL: "http://127.0.0.1:8000/api",

})


api.interceptors.request.use ((config) =>   {

    const token = getToken()

    if(token)  {

        config.headers.Authorization = "Token $(token)"

        }

    return config
    
})


export const generateSchedule = () => {

    return api.post("/schedules/generate/")

}


export const getSchedules = () => {

    return api.get("/schedules/")

}




// export const generateSchedule = () =>  {

//     return api.post("/schedules/generate/");

// }


// export const getPlans = () =>  {

//     return api.get("/schedules/");

// }

