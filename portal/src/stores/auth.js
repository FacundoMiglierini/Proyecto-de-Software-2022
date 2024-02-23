import { defineStore } from "pinia";
import { apiCall } from "../api.js";

export const useAuthStore = defineStore("state", {
    state: () => {
        return{
            user: {},
            isLogged: false,
        }
    },
    
    getters: {
        isLoggedIn: function(){
            if (!this.isLogged)
                this.getSession();
            return this.isLogged
        },
        getUser: function(){
            if (!this.user['id'])
                this.getUserSession();
            return this.user
        }
    },    
    actions: {
        async loginUser(user) {
            await apiCall('/api/auth', this.setSession, "POST", user)
            await this.fetchUser()
        },
        setSession(data){
            this.isLogged = true
            sessionStorage.setItem('session', JSON.stringify(data))
        },
        async fetchUser() {
            await apiCall('/api/auth/user_jwt', this.setUser, "GET")
        },
        async logoutUser() {
            await apiCall('api/auth/logout_jwt', this.clearUser, "GET")
        },
        getSession() { 
            const session = sessionStorage.getItem('session')
            if (session && typeof session === 'string' && session !== ''){
                this.isLogged = true;
            }
        },
        getUserSession(){
            const user = sessionStorage.getItem('user')
            if (user && typeof user === 'string' && user !== ''){
                const data = JSON.parse(user);
                this.setUser(data)
            }
        },
        setUser(data){
            this.user = data;
            sessionStorage.setItem('user', JSON.stringify(data))
        },
        clearUser(){
            sessionStorage.clear()
            this.user = {};
            this.isLogged = false;
        }
    },
})