<template>
  <div class="register-box">
    <div class="register-container">
      <div id="register-header">
        <h2>用户注册</h2>
      </div>
      <el-form ref="registerForm" :model="registerForm" :rules="registerRules" class="register-form" auto-complete="on"
        label-position="left">

        <el-form-item prop="username">
          <span class="svg-container">
            <svg-icon icon-class="user" />
          </span>
          <el-input ref="username" v-model="registerForm.username" placeholder="用户名" name="username" type="text"
            tabindex="1" auto-complete="on" />
        </el-form-item>

        <el-form-item prop="password">
          <span class="svg-container">
            <svg-icon icon-class="password" />
          </span>
          <el-input :key="passwordType" ref="password" v-model="registerForm.password" :type="passwordType"
            placeholder="密码" name="password" tabindex="2" auto-complete="on" />
          <span class="show-pwd" @click="showPwd">
            <svg-icon :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'" />
          </span>
        </el-form-item>

        <el-form-item prop="confirm_password">
          <span class="svg-container">
            <svg-icon icon-class="password" />
          </span>
          <el-input :key="passwordType" ref="confirm_password" v-model="registerForm.confirm_password"
            :type="passwordType" placeholder="再次确认密码" name="confirm_password" tabindex="2" auto-complete="on"
            @keyup.enter.native="handleRegister" />
        </el-form-item>

        <el-button :loading="loading" type="primary" style="width:100%;margin-bottom:20px;"
          @click.native.prevent="handleRegister">注册</el-button>
      </el-form>

      <div class="login">
        <router-link to="/login">
          <el-link type="primary">返回登录</el-link>
        </router-link>
      </div>
    </div>
  </div>
</template>
  
<script>
import { usernameCount } from "@/api/user";

export default {
  data() {
    const validateUsername = (rule, value, callback) => {
      if (value.trim() === '') {
        callback(new Error('请输入用户名'));
      } else if (value.length < 3 || value.length > 16) {
        callback(new Error('用户名必须为3-16个字符'))
      } else {
        //检查用户名是否重复
        usernameCount(value).then((res) => {
          console.log(res)
          if (res.data.count > 0) {
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
      } else {
        callback()
      }
    }
    const validateConfirmPassword = (rule, value, callback) => {
      if (value.trim() === '') {
        callback(new Error('请再次输入密码'));
      } else if (value !== this.registerForm.password) {
        callback(new Error('两次输入密码不一致!'));
      } else {
        callback();
      }
    }
    return {
      registerForm: {
        username: '',         //用户名
        password: '',         //密码
        confirm_password: '', //确认密码
        avatar: null,         //头像默认为空
        role: 'user'          //角色，默认为用户
        // code: '',             //验证码
      },
      registerRules: {
        username: [{ required: true, trigger: 'blur', validator: validateUsername }],
        password: [{ required: true, trigger: 'blur', validator: validatePassword }],
        confirm_password: [{ required: true, trigger: 'blur', validator: validateConfirmPassword }]
      },
      loading: false,
      passwordType: 'password',
      redirect: undefined
    }
  },
  methods: {
    //是否显示密码
    showPwd() {
      if (this.passwordType === 'password') {
        this.passwordType = ''
      } else {
        this.passwordType = 'password'
      }
      this.$nextTick(() => {
        this.$refs.password.focus()
      })
    },
    //注册
    handleRegister() {
      this.$refs.registerForm.validate(valid => {
        if (valid) {
          this.loading = true
          this.$store.dispatch('user/register', this.registerForm).then(() => {
            //跳转到登录页面
            this.$router.push({ path: '/login' })
            this.loading = false
          }).catch((error) => {
            this.loading = false
            this.$message.error('注册出错，请重新注册。')
          })
        } else {
          this.$message.error('invalid')
          return false
        }
      })
    },

  }
}
</script>
  
<style lang="scss">
/* 修复input 背景不协调 和光标变色 */
/* Detail see https://github.com/PanJiaChen/vue-element-admin/pull/927 */

$bg: #dddddd;
$light_gray: rgb(0, 0, 0);
$cursor: #1e5871;

@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  .register-container .el-input input {
    color: $cursor;
  }
}

/* reset element-ui css */
.register-container {
  .el-input {
    display: inline-block;
    height: 47px;
    width: 85%;

    input {
      background: transparent;
      border: 0px;
      border-radius: 0px;
      padding: 12px 5px 12px 15px;
      color: $light_gray;
      height: 47px;
      caret-color: $cursor;

      &:-webkit-autofill {
        box-shadow: 0 0 0px 1000px $bg inset !important;
        -webkit-text-fill-color: $cursor !important;
      }
    }
  }

  .el-form-item {
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    color: #454545;
  }
}
</style>

<style scoped>
.register-box {
  width: 450px;
  height: 400px;
  border: 1px solid #dddddd;
  border-radius: 5px;
  box-shadow: 5px 5px 20px #aaa;

  margin-left: auto;
  margin-right: auto;
  margin-top: 150px;
}

.register-box .register-container {
  padding: 10px 35px;
}

.register-box #register-header {
  padding: 10px 30px;
  text-align: center;
}

.login {
  float: right;
  font-size: 15px;
  color: blue;
  margin-bottom: 10px;
}
</style>
  