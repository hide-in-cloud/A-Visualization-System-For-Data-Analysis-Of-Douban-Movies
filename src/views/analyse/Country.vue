<template>
    <div>
        <div class="chart-container">
            <el-card>
                <el-row>
                    <el-col :span="4" :push="8">
                        <el-select v-model="start_year" clearable placeholder="请选择开始年份" @change="initBarChart">
                            <el-option v-for="item in years" :key="item" :value="item">
                            </el-option>
                        </el-select>
                    </el-col>
                    <el-col :span="4" :push="8">
                        <el-select v-model="end_year" clearable placeholder="请选择结束年份" @change="initBarChart">
                            <el-option v-for="item in years" :key="item" :value="item">
                            </el-option>
                        </el-select>
                    </el-col>
                </el-row>
                <div id="barChart" class="chart" style="height: 600px; width: 100%;" />
            </el-card>
        </div>
    </div>
</template>
  
<script>
// require('echarts/theme/macarons') // echarts theme
import { getCountrySort } from '@/api/movie'
import { mapGetters } from 'vuex'

export default {
    name: 'Country',
    data() {
        return {
            barChart: null,
            start_year: null,
            end_year: null
        }
    },
    computed: {
        ...mapGetters([
            'years'
        ]),
    },
    mounted() {
        this.initBarChart()
        this.$store.dispatch('movie/GetAllMovieYears')
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
                        text: '各国家电影总数排名',
                        subtext: '数据来自豆瓣电影'
                    },
                    grid: {
                        top: "18%",
                        bottom: '15%',
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
                    legend: {
                        top: '20%S'
                    },
                    xAxis: {
                        type: 'category',
                        data: [],
                        axisPointer: {
                            show: true
                        },
                        axisLabel: {
                            // rotate: 10
                        }
                    },
                    yAxis: [
                        {
                            name: '电影总数',
                            type: 'value',
                            axisLabel: {
                                show: true
                            },
                        },
                        {
                            name: '优秀电影总数',
                            type: 'value',
                            axisLabel: {
                                show: true
                            },
                        }
                    ],
                    series: [
                        {
                            name: '电影总数',
                            type: 'bar',
                            data: [],
                            label: {
                                show: true,
                                position: 'top'
                            }
                        },
                        {
                            name: '优秀电影总数',
                            type: 'bar',
                            data: [],
                            label: {
                                show: true,
                                position: 'top'
                            }
                        }
                    ],
                }
            })
            getCountrySort(this.start_year, this.end_year).then(response => {
                this.barChart.hideLoading()
                this.barChart.setOption({
                    xAxis: {
                        data: response.data.data.countries
                    },
                    series: [
                        {
                            name: '电影总数',
                            data: response.data.data.count
                        },
                        {
                            name: '优秀电影总数',
                            data: response.data.data.good_count
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