<template>
    <div class="app-container">
        <el-form ref="form" :model="form" label-width="120px">
            <el-form-item label="电影名称">
                <el-col :span="6">
                    <el-input v-model="form.title" />
                </el-col>
            </el-form-item>
            <el-form-item prop="types" label="类型">
                <el-checkbox-group v-model="form.types">
                    <el-checkbox v-for="item in types" :label="item" :key="item">{{ item }}</el-checkbox>
                </el-checkbox-group>
            </el-form-item>
            <el-form-item label="年份">
                <el-col :span="6">
                    <el-input type="number" v-model="form.year" />
                </el-col>
            </el-form-item>
            <el-form-item label="导演">
                <el-col :span="6">
                    <el-input v-model="form.directors" />
                </el-col>
            </el-form-item>
            <el-form-item label="演员">
                <el-input v-model="form.actors" />
            </el-form-item>
            <el-form-item label="简介">
                <el-input type="textarea" v-model="form.summary" />
            </el-form-item>
            <el-form-item label="豆瓣评分">
                <el-col :span="6">
                    <el-input type="number" step="0.1" v-model="form.rate" />
                </el-col>
            </el-form-item>
            <el-form-item label="制片国家">
                <el-checkbox-group v-model="form.countries">
                    <el-checkbox v-for="item in countries" :label="item" :key="item">{{ item }}</el-checkbox>
                </el-checkbox-group>
            </el-form-item>
            <el-form-item label="语言">
                <el-checkbox-group v-model="form.lang">
                    <el-checkbox v-for="item in langs" :label="item" :key="item">{{ item }}</el-checkbox>
                </el-checkbox-group>
            </el-form-item>
            <el-form-item label="上映日期">
                <el-col :span="6">
                    <el-date-picker v-model="form.release_date" type="date" placeholder="Pick a date"
                        style="width: 100%;" />
                </el-col>
            </el-form-item>
            <el-form-item label="时长(分钟)">
                <el-col :span="6">
                    <el-input type="number" v-model="form.runtime" />
                </el-col>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="onSubmit">修改</el-button>
                <el-button @click="onCancel">取消</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>
  
<script>
import { getMovieDetailByID, editMovieInfo } from "@/api/movie";
import { mapGetters } from 'vuex'

export default {
    data() {
        return {
            form: {
                title: '',
                types: [],
                year: null,
                directors: '',
                actors: '',
                summary: '',
                rate: null,
                detail_url: '',
                countries: [],
                lang: [],
                release_date: null,
                runtime: null,
            },
            movie_id: null
        }
    },
    computed: {
        ...mapGetters([
            'types',
            'countries',
            'langs'
        ]),
    },
    mounted() {
        this.fetchInfo()
        this.$store.dispatch('movie/GetAllMovieTypes')
        this.$store.dispatch('movie/GetAllMovieCountries')
        this.$store.dispatch('movie/GetAllMovieLang')
    },
    methods: {
        //从路径参数中获取id，查询对应的数据
        fetchInfo() {
            this.movie_id = this.$route.params.id;
            getMovieDetailByID(this.movie_id).then(response => {
                this.form = response.data
                this.form.types = this.form.types.split(',')
                this.form.countries = this.form.countries.split(',')
                this.form.lang = this.form.lang.split(',')
                console.log(this.form.lang)
            }).catch(error => {
                this.$message.error('服务器出错:', error)
            })
        },

        //选择图片触发事件
        getImageFile: function (e) {
            let file = e.target.files[0];
            if (file) {
                this.form.cover = file
            }
        },

        //修改事件
        onSubmit() {
            this.$refs.form.validate((valid) => {
                if (valid) {
                    // 用FormData提交数据
                    let formData = new FormData
                    formData.append('title', this.form.title)
                    formData.append('types', this.form.types)
                    formData.append('year', this.form.year)
                    formData.append('directors', this.form.directors)
                    formData.append('actors', this.form.actors)
                    formData.append('summary', this.form.summary)
                    formData.append('rate', this.form.rate)
                    formData.append('detail_url', this.form.detail_url)
                    formData.append('countries', this.form.countries)
                    formData.append('lang', this.form.lang)
                    formData.append('release_date', this.form.release_date)
                    formData.append('runtime', this.form.runtime)
                    console.log('form:', this.form)
                    editMovieInfo(this.movie_id, formData).then(() => {
                        this.$message.success('修改成功!')
                        //跳转回用户列表
                        this.$router.push({ path: '/movieManage/index' })
                    }).catch(error => {
                        this.$message.error(error)
                    })
                } else {
                    this.$message.error('数据格式不正确');
                    return false;
                }
            });
        },
        onCancel() {
            this.$message.warning('取消!')
            //跳转回电影列表
            this.$router.go(-1)
        },
    }
}
</script>
  
<style scoped>
.line {
    text-align: center;
}
</style>
  
  