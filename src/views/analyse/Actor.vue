<template>
    <div>
        <div class="chart-container">
            <el-card>
                <div id="barChart" class="chart" style="height: 500px; width: 100%;" />
            </el-card>
        </div>
    </div>
</template>
  
<script>
// require('echarts/theme/macarons') // echarts theme
import { getActorSort } from '@/api/movie'

export default {
    data() {
        return {
            barChart: null
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
        //初始化图表
        initBarChart() {
            this.barChart = this.$echarts.init(document.getElementById('barChart'))
            this.barChart.showLoading()
            this.barChart.setOption({
                baseOption: {
                    title: {
                        text: '楷模演员',
                        subtext: '数据来自豆瓣电影'
                    },
                    grid: {
                        top: "16%",
                        bottom: '14%',
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
                    xAxis: {
                        // name: '演员名称',
                        type: 'category',
                        axisPointer: {
                            show: true
                        },
                        axisLabel: {
                            rotate: 30
                        }
                    },
                    yAxis: [
                        {
                            name: '出场次数',
                            type: 'value',
                            axisLabel: {
                                show: true
                            },
                        }
                    ],
                    series: [
                        {
                            name: '出场次数',
                            type: 'bar',
                            barWidth: "60%",
                            data: [],
                            label: {
                                show: true,
                                position: 'top'
                            }
                        }
                    ],
                }
            })
            getActorSort().then(response => {
                this.barChart.hideLoading()
                this.barChart.setOption({
                    series: [
                        {
                            name: '出场次数',
                            data: response.data.data
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