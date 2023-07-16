<template>
  <div class="navbar">
    <hamburger :is-active="sidebar.opened" class="hamburger-container" @toggleClick="toggleSideBar" />

    <breadcrumb class="breadcrumb-container" />

    <div class="right-menu">
      <el-dropdown class="avatar-container" trigger="click">
        <div class="avatar-wrapper">
          <img :src="avatar || default_avatar + '?imageView2/1/w/80/h/80'" class="user-avatar">
          <i class="el-icon-caret-bottom" />
        </div>
        <el-dropdown-menu slot="dropdown" class="user-dropdown">
          <!-- <router-link to="/">
            <el-dropdown-item>
              Home
            </el-dropdown-item>
          </router-link> -->

          <el-dropdown-item @click.native="dialogInfoVisible = true">个人资料</el-dropdown-item>
          <!-- 个人资料的对话框 -->
          <el-dialog title="个人资料" :visible.sync="dialogInfoVisible" append-to-body width="40%">
            <!-- form表单 -->
            <el-form :model="form" :rules="rules" ref="form" label-width="100px">
              <!-- 头像 -->
              <el-form-item label="头像" prop="avatar">
                <el-avatar shape="square" :size="80" @error="errorHandler">
                  <img referrerpolicy="no-referrer" :src="imageUrl || avatar || default_avatar" class="avatar">
                </el-avatar>
                <!-- 头像上传 -->
                <input type="file" @change="getImageFile" accept="image/*" id="avatar" style="margin-left: 20px;">
              </el-form-item>
              <!-- 用户名 -->
              <el-form-item label="用户名" prop="username">
                <el-input v-model="form.username"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button @click.native="dialogInfoVisible = false">取 消</el-button>
                <el-button type="primary" @click.native="onSubmit()">确 定</el-button>
              </el-form-item>
            </el-form>
          </el-dialog>

          <el-dropdown-item @click.native="dialogPasswordVisible = true">修改密码</el-dropdown-item>
          <!-- 修改密码的对话框 -->
          <el-dialog title="修改密码" :visible.sync="dialogPasswordVisible" append-to-body width="40%">
            <!-- form表单 -->
            <el-form :model="passwordForm" :rules="passwordRules" ref="passwordForm" label-width="100px">
              <el-form-item label="旧密码" prop="old_password">
                <el-input v-model="passwordForm.old_password"></el-input>
              </el-form-item>
              <el-form-item label="新密码" prop="password">
                <el-input v-model="passwordForm.password"></el-input>
              </el-form-item>
              <el-form-item label="确认新密码" prop="confirm_password">
                <el-input v-model="passwordForm.confirm_password"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button @click.native="dialogPasswordVisible = false">取 消</el-button>
                <el-button type="primary" @click.native="onSubmitPwd()">确 定</el-button>
              </el-form-item>
            </el-form>
          </el-dialog>

          <el-dropdown-item @click.native="dialogFavorVisible = true">收藏夹</el-dropdown-item>
          <!-- 收藏夹的对话框 -->
          <el-dialog title="收藏夹" :visible.sync="dialogFavorVisible" append-to-body width="50%">
            <ul class="subject-list">
              <li v-for="item in favorMovieList">
                <el-card>
                  <div class="subject-main">
                    <div class="subject-cover-container" style="padding-top: 140%; position: relative;">
                      <img class="cover-pic" referrerpolicy="no-referrer" :src="item.cover" alt="cover"
                        style="position: absolute;width: 100%; height: 100%; inset: 0px; display: block; object-fit: cover;">
                    </div>
                    <div class="subject-info">
                      <div class="subject-info-title">
                        <span class="subject-info-title-text">{{ item.title }}</span>
                      </div>
                      <div class="subject-info-rating">
                        <el-rate :value="stringToNumber(item.rate)" disabled show-score text-color="#ff9900"
                          :score-template="item.rate">
                        </el-rate>
                      </div>
                    </div>
                  </div>
                  <div>
                    <el-button type="primary" @click="handleRouterLink(item.id)">查看</el-button>
                    <el-popconfirm title="确定从收藏夹中移除吗" confirm-button-text="确定" cancel-button-text="取消"
                      @confirm="deleteFavor(item.id)" @cancel="handleCancel">
                      <el-button type="danger" slot="reference">删除</el-button>
                    </el-popconfirm>
                  </div>
                </el-card>
              </li>
            </ul>
          </el-dialog>

          <el-dropdown-item @click.native="dialogRatingVisible = true">个人评分</el-dropdown-item>
          <!-- 个人评分的对话框 -->
          <el-dialog title="个人评分" :visible.sync="dialogRatingVisible" append-to-body width="50%">
            <ul class="subject-list">
              <li v-for="item in ratingMovieList">
                <el-card>
                  <div class="subject-main">
                    <div class="subject-cover-container" style="padding-top: 140%; position: relative;">
                      <img class="cover-pic" referrerpolicy="no-referrer" :src="item.cover" alt="cover"
                        style="position: absolute;width: 100%; height: 100%; inset: 0px; display: block; object-fit: cover;">
                    </div>
                    <div class="subject-info">
                      <div class="subject-info-title">
                        <span class="subject-info-title-text">{{ item.title }}</span>
                      </div>
                      <div class="subject-info-rating">
                        <el-rate :value="stringToNumber(item.rate)" disabled show-score text-color="#ff9900"
                          :score-template="item.rate">
                        </el-rate>
                      </div>
                    </div>
                  </div>
                  <div>
                    <el-button type="primary" @click="handleRouterLink(item.id)">查看</el-button>
                    <el-popconfirm title="确定从个人评分中移除吗" confirm-button-text="确定" cancel-button-text="取消"
                      @confirm="deleteRating(item.id)" @cancel="handleCancel">
                      <el-button type="danger" slot="reference">删除</el-button>
                    </el-popconfirm>
                  </div>
                </el-card>
              </li>
            </ul>
          </el-dialog>

          <el-dropdown-item divided @click.native="logout">
            <span style="display:block;">注销</span>
          </el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </div>

    <div class="right-username">
      <span class="username-container">
        {{ name }}
      </span>
    </div>

  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { getToken } from '@/utils/auth'
