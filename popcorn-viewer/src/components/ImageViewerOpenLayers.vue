<template>
  <div class="flex flex-col relative h-full">
    <div class="bg-black text-white absolute top-0 bottom-0 left-0 right-0">
      <div ref="viewer" class="h-full"></div>
    </div>

    <div v-if="error" class="viewer-error">ERROR: {{ this.error }}</div>

    <ProgressBar class="iv-pbar" :loading="loading" :loaded="loaded" @done="loading=loaded=0" />
  </div>
</template>

<script>
import 'ol/ol.css'
import Map from 'ol/Map'
import View from 'ol/View'
import { defaults as defaultControls, OverviewMap } from 'ol/control'
import TileLayer from 'ol/layer/Tile'
import IIIF from 'ol/source/IIIF'
import IIIFInfo from 'ol/format/IIIFInfo'
import ProgressBar from './ProgressBar'

export default {
  components: {
    ProgressBar
  },
  props: {
    id: String,
    canvas: Object,
    basePath: {
      type: String,
      default: '/',
    },
  },
  data() {
    return {
      error: null,
      loading: 0,
      loaded: 0
    }
  },
  mounted() {
    this.initialize()
  },
  watch: {
    canvas() {
      if (this.instance) {
        console.log('DESTROY')
        this.instance.setTarget(null)
        this.instance = null
      }
      this.$nextTick(() => {
        this.initialize()
      })
    }
  },
  methods: {
    initialize() {
      this.error = null
      if (!this.canvas) {
        return
      }

      const layer = new TileLayer()
      const overviewLayer = new TileLayer()

      const overviewMapControl = new OverviewMap({
        layers: [overviewLayer]
      })

      this.instance = new Map({
        layers: [layer],
        target: this.$refs.viewer,
        controls: defaultControls().extend([overviewMapControl])
      })

      const imageServiceUrl = this.canvas.images[0].resource.service['@id']

      fetch(imageServiceUrl)
        .then(response => {
          response
            .json()
            .then(imageInfo => {
              const options = new IIIFInfo(imageInfo).getTileSourceOptions()
              if (options === undefined || options.version === undefined) {
                this.error =
                  'Data does not seem to be valid IIIF image information.'
                return
              }
              options.zDirection = -1
              const iiifTileSource = new IIIF(options)
              const iiifTileSource2 = new IIIF(options)

              iiifTileSource.on('tileloadstart', () => {
                this.error = null
                this.loading++
              })

              iiifTileSource.on('tileloadend', () => {
                this.loaded++
              })

              iiifTileSource.on('tileloaderror', () => {
                console.error('Failed to load tile')
                this.error = 'Failed to load tile'
                this.loaded++
              })

              layer.setSource(iiifTileSource)
              overviewLayer.setSource(iiifTileSource2)

              this.instance.setView(
                new View({
                  resolutions: iiifTileSource.getTileGrid().getResolutions(),
                  extent: iiifTileSource.getTileGrid().getExtent(),
                  constrainOnlyCenter: true
                })
              )
              this.instance
                .getView()
                .fit(iiifTileSource.getTileGrid().getExtent())
            })
            .catch(body => {
              this.error = 'Could not read image info json. ' + body
            })
        })
        .catch(() => {
          this.error = 'Could not read data from URL.'
        })
    }
  }
}
</script>

<style lang="sass" scoped>
.iv-pbar
  position: absolute
  top: 0
  left: 0
  height: 4px
</style>