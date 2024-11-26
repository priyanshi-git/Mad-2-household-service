export default {
  template: `
  <div>
    <h2 class="headings" id="professionals">Professionals for {{ serviceName }}</h2>
    <div v-if="professionals.length === 0">
      <h4>No Professionals Available.</h4>
    </div>
    <div v-else>
      <table class="table table-bordered table-hover">
        <thead class="thead-dark">
          <tr>
            <th scope="row">S. No.</th>
            <th scope="col">Name</th>
            <th scope="col">Experience</th>
            <th scope="col">Email</th>
            <th scope="col">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(prof, index) in professionals" :key="prof.id">
            <th scope="row">{{ index + 1 }}</th>
            <td>{{ prof.name }}</td>
            <td>{{ prof.experience }}</td>
            <td>{{ prof.email }}</td>
            <td>
              <button class="btn btn-primary" @click="bookService(prof.id)">Book</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  `,

  data() {
    return {
      professionals: [],
      serviceName: "",
      token: localStorage.getItem('auth-token'),
    };
  },

  methods: {
    async bookService(profID) {
      const serviceId = this.$route.params.id; // Service ID from route
      const response = await fetch(`/service/${serviceId}/book`, {
        method: 'POST',
        headers: {
          'Authentication-Token': this.token,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          "professional_id": profID
        }),
      });

      const data = await response.json();
      if (response.ok) {
        alert(data.message);
        this.$router.push({ path: '/' });
      } else {
        alert(data.message || 'Error booking service');
        this.$router.push({ path: '/' });
      }
    },
  },

  async mounted() {
    const serviceId = this.$route.params.id; // Get service ID from route
    const response = await fetch(`/service/${serviceId}/professionals`, {
      method: 'GET',
      headers: {
        'Authentication-Token': this.token,
      },
    });

    if (response.ok) {
      const data = await response.json();
      this.professionals = data;
      this.serviceName = data.length > 0 ? data[0].service_name : "Unknown Service";
    } else {
      alert('Error fetching professionals');
    }
  },
};
