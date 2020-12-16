<template>
  <form>
  <v-form
    ref="form"
    v-model="valid"
    lazy-validation
  >

    <v-text-field
      v-model="email"
      :rules="emailRules"
      label="E-mail"
      required
    ></v-text-field>

    <v-text-field
      v-model="password"
      label="password"
      :type="'password'"
      required
    ></v-text-field>
    
        <button><v-btn
      color="success"
      class="mr-4"
    >
      Log In!
    </v-btn></button>

  </v-form></form>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Login',
  data() {
    return {
      email: '', 
      password: '',
    };
  },
  methods: {
    getInfo() {
    const path = 'http://localhost:5000/login';
    axios.get(path)
        .then((res) => {
            this.email = res.data.email;
            this.password = res.data.password;
        }) 
        .catch((error) => {
            console.error(error);
        });
    },
  },
  created() {
    this.getInfo();
  }
};
</script>

<style scoped>
</style>