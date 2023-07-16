<template>
  <div>
    <div id="chart" :class="className" :style="{ height: height, width: width }" />
  </div>
</template>

<script>
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
import { getRateDistribution } from '@/api/movie'

const animationDuration = 6000

export default {
  props: {
    className: {
      type: String,
      default: 'chart'
    },
    width: {
      type: String,
      default: '100%'
    },
    height: {
      type: String,
      default: '500px'
    }
  },
  data() {
    return {
      chart: null
    }
  },
  mounted() {
    this.initChart()
  },
  beforeDestroy() {
    if (!this.chart) {
      return
    }
    this.chart.dispose()
    this.chart = null
  },
  methods: {
    initChart() {
      this.chart = echarts.init(document.getElementById('chart'))
      this.chart.showLoading()
      this.chart.setOption({
        title: {
          text: '电影评分分布折线图'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: { // 坐标轴指示器，坐标轴触发有效
            type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
          }
        },
        grid: {
          top: '10%',
          left: '3%',
          right: '5%',
          bottom: '2%',
          containLabel: true
        },
        xAxis: [{
          type: 'category',
          name: '评分',
          data: [],
          // data: [(5.0, 5.5), (5.5, 6.0), (6.0, 6.5),(6.5, 7.0), (7.0, 7.5), (7.5, 8.0),(8.0, 8.5), (8.5,9.0), (9.0,9.5),(9.5, 10.0)],
          axisTick: {
            alignWithLabel: true
          }
        }],
        yAxis: [{
          type: 'value',
          name: '电影数目',
          bar_width: '100%',
          axisTick: {
            show: true
          }
        }],
        series: [{
          name: '电影数目',
          type: 'line',
          smooth: true,
          areaStyle: {},
          data: [],
          animationDuration
        }]
      })
      getRateDistribution().then(response => {
        if (response.data.res_code) {
          this.chart.hideLoading()
          this.chart.setOption({
            xAxis: {
              data: response.data.data.x_data
            },
            series: [
              {
                // 根据名字对应到相应的系列
                name: '电影数目',
                data: response.data.data.y_data
              }
            ]
          })
        } else {
          console.log(response.data.msg)
        }
      })
    }

    // initChart() {
    //   this.chart = echarts.init(this.$el, 'macarons')
    //   this.chart.showLoading()
    //   //向后端请求数据
    //   getRateDistribution().then(response=>{
    //     this.chart.hideLoading()
    //     this.chart.setOption(response.data.data)
    //   })

    // }
  }
}
</script>
