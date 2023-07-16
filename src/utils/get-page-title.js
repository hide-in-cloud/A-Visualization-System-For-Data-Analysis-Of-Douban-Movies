import defaultSettings from '@/settings'

const title = defaultSettings.title || '豆瓣电影数据可视化分析'

export default function getPageTitle(pageTitle) {
  if (pageTitle) {
    return `${pageTitle} - ${title}`
  }
  return `${title}`
}
