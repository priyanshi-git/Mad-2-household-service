export default {
  template: `
  <div> 
  <! -- ------------------------------------------ SERVICE TABLE ----------------------------------------------------------- -->
    <h2 class="headings" id="services">Services</h2>
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
              <router-link :to="'/service/' + service.id + '/professionals'" class="btn btn-primary">View Providers</router-link>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  <! -- ------------------------------------------ SERVICE TABLE ----------------------------------------------------------- -->
  <! -- ------------------------------------------ HISTORY TABLE ----------------------------------------------------------- -->

    <h2 class="headings" id="requests">Service History</h2>
    <div v-if="reqs.length === 0">
      <h4>No Services Requests.</h4>
    </div>
    <div v-else>
      <table class="table table-bordered table-hover">
        <thead class="thead-dark">
          <tr>
            <th scope="row">S. No.</th>
            <th scope="col">Service Name</th>
            <th scope="col">Professional Name</th>
            <th scope="col">Date Requested</th>
            <th scope="col">Status</th>
          </tr>
        </thead>
        <tbody class="table-group-divider">
          <tr v-for="(req, index) in reqs" :key="req.id">
            <th scope="row">{{ index+1 }}</th>
            <td>{{ req.service_name }}</td>
            <td>{{ req.professional_name }}</td>
            <td>{{ req.date_requested }}</td>
            <td>{{ req.user_status }}</td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>`,

  data() {
    return {
      services: null,
      reqs: null,
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

    const r_response = await fetch('/user/service-requests', {
      method: 'GET',
      headers: {
        'Authentication-Token': this.token,
      },
    });
    const r_data = await r_response.json().catch((e) => {});
    if (r_response.ok) {
      this.reqs = r_data;
    } else {
      this.error = r_response.status;
    }
  },
};