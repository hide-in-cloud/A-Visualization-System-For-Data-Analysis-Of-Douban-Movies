<template>
    <div class="app-container">
        <el-container>
            <el-header style="font-size: 30px">
                <div style="margin: 0;">
                    <el-autocomplete ref="search" v-model="inputValue" :fetch-suggestions="querySearch" clearable
                        placeholder="请输入电影名称" :trigger-on-focus="false" @select="handleSelect"
                        @keyup.enter.native="fetchPage1">
                        <el-button slot="append" icon="el-icon-search" @click="fetchPage1"></el-button>
                    </el-autocomplete>
                </div>

                <div style="margin: 5px 0;">
                    <el-row :gutter="20">
                        <el-col :span="4">
                            <el-select v-model="movie_type" clearable placeholder="请选择电影类型" @change="fetchPage1">
                                <el-option v-for="item in types" :key="item" :value="item">
                                </el-option>
                            </el-select>
                        </el-col>
                        <el-col :span="4">
                            <el-select v-model="movie_year" clearable placeholder="请选择年份" @change="fetchPage1">
                                <el-option v-for="item in years" :key="item" :value="item">
                                </el-option>
                            </el-select>
                        </el-col>
                        <el-col :span="4">
                            <el-select v-model="movie_country" clearable placeholder="请选择国家" @change="fetchPage1">
                                <el-option v-for="item in countries" :key="item" :label="item" :value="item">
                                </el-option>
                            </el-select>
                        </el-col>
                    </el-row>
                </div>
            </el-header>

            <el-main style="margin-top: 15px;">
                <el-table v-loading="listLoading" element-loading-text="Loading" :data="pageMovie" border fit
                    highlight-current-row stripe style="width: 100%">
                    <el-table-column prop="id" label="ID" width="80" align="center"></el-table-column>
                    <el-table-column label="电影信息">
                        <template slot-scope="scope">
                            <el-card body-style="padding: 5px;">
                                <router-link :to="{
                                        name: 'Detail',
                                        params: { movie_id: scope.row.id }
                                    }">
                                    <div class="subject-card movie">
                                        <div class="cover subject-card-cover">
                                            <div class="cover-container" style="padding-top: 140%; position: relative;">
                                                <img class="cover-pic" referrerpolicy="no-referrer" :src="scope.row.cover"
                                                    alt="cover"
                                                    style="position: absolute;width: 100%; height: 100%; inset: 0px; display: block; object-fit: cover;">
                                            </div>
                                        </div>
                                        <div class="subject-card-main">
                                            <div class="subject-info">
                                                <div class="subject-info-title">
                                                    <span class="subject-info-title-text">{{ scope.row.title }}</span>
                                                    <div class="subject-info-subtitle">{{ scope.row.year }} /
                                                        {{ scope.row.countries }} / {{ scope.row.types }} / {{
                                                            scope.row.directors }}</div>
                                                </div>
                                                <div class="subject-info-rating">
                                                    <el-rate :value="stringToNumber(scope.row.rate)" disabled show-score
                                                        text-color="#ff9900" :score-template="scope.row.rate">
                                                    </el-rate>
                                                </div>
                                                <div class="subject-info-summary">
                                                    <p class="subject-info-summary-text">简介：{{ scope.row.summary }}</p>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </router-link>
                            </el-card>
                        </template>
                    </el-table-column>
                    <!-- <el-table-column prop="rating" label="评分" width="160" align="center">
                        <template slot-scope="scope">
                            <el-rate v-model="rating" @change="handleRating"></el-rate>
                        </template>
                    </el-table-column>
                    <el-table-column prop="Favorites" label="收藏" width="80" align="center">
                        <template slot-scope="scope">
                            <el-button class="icon-favor" icon="el-icon-star-off" v-show="!isFavor(scope.row.id)"
                                @click="handleFavor(scope.row.id)" circle></el-button>
                            <el-button type="warning" class="icon-favor" icon="el-icon-star-on"
                                v-show="isFavor(scope.row.id)" @click="handleFavor(scope.row.id)" circle></el-button>
                        </template>
                    </el-table-column> -->
                </el-table>
            </el-main>

            <el-footer style="margin-left: 300px; font-size: 30px">
                <div class="block">
                    <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange"
                        :current-page="currentPage" background :page-sizes="pageSizes" :page-size="pageSize"
                        layout="total, sizes, prev, pager, next, jumper" :total="total">
                    </el-pagination>
                </div>
            </el-footer>
        </el-container>
    </div>
