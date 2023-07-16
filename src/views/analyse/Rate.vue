<template>
    <div>
        <div class="chart-container">
            <el-card>
                <div id="barChart" class="chart" style="height: 500px; width: 100%;" />
            </el-card>
        </div>
        <div class="chart-container">
            <el-card>
                <div id="lineChart" class="chart" style="height: 500px; width: 80%;" />
            </el-card>
        </div>
    </div>
</template>
  
<script>
// require('echarts/theme/macarons') // echarts theme
import { getRateSort, getBadMovie } from '@/api/movie'

export default {
    data() {
        return {
            barChart: null,
            lineChart: null,
            timer: null,
            startYear: 2014
        }
    },
    mounted() {
        this.initBarChart()
        this.initLineChart()
    },
    beforeDestroy() {
        //清除定时器
        if (this.timer) {
            clearInterval(this.timer)
        }
        //销毁chart
        if (!this.barChart && !this.lineChart) {
            return
        }
        this.barChart.dispose()
        this.barChart = null
        this.lineChart.dispose()
        this.lineChart = null
    },
    methods: {
        //折线图
        initBarChart() {
            this.barChart = this.$echarts.init(document.getElementById('barChart'))
            this.barChart.showLoading()
            var xAxis_data = []
            for (let index = 0; index < 10; index++) {
                xAxis_data.push(this.startYear + index)
            }
            this.barChart.setOption({
                baseOption: {
                    title: {
                        subtext: '数据来自豆瓣电影'
                    },
                    grid: {
                        top: "16%",
                        bottom: '12%',
                        left: '18%',
                        right: '14%'
                    },
                    timeline: {
                        axisType: 'category',
                        autoPlay: true,
                        playInterval: 5000,
                        // controlStyle: {
                        //     position: 'left'
                        // },
                        data: xAxis_data
                    },
                    xAxis: {
                        name: '评分',
                        type: 'value',
                        
                    },
                    yAxis: {
                        name: '电影名称',
                        type: 'category',
                        // data: [],
                        axisLabel: {
                            show: true,
                            fontSize: 16,
                            rich: {
                                flag: {
                                    fontSize: 25,
                                    padding: 5
                                }
                            }
                        },
                    },
                    series: [
                        {
                            name: 'TOP10',
                            type: 'bar',
                            data: [],
                            label: {
                                show: true,
                                precision: 1,
                                position: 'right',
                                fontSize: 16,
                                valueAnimation: true,
                                fontFamily: 'monospace'
                            }
                        }
                    ],
                }
            })
            getRateSort(this.startYear).then(response => {
                this.barChart.hideLoading()
                var options = []
                for (let i = 0; i < 10; i++) {
                    options.push({
                        title: { text: xAxis_data[i] + '年TOP10电影' },
                        yAxis: [],
                        series: [{ data: response.data.data[i] }]
                    })
                }
                this.barChart.setOption({
                    options: options
                })
            })
        },

        //烂片数量及占比的年变化图
        initLineChart() {
            this.lineChart = this.$echarts.init(document.getElementById('lineChart'))
            this.lineChart.showLoading()
            this.lineChart.setOption({
                baseOption: {
                    title: {
                        text: '烂片数量及占比的年变化图',
                        subtext: '数据来自豆瓣电影'
                    },
                    grid: {
                        top: "18%",
                        bottom: '12%',
                        left: '20%',
                        right: '14%'
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'cross',
                            crossStyle: {
                                color: '#999'
                            }
                        }
                    },
                    color: ['#5470c6', '#fc8452'],
                    legend: {},
                    xAxis: {
                        // name: '年份',
                        type: 'category',
                        data: [],
                        axisPointer: {
                            show: true
                        },
                    },
                    yAxis: [
                        {
                            name: '烂片数量',
                            type: 'value',
                            min: 0,
                            max: 15,
                            interval: 3,
                            axisLabel: {
                                show: true
                            },
                        },
                        {
                            type: 'value',
                            name: '烂片占比',
                            min: 0,
                            max: 0.5,
                            interval: 0.1,
                            // axisLabel: {
                            //     show: true
                            // },
                        }
                    ],
                    series: [
                        {
                            name: '烂片数量',
                            type: 'line',
                            data: [],
                            label: {
                                show: true
                            }
                        },
                        {
                            name: '烂片占比',
                            type: 'line',
                            yAxisIndex: 1,
                            data: [],
                            label: {
                                show: true
                            }
                        }
                    ],
                }
            })
            getBadMovie().then(response => {
                this.lineChart.hideLoading()
                this.lineChart.setOption({
                    xAxis: {
                        data: response.data.data.year
                    },
                    series: [
                        {
                            name: '烂片数量',
                            data: response.data.data.count
                        },
                        {
                            name: '烂片占比',
                            data: response.data.data.proportion
                        }
                    ]
                })
            })
        },
    }
}
</script>

<style scoped>
.chart-container {
    padding: 10px;
}
</style>