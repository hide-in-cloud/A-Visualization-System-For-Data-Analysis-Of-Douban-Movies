import Vue from 'vue'
import { Message } from 'element-ui';
import { getRole } from '@/utils/auth'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'
import store from '@/store'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },

  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/register/index'),
    hidden: true
  },

  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },

  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: 'dashboard',
      name: 'Dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: { title: '首页', icon: 'dashboard' }
    }]
  },

  {
    path: '/search',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'Search',
        component: () => import('@/views/search/index'),
        meta: { title: '搜索电影', icon: 'list' }
      }
    ]
  },

  {
    path: '/movie_detail',
    component: Layout,
    hidden: true,
    children: [
      {
        path: 'index/:movie_id',
        name: 'Detail',
        component: () => import('@/views/movie_detail/index'),
        meta: { title: '电影详情'}
      }
    ]
  },

  {
    path: '/analyse',
    component: Layout,
    redirect: '/analyse/time',
    name: 'Analyse',
    meta: { title: '数据分析', icon: 'el-icon-s-help' },
    children: [
      {
        path: 'time',
        name: 'Time',
        component: () => import('@/views/analyse/Time'),
        meta: { title: '基于时间分析', icon: 'form' }
      },
      {
        path: 'rate',
        name: 'Rate',
        component: () => import('@/views/analyse/Rate'),
        meta: { title: '基于评分分析', icon: 'form' }
      },
      {
        path: 'country',
        name: 'Country',
        component: () => import('@/views/analyse/Country'),
        meta: { title: '基于国家分析', icon: 'form' }
      },
      {
        path: 'director',
        name: 'Director',
        component: () => import('@/views/analyse/Director'),
        meta: { title: '基于导演分析', icon: 'form' }
      },
      {
        path: 'actor',
        name: 'Actor',
        component: () => import('@/views/analyse/Actor'),
        meta: { title: '基于演员分析', icon: 'form' }
      },
      {
        path: 'wordCloud',
        name: 'WordCloud',
        component: () => import('@/views/analyse/WordCloud'),
        meta: { title: '词云分析图', icon: 'form' }
      },
    ]
  },

  {
    path: '/recommend',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'Recommend',
        component: () => import('@/views/recommend/index'),
        meta: { title: '电影推荐', icon: 'el-icon-s-help' }
      }
    ]
  },
  
  {
    path: '/movieManage',
    component: Layout,
    // redirect: '/movieManage/index',
    children: [
      {
        path: 'index',
        name: 'MovieManage',
        component: () => import('@/views/movieManage/index'),
        meta: { role:['admin'], title: '电影数据管理', icon: 'table' }
      },
      {
        path: 'form',
        name: 'MovieForm',
        hidden: true,
        component: () => import('@/views/movieManage/form'),
        meta: { role:['admin'], title: '添加电影', icon: 'table' }
      },
      {
        path: 'edit/:id',
        name: 'MovieEdit',
        hidden: true,
        component: () => import('@/views/movieManage/edit'),
        meta: { role:['admin'], title: '编辑电影', icon: 'form' }
      },
    ]
  },

  {
    path: '/userManage',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'UserManage',
        component: () => import('@/views/userManage/index'),
        meta: { role:['admin'], title: '用户管理', icon: 'table' }
      },
      {
        path: 'form',
        name: 'UserForm',
        hidden: true,
        component: () => import('@/views/userManage/form'),
        meta: { role:['admin'], title: '添加用户', icon: 'form' }
      },
      {
        path: 'edit/:id',
        name: 'UserEdit',
        hidden: true,
        component: () => import('@/views/userManage/edit'),
        meta: { role:['admin'], title: '编辑用户', icon: 'form' }
      },
    ]
  },

  // {
  //   path: 'external-link',
  //   component: Layout,
  //   children: [
  //     {
  //       path: 'https://panjiachen.github.io/vue-element-admin-site/#/',
  //       meta: { title: 'External Link', icon: 'link' }
  //     }
  //   ]
  // },

  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

//路由守卫
router.beforeEach((to, from, next) => {
  if (to.meta.role) {
    //获取当前cookie中保存的角色
    let userRole = getRole()
    console.log('当前角色:',userRole)
    let allowRoleList = to.meta.role
    if (allowRoleList.indexOf(userRole) !== -1) {
      //有权限
      next();
    }else{
      //无权限
      Message.error('您没有权限')
    }
  } else {
    next()
  }
})

export default router
