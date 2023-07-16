import request from '@/utils/request'

//获取全部的电影信息
export function getAllMovieDetail() {
    return request({
        url: '/movie/info/',
        method: 'get'
    })
}

//获取某个电影信息
export function getMovieDetailByID(id) {
    return request({
        url: `/movie/info/${id}/`,
        method: 'get'
    })
}

//删除某个电影
export function deleteMovieInfo(id) {
    return request({
        url: `/movie/info/${id}/`,
        method: 'delete'
    })
}

//修改某个电影
export function editMovieInfo(id, form) {
    return request({
        url: `/movie_update/${id}/`,
        method: 'patch',
        data: form
    })
}

//获取电影所有类型
export function getAllMovieTypes() {
    return request({
        url: `/movie/info/allMovieTypes/`,
        method: 'get'
    })
}

//获取电影所有年份
export function getAllMovieYears() {
    return request({
        url: `/movie/info/allMovieYears/`,
        method: 'get'
    })
}

//获取电影所有制片国家
export function getAllMovieCountries() {
    return request({
        url: `/movie/info/allMovieCountries/`,
        method: 'get'
    })
}

//获取电影所有制片国家
export function getAllMovieLang() {
    return request({
        url: `/movie/info/allMovieLang/`,
        method: 'get'
    })
}

//根据分页获取电影信息(模糊搜索)
export function getMovieDetailByPage(params) {
    return request({
        url: '/movie/page/',
        method: 'get',
        params
    })
}

//获取电影首页的各种信息
export function getHomeInfo() {
    return request({
        url: '/movie/info/homeInfo/',
        method: 'get',
    })
}

//获取电影种类分布饼状图的option
export function getTypesDistribution() {
    return request({
        url: '/movie/chart/typesDistribution/',
        method: 'get',
    })
}

//获取电影评分分布直方图的option
export function getRateDistribution() {
    return request({
        url: 'movie/chart/rateDistribution/',
        method: 'get',
    })
}

//获取电影时长分布饼状图的数据
export function getRuntimeDistribution() {
    return request({
        url: 'movie/chart/runtimeDistribution/',
        method: 'get',
    })
}

//获取电影时长分布饼状图的数据
export function getTimeLine() {
    return request({
        url: 'movie/chart/timeLine/',
        method: 'get',
    })
}

//获取每年电影前10名柱状图的数据
export function getRateSort(start_year) {
    return request({
        url: 'movie/chart/rateSort/',
        method: 'get',
        params: {start_year}
    })
}

//获取各个国家的总电影数
export function getCountrySort(start_year, end_year) {
    return request({
        url: 'movie/chart/countrySort/',
        method: 'get',
        params: {start_year, end_year}
    })
}

//获取作品评分前10名导演柱状图的数据
export function getDirectorSort() {
    return request({
        url: 'movie/chart/directorSort/',
        method: 'get'
    })
}

//获取全球烂片年变化折线图的数据
export function getBadMovie() {
    return request({
        url: 'movie/chart/badMovie/',
        method: 'get'
    })
}

//获取出场次数前10名的演员柱状图的数据
export function getActorSort() {
    return request({
        url: 'movie/chart/actorSort/',
        method: 'get'
    })
}

//根据输入的关键词搜索相关电影名称
export function getSearchTitles(keyword) {
    return request({
        url: 'movie/info/getSearchTitles/',
        method: 'get',
        params: { keyword }
    })
}

//获取用户评论词云图
export function getWordCloud(title) {
    return request({
        url: 'movie/chart/getWordCloud/',
        method: 'get',
        params: { title }
    })
}

//获取当前用户基于 电影内容 的电影推荐信息
export function getRecommendBaseContent(token) {
    return request({
        url: '/movie/info/recommendBaseContent/',
        method: 'get',
        params: { token }
    })
}

//获取当前用户基于 user-base CF 的电影推荐信息
export function getRecommendBaseUserCF(token) {
    return request({
        url: '/movie/info/recommendBaseUserCF/',
        method: 'get',
        params: { token }
    })
}

//获取当前用户基于 item-base CF 的电影推荐信息
export function getRecommendBaseItemCF(token) {
    return request({
        url: '/movie/info/recommendBaseItemCF/',
        method: 'get',
        params: { token }
    })
}
