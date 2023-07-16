<template>
    <div>
        <div class="chart-container">
            <el-card>
                <div id="lineChart" class="chart" style="height: 500px; width: 100%;" />
            </el-card>
        </div>
        <div class="chart-container">
            <el-card>
                <div id="pieChart" class="chart" style="height: 500px; width: 50%;" />
            </el-card>
        </div>
    </div>
</template>
  
<script>
// import echarts from 'echarts'
// require('echarts/theme/macarons') // echarts theme
import { getRuntimeDistribution, getTimeLine } from '@/api/movie'

export default {
    data() {
        return {
            lineChart: null,
            pieChart: null,
            timer: null,
        }
    },
    mounted() {
        this.initLineChart()
        this.initPieChart()
    },
    beforeDestroy() {
        //清除定时器
        if (this.timer) {
            clearInterval(this.timer)
        }
        //销毁chart
        if (!this.lineChart && !this.pieChart) {
            return
        }
        this.lineChart.dispose()
        this.lineChart = null
        this.pieChart.dispose()
        this.pieChart = null
    },
    methods: {
        //折线图
        initLineChart() {
            this.lineChart = this.$echarts.init(document.getElementById('lineChart'))
            this.lineChart.showLoading()
            this.lineChart.setOption({
                title: {
                    text: '统计每年电影平均评分的折线图'
                },
                tooltip: {
                    trigger: 'axis'
                },
                legend: {},
                xAxis: {
                    name: '年',
                    type: 'category',
                    data: [],
                },
                yAxis: {
                    name: '平均评分',
                    type: 'value',
                },
                grid: {
                    show: true,
                    top: '20%',
                    right: '10%',
                    left: '10%',
                    bottom: '12%',
                },
                series: [
                    {
                        name: '全球平均评分',
                        type: 'line',
                        smooth: 'true',
                        // label: {
                        //     show: true
                        // },
                        data: []
                    },
                    {
                        name: '中国平均评分',
                        type: 'line',
                        smooth: 'true',
                        // label: {
                        //     show: true
                        // },
                        data: []
                    },
                    {
                        name: '美国平均评分',
                        type: 'line',
                        smooth: 'true',
                        // label: {
                        //     show: true
                        // },
                        data: []
                    }
                ]
            })
            getTimeLine().then(response => {
                this.lineChart.hideLoading()
                this.lineChart.setOption({
                    xAxis: {
                        data: response.data.data.world.x_data
                    },
                    series: [
                        {
                            // 根据名字对应到相应的系列
                            name: '全球平均评分',
                            data: response.data.data.world.y_data
                        },
                        {
                            name: '中国平均评分',
                            data: response.data.data.china.y_data
                        },
                        {
                            name: '美国平均评分',
                            data: response.data.data.america.y_data
                        },
                    ]
                })
            })
        },
        // 饼状图
        initPieChart() {
            this.pieChart = this.$echarts.init(document.getElementById('pieChart'))
            this.pieChart.showLoading()
            //向后端请求数据
            getRuntimeDistribution().then(response => {
                this.pieChart.hideLoading()
                this.pieChart.setOption(response.data.data)
            })
        }
    }
}
</script>

<style scoped>
.chart-container {
    padding: 10px;
}
</style>