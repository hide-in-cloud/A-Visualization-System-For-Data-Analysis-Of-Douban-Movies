<template>
    <div class="dashboard-container">
        <div class="zone-container">
            <div>
                <h2>基于电影内容的推荐</h2>
                <!-- <button @click="getRecommendBaseContent">刷新</button> -->
            </div>
            <div>
                <el-row :gutter="40">
                    <ul class="subject-list">
                        <li v-for="item in recommendMovieList">
                            <el-card body-style="padding: 5px;">
                                <router-link :to="{
                                    name: 'Detail',
                                    params: { movie_id: item.id }
                                }">
                                    <!-- <a :href="item.detail_url" target="_blank"> -->
                                    <div class="subject-main">
                                        <div class="subject-cover-container" style="padding-top: 140%; position: relative;">
                                            <img class="cover-pic" referrerpolicy="no-referrer" :src="getImages(item.cover)"
                                                alt="cover"
                                                style="position: absolute;width: 100%; height: 100%; inset: 0px; display: block; object-fit: cover;">
                                        </div>
                                        <div class="subject-info">
                                            <div class="subject-info-title">
                                                <span class="subject-info-title-text">{{ item.title }}</span>
                                            </div>
                                            <div class="subject-info-rating">
                                                <el-rate :value="stringToNumber(item.rate)" disabled show-score
                                                    text-color="#ff9900" :score-template="item.rate">
                                                </el-rate>
                                            </div>
                                        </div>
                                    </div>
                                    <!-- </a> -->
                                </router-link>
                            </el-card>
                        </li>
                    </ul>
                </el-row>
            </div>
        </div>
        <div class="zone-container">
            <div>
                <h2>基于用户的协同过滤推荐</h2>
            </div>
            <div>
                <el-row :gutter="40">
                    <h3 class="subject-tip" v-if="!showUserCF">没有相似用户（没有评分记录）</h3>
                    <ul class="subject-list" v-if="showUserCF">
                        <li v-for="item in recommendMovieList2">
                            <el-card body-style="padding: 5px;">
                                <a :href="item.detail_url" target="_blank">
                                    <div class="subject-main">
                                        <div class="subject-cover-container" style="padding-top: 140%; position: relative;">
                                            <img class="cover-pic" referrerpolicy="no-referrer" :src="getImages(item.cover)"
                                                alt="cover"
                                                style="position: absolute;width: 100%; height: 100%; inset: 0px; display: block; object-fit: cover;">
                                        </div>
                                        <div class="subject-info">
                                            <div class="subject-info-title">
                                                <span class="subject-info-title-text">{{ item.title }}</span>
                                            </div>
                                            <div class="subject-info-rating">
                                                <el-rate :value="stringToNumber(item.rate)" disabled show-score
                                                    text-color="#ff9900" :score-template="item.rate">
                                                </el-rate>
                                            </div>
                                        </div>
                                    </div>
                                </a>
                            </el-card>
                        </li>
                    </ul>
                </el-row>
            </div>
        </div>
        <div class="zone-container">
            <div>
                <h2>基于物品的协同过滤推荐</h2>
            </div>
            <div>
                <el-row :gutter="40">
                    <h3 class="subject-tip" v-if="!showItemCF">没有相似物品（没有评分记录）</h3>
                    <ul class="subject-list" v-if="showItemCF">
                        <li v-for="item in recommendMovieList3">
                            <el-card body-style="padding: 5px;">
                                <a :href="item.detail_url" target="_blank">
                                    <div class="subject-main">
                                        <div class="subject-cover-container" style="padding-top: 140%; position: relative;">
                                            <img class="cover-pic" referrerpolicy="no-referrer" :src="getImages(item.cover)"
                                                alt="cover"
                                                style="position: absolute;width: 100%; height: 100%; inset: 0px; display: block; object-fit: cover;">
                                        </div>
                                        <div class="subject-info">
                                            <div class="subject-info-title">
                                                <span class="subject-info-title-text">{{ item.title }}</span>
                                            </div>
                                            <div class="subject-info-rating">
                                                <el-rate :value="stringToNumber(item.rate)" disabled show-score
                                                    text-color="#ff9900" :score-template="item.rate">
                                                </el-rate>
                                            </div>
                                        </div>
                                    </div>
                                </a>
                            </el-card>
                        </li>
                    </ul>
                </el-row>
            </div>
        </div>
    </div>
