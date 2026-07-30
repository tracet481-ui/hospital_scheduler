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


// constraint ekleme -------------------------------------------------- 



export interface GenerateScheduleRequest {

    soft_constraints: {

        day_balance: number
        anesthesia_balance: number
        room_idle: number
        surgeon_idle: number

    }

}



export const generateSchedule = (
    data: GenerateScheduleRequest
) => {

    return api.post(
        "/schedules/generate/",
        data,
    )

}


// -------------------------------------------------- constraint ekleme


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


export const getSurgeryTypes = () => {

    return api.get<SurgeryTypeOption[]>("/surgery-types/")

}


export const getSurgeryRequest = (
    page = 1,
    pageSize = 20,
) => {

    return api.get("/surgery-requests/", {

        params: {
            page: page,
            page_size: pageSize,
        },

    })

}


export const createSurgeryRequest = (data: SurgeryRequestPayload) => {

    return api.post<SurgeryRequestResponse>("/surgery-requests/",data,)

}


    // ----------------------------------  operasyon ekleme 
    // operasyon ekleme ----------------------------------   

export interface SurgeryTypeOption {

    id : string
    name : string
    duration_slots : number
    specialty_name : string

    priority : SurgeryPriority
    priority_display : string

}


export type SurgeryPriority = 

    |   "critical"
    |   "high"
    |   "medium"
    |   "low"


export interface SurgeryRequestPayload {

    patient_code : string
    surgery_type : string

}



export interface SurgeryRequestResponse {

    id : string

    patient_name : string

    surgery_type : string
    surgery_name : string

    priority : SurgeryPriority
    priority_display : string

}


    // ----------------------------------  operasyon ekleme 




