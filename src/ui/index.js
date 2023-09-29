import AirMap from "../SightMap"
const coms = [AirMap]

//批量组件注册
const install = function (Vue) {
    coms.forEach(com => {
        Vue.component(com.name, com)
    })
}

export default install
