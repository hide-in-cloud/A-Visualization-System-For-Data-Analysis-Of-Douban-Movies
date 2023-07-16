import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/user/login/',
    method: 'post',
    data
  })
}

//查询当前用户名的数量， 1：已存在   0：没人使用
export function usernameCount(username) {
  return request({
    url: '/user/usernameCount/',
    method: 'get',
    params: { username }
  })
}

//用户注册
export function register(data) {
  return request({
    url: '/user/',
    method: 'post',
    data
  })
}

//通过ID获取用户信息
export function getUserByID(id) {
  return request({
    url: `/user/${id}/`,
    method: 'get'
  })
}

// //修改用户资料
// export function editUser(id, data) {
//   return request({
//     url: `/user/${id}/`,
//     method: 'put',
//     data
//   })
// }

//删除用户
export function deleteUser(id) {
  return request({
    url: `/user/${id}/`,
    method: 'delete'
  })
}

//获取用户信息
export function getInfo(token) {
  return request({
    url: '/user/info/',
    method: 'get',
    params: { token }
  })
}

//修改用户部分资料
export function editUserInfo(id, userInfoForm) {
  return request({
    url: `/user_update/${id}/`,
    method: 'patch',
    data: userInfoForm
  })
}

//用户注销
export function logout(token) {
  return request({
    url: '/user/logout/',
    method: 'post',
    data: token
  })
}

//根据输入的关键词搜索相关用户名
export function getSearchUsername(keyword) {
  return request({
    url: '/user/getSearchUsername/',
    method: 'get',
    params: { keyword }
  })
}

//初始化，显示用户收藏
export function getFavorIDList(token) {
  return request({
    url: '/user/favorIDList/',
    method: 'get',
    params: { token }
  })
}

//用户点击收藏或取消
export function favor(token, movie_id) {
  return request({
    url: '/user/favor/',
    method: 'post',
    params: { token, movie_id }
  })
}

//初始化显示用户对电影的评分
export function getUserFavor(token, movie_id) {
  return request({
    url: '/user/getUserFavor/',
    method: 'get',
    params: { token, movie_id }
  })
}

//初始化，显示用户收藏
export function getRatingIDList(token) {
  return request({
    url: '/user/getRatingIDList/',
    method: 'get',
    params: { token }
  })
}

//用户评分电影
export function userRating(token, movie_id, rating) {
  return request({
    url: '/user/userRating/',
    method: 'post',
    params: { token, movie_id, rating }
  })
}

//初始化显示用户对电影的评分
export function getUserRate(token, movie_id) {
  return request({
    url: '/user/getUserRate/',
    method: 'get',
    params: { token, movie_id }
  })
}

//根据用户id和电影id删除对应的用户评分信息
export function deleteUserRate(token, movie_id) {
  return request({
    url: '/user/deleteUserRate/',
    method: 'post',
    params: { token, movie_id }
  })
}

//根据分页获取用户信息(模糊搜索)
export function getAllUserByPage(params) {
  return request({
      url: '/userByPage/',
      method: 'get',
      params
  })
}