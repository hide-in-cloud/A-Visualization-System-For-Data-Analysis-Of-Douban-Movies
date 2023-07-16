import { login, register, logout, getInfo, editUserInfo, getFavorIDList, favor, getRatingIDList, userRating, deleteUserRate } from '@/api/user'
import { getMovieDetailByID } from '@/api/movie'
import { getToken, setToken, removeToken, getRole, setRole, removeRole } from '@/utils/auth'
import { resetRouter } from '@/router'
import Vue from 'vue';


const getDefaultState = () => {
  return {
    token: getToken(),
    id: null,
    name: '',
    password: '',
    avatar: null,
    role: getRole(),
    favorIDList: [],   //收藏夹电影ID
    favorMovieList: [],   //收藏夹电影信息
    ratingIDList: [],   //个人评分电影ID
    ratingMovieList: [],   //个人评分电影信息
  }
}

const state = getDefaultState()

//作用：修改state,只能写同步方法
const mutations = {
  RESET_STATE: (state) => {
    Object.assign(state, getDefaultState())
  },
  SET_TOKEN: (state, token) => {
    state.token = token
  },
  SET_ID: (state, id) => {
    state.id = id
  },
  SET_NAME: (state, name) => {
    state.name = name
  },
  SET_PASSWORD: (state, password) => {
    state.password = password
  },
  SET_AVATAR: (state, avatar) => {
    state.avatar = avatar
  },
  SET_ROLE: (state, role) => {
    state.role = role
  },
  //设置(初始化)收藏ID列表
  SET_FAVORIDLIST: (state, favorIDList) => {
    state.favorIDList = favorIDList
  },
  //添加该id到收藏列表中
  PUSH_FAVORIDLIST: (state, movie_id) => {
    state.favorIDList.push(movie_id)
  },
  //从收藏列表中删除该id
  POP_FAVORIDLIST: (state, movie_id) => {
    state.favorIDList.splice(state.favorIDList.indexOf(movie_id), 1)
  },
  SET_RATINGIDLIST: (state, ratingIDList) => {
    state.ratingIDList = ratingIDList
  },
  //添加该id到个人评分列表中
  PUSH_RATINGIDLIST: (state, movie_id) => {
    state.ratingIDList.push(movie_id)
  },
  //从个人评分列表中删除该id
  POP_RATINGIDLIST: (state, movie_id) => {
    state.ratingIDList.splice(state.ratingIDList.indexOf(movie_id), 1)
  },
  SET_FAVORMOVIELIST: (state, favorMovieList) => {
    state.favorMovieList = favorMovieList
  },
  //添加该电影到列表中
  PUSH_FAVORMOVIELIST: (state, movie_obj) => {
    state.favorMovieList.push(movie_obj)
  },
  //从收藏列表中删除该电影
  POP_FAVORMOVIELIST: (state, movie_id) => {
    state.favorMovieList = state.favorMovieList.filter(item => item.id !== movie_id)
  },
  SET_RATINGMOVIELIST: (state, ratingMovieList) => {
    state.ratingMovieList = ratingMovieList
  },
  //添加该电影到个人评分列表中
  PUSH_RATINGMOVIELIST: (state, movie_obj) => {
    state.ratingMovieList.push(movie_obj)
  },
  //从个人评分列表中删除该电影
  POP_RATINGMOVIELIST: (state, movie_id) => {
    state.ratingMovieList = state.ratingMovieList.filter(item => item.id !== movie_id)
  }
}

