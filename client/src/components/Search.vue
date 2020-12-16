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
          <div v-if="center == null"> 
            {{status}}
          </div>
          <div v-else> Your location is {{this.myAddressStr}} </div>
          <v-btn small v-on:click="setLocationDialog = true"> Change Location </v-btn>
          </v-row>
          <v-text-field
            v-model="query.keyword"
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
              :items-per-page="9"
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
        <div v-if="center == null"> 
          <gmap-map class="map"
            :center="{lat:29.590190,lng: -31.428414}"
            :zoom="2"
          ></gmap-map>
        </div>
        <div v-else>
          <gmap-map class="map"
            :center="center"
            :zoom="13"
          >
          <gmap-marker
            :key="index"
            v-for="(result, index) in results"
            :position="result.geometry.location"
            @click="handleClick"
          ></gmap-marker>
          <gmap-marker  :position="center" />
          </gmap-map>
        </div>
      </v-col>
    </v-row>

    <v-dialog
      v-model="setLocationDialog"
      persistent
      max-width="80%">
      <v-card>
        <v-card-title>
          Enter your current location to get nearby results
        </v-card-title>

        <v-card-text>
          <v-container>
            <div v-if="invalidAddress"> Please enter a valid address! </div>
            <v-row>
              <v-text-field
                v-model="myAddress.myStreet"
                label="Solo"
                placeholder="Street"
                solo
              ></v-text-field>
            </v-row>
            <v-row>
              <v-text-field
                v-model="myAddress.myCity"
                label="Solo"
                placeholder="City"
                solo
              ></v-text-field>
            </v-row>
            <v-row>
              <v-text-field
                v-model="myAddress.myState"
                label="Solo"
                placeholder="State 2 letter abbreviation"
                solo
              ></v-text-field>
            </v-row>
          </v-container>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="setCoords">Set location</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
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
      center: null,
      myAddress: {
        myStreet: "",
        myCity: "",
        myState: "",
      },
      myAddressStr: "",
      query: {
        lat: 0,
        lng: 0,
        radius: 4000,
        keyword: ""
      },
      setLocationDialog: false,
      invalidAddress: false,
      status: "Locating your position..."
    };
  },
  methods: {
    getSearchResults() {
      this.query.lat = this.center.lat;
      this.query.lng = this.center.lng;
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
      var form = this.query
      axios.post(path, getParams(form), config)
        .then((res) => {
          this.results = [];
          var data = JSON.parse(res.data);
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
    },
    setCoords() {
      const path = 'http://localhost:5000/address_to_coords';
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
      var form = this.myAddress
      axios.post(path, getParams(form), config)
        .then((res) => {
          // set coords as first api result
          var data = JSON.parse(res.data);
          if (data.results.length > 0) {
            this.setAddress()
            this.center = {lat:data.results[0].geometry.location.lat, lng:data.results[0].geometry.location.lng}
            this.setLocationDialog = false;
          } else {
            this.invalidAddress = true;
          }
        })
        .catch((error) => {
            console.error(error);
        });
    },
    getAddress() {
      const path = 'http://localhost:5000/coords_to_address';
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
      var form = this.center
      axios.post(path, getParams(form), config)
        .then((res) => {
          // set address as first api result
          var data = JSON.parse(res.data);
          this.myAddressStr = data.results[0].formatted_address
        })
        .catch((error) => {
            console.error(error);
        });
    },
    setAddress() {
      this.myAddressStr = this.myAddress.myStreet + ", " + this.myAddress.myCity + ", " + this.myAddress.myState
    }
  },
  created() {
    // check geolocation support
    if(!("geolocation" in navigator)) {
      console.log('Geolocation is not available.');
      this.status = "Cannot detect your location automatically.";
      return;
    }

    // get location
    navigator.geolocation.getCurrentPosition(pos => {
      this.center = {lat:pos.coords.latitude,lng:pos.coords.longitude}
      this.getAddress()
    }, err => {
      // ask user to enter location manually
      this.status = "Cannot detect your location automatically.";
      console.log(err,"error getting location!")
    })
  }
};
</script>

<style scoped>
  .map {
    width: 100%;
    height: 750px;
  }
</style>