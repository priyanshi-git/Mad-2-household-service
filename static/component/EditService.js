export default {
  template: `<div class="container mt-5">
    <div class="card shadow p-4">
      <h3 class="text-center mb-4">Edit Service</h3>
      <form @submit.prevent="updateService">
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
          <button type="submit" class="btn btn-primary">Save Changes</button>
        </div>
      </form>
    </div>
  </div>`,

  data() {
    return {
      resource: {
        name: null,
        description: null,
        price: null,
      },
      token: localStorage.getItem("auth-token"),
    };
  },

  async created() {
    const serviceId = this.$route.params.service_id; // Get the service ID from the route
    try {
      const response = await fetch(`/services/${serviceId}`, {
        method: "GET",
        headers: {
          "Authentication-Token": this.token,
        },
      });

      if (response.ok) {
        this.resource = await response.json();
      } else {
        alert("Failed to fetch the service details.");
      }
    } catch (error) {
      console.error("Error fetching service:", error);
    }
  },

  methods: {
    async updateService() {
      const serviceId = this.resource.id; // Use the ID from the resource object
      try {
        const response = await fetch(`/update_service/${serviceId}`, {
          method: "PUT",
          headers: {
            "Authentication-Token": this.token,
            "Content-Type": "application/json",
          },
          body: JSON.stringify(this.resource),
        });

        const data = await response.json();
        if (response.ok) {
          alert(data.message);
          this.$router.push({ path: '/' });
        } else {
          alert(`Failed to update the service: ${data.message}`);
        }
      } catch (error) {
        console.error("Error updating service:", error);
      }
    },
  },
};
