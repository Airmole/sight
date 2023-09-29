<template>
  <a-layout :style="{height: `${screenHeight}px`, overflow: 'hidden' }">
    <a-card
        ref="toolbox"
        class="toolcard"
        :tab-list="tabList"
        :active-tab-key="activeKey"
        @tabChange="key => { activeKey = key }"
        v-drag
    >
      <!--工具栏标题-->
      <template #title>
        <a-tooltip color="grey">
          <template #title>
            <a-typography-text class="ant-typography" keyboard>Ctrl</a-typography-text> + <a-typography-text class="ant-typography" keyboard>A</a-typography-text> 隐藏工具栏
            <br/><a-typography-text class="ant-typography" keyboard>Ctrl</a-typography-text> + <a-typography-text class="ant-typography" keyboard>D</a-typography-text> 复位工具栏
            <br/><a-typography-text class="ant-typography" keyboard>Ctrl</a-typography-text> + <a-typography-text class="ant-typography" keyboard>R</a-typography-text> 重载渲染地图
          </template>
          SightMap
        </a-tooltip>
      </template>
      <!--工具栏右侧-->
      <template #extra>
        <a-tooltip v-if="foldToolbox">
          <template #title>
            <a-typography-text class="ant-typography" keyboard>Ctrl</a-typography-text> + <a-typography-text class="ant-typography" keyboard>F</a-typography-text> 折叠工具栏
          </template>
          <a-button type="link" @click="foldToolbox = false">
            <template #icon><down-outlined/></template>
          </a-button>
        </a-tooltip>
        <a-tooltip v-else>
          <template #title>
            <a-typography-text class="ant-typography" keyboard>Ctrl</a-typography-text> + <a-typography-text class="ant-typography" keyboard>F</a-typography-text> 折叠工具栏
          </template>
          <a-button type="link" @click="foldToolbox = true">
            <template #icon><up-outlined/></template>
          </a-button>
        </a-tooltip>
      </template>
      <!--工具栏选项卡-->
      <template #customTab="item" v-if="!foldToolbox">
        <span> {{ item.tab }} </span>
      </template>
      <!--工具栏内容-->
      <div class="toolbox-content" @mousedown.stop :style="{ height: `${screenHeight-190}px`}" v-if="!foldToolbox">
        <template v-if="activeKey === '1'">
          <p v-for="(item, index) in sight5A" :key="index">{{ item.name }}</p>
        </template>
      </div>
    </a-card>
    <a-layout-content>
      <!--地图实例-->
      <el-amap
          class="amap"
          v-if="models.map.render"
          style="z-index: -10"
          :center="models.map.center"
          :zoom="models.map.zoom"
          :rotation="models.map.rotation"
          :features="models.map.features"
          :mapStyle="models.map.mapStyle"
          :pitch="models.map.pitch"
          :viewMode="models.map.viewMode"
          :skyColor="models.map.skyColor"
          :showLabel="models.map.showLabel"
          :webGLParams="{ preserveDrawingBuffer: true }"
          :mask="models.map.hasMask ? models.map.mask : null"
          @init="init"
          @click="click"
          @dragend="dragend"
          @zoomend="zoomend"
      >
        <el-amap-layer-labels>
          <el-amap-label-marker
              v-for="(item, index) in makers5A"
              :key="index"
              :visible="item.visible"
              :position="item.position"
              :text="item.text"
              :icon="item.icon"
              @click="makers5AClicked"
          />
        </el-amap-layer-labels>
      </el-amap>
    </a-layout-content>
  </a-layout>
</template>

<script>
import {
  UpOutlined,
  DownOutlined,
} from '@ant-design/icons-vue'
const sight5A = require('../../data/5A.json')

