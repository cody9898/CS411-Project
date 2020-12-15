<template>
  <form><v-form
    ref="form"
    @submit.prevent="process"
    method = "POST"
    action = "/signup"
    >

    <v-text-field
      label="Name"
      v-model = "form.name"
      name = "name"
      required
    ></v-text-field>

    <v-text-field
      label="E-mail"
      v-model = "form.email"
      name = "email"
      required
    ></v-text-field>

    <v-text-field
      label="password"
      :type="'password'"
      v-model = "form.password"
      name = "password"
      required
    ></v-text-field>

    <button type="submit"><v-btn
      color="success"
      class="mr-4"
    >
      Sign Up!
    </v-btn></button>

  </v-form></form>
</template>

<script>
import axios from 'axios'
export default {
  name: 'Signup',
  data() {
    return {
      form: {
      name: '',
      email: '', 
      password: ''
      }
    };
  },
methods: {
  process(){
    const data = {name: this.form.name, email: this.form.email, password: this.form.password};
    const path = 'http://localhost:5000/signup';
    axios.post(path, data)
    .then(response => {
      var jname = JSON.parse(response.config.data.name)
      console.log(jname);
    })
    .catch(e => {
      console.error(e);
    });
  }
}

};
</script>

<style scoped>
</style>