import { usernameCount } from "@/api/user";
import Breadcrumb from '@/components/Breadcrumb'
import Hamburger from '@/components/Hamburger'

export default {
  components: {
    Breadcrumb,
    Hamburger
  },
  data() {
    const validateUsername = (rule, value, callback) => {
      if (value.trim() === '') {
        callback(new Error('请输入用户名'));
      } else if (value.length < 3 || value.length > 16) {
        callback(new Error('用户名必须为3-16个字符'))
      } else if (value === this.$store.state.user.name) {
        callback()
      } else {
        //检查用户名是否重复
        usernameCount(value).then((res) => {
          if (res.data.count > 0) {
            //如果用户名不变，则通过
            if (value === this.userInfo.username) {
              callback()
            }
            callback(new Error('用户名已存在!'))
          } else {
            callback()
          }
        })
      }
    }
    const validatePassword = (rule, value, callback) => {
      if (value.length < 6) {
        callback(new Error('密码不能少于6位'))
      } else if (value === this.passwordForm.old_password) {
        callback(new Error('新密码不能与旧密码一致'))
      } else {
        callback()
      }
    }
    const validateConfirmPassword = (rule, value, callback) => {
      if (value.trim() === '') {
        callback(new Error('请再次输入密码'));
      } else if (value !== this.passwordForm.password) {
        callback(new Error('两次输入密码不一致!'));
      } else {
        callback();
      }
    }
    return {
      dialogInfoVisible: false,
      dialogPasswordVisible: false,
      dialogFavorVisible: false,
      dialogRatingVisible: false,

      form: {
        avatar: null,                              //头像
        username: this.$store.state.user.name,     //用户名
      },
      rules: {
        username: [{ required: true, trigger: 'blur', validator: validateUsername }]
      },
      default_avatar: "https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png",  //默认头像
      // actionUrl: process.env.VUE_APP_BASE_API + '/uploadImg/',    //上传头像的服务路径
      imageUrl: '',

      passwordForm: {
        old_password: null,                 //旧密码
        password: null,                     //新密码
        confirm_password: null,             //确认密码
      },
      passwordRules: {
        password: [{ required: true, trigger: 'blur', validator: validatePassword }],
        confirm_password: [{ required: true, trigger: 'blur', validator: validateConfirmPassword }]
      },
    }
  },
  computed: {
    ...mapGetters([
      'sidebar',
      'avatar',
      'name',
      'password',
      'favorMovieList',
      'ratingMovieList'
    ])
  },
  mounted() {
    this.$store.dispatch('user/initFavor')    //初始化收藏列表
    this.$store.dispatch('user/initRatingIDList')    //初始化收藏列表
  },
  methods: {
    //(展示/隐藏)左旁栏
    toggleSideBar() {
      this.$store.dispatch('app/toggleSideBar')
    },
    //注销
    async logout() {
      await this.$store.dispatch('user/logout')
      this.$router.push(`/login?redirect=${this.$route.fullPath}`)
    },

    //图片加载失败
    errorHandler() {
      return true
    },

    //预览图片
    preview(file) {
      // 保存下当前 this ，就是vue实例
      var _this = this;
      // 创建一个FileReader()对象，它里面有个readAsDataURL方法
      let reader = new FileReader();
      // readAsDataURL方法可以将上传的图片格式转为base64,然后在存入到图片路径
      reader.readAsDataURL(file);
      // 文件读取成功完成时触发
      reader.onloadend = function () {
        _this.imageUrl = this.result // reader.result返回文件的内容。
      }
    },
    //选择图片触发事件
    getImageFile: function (e) {
      let file = e.target.files[0];
      if (file) {
        this.preview(file)
        this.form.avatar = file
      } else {
        return
      }
    },
    //确认修改用户信息
    onSubmit() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          //用户信息不变，不需要修改
          if (this.form.username === this.name && this.form.avatar === null) {
            this.dialogInfoVisible = false  //隐藏对话框
            return
          }
          //用FormData提交数据
          let formData = new FormData
          formData.append('username', this.form.username)
          if (this.form.avatar) {
            formData.append('avatar', this.form.avatar)
          }
          // console.log(this.form)
          this.$store.dispatch('user/editInfo', formData).then(() => {
            this.$message.success('修改成功!')
            this.dialogInfoVisible = false  //隐藏对话框
          }).catch(error => {
            this.$message.error(error)
          })
        } else {
          this.$message.error('数据格式不正确');
          return false;
        }
      });
    },

    //确认修改密码
    onSubmitPwd() {
      this.$refs.passwordForm.validate((valid) => {
        if (valid) {
          //验证旧密码
          if (this.passwordForm.old_password !== this.password) {
            this.$message.error('旧密码不正确');
            return
          }
          //用FormData提交数据
          let formData = new FormData
          formData.append('password', this.passwordForm.password)
          this.$store.dispatch('user/editPassword', formData).then(() => {
            this.$message.success('修改成功!')
            this.$refs.passwordForm.resetFields()
            this.dialogPasswordVisible = false  //隐藏对话框
          }).catch(error => {
            this.$message.error(error)
          })
        } else {
          this.$message.error('数据格式不正确');
          return false;
        }
      });
    },

    //从收藏夹中移除一项
    deleteFavor(movie_id) {
      this.$store.dispatch('user/handleFavor', movie_id).then(() => {
        this.$message.success('删除成功!');
      }, reason => {
        this.$message.error(reason)
      }).catch(error => {
        this.$message.error('服务器出错:', error)
      })
    },
    //取消删除
    handleCancel() {
      this.$message('取消删除');
    },

    //从个人评分表中移除一项
    deleteRating(movie_id) {
      this.$store.dispatch('user/deleteRating', movie_id).then(() => {
        this.$message.success('删除成功!');
      }, reason => {
        this.$message.error(reason)
      }).catch(error => {
        this.$message.error('服务器出错:', error)
      })
    },

    //跳转到详情页面
    handleRouterLink(movie_id){
      this.dialogFavorVisible = false
      this.dialogRatingVisible = false
      this.$router.push({
                        name: 'Detail',
                        params: { movie_id: movie_id }
                      })
    },
  }
}
</script>

