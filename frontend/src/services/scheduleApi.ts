import axios from "axios"
import { getToken } from "./authService"

const api = axios.create({
    baseURL: "http://127.0.0.1:8000/api",
})

api.interceptors.request.use((config) => {
    const token = getToken()

    if (token) {
        config.headers.Authorization = `Token ${token}`
    }

    return config
})

export const generateSchedule = () => {
    return api.post("/schedules/generate/")
}

export const getPlans = () => {
    return api.get("/schedules/")
}

export const getPlanDetail = (planId: string) => {
    return api.get(`/schedules/${planId}/`)
}


// latest planı front a aktarıcaz

export const getLatestPlan = () => {

    return api.get("/schedules/latest/")

}

    // operasyon ekleme ----------------------------------

// export const getSurgeryTypes = () => {

//     return api.get ("/surgery-types/")

// }


// export const createSurgeryType = (data) => {

//     return api.post("/surgery-types/", data)

// }



export const getPatients = () =>  {

    return api.get("/patients/")

}


export const getSurgeryTypes = () => {

    return api.get("/surgery-types/")

}

export const createSurgeryRequest = (data: any) => {

    return api.post("/surgery-requests", data) 

}


    // ----------------------------------  operasyon ekleme 
