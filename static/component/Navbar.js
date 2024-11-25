export default {
  template: `
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
  <div class="container-fluid">
    <span class="navbar-brand" v-if="role==null">Welcome to Household Services</span>
    <span class="navbar-brand" v-if="role=='admin'">Welcome to Admin</span>
    <span class="navbar-brand" v-if="role=='user'">Welcome to User</span>
    <span class="navbar-brand" v-if="role=='professional'">Welcome to Professional</span>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse justify-content-end" id="navbarSupportedContent">
      <ul class="navbar-nav">
        <li class="nav-item">
          <router-link class="nav-link active" aria-current="page" to="/">Home</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/users">User</router-link>
        </li>
        <li class="nav-item text-end" v-if='is_login'>
          <button class="nav-link" aria-current="page" @click='logout' href="#"> Logout</button>
        </li>
      </ul>
    </div>
  </div>
</nav>
  `,
  data(){
    return {
      role: localStorage.getItem('role'),
      is_login: localStorage.getItem('auth-token'),
    }
  },
  methods: {
    logout(){
      localStorage.removeItem('auth-token')
      localStorage.removeItem('role')
      this.$router.push({path: '/login'})
    },
  },
}