import { apiConnector } from "../apiConnector";
import { sectionEndpoints } from "../apis";
import { store } from "@/main";
const { GET_ALL_SECTIONS_API, ADD_SECTION_API, DELETE_SECTION_API, UPDATE_SECTION_API } = sectionEndpoints

export async function fetchAllSections() {
    try {
        const response = await apiConnector('GET', GET_ALL_SECTIONS_API)
        const responseData = response.data
        store.commit('setAllSection', responseData.sections)
        return { success: true, responseData }
    } catch (error) {
        console.error('Error during getting all the sections:', error)
        console.error('Error response:', error.response)
        const errorMessage = error.response.data.message
        return { success: false, errorMessage }
    }
}

export async function createSection(data) {
    try {
        const response = await apiConnector('POST', ADD_SECTION_API, data)
        return {success: true, response}
    } catch (error) {
        console.error('Error Adding a Section:', error)
        console.error('Error response:', error.response)
    
        const errorMessage = error.response.data.message
        return { success: false, message: errorMessage }
    }
}

export async function editSection(data, sectionId) {
    try {
        const response = await apiConnector('PUT', `${UPDATE_SECTION_API.replace(':sectionId', sectionId)}`, data);
        return { success: true, response };
    } catch (error) {
        console.error('Error Editing a Section:', error);
        console.error('Error response:', error.response);
    
        const errorMessage = error.response.data.message;
        return { success: false, message: errorMessage };
    }
}

export async function deleteSection(sectionId) {
    try {
        const response = await apiConnector('DELETE', `${DELETE_SECTION_API.replace(':sectionId', sectionId)}`);
        return { success: true, response };
    } catch (error) {
        console.error('Error Deleting a Section:', error);
        console.error('Error response:', error.response);
    
        const errorMessage = error.response.data.message;
        return { success: false, message: errorMessage };
    }
}
