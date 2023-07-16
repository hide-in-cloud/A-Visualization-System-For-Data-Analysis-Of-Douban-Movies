<template>
    <div class="app-container">
        <el-main>
            <el-card v-loading="imgLoading">
                <div class="card-title">
                    <h3>
                        <span>
                            电影评论词云图
                        </span>
                    </h3>
                </div>

                <el-divider></el-divider>

                <div style="margin: 0;">
                    <el-autocomplete ref="search" class="inline-input" v-model="inputValue" :fetch-suggestions="querySearch"
                        clearable placeholder="请输入电影名称" :trigger-on-focus="false" @select="handleSelect"
                        @keyup.enter.native="handleSearch">
                        <el-button slot="append" icon="el-icon-search" @click="handleSearch"></el-button>
                    </el-autocomplete>
                </div>
                
                <el-divider></el-divider>

                <div class="img-container" style="height: 500px; width: 100%; text-align: center; padding-top: 125px;">
                    <img :src="wc_img" alt="">
                </div>
            </el-card>
        </el-main>
    </div>
</template>
  
<script>
import { getSearchTitles, getWordCloud } from '@/api/movie'
// import { mapGetters } from 'vuex'

export default {
    name: 'WordCloud',
    data() {
        return {
            inputValue: '',                 //搜索框里的内容
            timeout: null,                 //定时器

            wc_img: null,                   //词云图存放路径

            imgLoading: false
        }
    },
    mounted() {

    },
    methods: {
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

        //获取电影评论词云图
        handleSearch() {
            this.imgLoading = true
            getWordCloud(this.inputValue).then(response => {
                if (response.data.res_code === 0) {
                    this.imgLoading = false
                    this.$message.error(response.data.msg)
                } else {
                    var img_path = response.data.img
                    this.wc_img = process.env.VUE_APP_BASE_API + img_path
                    this.imgLoading = false
                }
            }).catch(error => {
                this.imgLoading = false
                this.$message.error(error)
            })
        }
    }
}
</script>
  
<style scoped>
.app-container {
    padding: 8px;
}
</style>
  