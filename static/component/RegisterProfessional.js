export default {
  template: `
    <div class="d-flex justify-content-center align-items-center vh-100">
      <div class="card shadow p-5">
        <h3 class="card-title text-center mb-4">Professional Sign Up</h3>
        <div class="form-group mb-3">
          <input v-model="name" type="name" class="form-control" placeholder="Name" required/>
        </div>
        <div class="form-group mb-3">
          <input v-model="email" type="email" class="form-control" placeholder="Email" required/>
        </div>
        <div class="form-group mb-4">
          <input v-model="password" type="password" class="form-control" placeholder="Password" required/>
        </div>
        <div class="form-group mb-4">
          <select v-model="service" class="form-control" required>
            <option value="" disabled selected>Select a Service</option>
            <option v-for="(service, index) in allServices">
              {{ service.name }}
            </option>
          </select>
        </div>
        <div class="form-group mb-3">
          <input v-model="experience" type="experience" class="form-control" placeholder="Experience" required/>
        </div>
        <div class="form-group mb-3">
          <input v-model="pincode" type="pincode" class="form-control" placeholder="Pincode" required/>
        </div>
        <button class="btn btn-primary w-100" @click="register">Register</button>
        <div class="text-danger">{{ error }}</div>
      </div>
    </div>
  `,
  data() {
    return {
      name: "",
      email: "",
      password: "",
      service: "",
      experience: "",
      pincode: "",
      role: "professional",
      error: null,
      allServices: null,
    };
  },
  methods: {
    async register() {
      const origin = window.location.origin;
      const url = `${origin}/registerprofessional`;
      const res = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: this.email,
          name: this.name,
          password: this.password,
          service: this.service,
          experience: this.experience,
          pincode: this.pincode,
          role: this.role,
        }),
        credentials: "same-origin",
      });

      const data = await res.json();
      if (res.ok) {
        console.log(data);
        // Handle successful sign up, e.g., redirect or store token
        this.$router.push({path: '/login'})
      } else {
        this.error = data.message
        // Handle sign up error
      }
    },

    async fetchedservices(){
      const res = await fetch('/api/services', {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        }})
      const data = await res.json().catch((e)=> {})
      if(res.ok){
        this.allServices = data
      }else{
        this.error = res.status
      }
    },
  },
  created() {
    this.fetchedservices(); // Fetch services when the component is created
  },
};