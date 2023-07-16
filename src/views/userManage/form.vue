<template>
    <div class="app-container">
        <el-form ref="userForm" :model="userForm" :rules="rules" label-width="120px">
            <el-form-item prop="username" label="用户名">
                <el-col :span="8">
                    <el-input v-model="userForm.username" />
                </el-col>
            </el-form-item>
            <el-form-item prop="password" label="密码">
                <el-col :span="8">
                    <el-input v-model="userForm.password" type="password" placeholder="请输入密码" name="password"
                        auto-complete="on" />
                </el-col>
            </el-form-item>
            <el-form-item prop="confirm_password" label="确认密码">
                <el-col :span="8">
                    <el-input v-model="userForm.confirm_password" type="password" placeholder="请再次确认密码"
                        name="confirm_password" auto-complete="on" />
                </el-col>
            </el-form-item>
            <el-form-item prop="avatar" label="头像">
                <el-col :span="4">
                    <input type="file" @change="getImageFile" accept="image/*" id="avatar" style="margin-left: 20px;">
                </el-col>
            </el-form-item>
            <el-form-item prop="role" label="角色">
                <el-radio v-model="userForm.role" label="user">用户</el-radio>
                <el-radio v-model="userForm.role" label="admin">管理员</el-radio>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="onSubmit">创建</el-button>
                <el-button @click="onCancel">取消</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>
  
<script>
import { usernameCount, register } from "@/api/user";

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
            } else if (value !== this.userForm.password) {
                callback(new Error('两次输入密码不一致!'));
            } else {
                callback();
            }
        }
        return {
            userForm: {
                username: '',
                password: '',
                confirm_password: '', //确认密码
                avatar: null,
                role: 'user'
            },
            rules: {
                username: [{ required: true, trigger: 'blur', validator: validateUsername }],
                password: [{ required: true, trigger: 'blur', validator: validatePassword }],
                confirm_password: [{ required: true, trigger: 'blur', validator: validateConfirmPassword }]
            },
            redirect: undefined
        }
    },
    methods: {
        //选择图片触发事件
        getImageFile: function (e) {
            let file = e.target.files[0];
            if (file) {
                this.userForm.avatar = file
            }
        },
        //添加用户事件
        onSubmit() {
            this.$refs.userForm.validate((valid) => {
                if (valid) {
                    // 用FormData提交数据
                    let formData = new FormData
                    formData.append('username', this.userForm.username)
                    formData.append('password', this.userForm.password)
                    if (this.userForm.avatar) {
                        formData.append('avatar', this.userForm.avatar)
                    }
                    formData.append('role', this.userForm.role)
                    register(formData).then(() => {
                        this.$message.success('添加成功!')
                        //跳转回用户列表
                        this.$router.push({ path: '/userManage/index' })
                    }).catch(error => {
                        this.$message.error(error)
                    })
                } else {
                    this.$message.error('数据格式不正确');
                    return false;
                }
            });
        },
        //取消按钮事件
        onCancel() {
            this.$message.warning('取消!')
            //跳转回用户列表
            this.$router.go(-1)
        }
    }
}
</script>
  
<style scoped>
.line {
    text-align: center;
}
</style>
  
  