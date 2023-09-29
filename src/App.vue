<template>
  <a-config-provider :locale="zh_CN">
    <div id="app">
      <air-map :models="models"/>
    </div>
  </a-config-provider>
</template>

<script>
import zh_CN from 'ant-design-vue/lib/locale-provider/zh_CN'
import SightMap from "@/SightMap/Index"
export default {
  components: {
    AirMap: SightMap,
  },
  watch: {
    models: {
      handler(val) {
        console.log("数据更新", val)
      },
      deep: true,
    },
  },
  mounted() {
    if (this._isMobile()) alert('未做移动端适配，建议切换PC浏览器使用')
  },
  data() {
    return {
      zh_CN: zh_CN,
      models: {
        map: {
          render: true,
          center: null,
          mapStyle: 'amap://styles/normal',
          zoom: 8,
          rotation: 0,
          features: ['bg', 'point', 'road', 'building'],
          showScale: false,
          showHawkeye: false,
          viewMode: '2D',
          pitch: 60,
          showLabel: true,
          skyColor: '#5D91D7',
          hasMask: false,
          mask: []
        },
        layer: {
          traffic: {
            visible: false,
            opacity: 1,
            zIndex: 4
          },
          satellite: {
            visible: false,
            opacity: 1,
            zIndex: 4
          },
          roadnet: {
            visible: false,
            opacity: 1,
            zIndex: 4
          },
          district: {
            visible: false,
            adcode: '350200',
            opacity: 1,
            zIndex: 4,
            styles: {
              zIndex: 0,
              fill: '#46A4E7',
              'stroke-width': 1,
              'coastline-stroke':  'rgba(18,63,94,1)',
              'nation-stroke': 'rgba(35,35,35,1)',
              'province-stroke': 'rgba(50,50,50,1)',
              'city-stroke': 'rgba(70,70,70,1)',
              'county-stroke': 'rgba(85,85,85,1)',
            },
          }
        },
        markers: [],
        labelMarkers: [],
        textMarkers: [],
        elasticMarkers: [],
        infoWindows: [],
        polygons: [],
        polylines: [],
        beziers: [],
        circles: [],
        ellipses: [],
        rectangles: []
      }
    }
  },
  methods: {
    _isMobile () {
      return navigator.userAgent.match(/(phone|pad|pod|iPhone|iPod|ios|iPad|Android|Mobile|BlackBerry|IEMobile|MQQBrowser|JUC|Fennec|wOSBrowser|BrowserNG|WebOS|Symbian|Windows Phone)/i);
    }
  },
};
</script>
<style>
/*移除高德地图logo*/
.amap-logo {
  display: none;
  opacity: 0 !important;
}

.amap-copyright {
  opacity: 0;
}

.ant-layout-sider-children {
  overflow-y: scroll;
}
</style>
