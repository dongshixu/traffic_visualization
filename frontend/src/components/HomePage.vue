<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang='less' scoped>
  .home{
    height: 99.5%;
    display: flex;
    flex-direction: row;
  }
  #map{
      height: 100%;
      width: 85%;
      border: 1px solid red;
      background-color: whitesmoke;
      z-index: 0;
    }
  .toolbar{
    height: 100%;
    width: 15%;
    display: flex;
    flex-direction: column;
    /* justify-content: space-around; */
    margin: 0;
    padding: 0;
  }
  .toolbar-top{
    padding: 0;
    width: 95%;
    height: 30%;
    /* border: 1px solid green; */
    border-radius: 3%;
    margin: 0 0 0 2.5%;
    box-Shadow: 0 2px 3px 2px rgba(0,0,0,.1);
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    div{
      height: 23%;
      border: 1px dashed #3c3c3c;
      border-width: 0 0 1px 0;
      border-radius: 3%;
      p{
        margin: 0;
        padding: 0;
        height: 50%;
        // text-align: left;
        span{
        font-size: 15px;
        font-weight: 700;
        margin: 0 0 0 3%;
        // display: inline-block;
        }
        button{
          margin: 0;
          padding: 0;
          outline: none;
          height: 70%;
          width: 22%;
          border-radius: 15%;
          margin: 0 0 0 5%;
        }
        input{
          margin: 0 0 0 10%;
        }
      }
    }
  }
  .toolbar-middle, .toolbar-bottom{
    margin: 2.5% 0 0 2.5%;
    padding: 0;
    height: 30%;
    box-Shadow: 0 2px 3px 2px rgba(0,0,0,.1);
    border-radius: 3%;
    display: flex;
    flex-direction: column;
    span{
        font-size: 14px;
        font-weight: 700;
        margin: 0 0 0 3%;
        // display: inline-block;
    }
    /* box-Shadow: 0 2px 3px 2px rgba(0,0,0,.1); */
    /* border: 1px solid yellow; */
  }
  .toolbar-bottom{
    height: 40%;
  }
  .theam{
    position: absolute;
    font-size: 30px;
    font-weight: 700;
    font-family: 'Times New Roman', Times, serif;
    z-index: 10;
    margin: 5px 0 0 10px;
  }
  .odTag{
    position: absolute;
    font-size: 20px;
    font-weight: 600;
    font-family: 'Times New Roman', Times, serif;
    z-index: 10;
    margin: 10px 0 0 76%;
  }
</style>
<template>
  <div class="home">
    <div id="map"></div>
    <span :class="['theam']">城市网约车 OD 数据探索系统</span>
    <span :class="['odTag']">当前OD数：{{ ODNum }}</span>
    <div class="toolbar">
      <div :class="['toolbar-top']">
        <div>
          <p>
            <span :style={}># OD展示:</span>
          </p>
          <p >
            <button
            @click="original()"
            >起点
            </button>
            <button
            @click="destination()"
            >终点
            </button>
            <button
            @click="track()"
            >OD轨迹
            </button>
          </p>
        </div>
        <div>
          <p>
            <span :style={}># 聚类:</span>
          </p>
          <p>
            <input type="text" name="" id="" placeholder="0" v-model="cluter">
          </p>
        </div>
        <div>
          <p>
            <span :style={}># 采样:</span>
          </p>
          <p>
            <input type="text" name="" id="" placeholder="1" v-model="sample">
          </p>
        </div>
        <div>
          <p>
            <span :style={}># 颜色选择:</span>
          </p>
          <p>
            <input type="text" name="" id="" placeholder="schemeCategory10">
          </p>
        </div>
      </div>
      <div :class="['toolbar-middle']">
        <span>* OD 聚类分布图</span>
      </div>
      <div :class="['toolbar-bottom']">
        <span>* OD 矩阵图</span>
      </div>
      <div></div>
    </div>
  </div>
</template>

<script>
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import axios from 'axios'
import * as d3 from 'd3'

