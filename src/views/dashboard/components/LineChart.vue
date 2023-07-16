<template>
  <div>
    <div :class="className" :style="{ height: height, width: width }" id="lineChart" />
  </div>
</template>

<script>
// import echarts from 'echarts'
// require('echarts/theme/macarons') // echarts theme

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
      default: '350px'
    },
  },
  data() {
    return {
      chart: null,
      timer: null,
      data: [],
    }
  },

  mounted() {
    this.initChart()
  },
  beforeDestroy() {
    //清除定时器
    if (this.timer) {
      clearInterval(this.timer)
    }
    //销毁chart
    if (!this.chart) {
      return
    }
    this.chart.dispose()
    this.chart = null
  },

  methods: {
      randomData(now, oneDay, value) {
        var now = new Date(+now + oneDay);
        var value = value + Math.random() * 21 - 10;
        return {
          name: now.toString(),
          value: [
            [now.getFullYear(), now.getMonth() + 1, now.getDate()].join('/'),
            Math.round(value)
          ]
        };
      },
      initChart() {
        let now = new Date(1997, 9, 3);
        let oneDay = 24 * 3600 * 1000;
        let value = Math.random() * 1000;
        for (var i = 0; i < 1000; i++) {
          this.data.push(this.randomData(now, oneDay, value));
        }
        this.chart = this.$echarts.init(document.getElementById('lineChart'))
        var option = {
          title: {
            text: 'Dynamic Data & Time Axis'
          },
          tooltip: {
            trigger: 'axis',
            formatter: function (params) {
              params = params[0];
              var date = new Date(params.name);
              return (
                date.getDate() +
                '/' +
                (date.getMonth() + 1) +
                '/' +
                date.getFullYear() +
                ' : ' +
                params.value[1]
              );
            },
            axisPointer: {
              animation: false
            }
          },
          xAxis: {
            type: 'time',
            splitLine: {
              show: false
            }
          },
          yAxis: {
            type: 'value',
            boundaryGap: [0, '100%'],
            splitLine: {
              show: false
            }
          },
          series: [
            {
              name: 'Fake Data',
              type: 'line',
              showSymbol: false,
              data: this.data
            }
          ]
        };
        // this.timer = setInterval(() => {
        //   for (var i = 0; i < 5; i++) {
        //     this.data.shift();
        //     this.data.push(this.randomData(now, oneDay, value));
        //   }
        //   this.chart.setOption({
        //     series: [
        //       {
        //         data: this.data
        //       }
        //     ]
        //   });
        //   console.log(this.data)
        // }, 1000);
        this.chart.setOption(option)
      },

    // initChart2() {
    //   this.chart = this.$echarts.init(document.getElementById('lineChart'))
    //   var option = {
    //     title: {
    //       text: 'Temperature Change in the Coming Week'
    //     },
    //     tooltip: {
    //       trigger: 'axis'
    //     },
    //     legend: {},
    //     toolbox: {
    //       show: true,
    //       feature: {
    //         dataZoom: {
    //           yAxisIndex: 'none'
    //         },
    //         dataView: { readOnly: false },
    //         magicType: { type: ['line', 'bar'] },
    //         restore: {},
    //         saveAsImage: {}
    //       }
    //     },
    //     xAxis: {
    //       type: 'category',
    //       boundaryGap: false,
    //       data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    //     },
    //     yAxis: {
    //       type: 'value',
    //       axisLabel: {
    //         formatter: '{value} °C'
    //       }
    //     },
    //     series: [
    //       {
    //         name: 'Highest',
    //         type: 'line',
    //         data: [10, 11, 13, 11, 12, 12, 9],
    //         markPoint: {
    //           data: [
    //             { type: 'max', name: 'Max' },
    //             { type: 'min', name: 'Min' }
    //           ]
    //         },
    //         markLine: {
    //           data: [{ type: 'average', name: 'Avg' }]
    //         }
    //       },
    //       {
    //         name: 'Lowest',
    //         type: 'line',
    //         data: [1, -2, 2, 5, 3, 2, 0],
    //         markPoint: {
    //           data: [{ name: '周最低', value: -2, xAxis: 1, yAxis: -1.5 }]
    //         },
    //         markLine: {
    //           data: [
    //             { type: 'average', name: 'Avg' },
    //             [
    //               {
    //                 symbol: 'none',
    //                 x: '90%',
    //                 yAxis: 'max'
    //               },
    //               {
    //                 symbol: 'circle',
    //                 label: {
    //                   position: 'start',
    //                   formatter: 'Max'
    //                 },
    //                 type: 'max',
    //                 name: '最高点'
    //               }
    //             ]
    //           ]
    //         }
    //       }
    //     ]
    //   };
    //   this.chart.setOption(option)
    // },

  }
}
</script>
