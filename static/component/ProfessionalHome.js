export default {
  template: `
  <div> 
  <! -- ------------------------------------ SERVICE Request TABLE ------------------------------------------------------- -->
    <h2 class="headings" id="reqservices">Requested Services</h2>
    <div v-if="reqs == []">
      <h4>No Current Requests.</h4>
    </div>
    <div v-else>
      <table class="table table-bordered table-hover">
        <thead class="thead-dark">
          <tr>
            <th scope="row">S. No.</th>
            <th scope="col">Customer Name</th>
            <th scope="col">Date Requested</th>
            <th scope="col">Pincode</th>
            <th scope="col">Actions</th>
          </tr>
        </thead>
        <tbody class="table-group-divider">
          <tr v-for="(req, index) in reqs" :key="req.id">
            <th scope="row">{{ index+1 }}</th>
            <td>{{ req.customer_name }}</td>
            <td>{{ req.date_requested }}</td>
            <td>{{ req.pincode }}</td>
            <td>
              <div v-if="req.service_status === 'Pending'">
                <button type="button" class="btn btn-primary" @click="acceptService(req.id)">Accept</button>
                <button type="button" class="btn btn-danger" @click="rejectService(req.id)">Reject</button>
              </div>
              <div v-else>
                {{ req.service_status }}
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  <! -- ------------------------------------ SERVICE Request TABLE ------------------------------------------------------- -->
  <! -- ------------------------------------ CLOSED service TABLE --------------------------------------------------------- -->
    <h2 class="headings" id="reqservices">Closed Services</h2>
    <div>
      <table class="table table-bordered table-hover">
        <thead class="thead-dark">
          <tr>
            <th scope="row">S. No.</th>
            <th scope="col">Customer Name</th>
            <th scope="col">Date Requested</th>
            <th scope="col">Pincode</th>
            <th scope="col">Status</th>
          </tr>
        </thead>
        <tbody class="table-group-divider">
          <tr v-for="(req, index) in reqs" :key="req.id" v-if="req.service_status == 'Closed'">
            <th scope="row">{{ index+1 }}</th>
            <td>{{ req.customer_name }}</td>
            <td>{{ req.date_requested }}</td>
            <td>{{ req.pincode }}</td>
            <td>{{ req.service_status }}</td>
          </tr>
        </tbody>
      </table>
    </div>


  </div>`,

  data() {
    return {
      reqs: null,
      token: localStorage.getItem('auth-token'),
      role: localStorage.getItem('role'),
      error: null,
    };
  },

  async mounted() {
    const r_response = await fetch('/professional/service-requests', {
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

  methods: {
    async rejectService(reqID) {
      const response = await fetch(`/close/${reqID}`, {
        method: "PUT",
        headers: {
          "Authentication-Token": this.token,
        },
      });

      const data = await response.json();
      if (response.ok) {
        alert(data.message);

        // Dynamically update the local reqs array
        const reqIndex = this.reqs.findIndex((req) => req.id === reqID);
        if (reqIndex !== -1) {
          this.reqs[reqIndex].service_status = "Closed";
        }
      } else {
        alert(`Failed to reject the service: ${data.message}`);
      }
    },

    async acceptService(reqID) {
      const response = await fetch(`/accept/${reqID}`, {
        method: "PUT",
        headers: {
          "Authentication-Token": this.token,
        },
      });

      const data = await response.json();
      if (response.ok) {
        alert(data.message);

        // Dynamically update the local reqs array
        const reqIndex = this.reqs.findIndex((req) => req.id === reqID);
        if (reqIndex !== -1) {
          this.reqs[reqIndex].service_status = "Ongoing";
        }
      } else {
        alert(`Failed to reject the service: ${data.message}`);
      }
    },
  },
};