import Home from './component/Home.js'
import Login from './component/Login.js'
import Users from './component/Users.js'
import RegisterUser from './component/RegisterUser.js'
import RegisterProfessional from './component/RegisterProfessional.js'
import ServiceResourceForm from './component/ServiceResourceForm.js'
import EditService from './component/EditService.js'

const routes = [
  {path:'/', component: Home, name: "Home"},
  {path:'/login', component: Login, name:"Login"},
  {path: '/users', component: Users},
  { path : '/registeruser', component : RegisterUser },
  { path : '/registerprofessional', component : RegisterProfessional },
  { path : '/createservice', component : ServiceResourceForm },
  { path : '/editservice/:service_id', component : EditService },
]

export default new VueRouter({
  routes,
})