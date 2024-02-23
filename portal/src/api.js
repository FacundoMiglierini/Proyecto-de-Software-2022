import axios from 'axios';
import { useAuthStore } from './stores/auth';
import Router from './router';

let development = process.env.NODE_ENV !== 'production'

const apiService = axios.create({
    baseURL: development ? 'http://localhost:5000' : 'https://admin-grupo19.proyecto2022.linti.unlp.edu.ar/',
    withCredentials: true,
    xsrfCookieName: 'csrf_access_token',
});


async function apiCall(url, actions, method, data, headers){
    if (method === "POST"){
        await apiService.post(url, data, {headers: headers})
            .then(res => {
                actions(res.data)
            })
            .catch(function (error) {
                if (error.response.status == 401){
                    const authStore = useAuthStore()
                    authStore.clearUser()
                    Router.push('/');
                }
            })
    } else
    if (method === "GET"){
        await apiService.get(url)
            .then(res => {
                actions(res.data)
            })
            .catch(function (error) {
                if (error.response.status == 401){
                    const authStore = useAuthStore()
                    authStore.clearUser()
                    Router.push('/');
                }
            })
    }
}

export { apiService, apiCall};