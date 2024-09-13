import { authEndpoints } from "../apis";
import { apiConnector } from "../apiConnector";
import { store } from "@/main";
import router from "@/router";
const { LOGIN_API, SIGNUP_API, LOGOUT_API } = authEndpoints

export async function login(formData) {
    try {

      const response = await apiConnector('POST', LOGIN_API, formData)
      const responseData = response.data
  
      // Assuming response data includes a message and user
      const { message, user } = responseData
  
      // Update store or handle response as needed
      store.commit('login', user)
  
      router.push('/dashboard')
  
      return { success: true, message, user }
    } catch (error) {
      console.error('Error logging in:', error)
      console.error('Error response:', error.response)
  
      const errorMessage = error.response.data.message
      return { success: false, message: errorMessage }
    }
}

export async function signup(formData) {
    try {
        const response = await apiConnector('POST', SIGNUP_API, formData)
        const responseData = response.data

        // Assuming response data includes a message and user
        const { message, user } = responseData

        // Update store or handle response as needed
        store.commit('login', user)

        router.push('/dashboard')

        return { success: true, message, user }
    } catch (error) {
        console.error('Error:', error)

        const errorMessage = error.response.data.message
        return { success: false, message: errorMessage }
    }
}

export async function logout() {
    try {
      // Send logout request
      const response = await apiConnector('POST', LOGOUT_API)
  
      // Handle response as needed
      console.log(response)
  
      return { success: true }
    } catch (error) {
      console.error('Error:', error.response)
  
      return { success: false }
    }
}