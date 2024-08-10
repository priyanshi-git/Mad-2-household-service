import BookResource from "../components/BookResources.js";

const DashboardStud = {
  template: `<div>
            <h1>This is Student dashboard</h1>
              <div v-for="resource in allResources">
                <BookResource :book_title="resource.b_title" :section="resource.b_section" :author="resource.b_author"/>
              </div>
          </div>`,
  data() {
    return {
      allResources: [],
    };
  },
  async mounted() {
    const res = await fetch(window.location.origin + '/api/books', {
      
    });
    const data = await res.json();
    this.allResources = data;
  },
  components: { BookResource },
};

export default DashboardStud;