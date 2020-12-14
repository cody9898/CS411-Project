<template>
  <div>
    <v-row no-gutters>
      <v-col
        cols="6"
        md="4"
      >
        <v-col
          cols="3"
          md="12"
        >
          <v-row>
          Your location is {{center.lat}}, {{center.lng}}
          <v-spacer></v-spacer>
          <v-btn small > Change Location </v-btn>
          </v-row>
          <v-text-field
            v-model="form.keyword"
            label="Solo"
            placeholder="Search nearby businesses"
            solo
            @keydown.enter="getSearchResults()"
            clearable
          ></v-text-field>
          <div v-if="loaded">
            <v-data-table
              :headers="headers"
              :items="results"
              :items-per-page="20"
              @click:row="handleClick"
              class="elevation-1"
            ></v-data-table>
          </div>
        </v-col>
      </v-col>
      <v-col
        cols="12"
        sm="6"
        md="8"
      >
        <gmap-map class="map"
        :center="center"
        :zoom="12"
        >
        <gmap-marker  :position="center" />
        </gmap-map>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Search',
  data() {
    return {
      headers: [
      {
          text: 'Name',
          align: 'start',
          sortable: false,
          value: 'name',
      }
      ],
      results: [],
      loaded: false,
      center: {lat: 42.351775, lng: -71.128863},
      form: {
        lat: 0,
        lng: 0,
        radius: 1000,
        keyword: ""
      }
    };
  },
  methods: {
    getSearchResults() {
      this.form.lat = this.center.lat;
      this.form.lng = this.center.lng;
      const path = 'http://localhost:5000/search';
      const config = {
        headers: { 'content-type': 'application/x-www-form-urlencoded' }
      }
      const getParams = (obj) => {
          const params = new URLSearchParams();
          const keys = Object.keys(obj);
          for(let k of keys){
              params.append(k, obj[k]);
          }
          return params;
      }
      axios.post(path, getParams(this.form), config)
        .then((res) => {
          this.results = [];
          var data = JSON.parse(res.data);
          console.log(data.results[0])
          for (var i = 0; i < data.results.length; i++) {
            this.results.push(data.results[i]);
          }
          this.loaded = true;
        })
        .catch((error) => {
            console.error(error);
        });
    },
    handleClick(place) {
      console.log(place.place_id)
      this.$router.push({path: `/location/${place.place_id}`})
    }
  }
};
</script>

<style scoped>
  .map {
    width: 100%;
    height: 750px;
  }
</style>