<template>
  <div>
    Welcome, Stephany!
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Profile',
  data() {
    return {
      msg: 'profile',
    };
  },
  methods: {
    getMessage() {
    const path = 'http://localhost:5000/profile';
    axios.get(path)
        .then((res) => {
            this.msg = res.data;
        })
        .catch((error) => {
            console.error(error);
        });
    },
  },
  created() {
    this.getMessage();
  }
};
</script>

<style scoped>
</style>