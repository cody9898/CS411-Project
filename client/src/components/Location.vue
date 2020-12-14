<template>
  <div>
    {{placeid}}
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
    console.log(this.placeid)
  }
}
</script>

<style scoped>

</style>