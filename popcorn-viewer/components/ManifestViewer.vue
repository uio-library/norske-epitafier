<template>
  <div class="flex flex-col">
    <h2 class="px-4 pt-6 pb-4">{{ manifest.label }}</h2>

    <div class="flex-grow flex flex-col-reverse sm:flex-row overflow-auto">
      <div
        class="ml-3 mr-3 flex flex-row flex-initial flex-wrap content-start overflow-auto  sm:mv-single-column"
        :class="{'lg:mv-double-column': canvases.length > 3}"
      >
        <button
          v-for="canvas in canvases"
          :key="canvas['@id']"
          :title="canvas.label"
          style="width: 6rem"
          class="m-1 px-2 py-1 transition duration-500 rounded ease-out"
          :class="{'bg-gray-600 text-white': activeCanvas === canvas, 'text-gray-900': activeCanvas !== canvas}"
          @click="activeCanvas = canvas"
        >
          <img
            :src="canvas.thumbnail['@id']"
            :alt="canvas.label"
            class="object-contain w-full"
            style="height: 6rem"
          />
          <div class="text-xs text-center pt-1 overflow-hidden mv-thumb-label">{{ canvas.label }}</div>
        </button>
      </div>

      <div class="flex-grow flex flex-col overflow-auto" style="min-height: 500px;">
        <div class="flex-grow">
          <component v-bind:is="activeViewer" :canvas="activeCanvas"></component>
        </div>
        <app-tabs
          :items="viewers"
          :selected="activeViewer"
          position="bottom"
          @change="activeViewer=$event"
        ></app-tabs>
      </div>
    </div>
  </div>
</template>

<script>
import ImageViewerOpenSeadragon from './ImageViewerOpenSeadragon'
import ImageViewerOpenLayers from './ImageViewerOpenLayers'
import ImageViewerLeaflet from './ImageViewerLeaflet'
import AppTabs from './AppTabs'

export default {
  components: {
    ImageViewerOpenSeadragon,
    ImageViewerOpenLayers,
    ImageViewerLeaflet,
    AppTabs
  },
  props: {
    manifest: Object
  },
  data() {
    return {
      canvases: [],
      activeCanvas: null,
      viewers: [
        {
          value: 'ImageViewerOpenSeadragon',
          label: 'OpenSeadragon'
        },
        {
          value: 'ImageViewerOpenLayers',
          label: 'OpenLayers'
        },
        {
          value: 'ImageViewerLeaflet',
          label: 'Leaflet'
        }
      ],
      activeViewer: 'ImageViewerOpenSeadragon'
    }
  },
  mounted() {
    this.initialize()
  },
  watch: {
    manifest() {
      this.initialize()
    }
  },
  methods: {
    initialize() {
      this.canvases = this.manifest.sequences[0].canvases
      this.activeCanvas = this.canvases[0]
    }
  }
}
</script>

<style scoped>
@responsive {
  .mv-single-column {
    width: 7.4rem;
  }
  .mv-double-column {
    width: 14rem;
  }
}

.mv-thumb-label {
  text-overflow: ellipsis;
}
</style>