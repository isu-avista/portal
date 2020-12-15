<template>
  <b-container class="config text-left">
    <br/>
    <b-card no-body>
      <b-tabs card>
        <b-tab title="Server Configuration">
          <b-container>
            <b-row>
              <b-col>
                <SysConfig/>
              </b-col>
            </b-row>
            <br/><br/>
            <b-row>
              <b-col>
                <DbConfig/>
              </b-col>
            </b-row>
            <br/><br/>
          </b-container>
        </b-tab>
        <b-tab title="Attached Device Configuration">
          <DevicesConfig/>
        </b-tab>
        <b-tab title="Security Configuration">
          <UserConfig/>
        </b-tab>
      </b-tabs>
    </b-card>
    <br/><br/>
  </b-container>
</template>

<script>
import SysConfig from '@/components/config/SysConfig.vue';
import DbConfig from '@/components/config/DbConfig.vue';
import DevicesConfig from '@/components/config/DevicesConfig.vue';
import UserConfig from '@/components/config/UserConfig.vue';

export default {
  name: 'Config',
  components: {
    SysConfig,
    DbConfig,
    DevicesConfig,
    UserConfig,
  },
};
</script>

<style>

</style>
