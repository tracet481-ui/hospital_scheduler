import axios from "axios"

const api = axios.create ({

    baseURL: "http://127.0.0.1:8000/api",

});

export const generateSchedule = () =>  {

    return api.post("/schedules/generate/");

}


export const getPlans = () =>  {

    return api.get("/schedules/");

}

