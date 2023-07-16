<template>
    <div>
        <div class="chart-container">
            <el-card>
                <div id="barChart" class="chart" style="height: 600px; width: 100%;" />
            </el-card>
        </div>
        <!-- <div class="chart-container">
            <el-card>
                <div id="pieChart" class="chart" style="height: 500px; width: 50%;" />
            </el-card>
        </div> -->
    </div>
</template>
  
<script>
// require('echarts/theme/macarons') // echarts theme
import { getDirectorSort } from '@/api/movie'

export default {
    data() {
        return {
            barChart: null,
            // pieChart: null
        }
    },
    mounted() {
        this.initBarChart()
    },
    beforeDestroy() {
        //销毁chart
        if (!this.barChart) {
            return
        }
        this.barChart.dispose()
        this.barChart = null
    },
    methods: {
        //
        initBarChart() {
            this.barChart = this.$echarts.init(document.getElementById('barChart'))
            this.barChart.showLoading()
            this.barChart.setOption({
                baseOption: {
                    title: {
                        text: '优秀电影导演',
                        subtext: '数据来自豆瓣电影'
                    },
                    grid: {
                        top: "16%",
                        bottom: '12%',
                        left: '16%',
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
                        // name: '导演名称',
                        type: 'category',
                        data: [],
                        axisPointer: {
                            show: true
                        },
                        axisLabel: {
                            rotate: 30
                        }
                    },
                    yAxis: [
                        {
                            name: '平均评分',
                            type: 'value',
                            axisLabel: {
                                show: true
                            },
                        },
                        {
                            type: 'value',
                            name: '电影数量',
                            min: 0,
                            max: 16,
                            interval: 4
                        }
                    ],
                    series: [
                        {
                            name: '平均评分',
                            type: 'bar',
                            barWidth: "60%",
                            data: [],
                            label: {
                                show: true,
                                position: 'top'
                            }
                        },
                        {
                            name: '电影数量',
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
            getDirectorSort().then(response => {
                this.barChart.hideLoading()
                this.barChart.setOption({
                    xAxis: {
                        data: response.data.data.directors
                    },
                    series: [
                        {
                            name: '平均评分',
                            data: response.data.data.mean_rate
                        },
                        {
                            name: '电影数量',
                            data: response.data.data.movie_sum
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