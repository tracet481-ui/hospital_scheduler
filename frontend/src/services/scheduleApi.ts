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




export const getPatients = () =>  {

    return api.get<PatientOption[]>("/patients/")

}


export const getSurgeryTypes = () => {

    return api.get<SurgeryTypeOption[]>("/surgery-types/")

}


export const getSurgeryRequest = () => {

    return api.get<SurgeryRequestResponse[]>("/surgery-requests/")

}


export const createSurgeryRequest = (data: SurgeryRequestPayload) => {

    return api.post<SurgeryRequestResponse>("/surgery-requests/",data,)

}


    // ----------------------------------  operasyon ekleme 
    // operasyon ekleme ----------------------------------   


export interface PatientOption {

    id : string
    code : string

}


export interface SurgeryTypeOption {

    id : string
    name : string
    duration_slots : number
    specialty_name : string

}


export type SurgeryPriority = 

    |   "critical"
    |   "high"
    |   "medium"
    |   "low"


export interface SurgeryRequestPayload {

    patient : string
    surgery_type : string
    priority : SurgeryPriority 

}


export interface SurgeryRequestResponse {

    id : string

    patient : string
    patient_name : string

    surgery_type : string
    surgery_name : string

    priority : string

}


    // ----------------------------------  operasyon ekleme 




