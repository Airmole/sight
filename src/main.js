import { createApp } from 'vue'
import Antd from 'ant-design-vue'
import App from './App'
import 'ant-design-vue/dist/antd.css'
import * as Icons from "@ant-design/icons-vue"
import VueAMap, {initAMapApiLoader} from '@vuemap/vue-amap';
import '@vuemap/vue-amap/dist/style.css'
import '@/SightMap/index.css'

initAMapApiLoader({
    key: process.env.VUE_APP_AMAP_KEY,
    securityJsCode: process.env.VUE_APP_AMAP_SECURITY_CODE,
    plugins: ['AMap.CitySearch', 'AMap.DistrictSearch', 'AMap.MouseTool', 'AMap.MoveAnimation']
})

HTMLCanvasElement.prototype.getContext = function (origFn) {
    return function (type, attributes) {
        if (type === 'webgl') {
            attributes = Object.assign({}, attributes, {
                preserveDrawingBuffer: true,
            });
        }
        return origFn.call(this, type, attributes);
    };
}(HTMLCanvasElement.prototype.getContext);


const app = createApp(App)

app.use(Antd).use(VueAMap).mount('#app')

const icons = Icons
for (const i in icons) {
    app.component(i, icons[i])
}
