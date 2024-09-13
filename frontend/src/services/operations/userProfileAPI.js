import { apiConnector } from "../apiConnector";
import { userProfileEndpoints } from "../apis";
import { store } from "@/main";
const { EDIT_PROFILE_API } =  userProfileEndpoints

export async function editProfile(formData) {
    try {
        const response = await apiConnector('POST', EDIT_PROFILE_API, formData)
        const responseData = response.data
  
        // Assuming response data includes a message and user
        const { message, user } = responseData
    
        // Update store or handle response as needed
        store.commit('login', user)

        return { success: true, message, user }
    } catch (error) {
        console.error('Error:', error)
        const errorMessage = error.response.data.message
        return { success: false, message: errorMessage }
    }
};