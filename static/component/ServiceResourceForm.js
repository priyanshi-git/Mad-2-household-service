export default {
  template: `<div class="container mt-5">
    <div class="card shadow p-4">
      <h3 class="text-center mb-4" >Add New Service</h3>
      <form @submit.prevent="createService">
        <div class="mb-3">
          <label for="serviceName" class="form-label">Service Name</label>
          <input 
            type="text" 
            id="serviceName" 
            class="form-control" 
            placeholder="Enter service name" 
            v-model="resource.name" 
            required
          />
        </div>
        <div class="mb-3">
          <label for="serviceDescription" class="form-label">Description</label>
          <textarea 
            id="serviceDescription" 
            class="form-control" 
            rows="3" 
            placeholder="Enter service description" 
            v-model="resource.description" 
            required
          ></textarea>
        </div>
        <div class="mb-3">
          <label for="servicePrice" class="form-label">Price</label>
          <input 
            type="number" 
            id="servicePrice" 
            class="form-control" 
            placeholder="Enter price" 
            v-model="resource.price" 
            required
          />
        </div>
        <div class="d-grid">
          <button type="submit" class="btn btn-primary">Add Service</button>
        </div>
      </form>
    </div>
  </div>`,

  data(){
    return {
      resource: {
        name: null,
        description: null,
        price: null,
      },
      token: localStorage.getItem("auth-token")
    }
  },

  methods: {
    async createService() {
      const res = await fetch('/api/services', {
        method: "POST",
        headers: {
          "Authentication-Token": this.token,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(this.resource),
      })

      const data = await res.json()
      if(res.ok){
        alert(data.message)
        this.$router.push({path: '/'})
      }
    },
  },
}