export default {
  name: 'map',
  data () {
    return {
      myMap: Object,
      color: '',
      ODNum: 0,
      testData: {'0': [1261, 480, 348, 1518, 789, 49, 20, 1557, 596, 1107], '1': [0, 0, 1, 0, 0, 0, 0, 0, 0, 0], '2': [1384, 1849, 280, 3145, 3128, 269, 73, 2900, 2220, 1891], '3': [0, 0, 0, 0, 0, 0, 0, 1, 0, 0], '4': [459, 132, 1332, 513, 274, 101, 48, 384, 215, 345], '5': [488, 2112, 165, 1489, 2021, 362, 27, 1749, 629, 561], '6': [52, 466, 42, 227, 287, 403, 5, 138, 92, 51], '7': [1305, 1157, 198, 1952, 1496, 115, 89, 2149, 759, 827], '8': [491, 450, 140, 1820, 1272, 111, 32, 1018, 1853, 851], '9': [74, 109, 35, 104, 94, 18, 47, 189, 56, 32]},
      testRawData: '',
      sample: 1,
      cluter: 0
    }
  },
  watch: {
    sample: function () {
      console.log(this.sample)
    }
  },
  mounted () {
    this.initMap()
    this.getData('2017-05-01', 10)
    this.drawODMatrix(this.testData)
    // console.log(d3)
  },
  methods: {
    initMap () {
      var newmap = L.tileLayer('http://map.geoq.cn/ArcGIS/rest/services/ChinaOnlineStreetGray/MapServer/tile/{z}/{y}/{x}')
      let initMap = L.map('map', {
        center: [20.016097083891825, 110.33584131749194],
        zoom: 13,
        layers: [newmap],
        zoomControl: false
      })
      this.myMap = initMap
      this.color = d3.schemeCategory10
      initMap.on('click', this.onMapclick)
    },
    original () {
      d3.selectAll('.circle').remove()
      d3.selectAll('.road').remove()
      console.log(typeof (this.sample))
      if (this.sample === 1 && this.cluter === 0) {
        this.ODNum = this.testRawData[0]['o'].length
        this.testRawData[0]['o'].forEach(latlng => {
          this.drawSignalCircle(latlng, 'circle', 'red', 1)
        })
      } else {
        for (let k in this.testRawData[1]) {
          this.ODNum += this.testRawData[1][k].length
        }
        // 起点聚类效果
        Object.keys(this.testRawData[1]).forEach((res, i) => {
          if (this.testRawData[1][res].length !== 0) {
            this.drawCircle(this.testRawData[1][res], this.color[i])
            // this.drawLine(this.testRawData[1][res], this.color[i], i)
          }
          // lineChartData.push([i, this.testRawData[1][res].length])
        })
        // this.drawLineChart(lineChartData)
      }
    },
    destination () {
      d3.selectAll('.circle').remove()
      d3.selectAll('.road').remove()
      if (this.sample === 1 && this.cluter === 0) {
        this.ODNum = this.testRawData[0]['d'].length
        this.testRawData[0]['d'].forEach(latlng => {
          this.drawSignalCircle(latlng, 'circle', 'black', 1)
        })
      } else {
      }
    },
    track () {
      this.ODNum = this.testRawData[0]['d'].length
      d3.selectAll('.circle').remove()
      d3.selectAll('.road').remove()
      this.testRawData[0]['d'].forEach(latlng => {
        this.drawSignalCircle(latlng, 'circle', 'black', 1)
      })
    },
    onMapclick (e) {
      console.log(e.latlng)
    },
    drawCircle (data, c) {
      data.forEach(element => {
        L.circle(element[0][0], {
          color: c,
          fillColor: c,
          fillOpacity: 1, // 透明度
          opacity: 1,
          weight: 1,
          radius: 0, // 25,
          className: 'circle'
        }).addTo(this.myMap)
      })
    },
    drawSignalCircle (data, className, cc, r) {
      L.circle(data, {
        color: cc,
        fillColor: cc,
        fillOpacity: 1, // 透明度
        opacity: 1,
        weight: r,
        radius: 0, // 25,
        className: className
      }).addTo(this.myMap)
    },
    drawLine (data, c, flag) {
      data.forEach((element, j) => {
        L.polyline(element[0], {color: c, opacity: 0.5, weight: 1, className: 'od' + flag}).addTo(this.myMap)
        this.drawSignalCircle(element[0][0], 'od_o' + flag, 'red')
        this.drawSignalCircle(element[0][1], 'od_d' + flag, 'black')
      })
    },
    drawSignalLine (data, c, flag) {
      L.polyline(data, {color: c, opacity: 0.5, weight: 1, className: 'od' + flag}).addTo(this.myMap)
      this.drawSignalCircle(data[0], 'od_o' + flag, 'red')
      this.drawSignalCircle(data[1], 'od_d' + flag, 'black')
    },
    getData (curData, num) {
      let url = 'http://localhost:8000/first/'
      let data = {
        'date': curData,
        'classfilier': num
      }
      axios.post(url, JSON.stringify(data)).then(res => {
        let rawData = res.data.data
        console.log(rawData)
        // let lineChartData = []
        // this.ODNum = rawData[0]['o'].length
        this.testRawData = rawData
      //   console.log(rawData)
      //   Object.keys(rawData[1]).forEach((res, i) => {
      //     if (rawData[1][res].length !== 0) {
      //       // this.drawCircle(rawData[1][res], this.color[i])
      //       this.drawLine(rawData[1][res], this.color[i], i)
      //     }
      //     lineChartData.push([i, rawData[1][res].length])
      //   })
      //   this.drawLineChart(lineChartData)
      })
    },
    drawODMatrix (data) {
      let len = Object.keys(data).length
      let dataTransfer = []
      Object.keys(data).forEach(key => {
        data[key].forEach(val => {
          dataTransfer.push(val)
        })
      })
      console.log(len)
      let compute = d3.interpolate('#076383', '#e9f6fa')
      let constants = {width: 280, height: 320, top: 40, left: 20, right: 20, bottom: 40}
      let maxWidth = constants.width - constants.left - constants.right
      let maxHeight = constants.height - constants.top - constants.bottom
      let matrixChart = d3.select('.toolbar-bottom').append('svg')
        .attr('width', constants.width)
        .attr('height', constants.height)
        .attr('class', 'matrixChart')
      const xScale = d3.scaleLinear()
        .domain([0, len])
        .range([0, maxWidth])
      const yScale = d3.scaleLinear()
        .domain([d3.min(dataTransfer), d3.max(dataTransfer)])
        .range([0, 1])
      let rectHeight = xScale(1) - xScale(0)
      console.log(rectHeight)
      matrixChart.append('g')
        .selectAll('colorRect')
        .data(dataTransfer)
        .enter()
        .append('rect')
        .attr('fill', (d, i) => compute(yScale(d)))
        .attr('transform', `translate(${constants.left}, ${constants.top})`)
        .attr('x', (d, i) => (i % len) * rectHeight)
        .attr('y', (d, i) => maxHeight - rectHeight - parseInt(i / len) * rectHeight)
        .attr('width', rectHeight)
        .attr('height', rectHeight)
        .attr('class', 'colorRect')
    },
    drawLineChart (data) {
      // console.log(data)
      let spiltDataX = []
      let spiltDataY = []
      data.forEach(res => {
        spiltDataX.push(res[0])
        spiltDataY.push(res[1])
      })
      let constants = {width: 280, height: 255, top: 20, left: 60, right: 20, bottom: 30}
      let maxWidth = constants.width - constants.left - constants.right
      let maxHeight = constants.height - constants.top - constants.bottom
      let lineChart = d3.select('.toolbar-middle').append('svg')
        .attr('width', constants.width)
        .attr('height', constants.height)
        .attr('class', 'lineChart')
      const xScale = d3.scaleLinear()
        .domain([d3.min(spiltDataX), d3.max(spiltDataX)])
        .range([0, maxWidth])
      const yScale = d3.scaleLinear()
        .domain([d3.min(spiltDataY), d3.max(spiltDataY) + 0.2 * d3.max(spiltDataY)])
        .range([maxHeight, 0])
      let line = d3.line()
        .x(function (d, i) { return xScale(d[0]) })
        .y(function (d, i) { return yScale(d[1]) })
      const axisLeft = d3.axisLeft(yScale).ticks(5)
      lineChart.append('g')
        .attr('transform', `translate(${constants.left}, 0)`)
        .call(axisLeft)
      const axisBottom = d3.axisBottom(xScale)
      lineChart.append('g')
        .attr('transform', `translate(${constants.left}, ${maxHeight})`)
        .call(axisBottom)
      lineChart.append('g')
        .append('path')
        .attr('transform', 'translate(' + constants.left + ', 0)')
        .attr('d', line(data))
        .attr('stroke-width', 2.5)
        .attr('stroke', '#6FC9FC')
        .attr('fill', 'none')
      lineChart.append('g')
        .selectAll('clusterNode')
        .data(data)
        .enter()
        .append('circle')
        .attr('cx', (d, i) => xScale(d[0]))
        .attr('cy', (d, i) => yScale(d[1]))
        .attr('transform', 'translate(' + constants.left + ', 0)')
        .attr('r', 4)
        .attr('fill', (d, i) => this.color[i])
        .attr('stroke', (d, i) => this.color[i])
        .attr('class', 'clusterNode')
        .on('mouseover', (d, i) => {
          for (let j = 0; j < data.length; j++) {
            if (i !== j) {
              d3.selectAll('.od' + i).attr('stroke-width', 2)
              d3.selectAll('.od' + j).attr('opacity', 0)
              d3.selectAll('.od_o' + j).attr('opacity', 0)
              d3.selectAll('.od_d' + j).attr('opacity', 0)
            }
          }
        })
        .on('mouseout', (d, i) => {
          for (let j = 0; j < data.length; j++) {
            if (i !== j) {
              d3.selectAll('.od' + i).attr('stroke-width', 1)
              d3.selectAll('.od' + j).attr('opacity', 1)
              d3.selectAll('.od_o' + j).attr('opacity', 1)
              d3.selectAll('.od_d' + j).attr('opacity', 1)
            }
          }
        })
      let textContents = ['数量', '聚类类目']
      lineChart.append('g')
        .selectAll('legend')
        .data(textContents)
        .enter()
        .append('text')
        .attr('fill', 'black')
        .attr('x', (_, i) => 10 + i * 130)
        .attr('y', (_, i) => 120 + i * 120)
        .attr('class', 'legend')
        .attr('transform', (_, i) => {
          if (i === 0) {
            return 'rotate(90 20 120)'
          }
        })
        .style('font-weight', '700')
        .style('font-size', '13px')
        .style('font-family', 'times new roman')
        .text(function (d) {
          return d
        })
    }
  }
}
</script>
