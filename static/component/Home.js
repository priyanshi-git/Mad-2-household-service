import AdminHome from "./AdminHome.js"
import UserHome from "./UserHome.js"
import ProfessionalHome from "./ProfessionalHome.js"

export default {
  template: `<div> 
  <UserHome v-if="userRole=='user'"/>
  <AdminHome v-if="userRole=='admin'"/>
  <ProfessionalHome v-if="userRole=='professional'"/>
  </div>`,

  data(){
    return {
      userRole: localStorage.getItem('role'),
    }
  },

  components: {
    UserHome,
    ProfessionalHome,
    AdminHome,
  }
}