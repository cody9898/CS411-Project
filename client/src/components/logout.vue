<template>
  <div>
    {{this.msg}}
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Logout',
  data() {
    return {
      msg: 'logout',
    };
  },
  methods: {
    getMessage() {
    const path = 'http://localhost:5000/logout';
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