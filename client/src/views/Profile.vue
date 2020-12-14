<template>
  <b-container class="text-left">
    <b-jumbotron class="text-center">
      <template #header>
        {{ currentUser.first_name }} {{ currentUser.last_name }}
      </template>
    </b-jumbotron>
    <p>
      <strong>Token:</strong>
      {{ currentUser.token.substring(0, 20) }} ...
      {{ currentUser.token.substr(currentUser.token.length - 20) }}
    </p>
    <p>
      <strong>Email:</strong>
      {{ currentUser.email }}
    </p>
    <strong>Roles:</strong>
    <ul>
      <li v-for="(role,index) in currentUser.roles" :key="index">{{role}}</li>
    </ul>
  </b-container>
</template>

<script>
export default {
  name: 'Profile',
  computed: {
    currentUser() {
      return this.$store.state.auth.user;
    },
  },
  mounted() {
    if (!this.currentUser) {
      this.$router.push('/login');
    }
  },
};
</script>
