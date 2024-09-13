const BASE_URL = import.meta.env.VITE_BACKEND_URL

// AUTH ENDPOINT
export const authEndpoints = {
    LOGIN_API: `${BASE_URL}/auth/login`,
    SIGNUP_API: `${BASE_URL}/auth/signup`,
    LOGOUT_API: `${BASE_URL}/auth/logout`
}

export const sectionEndpoints = {
    GET_ALL_SECTIONS_API:  `${BASE_URL}/section/all`,
    ADD_SECTION_API: `${BASE_URL}/section/add`,
    DELETE_SECTION_API: `${BASE_URL}/section/delete/:sectionId`,
    UPDATE_SECTION_API: `${BASE_URL}/section/update/:sectionId`,
}
export const bookEndpoints = {
    GET_ALL_BOOKS_API: `${BASE_URL}/book/all`,
    ADD_BOOK_API: `${BASE_URL}/book/add`,
    DELETE_BOOK_API: `${BASE_URL}/book/delete/:bookId`, 
    UPDATE_BOOK_API: `${BASE_URL}/book/update/:bookId`, 
}

export const bookIssuanceEndpoints = {
    REQUEST_BOOK_API: `${BASE_URL}/issue/books/request/:bookId`,
    READ_BOOK_API: `${BASE_URL}/issue/books/read/:bookId`,
    RETURN_BOOK_API: `${BASE_URL}/issue/books/return/:bookId`,
    GET_ISSUED_BOOKS_API: `${BASE_URL}/issue/books/approved`,

    GET_ALL_ISSUED_BOOKS_API: `${BASE_URL}/librarian/books/approved`,
    ISSUE_BOOK_API: `${BASE_URL}/librarian/books/issue/:bookId/:userId`,
    DENY_ISSUE_BOOK_API: `${BASE_URL}/librarian/books/deny/:bookId/:userId`,
    REVOKE_BOOK_API: `${BASE_URL}/librarian/books/revoke/:bookId/:userId`,
    GET_ALL_PENDING_ISSUANCE_API: `${BASE_URL}/librarian/books/requests/pending`,
}

export const userProfileEndpoints = {
    EDIT_PROFILE_API: `${BASE_URL}/user/edit_profile`
}

export const librarianEndpoints = {
    DASHBOARD_DATA_API: `${BASE_URL}/librarian/dashboard_data`
}