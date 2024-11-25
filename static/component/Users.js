export default {
  template: `<div>
  <div v-if="error"> {{error}}</div>
  <div v-for="(user, index) in allUsers">
  {{user.email}} 
  <button class="btn btn-primary" v-if='!user.active' @click="approve(user.id)"> Approve </button> </div>
  </div>`,
  data() {
    return {
      allUsers: null,
      token: localStorage.getItem("auth-token"),
      error: null,
    }
  },
  methods: {
    async approve(userID){
      const res = await fetch(`/activate/user/${userID}`, {
        headers: {
          "Authentication-Token": this.token,
        },
      })
      const data = await res.json()
      if (res.ok) {
        alert(data.message)
      }
    },
  },
  async mounted(){
    const res = await fetch('/users', {
      headers: {
        "Authentication-Token": this.token,
      },
    })
    const data = await res.json().catch((e)=> {})
    if(res.ok){
      this.allUsers = data
    }else{
      this.error = res.status
    }
  },
}