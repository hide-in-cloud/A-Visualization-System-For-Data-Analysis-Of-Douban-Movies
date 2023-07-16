<template>
  <div class="app-container">
    <el-form ref="form" :model="form" label-width="120px">
      <el-form-item label="电影名称">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item label="类型">
        <el-checkbox-group v-model="form.type">
          <el-checkbox label="Online activities" name="type" />
          <el-checkbox label="Promotion activities" name="type" />
          <el-checkbox label="Offline activities" name="type" />
          <el-checkbox label="Simple brand exposure" name="type" />
        </el-checkbox-group>
      </el-form-item>
      <el-form-item label="年份">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item label="导演">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item label="演员">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item label="简介">
        <el-input v-model="form.desc" type="textarea" />
      </el-form-item>
      <el-form-item label="豆瓣评分">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item label="豆瓣详情url">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item label="封面">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item label="制片国家">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item label="语言">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item label="上映日期">
        <el-col :span="11">
          <el-date-picker v-model="form.date1" type="date" placeholder="Pick a date" style="width: 100%;" />
        </el-col>
      </el-form-item>
      <el-form-item label="时长">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item label="豆瓣详情url">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item label="封面">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">Create</el-button>
        <el-button @click="onCancel">Cancel</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        name: '',
        region: '',
        date1: '',
        date2: '',
        delivery: false,
        type: [],
        resource: '',
        desc: ''
      }
    }
  },
  methods: {
    onSubmit() {
      this.$message('submit!')
    },
    onCancel() {
      this.$message({
        message: 'cancel!',
        type: 'warning'
      })
    }
  }
}
</script>

<style scoped>
.line{
  text-align: center;
}
</style>

