import { apiConnector } from "../apiConnector";
import { bookEndpoints } from "../apis";
import { store } from "@/main";
const { GET_ALL_BOOKS_API, ADD_BOOK_API, DELETE_BOOK_API, UPDATE_BOOK_API } = bookEndpoints


export async function fetchAllBooks() {
    try {
        const response = await apiConnector('GET', GET_ALL_BOOKS_API)
        const responseData = response.data
        store.commit('setAllBook', responseData.books)
        getBookImages(responseData.books)
        return { success: true, responseData }
    } catch (error) {
        console.error('Error during getting all the books:', error)
        console.error('Error response:', error.response)
        const errorMessage = error.response.data.message
        return { success: false, errorMessage }
    }
}
export function getBookImages(books) {
    let bookCovers = [];
    for (let i = 0; i < books.length; i++) {
        let book_cover_path = `../../assets${books[i].book_cover}`;
        let book_cover = new URL(book_cover_path, import.meta.url).href;
        bookCovers.push(book_cover);
    }
    store.commit('setAllBookCovers', bookCovers)
}
export async function addBook(data) {
    try {
        const response = await apiConnector('POST', ADD_BOOK_API, data)
        return {success: true, response}
    } catch (error) {
        console.error('Error Adding a Book:', error)
        console.error('Error response:', error.response)
    
        const errorMessage = error.response.data.message
        return { success: false, message: errorMessage }
    }
}

export async function editBook(data, bookId) {
    try {
        const response = await apiConnector('PUT', `${UPDATE_BOOK_API.replace(':bookId', bookId)}`, data);
        return { success: true, response };
    } catch (error) {
        console.error('Error Editing a Book:', error);
        console.error('Error response:', error.response);
    
        const errorMessage = error.response.data.message;
        return { success: false, message: errorMessage };
    }
}

export async function deleteBook(bookId) {
    try {
        const response = await apiConnector('DELETE', `${DELETE_BOOK_API.replace(':bookId', bookId)}`);
        return { success: true, response };
    } catch (error) {
        console.error('Error Deleting a Book:', error);
        console.error('Error response:', error.response);
    
        const errorMessage = error.response.data.message;
        return { success: false, message: errorMessage };
    }
}
