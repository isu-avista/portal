<template>
  <b-card header-tag="header">
    <template #header>
      <b-row>
        <b-col><h3 style="float: left;">Users</h3></b-col>
        <b-col>
          <h3 style="float: right;">
            <b-button-group>
              <b-button v-b-modal.user-modal variant="success">
                <b-icon icon="plus-circle"/>
              </b-button>
            </b-button-group>
          </h3>
        </b-col>
      </b-row>
    </template>
    <b-table hover :items='users' :fields='user_fields'>
      <template v-slot:cell(actions)="row">
        <b-button-group>
          <b-button v-b-modal.user-update-modal @click="editUser(row.item)">
            <b-icon icon='pencil-square'/></b-button>
          <b-button variant='danger' @click="onDeleteUser(row.item)">
            <b-icon icon='x-circle'/></b-button>
        </b-button-group>
      </template>
    </b-table>

    <b-modal ref="addUserModal"
             id="user-modal"
             title="Add a new User"
             hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-first_name-group"
                      label="First Name:"
                      label-for="form-first_name-input">
          <b-form-input id="form-first_name-input"
                        type="text"
                        v-model="addUserForm.first_name"
                        required
                        placeholder="Enter first name">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-last_name-group"
                      label="Last Name:"
                      label-for="form-last_name-input">
          <b-form-input id="form-last_name-input"
                        type="text"
                        v-model="addUserForm.last_name"
                        required
                        placeholder="Enter last name">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-email-group"
                      label="form-email-input"
                      label-for="Email:">
          <b-form-input id="form-email-input"
                        type="email"
                        v-model="addUserForm.email"
                        required
                        placeholder="Enter email">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-admin-group">
          <b-form-checkbox-group v-model="addUserForm.admin" id="form-checks">
            <b-form-checkbox value="true">Admin</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>

    <b-modal ref="editUserModal"
             id="user-update-modal"
             title="Add a new User"
             hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
        <b-form-group id="form-first_name-edit-group"
                      label="First Name:"
                      label-form="form-first_name-edit-input">
          <b-form-input id="form-first_name-edit-input"
                        type="text"
                        v-model="editForm.first_name"
                        required
                        placeholder="Enter first name">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-last_name-edit-group"
                      label="Last Name:"
                      label-form="form-last_name-edit-input">
          <b-form-input id="form-last_name-edit-input"
                        type="text"
                        v-model="editForm.last_name"
                        required
                        placeholder="Enter last name">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-email-edit-group"
                      label="form-email-edit-input"
                      label-form="Email:">
          <b-form-input id="form-email-edit-input"
                        type="email"
                        v-model="editForm.email"
                        required
                        placeholder="Enter email">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-admin-edit-group">
          <b-form-checkbox-group v-model="editForm.admin" id="form-checks">
            <b-form-checkbox value="true">Admin</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </b-card>
</template>

<script>
import axios from 'axios';
import authHeader from '@/services/auth-header';

const API_URL = 'http://localhost:5000/api/';

export default {
  name: 'UserConfig',
  data() {
    return {
      users: [],
      user_fields: ['first_name', 'last_name', 'email', 'admin', 'actions'],
      addUserForm: {
        first_name: '',
        last_name: '',
        email: '',
        admin: [],
      },
      editForm: {
        first_name: '',
        last_name: '',
        email: '',
        admin: [],
      },
    };
  },
  methods: {
    getData() {
      const path = `${API_URL}users`;
      axios.get(path, { headers: authHeader() })
        .then((res) => {
          this.users = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addUser(payload) {
      const path = `${API_URL}users`;
      axios.post(path, payload, { headers: authHeader() })
        .then(() => {
          this.getData();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getData();
        });
    },
    initForm() {
      this.addUserForm.first_name = '';
      this.addUserForm.last_name = '';
      this.addUserForm.email = '';
      this.addUserForm.admin = [];
      this.editForm.id = '';
      this.editForm.first_name = '';
      this.editForm.last_name = '';
      this.editForm.email = '';
      this.editForm.author = [];
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addUserModal.hide();
      let admin = false;
      if (this.addUserForm.admin[0]) admin = true;
      const payload = {
        first_name: this.addUserForm.first_name,
        last_name: this.addUserForm.last_name,
        email: this.addUserForm.email,
        admin,
      };
      this.addUser(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addUserModal.hide();
      this.initForm();
    },
    editUser(user) {
      this.editForm = user;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editUserModal.hide();
      let admin = false;
      if (this.editForm.admin[0]) admin = true;
      const payload = {
        first_name: this.editForm.first_name,
        last_name: this.editForm.last_name,
        email: this.editForm.email,
        admin,
      };
      this.updateUser(payload, this.editForm.id);
    },
    updateUser(payload, userID) {
      const path = `http://localhost:5000/users/${userID}`;
      axios.put(path, payload, { headers: authHeader() })
        .then(() => {
          this.getData();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getData();
        });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editUserModal.hide();
      this.initForm();
      this.getUsers();
    },
    removeUser(userID) {
      const path = `http://localhost:5000/users/${userID}`;
      axios.delete(path, { headers: authHeader() })
        .then(() => {
          this.getData();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getData();
        });
    },
    onDeleteUser(user) {
      this.removeUser(user.id);
    },
  },
  created() {
    this.getData();
  },
};
</script>
