import store from "../utils/store.js";

const Navbar = {
  template: `
  <nav class="h3 w-auto d-flex justify-content-between">
  <router-link to='/'>Home</router-link>
  <router-link v-if="!loggedIn" to='/login'>Login</router-link>
  <router-link v-if="!loggedIn" to='/signup'>Signup</router-link>
  <router-link v-if="loggedIn" to='/dashboard'>Dashboard</router-link>
  <a v-if="loggedIn" :href="url">Logout</a>
  </nav>
  `,
  data(){
    return{
      loggedIn: store.state.loggedIn,
      url : window.location.origin + "/logout",
    };
    },
  computed: {
    computedlog() {
      return loggedIn = store.state.loggedIn;
      return loggedIn;
    },
  },
};

export default Navbar;