<style lang="scss" scoped>
.navbar {
  height: 50px;
  overflow: hidden;
  position: relative;
  background: #fff;
  box-shadow: 0 1px 4px rgba(0, 21, 41, .08);

  .hamburger-container {
    line-height: 46px;
    height: 100%;
    float: left;
    cursor: pointer;
    transition: background .3s;
    -webkit-tap-highlight-color: transparent;

    &:hover {
      background: rgba(0, 0, 0, .025)
    }
  }

  .breadcrumb-container {
    float: left;
  }

  .right-username {
    float: right;
    height: 100%;
    line-height: 50px;
    margin-right: 16px;

    .username-container {
      font-size: 16px;
    }
  }

  .right-menu {
    float: right;
    height: 100%;
    line-height: 50px;

    &:focus {
      outline: none;
    }

    .right-menu-item {
      display: inline-block;
      padding: 0 8px;
      height: 100%;
      font-size: 18px;
      color: #5a5e66;
      vertical-align: text-bottom;

      &.hover-effect {
        cursor: pointer;
        transition: background .3s;

        &:hover {
          background: rgba(0, 0, 0, .025)
        }
      }
    }

    .avatar-container {
      margin-right: 30px;

      .avatar-wrapper {
        margin-top: 5px;
        position: relative;

        .user-avatar {
          cursor: pointer;
          width: 40px;
          height: 40px;
          border-radius: 10px;
        }

        .el-icon-caret-bottom {
          cursor: pointer;
          position: absolute;
          right: -20px;
          top: 25px;
          font-size: 12px;
        }
      }
    }
  }
}

.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.avatar-uploader .el-upload:hover {
  border-color: #409EFF;
}

.avatar-uploader-icon {
  font-size: 25px;
  color: #8c939d;
  width: 80px;
  height: 80px;
  line-height: 80px;
  text-align: center;
}

.avatar {
  border-radius: 10px;
  width: 80px;
  height: 80px;
}

ul {
  list-style: none;
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
  }
}

.subject-main {
  width: 167px;
  height: 232px;
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
