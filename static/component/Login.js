export default {
  template: `
    <div class="d-flex justify-content-center" style="margin-top: 30vh">
  <div class="mb-3 p-5 bg-light">
    <div class="d-flex justify-content-end mb-2">
      <button type="button" class="btn btn-link" @click="register_professional">Register as Professional</button>
    </div>

    <div class="text-danger">{{ error }}</div>
    <label for="user-email" class="form-label">Email address</label>
    <input type="email" class="form-control" id="user-email" placeholder="name@example.com" v-model="cred.email">
    <label for="user-password" class="form-label">Password</label>
    <input type="password" class="form-control" id="user-password" v-model="cred.password">
    <button class="btn btn-primary mt-2" @click="login">Login</button>
    <br>
    <div class="container vh-60 d-flex justify-content-center align-items-center">
      <div class="form-group text-center">
        <button type="button" class="btn btn-link" @click="register_user">Create New Account?</button>
      </div>
    </div>
  </div>
</div>

`,

  data(){
    return {
      cred:{
        "email": null,
        "password": null,
      },
      error: null,
    }
  },

  methods: {
    async login() {
      const res = await fetch('/user-login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.cred),
      })
      const data = await res.json()
      if (res.ok){
        localStorage.setItem('auth-token', data.token)
        localStorage.setItem('role', data.role)
        this.$router.push({path: '/'})
      }
      else{
        this.error = data.message
      }
    },
    register_user() {
      this.$router.push('/registeruser')
    },
    register_professional() {
      this.$router.push('/registerprofessional')
    },
  },
}