import { apiConnector } from "../apiConnector";
import { librarianEndpoints } from "../apis";
const { DASHBOARD_DATA_API } =  librarianEndpoints

export async function fetchDashboardData() {
    try {
        const response = await apiConnector('GET', DASHBOARD_DATA_API)
        const responseData = response.data
        return { success: true, responseData }
    } catch (error) {
        console.error('Error during getting all the books:', error)
        console.error('Error response:', error.response)
        const errorMessage = error.response.data.message
        return { success: false, errorMessage }
    }
}