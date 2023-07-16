<template>
  <div class="app-container">

    <el-header style="font-size: 30px">
      <div style="margin: 10px 0;">
        <el-autocomplete ref="search" v-model="inputValue" :fetch-suggestions="querySearch" placeholder="请输入用户名" clearable
          :trigger-on-focus="false" @select="handleSelect" @keyup.enter.native="fetchPage1">
          <el-button slot="append" icon="el-icon-search" @click="fetchPage1"></el-button>
        </el-autocomplete>
      </div>
      <div>
        <router-link :to="{ name: 'UserForm' }">
          <el-button size="mini" type="success">添加用户</el-button>
        </router-link>
      </div>
    </el-header>

    <el-main style="margin-top: 15px;">
      <el-table v-loading="listLoading" element-loading-text="Loading" :data="pageInfo" border fit highlight-current-row
        stripe style="width: 85%">
        <el-table-column prop="id" label="ID" width="100" align="center"></el-table-column>
        <el-table-column prop="username" label="用户名" width="300" align="center">
          <template slot-scope="scope">
            <div>
              <span>{{ scope.row.username }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="avatar" label="头像" width="500" align="center">
          <template slot-scope="scope">
            <div class="avatar-wrapper">
              <img :src="avatar(scope.row.avatar) || default_avatar + '?imageView2/1/w/80/h/80'" class="user-avatar">
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="role" label="角色" width="180" align="center">
          <template slot-scope="scope">
            <div>
              <span>{{ scope.row.role }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center" width="300" class-name="small-padding fixed-width">
          <template slot-scope="scope">
            <router-link :to="{
              name: 'UserEdit',
              params: { id: scope.row.id }
            }">
              <el-button size="mini" type="primary">编辑</el-button>
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
import { getAllUserByPage, getSearchUsername, deleteUser } from '@/api/user'
// import { mapGetters } from 'vuex'

export default {
  data() {
    return {
      pageInfo: [],                         //数据列表

      inputValue: '',                       //搜索框里的内容
      timeout: null,                        //定时器

      total: null,                          //总个数
      currentPage: 1,                       //当前页数
      pageSize: 10,                         //每页个数
      pageSizes: [10, 20, 50, 100],         //每页个数选择列表

      listLoading: false,                     //列表是否在加载

      default_avatar: "https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png"  //默认头像
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
        search: this.inputValue
      }
      getAllUserByPage(params).then(response => {
        // console.log('查询分页')
        this.pageInfo = response.data.results
        this.total = response.data.count
        this.listLoading = false
      }).catch(error => {
        this.listLoading = false
        this.$message.error(error)
      })
    },

    avatar(user_avatar) {
      if (user_avatar) {
        //用户有头像，给头像路径加上服务器api
        return process.env.VUE_APP_BASE_API + user_avatar
      } else {
        // console.log('使用默认头像')
        //默认头像
        return user_avatar
      }
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
        getSearchUsername(queryString).then(response => {
          results = response.data.data
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
    handleDelete(user_id) {
      if (confirm('确认删除吗?')) {
        deleteUser(user_id).then(() => {
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
  
<style lang="scss" scoped>
.el-autocomplete {
  width: 800px;
}

.cover-container {
  max-height: 155px;
  width: 115px;
  text-align: center;
}

.avatar-wrapper {
  margin-top: 5px;
  position: relative;

  .user-avatar {
    cursor: pointer;
    width: 80px;
    height: 80px;
    border-radius: 10px;
  }
}
</style>
  