export default {
  name: 'AirMap',
  components: {
    UpOutlined,
    DownOutlined,
  },
  props: {
    models: {
      type: [Object],
      required: true
    }
  },
  directives:{
    drag(el) {
      let oDiv = el // 当前元素
      // 禁止选择网页上的文字
      document.onselectstart = function () { return false }
      oDiv.onmousedown = function (e) {
        // 鼠标按下，计算当前元素距离可视区的距离
        let disX = e.clientX - oDiv.offsetLeft
        let disY = e.clientY - oDiv.offsetTop
        document.onmousemove = function (e) {
          // 通过事件委托，计算移动的距离
          let l = e.clientX - disX
          let t = e.clientY - disY
          oDiv.style.left = l + 'px'
          oDiv.style.top = t + 'px'
        }
        document.onmouseup = function () {
          document.onmousemove = null
          document.onmouseup = null
        }
        return false
      }
    }
  },
  data () {
    return {
      map: null,
      screenHeight: document.body.clientHeight,
      activeKey: '1',
      foldToolbox:false,
      sight5A: sight5A,
      makers5A: [],
      tabList: [
        { key: '1', tab: '5A景区' },
      ]
    }
  },
  mounted () {
    // 按键事件
    document.addEventListener('keydown', (e) => {
      this.keyboardControl(e)
    })
    window.addEventListener('resize', () => {
      this.screenHeight = document.body.clientHeight
    })
    this.makers5A = this.transformMakers5A()
  },
  methods: {
    init (map) {
      this.map = map
      var _this = this
      // IP定位到用户所在城市
      map.plugin('AMap.CitySearch', function () {
        var citySearch = new AMap.CitySearch()
        citySearch.getLocalCity(function (status, result) {
          if (status === 'complete' && result.info === 'OK') {
            _this.map.setBounds(result.bounds)
            _this.models.map.center = [
              _this.map.getCenter().lng,
              _this.map.getCenter().lat
            ]
          }
        })
      })
    },
    transformMakers5A () {
      const markers = []
      this.sight5A.forEach((sight) => {
        markers.push({
          visible: true,
          position: [sight.location.split(',')[0], sight.location.split(',')[1]],
          text: {
            content: sight.name,
            direction: 'right',
            style: {
              fontSize: 15,
              padding: [3, 5],
            }
          },
          icon: {
            image: 'https://a.amap.com/jsapi_demos/static/images/poi-marker.png',
            anchor: 'bottom-center',
            size: [25, 34],
            clipOrigin: [282, 7],
            clipSize: [50, 68]
          }
        })
      })
      return markers
    },
    click (e) {
      console.log(e)
    },
    dragend (e) {
      this.models.map.center = [ e.target.getCenter().lng, e.target.getCenter().lat ]
    },
    zoomend (e) {
      const zoom = e.target.getZoom()
      this.models.map.zoom = zoom
    },
    clickMarker (marker) {
      console.log(`点击了标号,标号ID： ${marker.id}`)
    },
    markerDragend (marker, e, index) {
      this.models.markers[index].position = [e.lnglat.lng, e.lnglat.lat]
    },
    textMarkerDragend (marker, e, index) {
      this.models.textMarkers[index].position = [e.lnglat.lng, e.lnglat.lat]
    },
    keyboardControl(e) {
      // [Ctrl] + [A] 隐藏控制板
      if (e.ctrlKey && e.keyCode === 65) {
        this.displayToolbox()
      }
      // [Ctrl] + [D] 初始化控制板(不修改参数值)
      if (e.ctrlKey && e.keyCode === 68) {
        this.displayToolbox(true)
      }
      // [Ctrl] + [F] 折叠展开控制板
      if (e.ctrlKey && e.keyCode === 70) {
        this.foldToolbox = !this.foldToolbox
      }
      // [Ctrl] + [R] 重新渲染加载地图实例
      if (e.ctrlKey && e.keyCode === 82) {
        this.models.map.render = false
        setTimeout(() => { this.models.map.render = true }, 1000) // 1秒后重新渲染地图实例
      }
      if (e.ctrlKey) e.preventDefault() // 阻止浏览器默认事件
    },
    displayToolbox (force = false) {
      this.showToolbox = !this.showToolbox
      this.$refs.toolbox.$el.style.display = this.showToolbox ? 'unset' : 'none'
      if (force === true) {
        this.$refs.toolbox.$el.style.top = '20px'
        this.$refs.toolbox.$el.style.left = `${document.body.clientWidth - 440}px`
        this.$refs.toolbox.$el.style.display = 'unset'
      }
    }
  }
}
</script>

<style lang="css" scoped>
.margin {
  margin: 15px;
}
.right {
  overflow-y: scroll;
}
.toolcard {
  width: 420px;
  top: 20px;
  right: 20px;
  z-index: 99;
  position: absolute;
  background-color: rgba(255, 255, 255, 0.80);
  border-radius: 10px;
}
.toolbox-content {
  overflow-x: hidden;
  overflow-y: scroll;
}
.ant-typography {
  background-color: #ffffff;
}

</style>
