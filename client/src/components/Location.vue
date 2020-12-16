<template>
  <div>
    <v-container>
      <h1> {{status}} </h1>
    </v-container>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Location',
  data() {
    return {
      placeid: "",
      status: ""
    }
  },
  created() {
    this.placeid = this.$route.params.placeid;
    const path = 'http://localhost:5000/info/'+this.placeid;
    console.log(path);
    axios.get(path)
        .then((res) => {
          // set address as first api result
          console.log(res.data)
          this.status = res.data;
        })
        .catch((error) => {
            console.error(error);
        });
  }
}
</script>

<style scoped>

</style>