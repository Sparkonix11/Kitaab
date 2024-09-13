import { apiConnector } from "../apiConnector";
import { bookIssuanceEndpoints } from "../apis";
const { REQUEST_BOOK_API, ISSUE_BOOK_API, READ_BOOK_API, RETURN_BOOK_API, REVOKE_BOOK_API, GET_ALL_PENDING_ISSUANCE_API, DENY_ISSUE_BOOK_API, GET_ISSUED_BOOKS_API, GET_ALL_ISSUED_BOOKS_API } = bookIssuanceEndpoints

export async function requestBook(bookId){
    try {
        const apiURL = REQUEST_BOOK_API.replace(':bookId', bookId)

        const response = await apiConnector('POST', apiURL)
        return {success: true, response}
    } catch (error) {
        console.error('Error Requesting a Book:', error)
        console.error('Error response:', error.response)
    
        const errorMessage = error.response.data.message
        return { success: false, message: errorMessage }
    }
}

export async function issueBook(bookId, userId){
    try {
        const apiURL = ISSUE_BOOK_API
                        .replace(':bookId', bookId)
                        .replace(':userId', userId)
        const response = await apiConnector('POST', apiURL)
        return {success: true, response}
    } catch (error) {
        console.error('Error Requesting a Book:', error)
        console.error('Error response:', error.response)
    
        const errorMessage = error.response.data.message
        return { success: false, message: errorMessage }
    }
}

export async function denyIssue(bookId, userId){
    try {
        const apiURL = DENY_ISSUE_BOOK_API
                        .replace(':bookId', bookId)
                        .replace(':userId', userId)
        const response = await apiConnector('POST', apiURL)
        return {success: true, response}
    } catch (error) {
        console.error('Error Requesting a Book:', error)
        console.error('Error response:', error.response)
    
        const errorMessage = error.response.data.message
        return { success: false, message: errorMessage }
    }
}

export async function readBook(bookId){
    try {
        const apiURL = READ_BOOK_API.replace(':bookId', bookId)
  
        const response = await apiConnector('POST', apiURL)
        return {success: true, response}
    } catch (error) {
        console.error('Error Requesting a Book:', error)
        console.error('Error response:', error.response)
    
        const errorMessage = error.response.data.message
        return { success: false, message: errorMessage }
    }
}

export async function returnBook(bookId){
    try {
        const apiURL = RETURN_BOOK_API.replace(':bookId', bookId)
  
        const response = await apiConnector('POST', apiURL)
        return {success: true, response}
    } catch (error) {
        console.error('Error Requesting a Book:', error)
        console.error('Error response:', error.response)
    
        const errorMessage = error.response.data.message
        return { success: false, message: errorMessage }
    }
}

export async function revokeBook(bookId, userId){
    try {
        const apiURL = REVOKE_BOOK_API
                        .replace(':bookId', bookId)
                        .replace(':userId', userId)  
        const response = await apiConnector('POST', apiURL)
        return {success: true, response}
    } catch (error) {
        console.error('Error Requesting a Book:', error)
        console.error('Error response:', error.response)
    
        const errorMessage = error.response.data.message
        return { success: false, message: errorMessage }
    }
}

export async function fetchAllPedningIssuance(){
    try {
        const response = await apiConnector('GET', GET_ALL_PENDING_ISSUANCE_API)
        const responseData = response.data
        return { success: true, responseData }

    } catch (error) {
        console.error('Error during getting all the pedning issuance:', error)
        console.error('Error response:', error.response)
        const errorMessage = error.response.data.message
        return { success: false, errorMessage }
    }

}

export async function fetchAllIssuedBooks(){
    try {
        const response = await apiConnector('GET', GET_ISSUED_BOOKS_API)
        const responseData = response.data
        return { success: true, responseData }

    } catch (error) {
        console.error('Error during getting all the pedning issuance:', error)
        console.error('Error response:', error.response)
        const errorMessage = error.response.data.message
        return { success: false, errorMessage }
    }

}

export async function fetchAllApprovedBooks(){
    try {
        const response = await apiConnector('GET', GET_ALL_ISSUED_BOOKS_API)
        const responseData = response.data
        return { success: true, responseData }

    } catch (error) {
        console.error('Error during getting all the pedning issuance:', error)
        console.error('Error response:', error.response)
        const errorMessage = error.response.data.message
        return { success: false, errorMessage }
    }

}