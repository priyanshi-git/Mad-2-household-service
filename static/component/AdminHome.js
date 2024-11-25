export default {
  template: `
  <div> 
  <! -- ------------------------------------------ SERVICE TABLE ----------------------------------------------------------- -->
    <h2 class="headings" id="books">Services</h2>
    <div class="">
      <router-link to="/createservice">Add New Service</router-link>
    </div>
    <div v-if="services.length === 0">
      <h4>No Services Available.</h4>
    </div>
    <div v-else>
      <table class="table table-bordered table-hover">
        <thead class="thead-dark">
          <tr>
            <th scope="row">S. No.</th>
            <th scope="col">Service Name</th>
            <th scope="col">Description</th>
            <th scope="col">Base Price</th>
            <th scope="col">Action</th>
          </tr>
        </thead>
        <tbody class="table-group-divider">
          <tr v-for="(service, index) in services" :key="service.id">
            <th scope="row">{{ index+1 }}</th>
            <td>{{ service.name }}</td>
            <td>{{ service.description }}</td>
            <td>{{ service.price }}</td>
            <td>
              <router-link :to="'/editservice/' + service.id" class="btn btn-primary">Edit</router-link>
              <button type="button" class="btn btn-danger" @click="deleteService(service.id)">
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  <! -- ------------------------------------------ SERVICE TABLE ----------------------------------------------------------- -->
  <! -- --------------------------------------- PROFESSIONAL TABLE --------------------------------------------------------- -->

  <h2 class="headings" id="books">Professionals</h2>
    <div v-if="professionals.length === 0">
      <h4>No Professionals Available.</h4>
    </div>
    <div v-else>
      <table class="table table-bordered table-hover">
        <thead class="thead-dark">
          <tr>
            <th scope="row">S. No.</th>
            <th scope="col">Name</th>
            <th scope="col">Experience (in yrs)</th>
            <th scope="col">Service Name</th>
            <th scope="col">Action</th>
          </tr>
        </thead>
        <tbody class="table-group-divider">
          <tr v-for="(prof, index) in professionals" :key="prof.id">
            <th scope="row">{{ index+1 }}</th>
            <td>{{ prof.name }}</td>
            <td>{{ prof.experience }}</td>
            <td>{{ prof.service }}</td>
            <td>
              <button class="btn btn-primary" v-if='!prof.active' @click="approve(prof.id)"> Approve </button>
              <button v-if='!prof.active' type="button" class="btn btn-danger" @click="deleteProf(prof.id)">Reject</button>
              <button v-if='prof.active' type="button" class="btn btn-danger" @click="deleteProf(prof.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>`,

  data() {
    return {
      services: null,
      professionals: null,
      token: localStorage.getItem('auth-token'),
      role: localStorage.getItem('role'),
      error: null,
    };
  },

  async mounted() {
    const s_response = await fetch('/services', {
      method: 'GET',
      headers: {
        'Authentication-Token': this.token,
      },
    });
    const s_data = await s_response.json().catch((e) => {});
    if (s_response.ok) {
      this.services = s_data;
    } else {
      this.error = s_response.status;
    }

    const p_response = await fetch('/get_professionals', {
      method: 'GET',
      headers: {
        'Authentication-Token': this.token,
      },
    });
    const p_data = await p_response.json().catch((e) => {});
    if (p_response.ok) {
      this.professionals = p_data;
    } else {
      this.error = p_response.status;
    }

  },

  methods: {
    async deleteService(serviceID) {
      if (confirm("Are you sure you want to delete this service?")) {
        const res = await fetch(`/delete/services/${serviceID}`, {
          method: "DELETE",
          headers: {
            "Authentication-Token": this.token,
            "Content-Type": "application/json",
          },
        });

        if (res.ok) {
          const data = await res.json();
          alert(data.message);

          // Remove the deleted service from the list
          this.services = this.services.filter(
            (service) => service.id !== serviceID
          );
        } else {
          const errorData = await res.json();
          alert(`Error: ${errorData.message}`);
        }
      }
    },

    async approve(userID) {
      const res = await fetch(`/activate/user/${userID}`, {
        headers: {
          "Authentication-Token": this.token,
        },
      });
      const data = await res.json();
      if (res.ok) {
        alert(data.message);
    
        // Update the `active` status of the approved professional
        const professional = this.professionals.find((prof) => prof.id === userID);
        if (professional) {
          professional.active = true; // Update the status to active
        }
      } else {
        alert(`Error: ${data.message}`);
      }
    },

    async deleteProf(profID) {
      if (confirm("Are you sure you want to delete this professional?")) {
        const res = await fetch(`/delete/professional/${profID}`, {
          method: "DELETE",
          headers: {
            "Authentication-Token": this.token,
            "Content-Type": "application/json",
          },
        });
    
        if (res.ok) {
          const data = await res.json();
          alert(data.message);
    
          // Remove the professional from the list
          this.professionals = this.professionals.filter(
            (prof) => prof.id !== profID
          );
        } else {
          const errorData = await res.json();
          alert(`Error: ${errorData.message}`);
        }
      }
    }
    ,
  },
};
