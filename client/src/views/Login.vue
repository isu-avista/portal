<template>
  <b-container class="col-6 col-md-4">
    <br/>
    <b-card title="Login">
      <b-card-sub-title class="error-msg">{{ message }}</b-card-sub-title>
      <b-form @submit.prevent="handleLogin" class="w-100">
        <b-form-row>
          <b-input-group class="mb-2 mr-sm-2 mb-sm-0">
            <b-input-group-prepend is-text>
              <b-icon icon="envelope-fill"/>
            </b-input-group-prepend>
            <b-form-input id="inline-form-input-email" placeholder="E-mail"
                          v-model="user.email" type="text" required>
            </b-form-input>
          </b-input-group>
        </b-form-row>
        <br/>
        <b-form-row>
          <b-input-group class="mb-2 mr-sm-2 mb-sm-0">
            <b-input-group-prepend is-text>
              <b-icon icon="lock-fill"/>
            </b-input-group-prepend>
            <b-form-input prepend="" id="form-password-input" type="password"
                          v-model="user.password" placeholder="Password" required />
          </b-input-group>
        </b-form-row>
        <br/>
        <b-form-row>
          <b-col align-self="end">
            <b-button-group>
              <b-button type="submit" variant="primary">Login</b-button>
            </b-button-group>
          </b-col>
        </b-form-row>
      </b-form>
    </b-card>
    <br/>
  </b-container>
</template>

<script>
import User from '../models/user';

export default {
  name: 'Login',
  data() {
    return {
      user: new User('', '', '', ''),
      loading: false,
      message: '',
    };
  },
  computed: {
    loggedIn() {
      return this.$store.state.auth.status.loggedIn;
    },
  },
  created() {
    if (this.loggedIn) {
      this.$router.push('/');
    }
  },
  methods: {
    handleLogin() {
      this.loading = true;
      this.$validator.validateAll().then((isValid) => {
        if (!isValid) {
          this.loading = false;
          return;
        }

        if (this.user.email && this.user.password) {
          this.$store.dispatch('auth/login', this.user).then(
            () => {
              this.$router.push('/');
            },
            (error) => {
              this.loading = false;
              this.message = (error.response && error.response.data)
                  || error.message
                  || error.toString();
            },
          );
        }
      });
    },
  },
};
</script>

<style scoped>
label {
  display: block;
  margin-top: 10px;
}

.card-container.card {
  max-width: 350px !important;
  padding: 40px 40px;
}

.card {
  background-color: #f7f7f7;
  padding: 20px 25px 30px;
  margin: 0 auto 25px;
  margin-top: 50px;
  -moz-border-radius: 2px;
  -webkit-border-radius: 2px;
  border-radius: 2px;
  -moz-box-shadow: 0px 2px 2px rgba(0, 0, 0, 0.3);
  -webkit-box-shadow: 0px 2px 2px rgba(0, 0, 0, 0.3);
  box-shadow: 0px 2px 2px rgba(0, 0, 0, 0.3);
}

.profile-img-card {
  width: 96px;
  height: 96px;
  margin: 0 auto 10px;
  display: block;
  -moz-border-radius: 50%;
  -webkit-border-radius: 50%;
  border-radius: 50%;
}
</style>
