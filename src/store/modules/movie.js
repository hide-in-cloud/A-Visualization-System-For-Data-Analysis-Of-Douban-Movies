import { getAllMovieDetail, getAllMovieTypes, getAllMovieYears, getAllMovieCountries, getAllMovieLang } from '@/api/movie'

const state = {
    info: [],       //所有电影信息
    total: 0,       //电影总数量
    types: [],      //电影所有类型
    years: [],      //电影所有年份
    countries: [],      //电影所有年份
    langs: [],       //电影所有语言
}

const mutations = {
    SET_INFO: (state, info) => {
        state.info = info
    },
    SET_TOTAL: (state, total) => {
        state.total = total
    },
    SET_TYPES: (state, types) => {
        state.types = types
    },
    SET_YEARS: (state, years) => {
        state.years = years
    },
    SET_COUNTRIES: (state, countries) => {
        state.countries = countries
    },
    SET_LANGS: (state, langs) => {
        state.langs = langs
    },
}

const actions = {
    // 获取全部的电影信息
    GetAllMovieInfo({ commit }) {
        return new Promise((resolve, reject) => {
            getAllMovieDetail().then(response => {
                const { data } = response
                // console.log('getAllMovieDetail', data)
                commit('SET_INFO', data)
                commit('SET_TOTAL', data.length)
                resolve(response)
            }).catch(error => {
                reject(error)
            })
        })
    },

    // 获取全部的电影类型
    GetAllMovieTypes({ commit }) {
        return new Promise((resolve, reject) => {
            getAllMovieTypes().then(response => {
                const { data } = response
                commit('SET_TYPES', data.types)
                resolve(response)
            }).catch(error => {
                reject(error)
            })
        })
    },

    // 获取全部的电影年份
    GetAllMovieYears({ commit }) {
        return new Promise((resolve, reject) => {
            getAllMovieYears().then(response => {
                const { data } = response
                commit('SET_YEARS', data.years)
                resolve(response)
            }).catch(error => {
                reject(error)
            })
        })
    },

    // 获取全部的电影类型
    GetAllMovieCountries({ commit }) {
        return new Promise((resolve, reject) => {
            getAllMovieCountries().then(response => {
                const { data } = response
                commit('SET_COUNTRIES', data.countries)
                resolve(response)
            }).catch(error => {
                reject(error)
            })
        })
    },

    // 获取全部的语言
    GetAllMovieLang({ commit }) {
        return new Promise((resolve, reject) => {
            getAllMovieLang().then(response => {
                const { data } = response
                commit('SET_LANGS', data.langs)
                resolve(response)
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
