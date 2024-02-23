import { defineStore } from "pinia";
import { apiCall } from "../api.js";

export const useContactStore = defineStore("contact", {
    state: () => {
        return{
            email: "",
            phone: "",
            address: "Camino Centenario y 48",
        }
    },

    getters: {
        getEmail: function(){
            if (this.email == "")
                this.fetchInfo();
            return this.email;
        },
        getPhone: function(){
            if (this.phone == "")
                this.fetchInfo();
            return this.phone;
        },
        getAddress: (state) => state.address
    },
    actions: {
        async fetchInfo(){
            await apiCall('api/club/info', this.setInfo, 'GET')
        },
        setInfo(data){
            this.email = data.email
            this.phone = data.phone
        }
    }
})