//不直接去操作state，而是去操作mutation,可包含异步操作
const actions = {
  // 用户名登录
  login({ commit }, userInfo) {
    const { username, password, role } = userInfo
    return new Promise((resolve, reject) => {
      login({ username: username.trim(), password: password, role: role }).then(response => {
        const { data } = response
        // console.log('login:',data)
        if (data.res_code) {
          console.log(data.msg)
          commit('SET_TOKEN', data.token)
          setToken(data.token)
          commit('SET_ROLE', role)
          setRole(role)
          resolve()
        } else {
          reject(data.msg)
        }
      }).catch(error => {
        reject(error)
      })
    })
  },

  // 用户注册
  register({ commit }, userInfo) {
    const { username, password, avatar, role } = userInfo
    return new Promise((resolve, reject) => {
      register({ username: username, password: password, avatar: avatar, role: role }).then(response => {
        console.log(response)
        if (response.code === 201) {
          console.log('注册成功')
          resolve(response)
        } else {
          reject(response.msg)
        }
      }).catch(error => {
        reject(error)
      })
    })
  },

  // 获取用户信息
  getInfo({ commit, state }) {
    return new Promise((resolve, reject) => {
      getInfo(state.token).then(response => {
        if (response.data.res_code) {
          const { data } = response.data
          if (!data) {
            return reject('Verification failed, please Login again.')
          }
          const { id, username, password, avatar } = data
          commit('SET_ID', id)
          commit('SET_NAME', username)
          commit('SET_PASSWORD', password)
          commit('SET_AVATAR', avatar)
          resolve(data)
        } else {
          return reject(data.msg)
        }
      }).catch(error => {
        reject(error)
      })
    })
  },

  //修改用户的基本信息
  editInfo({ commit, state }, formData) {
    return new Promise((resolve, reject) => {
      editUserInfo(state.id, formData).then(response => {
        // console.log('修改成功', response.data)
        const { username, avatar } = response.data
        commit('SET_NAME', username)
        commit('SET_AVATAR', avatar)
        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  //修改用户的密码
  editPassword({ commit, state }, formData) {
    return new Promise((resolve, reject) => {
      editUserInfo(state.id, formData).then(response => {
        // console.log('修改成功', response.data)
        const { password } = response.data
        commit('SET_PASSWORD', password)
        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  // 登出
  logout({ commit, state }) {
    return new Promise((resolve, reject) => {
      logout(state.token).then(() => {
        removeToken() // must remove  token  first
        removeRole() // 清除role
        resetRouter()
        commit('RESET_STATE')
        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  // 清除token
  resetToken({ commit }) {
    return new Promise(resolve => {
      removeToken() // must remove  token  first
      removeRole()
      commit('RESET_STATE')
      resolve()
    })
  },

  //初始化显示用户收藏夹,根据收藏列表获取电影信息
  initFavor({ commit, state }) {
    return new Promise((resolve, reject) => {
      getFavorIDList(state.token).then((response) => {
        if (response.data.res_code) {
          const favorIDList = response.data.data //初始化收藏列表
          let favorMovieList = []
          //根据收藏列表获取电影信息
          for (let index = 0; index < favorIDList.length; index++) {
            getMovieDetailByID(favorIDList[index]).then(response => {
              favorMovieList.push(response.data)
            })
          }
          commit('SET_FAVORIDLIST', favorIDList)
          commit('SET_FAVORMOVIELIST', favorMovieList)
          resolve()
        } else {
          this.$message.error('初始化收藏夹出错')
          reject(response.data.msg)
        }
      }).catch(error => {
        reject(error)
      })
    })
  },

  //点击收藏或取消收藏
  handleFavor({ commit, state }, movie_id) {
    return new Promise((resolve, reject) => {
      favor(state.token, movie_id).then((response) => {
        if (response.data.res_code) {
          const isFavor = response.data.isFavor
          if (isFavor) {      //收藏
            commit('PUSH_FAVORIDLIST', movie_id)
            getMovieDetailByID(movie_id).then(response => {
              commit('PUSH_FAVORMOVIELIST', response.data)
            }).catch(error => {
              reject(error)
            })
          } else {          //取消收藏
            commit('POP_FAVORIDLIST', movie_id)
            commit('POP_FAVORMOVIELIST', movie_id)
          }
          resolve(response)
        } else {
          reject(response.data.msg)
        }
      }).catch(error => {
        reject(error)
      })
    })
  },

  //初始化显示用户个人评分,根据评分列表获取电影信息
  initRatingIDList({ commit, state }) {
    return new Promise((resolve, reject) => {
      getRatingIDList(state.token).then((response) => {
        if (response.data.res_code) {
          const ratingIDList = response.data.data //初始化收藏列表
          let ratingMovieList = []
          //根据收藏列表获取电影信息
          for (let index = 0; index < ratingIDList.length; index++) {
            getMovieDetailByID(ratingIDList[index]).then(response => {
              ratingMovieList.push(response.data)
            })
          }
          commit('SET_RATINGIDLIST', ratingIDList)
          commit('SET_RATINGMOVIELIST', ratingMovieList)
          resolve()
        } else {
          this.$message.error('初始化个人评分出错')
          reject(response.data.msg)
        }
      }).catch(error => {
        reject(error)
      })
    })
  },

  //用户评分电影
  handleRating({ commit, state }, params) {
    const { movie_id, rating } = params
    return new Promise((resolve, reject) => {
      userRating(state.token, movie_id, rating).then((response) => {
        if (response.data.res_code) {
          if (state.ratingIDList.includes(movie_id)) {
            console.log('修改评分', rating)
          } else {
            console.log('添加评分', rating)
            commit('PUSH_RATINGIDLIST', movie_id)
            getMovieDetailByID(movie_id).then(response => {
              var movie_obj = response.data
              // movie_obj['user_rate'] = rating
              Vue.set(movie_obj, 'user_rate', rating)
              commit('PUSH_RATINGMOVIELIST', movie_obj)
            })
          }
          resolve(response)
        } else {
          reject(response.data.msg)
        }
      }).catch(error => {
        reject(error)
      })
    })
  },

  //用户删除个人评分
  deleteRating({ commit, state }, movie_id) {
    return new Promise((resolve, reject) => {
      deleteUserRate(state.token, movie_id).then((response) => {
        if (response.data.res_code) {
          commit('POP_RATINGIDLIST', movie_id)
          commit('POP_RATINGMOVIELIST', movie_id)
          resolve(response)
        } else {
          reject(response.data.msg)
        }
      }).catch(error => {
        reject(error)
      })
    })
  },
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}

