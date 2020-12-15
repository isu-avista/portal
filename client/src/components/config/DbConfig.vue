<template>
  <b-card header-tag='header'>
    <template #header>
      <b-row>
        <b-col><h3 style="float: left;">DbConfig</h3></b-col>
        <b-col>
          <h3 style="float: right;">
            <b-button-group>
              <b-button><b-icon icon="hdd"/></b-button>
              <b-button><b-icon icon="arrow-repeat"/></b-button>
              <b-button v-b-modal.db-update-modal
               @click="editData()"><b-icon icon="pencil-square"/></b-button>
            </b-button-group>
          </h3>
        </b-col>
      </b-row>
    </template>
    <b-table hover :items='items' :fields='dbFields'>
      <template v-slot:cell(item)="row">
        {{ row.item.item }}
      </template>
      <template v-slot:cell(value)="row">
        {{ row.item.value }}
      </template>
    </b-table>
    <b-modal ref="editDataModal"
             id="db-update-modal"
             title="Update"
             hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
        <template v-for="item in items">
          <b-form-group :key="item.item" :label="item.item">
            <b-form-input id="form-db-edit-input"
                          :type="item.type"
                          v-model="editForm[item.item]"
                          required>

            </b-form-input>
          </b-form-group>
        </template>
        <b-button-group>
          <b-button type="submit" variant="primary">Update</b-button>
          <b-button type="reset" variant="danger">Cancel</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </b-card>
</template>

<script>
import axios from 'axios';
import authHeader from '@/services/auth-header';

export default {
  name: 'DbConfig',
  data() {
    return {
      items: [],
      dbFields: ['item', 'value'],
      editForm: {},
    };
  },
  methods: {
    save() {

    },
    refresh() {

    },
    getData() {
      const path = 'http://localhost:5000/api/config/dbdata';
      axios.get(path, { headers: authHeader() })
        .then((res) => {
          this.items = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    editData() {
      this.items.forEach((item) => {
        this.editForm[item.item] = item.value;
      });
      this.getData();
      this.$refs.editDataModal.show();
    },
    onSubmitUpdate(evt) {
      const payload = this.items;
      evt.preventDefault();
      this.$refs.editDataModal.hide();
      for (let i = 0; i < payload.length; i += 1) {
        payload[i].value = this.editForm[payload[i].item];
      }
      this.updateData(payload);
    },
    updateData(payload) {
      const path = 'http://localhost:5000/config/dbdata';
      axios.put(path, payload, { headers: authHeader() })
        .then(() => {
          this.getData();
          this.message = 'Configuration Updated!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getData();
        });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editDataModal.hide();
      this.initForm();
      this.getData();
    },
    initForm() {
      // eslint-disable-next-line
      this.editForm.items.forEach((key, value) => this.editForm[key] = '');
    },
  },
  created() {
    this.getData();
  },
};
</script>

<style>

</style>
