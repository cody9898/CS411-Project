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
  }
}
</script>

<style scoped>

</style>