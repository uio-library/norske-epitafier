<template>
  <div class="flex flex-col relative h-full">
    <div class="bg-black text-white absolute top-0 bottom-0 left-0 right-0">
      <div ref="viewer" class="h-full"></div>
    </div>

    <div v-if="error" class="viewer-error">
      ERROR: {{ this.error }}.
      <a :href="'https://bibsys-k.alma.exlibrisgroup.com/view/UniversalViewer/47BIBSYS_UBO/' + id">Click here</a> to try an alternative viewer.
    </div>
  </div>
</template>

<script>
import OpenSeadragon from 'openseadragon'

export default {
  props: {
    id: String,
    manifestUrl: String,
    baseUrl: {
      type: String,
      default: '/',
    },
  },
  data() {
    return {
      error: null
    }
  },
  mounted() {
    this.initialize()
  },
  watch: {
    manifestUrl() {
      if (this.instance) {
        console.log('DESTROY')
        this.instance.destroy()
      }
      this.$nextTick(() => {
        this.initialize()
      })
    }
  },
  methods: {
    initialize() {
      this.error = null
      if (!this.manifestUrl) {
        return
      }

      console.log('MANIFEST:', this.manifestUrl)

      // Ref: https://openseadragon.github.io/docs/OpenSeadragon.html
      this.instance = OpenSeadragon({
        element: this.$refs.viewer,
        prefixUrl: this.baseUrl +'openseadragon-flat-toolbar-icons/images/',
        tileSources: [this.manifestUrl],
        sequenceMode: false,

        // 'https://bibsys.alma.exlibrisgroup.com/view/iiif/presentation/47BIBSYS_UBO/12223144170002204/manifest',
        // debugMode: true,

        showNavigationControl: true,

        showNavigator: true,

        navigatorPosition: 'BOTTOM_RIGHT',

        // We don't want to allow zooming outside of what's filling the window
        minZoomImageRatio: 1.0,

        // The percentage (as a number from 0 to 1) of the source image which must
        // be kept within the viewport. If the image is dragged beyond that limit,
        // it will 'bounce' back until the minimum visibility ratio is achieved.
        visibilityRatio: 1.0
      })

      this.instance.addHandler('tile-load-failed', event => {
        console.log('Tile failed to load', event)
        this.error = 'Failed to load image tile'
      })

      this.instance.addHandler('open-failed', () => {
        this.error = 'Failed to load image'
      })

      this.instance.addHandler('tile-loaded', () => {
        this.error = null
      })
    }
  }
}
</script>