</template>
  
<script>
import { getMovieDetailByPage, getSearchTitles } from '@/api/movie'
import { mapGetters } from 'vuex'

export default {
    data() {
        return {
            pageMovie: [],                        //分页数据
            //搜索参数
            inputValue: '',                       //搜索框里的内容
            timeout: null,                        //定时器
            movie_type: undefined,                //选择的电影类型
            movie_year: undefined,                //选择的电影年份
            movie_country: undefined,             //选择的电影制片国家
            //分页数据
            total: this.$store.state.movie.total, //电影数据总个数
            currentPage: 1,                       //当前页数
            pageSize: 10,                         //每页个数
            pageSizes: [10, 20, 50, 100],         //每页个数选择列表

            listLoading: true                    //列表是否在加载
        }
    },
    computed: {
        ...mapGetters([
            // 'favorIDList',
            // 'movieInfo',
            'types',
            'years',
            'countries'
        ]),
    },
    mounted() {
        this.fetchDataByPage()
        this.$store.dispatch('movie/GetAllMovieTypes')
        this.$store.dispatch('movie/GetAllMovieYears')
        this.$store.dispatch('movie/GetAllMovieCountries')
    },
    methods: {
        //根据分页查询数据(模糊搜索)
        fetchDataByPage() {
            this.listLoading = true
            var params = {
                page: this.currentPage,
                page_size: this.pageSize,
                search: this.inputValue,
                types: this.movie_type,
                year: this.movie_year,
                country: this.movie_country
            }
            getMovieDetailByPage(params).then(response => {
                // console.log('查询分页')
                this.pageMovie = response.data.results
                this.total = response.data.count
                this.listLoading = false
            }).catch(error => {
                this.listLoading = false
                this.$message.error(error)
            })
        },

        //查询第一页
        fetchPage1() {
            this.currentPage = 1
            scrollTo(0, 0)      //回到顶部
            this.fetchDataByPage()
        },

        //选择每页条数事件
        handleSizeChange(val) {
            this.pageSize = val
            scrollTo(0, 0)      //回到顶部
            this.fetchDataByPage()
        },
        //分页点击事件
        handleCurrentChange(val) {
            this.currentPage = val
            scrollTo(0, 0)      //回到顶部
            this.fetchDataByPage()
        },

        // 模糊搜索
        querySearch(queryString, cb) {
            //queryString:搜索内容,  cb: callback方法
            var results = [];
            if (queryString) {
                getSearchTitles(queryString).then(response => {
                    results = response.data.titles
                    results = results.map(x => ({ value: x }))  //加上value变成对象列表(内部用value)
                }).catch(error => {
                    this.$message.error(error)
                })
            }
            //设置定时器等待服务器返回数据
            clearTimeout(this.timeout);
            this.timeout = setTimeout(() => {
                cb(results); //调用 callback 返回建议列表的数据
            }, 500);
        },
        //从提示框中选择一个
        handleSelect(item) {
            this.inputValue = item.value    //获取用户选择的值
            this.$refs.search.focus()       //获取焦点
        },
    }
}
</script>
  
<style scoped>
/* div {
    margin: 0;
    padding: 0;
} */
.app-container {
    padding: 8px;
}

.el-autocomplete {
    width: 800px;
}

.subject-card {
    display: flex;
}

.subject-card-cover {
    margin-right: 15px;
    max-height: 155px;
    width: 115px;
}

a img {
    border-width: 0;
    vertical-align: middle;
}

img {
    max-width: 100%;
}

.subject-card-main {
    flex: 1;
}

.subject-info {
    float: left;
}

.subject-info-title {
    margin-top: 6px;
}

.subject-info-title-text {
    color: #27a;
    font-size: 28px;
    font-weight: 400;
}

.subject-info-subtitle {
    color: #1a1a1a;
    font-size: 15px;
    font-weight: 400;
}

.subject-info-rating {
    font-size: 18px;
    line-height: 18px;
}

.subject-info-summary-text {
    font-size: 16px;
    line-height: 20px;
}

.icon-favor {
    font-size: 20px;
}
</style>
  