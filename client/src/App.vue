<template>
  <div id="app">

    <div>
      <b-navbar toggleable="lg" type="dark" variant="dark">
        <b-navbar-brand href="#">ISU-Avista</b-navbar-brand>

        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

        <b-collapse id="nav-collapse" is-nav>
          <b-navbar-nav>
            <b-nav-item to="/" v-if="currentUser">
              <b-icon icon="house-fill"/>&nbsp;&nbsp;Overview
            </b-nav-item>
            <b-nav-item to="/monitor" v-if="currentUser">
              <b-icon icon="display-fill"/>&nbsp;&nbsp;Monitor
            </b-nav-item>
            <b-nav-item to="/issues" v-if="currentUser">
              <b-icon icon="bug-fill"/>&nbsp;&nbsp;Issues
            </b-nav-item>
            <b-nav-item to="/action" v-if="currentUser">
              <b-icon icon="gear-wide"/>&nbsp;&nbsp;Action
            </b-nav-item>
            <b-nav-item to="/config" v-if="currentUser && administrator">
              <b-icon icon="list-check"/>&nbsp;&nbsp;Configuration
            </b-nav-item>
            <b-nav-item to="/about">
              <b-icon icon="info-circle"/>&nbsp;&nbsp;About
            </b-nav-item>
          </b-navbar-nav>

          <b-navbar-nav class="ml-auto">
            <!--<b-nav-form>
              <b-input-group size="sm">
                <b-input-group-prepend is-text>
                  <b-icon icon="search"/>
                </b-input-group-prepend>
                <b-form-input size="sm" class="mr-sm-2" placeholder="Search"></b-form-input>
              </b-input-group>
              <b-button size="sm" class="my-2 my-sm-0" type="submit">Search</b-button>
            </b-nav-form>-->

            <b-nav-item-dropdown right v-if="currentUser">
              <template #button-content>
                <b-icon icon="person-circle"/> {{ userName }}
              </template>

              <b-dropdown-item to="/profile">
                <b-icon icon="person-lines-fill"/>&nbsp;&nbsp;Profile
              </b-dropdown-item>
              <b-dropdown-item href="#" @click="signout">
                <b-icon icon="door-closed"/>&nbsp;&nbsp;Sign Out
              </b-dropdown-item>
            </b-nav-item-dropdown>

            <b-nav-item v-if="!currentUser" to="/login">
              <b-icon icon="gear-fill"/>&nbsp;&nbsp;Login
            </b-nav-item>

          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
    </div>

    <div class="content">
      <router-view/>
    </div>

    <footer class="footer">
      <div class="fluid-container">
        <p class="text-right"><img alt="Vue logo" src="./assets/bengal.png" height="100px"></p>
        <span class="text-muted">Copyright &copy; 2020-2021 Idaho State University
         Empirical Software Engineering Laboratory</span>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  computed: {
    currentUser() {
      return this.$store.state.auth.user;
    },
    userName() {
      const fname = this.$store.state.auth.user.first_name;
      const lname = this.$store.state.auth.user.last_name;
      return `${fname} ${lname}`;
    },
    administrator() {
      return this.$store.state.auth.user.role === 'ADMIN';
    },
  },
  methods: {
    signout() {
      if (this.currentUser) {
        this.$store.dispatch('auth/logout').then(
          () => {
            this.$router.push('/login');
          },
          (error) => {
            // eslint-disable-next-line
            console.log(error);
          },
        );
      }
    },
  },
};
</script>

<style>
html, body {
  height: 100%;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  display: flex;
  flex-direction: column;
  height: 100%;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

.content {
  flex: 1 0 auto;
  padding: 20px;
}

.footer {
  flex-shrink: 0;
  width: 100%;
  padding-top: 10px;
  margin-bottom: 0;
  background: #222;
}

</style>
