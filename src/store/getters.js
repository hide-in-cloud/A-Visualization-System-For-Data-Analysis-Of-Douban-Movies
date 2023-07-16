const getters = {
  sidebar: state => state.app.sidebar,
  device: state => state.app.device,
  token: state => state.user.token,
  avatar(state){
    if (state.user.avatar) {
      //用户有头像，给头像路径加上服务器api
      return process.env.VUE_APP_BASE_API + state.user.avatar
    } else {
      // console.log('使用默认头像')
      //默认头像
      return state.user.avatar
    }
  },
  name: state => state.user.name,
  password: state => state.user.password,
  role: state => state.user.role,
  favorIDList: state => state.user.favorIDList,
  favorMovieList: state => state.user.favorMovieList,
  ratingIDList: state => state.user.ratingIDList,
  ratingMovieList: state => state.user.ratingMovieList,
  movieInfo: state => state.movie.info,
  total: state => state.movie.total,
  types: state => state.movie.types,
  years: state => state.movie.years,
  countries: state => state.movie.countries,
  langs: state => state.movie.langs,
}
export default getters
