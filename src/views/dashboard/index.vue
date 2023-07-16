<template>
  <div class="dashboard-container">
    <div class="panelgroup-container">
      <PanelGroup></PanelGroup>
    </div>
    <!-- <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:32px;">
      <LineChart></LineChart>
    </el-row> -->
    <div class="chart-container">
      <el-row :gutter="36">
        <el-col :xs="24" :sm="24" :lg="12">
          <el-card>
            <PieChart></PieChart>
          </el-card>
        </el-col>

        <el-col :xs="24" :sm="24" :lg="12">
          <el-card>
            <BarChart></BarChart>
          </el-card>
        </el-col>
      </el-row>
    </div>

  </div>
</template>

<script>
import PanelGroup from './components/PanelGroup'
import PieChart from './components/PieChart.vue'
import BarChart from './components/BarChart.vue'

export default {
  name: 'Dashboard',
  components: {
    PanelGroup,
    PieChart,
    BarChart,
  },
  data() {
    return {
    }
  },
  computed: {
    // ...mapGetters([
    //   'name'
    // ])
  },
  mounted() {
    this.$store.dispatch('user/getInfo')
  },
  methods: {

  },
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.dashboard {
  &-container {
    margin: 20px;
    background-color: rgb(240, 242, 245);
    padding: 1px 10px;

    .panelgroup-container {
    }

    .chart-container {
    }
  }

  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>
