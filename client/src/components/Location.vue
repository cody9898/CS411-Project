<template>
  <div>
    <v-container>
      <h1> Place id = {{placeid}} </h1>
    </v-container>
  </div>
</template>

<script>
export default {
  name: 'Location',
  data() {
    return {
      placeid: ""
    }
  },
  created() {
    this.placeid = this.$route.params.placeid
    //const path = 'http://localhost:5000/';
  }
}
</script>

<style scoped>

</style>