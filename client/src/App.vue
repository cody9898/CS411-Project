<template>
  <v-app dark>
    <v-app-bar
      app
      dense
      dark
    >

      <v-toolbar-items>
        <v-btn
        depressed
        class="title"
        >
        <v-img
          alt="Map Pin Logo"
          class="shrink mr-4"
          contain
          src="@/assets/map-pin-icon.png"
          transition="scale-transition"
          width="20"
        />
        Covid Meter
        </v-btn>
        <v-btn
        depressed
        
        >
        
        </v-btn>
      </v-toolbar-items>

      <v-spacer></v-spacer>

    </v-app-bar>

    <v-main>
      <router-view/>
    </v-main>

  </v-app>
</template> 

<script>

export default {
  name: 'App',

  data: () => ({
    //
  }),
};
</script>

<style scoped>
  *{ text-transform: none !important; } 
  .v-text-field .v-input__control .v-input__slot {
    min-height: fit-content !important;
  }
</style>