</template>
  
<script>
import { getRecommendBaseContent, getRecommendBaseUserCF, getRecommendBaseItemCF, getMovieDetailByID } from "@/api/movie";
import { getToken } from "@/utils/auth";

export default {
    name: 'Recommend',
    data() {
        return {
            midList: [],
            recommendMovieList: [],
            midList2: [],
            recommendMovieList2: [],
            showUserCF: true,
            midList3: [],
            recommendMovieList3: [],
            showItemCF: true,
        }
    },
    mounted() {
        this.getRecommendBaseContent()
        this.getRecommendBaseUserCF()
        this.getRecommendBaseItemCF()
    },
    methods: {
        //基于电影内容的推荐
        getRecommendBaseContent() {
            //初始化
            this.midList = []
            this.recommendMovieList = []
            var token = getToken()
            getRecommendBaseContent(token).then(response => {
                // 获取电影ID列表
                this.midList = response.data.data
                // console.log(this.midList)
                // 获取电影ID所对应的电影信息
                for (let index = 0; index < this.midList.length; index++) {
                    getMovieDetailByID(this.midList[index]).then(response => {
                        this.recommendMovieList.push(response.data)
                    }).catch(error => {
                        this.$message.error(error)
                    })
                }
            }).catch(error => {
                this.$message.error(error)
            })
        },

        //基于 user-base CF 的推荐
        getRecommendBaseUserCF() {
            //初始化
            this.midList2 = []
            this.recommendMovieList2 = []
            var token = getToken()
            getRecommendBaseUserCF(token).then(response => {
                this.midList2 = response.data.data
                if (this.midList2.length !== 0) {
                    this.showUserCF = true
                } else {
                    this.showUserCF = false
                }
                for (let index = 0; index < this.midList2.length; index++) {
                    getMovieDetailByID(this.midList2[index]).then(response => {
                        this.recommendMovieList2.push(response.data)
                    }).catch(error => {
                        this.$message.error(error)
                    })
                }
            }).catch(error => {
                this.$message.error(error)
            })
        },

        //基于 item-base CF 的推荐
        getRecommendBaseItemCF() {
            //初始化
            this.midList3 = []
            this.recommendMovieList3 = []
            var token = getToken()
            getRecommendBaseItemCF(token).then(response => {
                this.midList3 = response.data.data
                if (this.midList3.length !== 0) {
                    this.showItemCF = true
                } else {
                    this.showItemCF = false
                }
                for (let index = 0; index < this.midList3.length; index++) {
                    getMovieDetailByID(this.midList3[index]).then(response => {
                        this.recommendMovieList3.push(response.data)
                    }).catch(error => {
                        this.$message.error(error)
                    })
                }
            }).catch(error => {
                this.$message.error(error)
            })
        },
    },
}
</script>
  
<style rel="stylesheet/scss" lang="scss" scoped>
.zone-container {
    width: 1000px;
    margin: auto;
}


ul {
    list-style: none;
}

.subject-tip {
    text-align: center;
    color: red;
}

.subject-list {
    display: flex;
    flex-wrap: wrap;
    margin-left: -5px;
    margin-right: -5px;
    margin-top: 10px;

    li {
        margin-bottom: 10px;
        box-sizing: border-box;
        padding-left: 5px;
        padding-right: 5px;
        overflow: hidden;
    }
}

.subject-main {
    // width: 160px;
    // height: 234px;
    width: 140px;
    height: 200px;
}

.subject-info {
    overflow: hidden;
    float: left;
    text-align: center;
}

.subject-info-title {
    overflow: hidden;
    margin-top: 3px;
}

.subject-info-title-text {
    display: inline-block;
    color: #27a;
    font-size: 18px;
    vertical-align: top;
    height: 24px;
    line-height: 24px;
}

.subject-info-rating {
    font-size: 14px;
    line-height: 14px;
}
</style>
  