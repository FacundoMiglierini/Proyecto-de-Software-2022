import { defineStore } from "pinia";

export const usePaymentsStore = defineStore("payments", {
    state: () => {
        return{
            unpaid: null,
            loading: true
        }
    },
    getters: {
        getUnpaid: function(){
            return this.unpaid
        },
        getLoading: function(){
            return this.loading
        }
    },
    actions: {
        assignUnpaid(data){
            this.unpaid = data 
            this.loading = false
        },
    }
}

)