<template>
    <div class="detail-container">
        <el-header style="padding: 10px;">
            <div>
                <el-button type="primary" @click="onBack">返回</el-button>
            </div>
        </el-header>

        <el-main class="clearfix" style="padding: 10px;">
            <el-card>

                <div class="subjectwrap clearfix">
                    <div class="subject-title">
                        <h1>
                            <span>
                                {{ info.title }}
                            </span>
                        </h1>
                    </div>
                    <el-divider></el-divider>
                    <div class="subject clearfix">
                        <div id="mainpic">
                            <img referrerpolicy="no-referrer" :src="getImages(info.cover)" alt="cover">

                            <div style="margin-top: 10px;">
                                <div class="rating-wrap">
                                    <span>您的评价:</span>
                                    <el-rate v-model="rating" @change="handleRating"></el-rate>
                                </div>
                            </div>
                            <div style="margin-top: 10px;">
                                收藏:
                                <el-button class="icon-favor" icon="el-icon-star-off" v-show="!isFavor()"
                                    @click="handleFavor()" circle></el-button>
                                <el-button type="warning" class="icon-favor" icon="el-icon-star-on" v-show="isFavor()"
                                    @click="handleFavor()" circle></el-button>
                            </div>
                        </div>

                        <el-descriptions id="info" title="" :column="1" border>
                            <el-descriptions-item label="豆瓣评分">{{ info.rate }}</el-descriptions-item>
                            <el-descriptions-item label="导演">
                                {{ info.directors }}
                            </el-descriptions-item>
                            <el-descriptions-item label="主演">
                                {{ info.actors }}
                            </el-descriptions-item>
                            <el-descriptions-item label="类型">{{ info.types }}</el-descriptions-item>
                            <el-descriptions-item label="制片国家/地区">{{ info.countries }}</el-descriptions-item>
                            <el-descriptions-item label="语言">{{ info.lang }}</el-descriptions-item>
                            <el-descriptions-item label="上映日期">{{ info.release_date }}</el-descriptions-item>
                            <el-descriptions-item label="片长">{{ info.runtime }}分钟</el-descriptions-item>
                            <el-descriptions-item label="简介">{{ info.summary }}</el-descriptions-item>
                        </el-descriptions>
                    </div>
                </div>

                <el-divider></el-divider>

                <div class="img-title">
                    <h4>
                        <span>
                            图片列表
                        </span>
                    </h4>
                </div>
                <div style="text-align: center;">
                    <el-carousel type="card" indicator-position="outside">
                        <el-carousel-item v-for="item in img_list" :key="item">
                            <img referrerpolicy="no-referrer" style="height: 100%" :src="getImages(item)">
                        </el-carousel-item>
                    </el-carousel>
                </div>

                <el-divider></el-divider>

                <div class="img-title" v-show="haveVideo">
                    <h4>
                        <span>
                            预告片
                        </span>
                    </h4>
                    <div class="video-wrap">
                        <a referrerpolicy="no-referrer" :href="info.video" target="_blank">
                            <img src="@/assets/img/BNLvob5ope.png" alt="" style="height: 100%">
                        </a>
                    </div>
                </div>

            </el-card>

        </el-main>
    </div>
</template>

<script>
import { getMovieDetailByID } from '@/api/movie'
import { rating, getUserRate, getUserFavor } from '@/api/user'
import { getToken } from '@/utils/auth'
import { mapGetters } from 'vuex'

export default {
    name: 'Detail',
    components: {
    },
    data() {
        return {
            movie_id: null,
            info: {},
            rating: null,
            url: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
            srcList: [
                'https://fuss10.elemecdn.com/8/27/f01c15bb73e1ef3793e64e6b7bbccjpeg.jpeg',
                'https://fuss10.elemecdn.com/1/8e/aeffeb4de74e2fde4bd74fc7b4486jpeg.jpeg'
            ]
        }
    },
    computed: {
        ...mapGetters([
            'favorIDList',
            'ratingIDList',
        ]),
        img_list() {
            if (this.info.img_list) {
                return this.info.img_list.split(',')
            }
        },
        haveVideo() {
            if (this.info.video) {
                return true
            } else {
                return false
            }
        }
    },
    mounted() {
        this.fetchInfo()
        this.initUserRate()
    },
    methods: {
        //从路径参数中获取电影id，查询对应的电影数据
        fetchInfo() {
            this.movie_id = this.$route.params.movie_id;
            console.log(this.movie_id)
            getMovieDetailByID(this.movie_id).then(response => {
                this.info = response.data
            }).catch(error => {
                this.$message.error('服务器出错:', error)
            })
        },

        //用户评分处理
        handleRating() {
            var params = {
                'movie_id': this.movie_id,
                'rating': this.rating,
            }
            this.$store.dispatch('user/handleRating', params).then(() => {
                this.$message.success('评分成功!');
            }, reason => {
                this.$message.error(reason)
            }).catch(error => {
                this.$message.error('服务器出错:', error)
            })
        },

        //初始化显示用户对电影的评分
        initUserRate() {
            var token = getToken()
            getUserRate(token, this.movie_id).then(response => {
                this.rating = response.data.data
            }).catch(error => {
                this.$message.error('服务器出错:', error)
            })
        },

        //是否已收藏
        isFavor() {
            //根据当前行id是否在收藏列表中
            for (let index = 0; index < this.favorIDList.length; index++) {
                if (this.movie_id === this.favorIDList[index]) {
                    return true
                }
            }
            return false
        },

        //点击收藏或取消收藏
        handleFavor() {
            this.$store.dispatch('user/handleFavor', this.movie_id).then(response => {
                this.$message.success(response.data.msg);
            }, reason => {
                this.$message.error(reason)
            }).catch(error => {
                this.$message.error('服务器出错:', error)
            })
        },

        //返回按钮事件
        onBack(){
            //跳转回电影列表
            this.$router.go(-1)
        }
    },
}
</script>

<style rel="stylesheet/scss" scoped>
.detail-container {
    margin: 20px;
    /* background-color: rgb(240, 242, 245); */
}

.movie-bar {
    position: relative;
    margin-top: 10px;
}

.movie-bar-fav {
    position: absolute;
    top: 0;
    right: 0;
}

.subject {
    width: 100%;
}

.clearfix {
    display: block;
    zoom: 1;
}

.subject #mainpic {
    margin-right: 15px;
}

#mainpic {
    margin: 3px 0 0 0;
    float: left;
    text-align: center;
    margin: 3px 12px 0 0;
    width: 320px;
    max-width: 320px;
    overflow: hidden;
}

#mainpic img {
    margin-bottom: 10px;
    max-width: 100%;
}

img {
    border-width: 0;
    vertical-align: middle;
}

#info {
    max-width: 75%;
}

#info {
    float: left;
    max-width: 75%;
    word-wrap: break-word;
}

.el-carousel__item img {
    opacity: 0.9;
    margin: 0;
}

.el-carousel__item {
    background-color: #d3dce6;
}

.video-wrap {
    height: 180px;
    float: left;
    background-color: #d3dce6;
    margin-bottom: 10px;
}

/* .rating-wrap{
    float: left;
} */
</style>
