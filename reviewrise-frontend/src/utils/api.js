import axios from "axios";

const api = axios.create({
    baseURL: "http://127.0.0.1:5000", // Your Flask backend URL
  });

export const signupUser = async (username, password) => {
    try {
        const response = await api.post('/signup', { username, password });
        return response.data;

    } catch (error){
        console.log("Error signing up");
        throw error;
    }
};

export const loginUser = async (username, password) => {
    try {
        const response = await api.post('/login', { username, password });
        return response.data;
    } catch (error) {
        console.log("Error logging in");
        throw error;
    }
}