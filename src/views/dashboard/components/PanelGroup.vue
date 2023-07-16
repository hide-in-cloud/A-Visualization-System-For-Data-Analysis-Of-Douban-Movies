<template>
  <el-row :gutter="36" class="panel-group">
    <el-col :xs="16" :sm="16" :lg="6" class="card-panel-col">
      <div class="card-panel">
        <div class="card-panel-icon-wrapper icon-people">
          <div class="card-panel-cover" style="">
            <img referrerpolicy="no-referrer" :src="homeCover" alt="cover"
              style="width: 100%; height: 100%; inset: 0px; object-fit: fill;">
          </div>
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">本系统收录的电影数目为</div>
          <div class="card-panel-movie">
            <div style="font-size: 20px; color: #f4516c;">{{ movieSum }}部</div>
          </div>
        </div>
      </div>
    </el-col>
    <el-col :xs="16" :sm="16" :lg="6" class="card-panel-col">
      <div class="card-panel">
        <div class="card-panel-icon-wrapper icon-message">
          <div class="card-panel-cover" style="padding-top: 140%; position: relative;">
            <img referrerpolicy="no-referrer" :src="highestMovie.cover" alt="cover"
              style="position: absolute; width: 100%; height: 100%; inset: 0px; object-fit: fill;">
          </div>
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">豆瓣最高评分电影</div>
          <div class="card-panel-movie">
            <div v-loading="loading" class="card-panel-movie-title">{{ highestMovie.title }}</div>
            <div v-loading="loading" class="card-panel-movie-rate">{{ highestMovie.rate }}分</div>
          </div>
        </div>
      </div>
    </el-col>
    <el-col :xs="16" :sm="16" :lg="6" class="card-panel-col">
      <div class="card-panel">
        <div class="card-panel-icon-wrapper icon-money">
          <div class="card-panel-cover" style="">
            <img referrerpolicy="no-referrer" :src="latestMovie.cover" alt="cover"
              style="width: 100%; height: 100%; inset: 0px; object-fit: fill;">
          </div>
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">最新上映电影</div>
          <div class="card-panel-movie">
            <div v-loading="loading" class="card-panel-movie-title">{{ latestMovie.title }}</div>
            <div v-loading="loading" class="card-panel-movie-rate">{{ latestMovie.rate }}分</div>
          </div>
        </div>
      </div>
    </el-col>
    <el-col :xs="16" :sm="16" :lg="6" class="card-panel-col">
      <div class="card-panel">
        <div class="card-panel-icon-wrapper icon-shopping">
          <div class="card-panel-cover" style="padding-top: 140%; position: relative;">
            <img referrerpolicy="no-referrer" :src="hotMovie.cover" alt="cover"
              style="position: absolute;width: 100%; height: 100%; inset: 0px; object-fit: fill;">
          </div>
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">最近热门电影</div>
          <div class="card-panel-movie">
            <div v-loading="loading" class="card-panel-movie-title">{{ hotMovie.title }}</div>
            <div v-loading="loading" class="card-panel-movie-rate">{{ hotMovie.rate }}分</div>
          </div>
        </div>
      </div>
    </el-col>
  </el-row>
</template>
  
<script>
// import movie from '@/store/modules/movie';
import { mapActions } from 'vuex'
import { getHomeInfo } from '@/api/movie'

export default {
  data() {
    return {
      home_img: 'src/assets/img/img006.jpg',
      // info: this.$store.state.movie.info || [],
      homeCover: '',
      highestMovie: {},
      latestMovie: {},
      hotMovie: {},
      loading: true
    }
  },
  computed: {
    movieSum() {
      return this.$store.state.movie.total
    },
  },
  mounted() {
    this.GetAllMovieInfo()
    this.initHome()
  },
  methods: {
    //获取全部的电影信息
    ...mapActions('movie', { GetAllMovieInfo: 'GetAllMovieInfo' }),
    //初始化，获取首页信息
    initHome() {
      this.loading = true
      getHomeInfo().then(response => {
        this.homeCover = response.data.home_cover
        this.highestMovie = response.data.highest
        this.latestMovie = response.data.latest
        this.hotMovie = response.data.hot
      })
      this.loading = false
    },
    // //字符串转数字，并把10分制变为5分制
    // stringToNumber(val) {
    //   return parseFloat(val / 2)
    // }
  }
}
</script>
  
<style rel="stylesheet/scss" lang="scss" scoped>
img {
    border-width: 0;
    vertical-align: middle;
    max-width: 100%;
}

.panel-group {
  margin-top: 16px;

  .card-panel-col {
    margin-bottom: 24px;
  }

  .card-panel {
    display: flex;
    flex-wrap: wrap;
    max-height: 188px;
    font-size: 18px;
    // position: relative;
    overflow: hidden;
    color: #666;
    background: #fff;
    box-shadow: 4px 4px 10px rgba(0, 0, 0, .05);
    border-color: rgba(0, 0, 0, .05);

    &:hover {
      .card-panel-icon-wrapper {
        color: #fff;
      }
      .icon-people {
        background: #40c9c6;
      }
      .icon-message {
        background: #36a3f7;
      }
      .icon-money {
        background: #f4516c;
      }
      .icon-shopping {
        background: #34bfa3
      }
    }

    .card-panel-icon-wrapper {
      // float: left;
      padding: 8px;
      transition: all 0.38s ease-out;
      border-radius: 6px;
    }

    .card-panel-cover {
      width: 120px;
      max-height: 188px;
    }

    .card-panel-description {
      flex: 1;
      // float: right;
      font-weight: bold;
      text-align: center;
      margin: 15px;
      margin-top: 25px;

      .card-panel-text {
        max-width: 240px;
        font-size: 20px;
        margin-bottom: 18px;
      }

      .card-panel-movie {
        line-height: 20px;
        font-size: 20px;
        margin-bottom: 12px;
        .card-panel-movie-title {
          color: #27a;
          font-size: 20px;
          margin-bottom: 8px;
        }
        .card-panel-movie-rate {
          color: #ffac2c;
          font-size: 16px;
        }
      }
    }
  }
}
</style>
  