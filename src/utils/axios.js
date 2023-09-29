import axios from 'axios'
import { storage } from '@/utils/storage'
import { API_KEY } from '@/SightMap/store/mutation-types'

// 创建 axios 实例
const service = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL, // api base_url
  timeout: 30000 // 请求超时时间
})

const err = (error) => {
  if (error.response) {
    const data = error.response.data
    if (error.response.status === 403) {
      console.log(data)
    }
    if (error.response.status === 401) {
        console.log(data)
    }
  }
  return Promise.reject(error)
}

/**
 * @description 请求发起前的拦截器
 * @returns {AxiosRequestConfig} config
 */
service.interceptors.request.use(async (config) => {
  const apikey = storage.get(API_KEY)
  if (apikey) {
    config.headers.apikey = apikey // 让每个请求携带自定义 token 请根据实际情况自行修改
  }
  return config
})

/**
 * @description 响应收到后的拦截器
 *00urns {}
 */
service.interceptors.response.use(async (response) => {
  return Promise.resolve(response)
},
err
)

export default service
