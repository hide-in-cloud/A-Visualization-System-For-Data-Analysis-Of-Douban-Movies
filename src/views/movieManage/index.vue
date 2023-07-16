<template>
  <div class="app-container">

    <el-header style="font-size: 30px">
      <div style="margin: 10px 0;">
        <el-autocomplete ref="search" v-model="inputValue" :fetch-suggestions="querySearch" placeholder="请输入内容" clearable
          :trigger-on-focus="false" @select="handleSelect" @keyup.enter.native="fetchPage1">
          <el-button slot="append" icon="el-icon-search" @click="fetchPage1"></el-button>
        </el-autocomplete>
      </div>
    </el-header>

    <el-main>
      <el-table v-loading="listLoading" element-loading-text="Loading" :data="pageMovie" border fit highlight-current-row
        stripe style="width: 100%">
        <el-table-column prop="id" label="ID" width="95" align="center">
          <!-- <template slot-scope="scope">
          {{ scope.$index }}
        </template> -->
        </el-table-column>
        <el-table-column label="封面" width="180" align="center">
          <template slot-scope="scope">
            <div class="cover-container">
              <img class="cover-pic" referrerpolicy="no-referrer" :src="scope.row.cover" alt="cover"
                style="width: 100%; height: 100%; display: inline-block; object-fit: fill;">
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="title" label="电影名称" width="180" align="center">
          <template slot-scope="scope">
            <div>
              <span v-show="!scope.row.isEdit">{{ scope.row.title }}</span>
              <input type="text" ref="inputTitle" v-show="scope.row.isEdit" v-model="scope.row.title" />
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="rate" label="评分" width="100" align="center">
          <template slot-scope="scope">
            <div>
              <span v-show="!scope.row.isEdit">{{ scope.row.rate }}</span>
              <input type="text" width="50" ref="inputRate" v-show="scope.row.isEdit" v-model="scope.row.rate" />
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="types" label="种类" width="180" align="center">
          <template slot-scope="scope">
            <div>
              <span v-show="!scope.row.isEdit">{{ scope.row.types }}</span>
              <input type="text" ref="inputTypes" v-show="scope.row.isEdit" v-model="scope.row.types" />
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="directors" label="导演" width="180" align="center">
          <template slot-scope="scope">
            <div>
              <span v-show="!scope.row.isEdit">{{ scope.row.directors }}</span>
              <input type="text" ref="inputDirectors" v-show="scope.row.isEdit" v-model="scope.row.directors" />
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="countries" label="国家" width="120" align="center">
          <template slot-scope="scope">
            <div>
              <span v-show="!scope.row.isEdit">{{ scope.row.countries }}</span>
              <input type="text" ref="inputCountries" v-show="scope.row.isEdit" v-model="scope.row.countries" />
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="runtime" label="时长" width="120" align="center">
          <template slot-scope="scope">
            <div>
              <span v-show="!scope.row.isEdit">{{ scope.row.runtime }}分钟</span>
              <input type="text" ref="inputRuntime" v-show="scope.row.isEdit" v-model="scope.row.runtime" />
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="release_date" label="上映日期" width="180" align="center">
          <template slot-scope="scope">
            <div>
              <span v-show="!scope.row.isEdit">{{ scope.row.release_date }}</span>
              <input type="text" ref="inputRelease_date" v-show="scope.row.isEdit" v-model="scope.row.release_date" />
            </div>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center" width="230" class-name="small-padding fixed-width">
          <template slot-scope="scope">
            <router-link :to="{
              name: 'Detail',
              params: { movie_id: scope.row.id }
            }">
              <el-button type="primary" size="mini" style="display: inline-block; margin-right: 10px;">查看</el-button>
            </router-link>

            <router-link :to="{
              name: 'MovieEdit',
              params: { id: scope.row.id }
            }">
              <el-button size="mini" type="primary" style="display: inline-block; margin-right: 10px;">编辑</el-button>
            </router-link>

            <el-button size="mini" type="danger" @click="handleDelete(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-main>

    <el-footer style="margin-left: 300px; font-size: 30px">
      <div class="block">
        <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="currentPage"
          background :page-sizes="pageSizes" :page-size="pageSize" layout="total, sizes, prev, pager, next, jumper"
          :total="total">
        </el-pagination>
      </div>
    </el-footer>

  </div>
</template>

<script>
import { getMovieDetailByPage, getSearchTitles, deleteMovieInfo } from '@/api/movie'

export default {
  data() {
    return {
      pageMovie: this.$store.state.movie.info || [], //数据列表

      inputValue: '',                       //搜索框里的内容
      timeout: null,                        //定时器

      total: this.$store.state.movie.total, //总个数
      currentPage: 1,                       //当前页数
      pageSize: 10,                         //每页个数
      pageSizes: [10, 20, 50, 100],         //每页个数选择列表

      listLoading: false                     //列表是否在加载
    }
  },
  mounted() {
    this.fetchDataByPage()
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
      // console.log(`每页 ${val} 条`);
      this.pageSize = val
      scrollTo(0, 0)      //回到顶部
      this.fetchDataByPage()
    },
    //分页点击事件
    handleCurrentChange(val) {
      // console.log(`当前页: ${val}`);
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

    //删除按钮响应
    handleDelete(id) {
      if (confirm('确认删除吗?')) {
        deleteMovieInfo(id).then(() => {
          this.$message.success('删除成功')
          this.fetchDataByPage()
        }).catch(error => {
          this.$message.error(error)
        })
      }
    },
  }
}
</script>

<style scoped>
.el-autocomplete {
  width: 800px;
}

.cover-container {
  max-height: 155px;
  width: 115px;
  text-align: center;
}
</style>
