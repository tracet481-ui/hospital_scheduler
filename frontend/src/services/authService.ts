import axios from "axios"

const API_URL = "http://127.0.0.1:8000/api/auth/login/"


export const login = async (username : string, password: string) => {

    const response = await axios.post(API_URL, {
 
        username,
        password,

    })

  localStorage.setItem("token" , response.data.token)

  return response.data

}



export const logout = () => {

  localStorage.removeItem("token")

}


export const getToken = () => {
  return localStorage.getItem("token")
}

export const isAuthenticated = () => {
  return !!getToken()
}

 