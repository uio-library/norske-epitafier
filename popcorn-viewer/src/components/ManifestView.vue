<template>
  <!-- 
    Beware: https://stackoverflow.com/a/35609992/489916 
  -->
  <div class="bg-gray-900 flex-grow flex overflow-hidden-except-print">
    <div v-if="!manifest" class="bg-gray-900 flex-grow px-3 text-center text-gray-600">
      Loading...
    </div>
    <div v-if="manifest" class="flex-grow  grid overflow-hidden-except-print" :class="{
      'dragging': dragging, 
      'grid1': canvases.length <= 1, 
      'grid2': 1 < canvases.length && canvases.length <= 4, 
      'grid3': 4 < canvases.length,
    }">

      <!-- left column -->
      <div 
        v-if="canvases.length > 1"
        class="column-1 dont-print h-full-except-mobile overflow-auto bg-gray-900"
      >
        <simplebar class="h-full" data-simplebar-auto-hide="false">
          <button
            v-for="canvas in canvases"
            :key="canvas['@id']"
            :title="canvas.label"
            style="width: 6rem"
            class="mx-2 my-2 px-2 py-1 transition duration-500 rounded ease-out"
            :class="{'bg-gray-600 text-white': activeCanvas === canvas, 'text-gray-300': activeCanvas !== canvas}"
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
        </simplebar>
      </div>

      <!-- center column -->
      <div class="column-2 flex flex-col">
        <component 
          v-if="manifest"
          v-bind:is="activeViewer" 
          :manifest-url="activeCanvasUrl" 
          :id="manifest.id"
          :base-url="baseUrl"
          class="flex-grow" 
          style="min-height: 400px"
        ></component>
        <!--<app-tabs
          :items="viewers"
          :selected="activeViewer"
          position="bottom"
          @change="activeViewer=$event"
        ></app-tabs>-->
        <div class="text-white px-3 py-1 text-sm flex justify-center">
          <div v-if="activeCanvas">
            Foto: {{ getCredits(activeCanvas.label) }}
            | 
            <span v-for="render in activeCanvas.rendering" :key="render['@id']">
              <a :href="render['@id']">{{ render.label }}</a>
            </span>
          </div>
        </div>
      </div>

      <div class="gutter-column-3 vertical-gutter"></div>

      <!-- right column -->
      <div class="column-3 mv-overflow-auto" ref="mv-right-column">
        <div class="px-4 py-2">
          Om objektet:
          <metadata-element
            v-for="(value, key) in metadata" :key="key"
            :label="value.label" 
            :value="value.value"
          />
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import ImageViewerOpenSeadragon from './ImageViewerOpenSeadragon'
//import ImageViewerOpenLayers from './ImageViewerOpenLayers'
//import ImageViewerLeaflet from './ImageViewerLeaflet'
import MetadataElement from './MetadataElement'
import AppTabs from './AppTabs'
import Split from 'split-grid'
import simplebar from 'simplebar-vue'
import { settings } from '../settings'
import manifestService from '../manifest-service'
import 'simplebar/dist/simplebar.min.css' 

export default {
  components: {
    ImageViewerOpenSeadragon,
    //ImageViewerOpenLayers,
    //ImageViewerLeaflet,
    AppTabs,
    MetadataElement,
    simplebar,
  },
  data() {
    return {
      dragging: false,
      manifest: null,
      error: null,
      loading: true,
      canvases: [],
      activeCanvas: null,
      viewers: [
        {
          value: 'ImageViewerOpenSeadragon',
          label: 'OpenSeadragon'
        },
        // {
        //   value: 'ImageViewerOpenLayers',
        //   label: 'OpenLayers'
        // },
        // {
        //   value: 'ImageViewerLeaflet',
        //   label: 'Leaflet'
        // }
      ],
      activeViewer: 'ImageViewerOpenSeadragon'
    }
  },
  computed: {
    baseUrl() {
      return settings.baseUrl
    },
    activeCanvasUrl() {
      if (!this.activeCanvas) return null

      // If Alma Digital actually worked as it SHOULD, we could use this:
      // return this.activeCanvas.images[0].resource.service['@id']

      // But because of the 403 problem, we will use this instead:
      return `https://ub-media.uio.no/norske-epitafier-1537-1700/${this.activeCanvas.label}/info.json`
    },
    metadata() {
      if (!this.manifest) return {}
      return this.manifest.metadata.filter(value => value.label != 'Tittel')
    },
    photoCredits() {
      if (!this.manifest) return {}
      const values = this.manifest.metadata.filter(value => value.label == 'Kreditering')
      let out = {}
      if (values.length) {
        for (const match of values[0].value.matchAll('([-a-z0-9]+)\\.[a-zA-Z]{3}: (.+?) \\((.*?)\\)')) {
          out[match[1]] = {name: match[2], license: match[3]}
        }
      }
      return out
    },
  },
  mounted() {
    document.body.parentNode.classList.add('h-full-except-mobile')
    document.body.classList.add('h-full-except-mobile')

    this.error = null
    this.loading = true
    manifestService.loadManifest(this.$route.params.id)
      .catch(err => {
        console.error(err)
        this.error = err
        this.loading = false
      })   
      .then(manifest => {
        this.manifest = manifest
        this.initialize()
        console.info('GOT MANI', manifest)
        setTimeout(() => {
          this.split = Split({
            columnGutters: [{
              track: this.canvases.length == 1 ? 1 : 2,
              element: document.querySelector('.gutter-column-3'),
            }],
            snapOffset: 100,
            minSize: 0,
            onDragStart: () => this.dragging = true,
            onDragEnd: () => this.dragging = false,
          })
        }, 300)
      })
  },
  beforeDestroy() {
    document.body.parentNode.classList.remove('h-full')
    document.body.classList.remove('h-full')
    if (this.split) this.split.destroy()

    manifestService.loadManifest(null)

  },
  // watch: {
  //   id() {
  //     this.loadManifest().then(() => {
  //       this.initialize()
  //     })
  //   }
  // },
  methods: {
    getCredits(filename) {
      if (!this.photoCredits[filename]) {
        return '(???)'
      }
      return `${this.photoCredits[filename].name} (${this.photoCredits[filename].license})`
    },
    initialize() {
      this.canvases = this.manifest.sequences[0].canvases
      this.activeCanvas = this.canvases[0]

      console.log('activeCanvas', this.activeCanvas)
    },
  }
}
</script>

<style scoped>

@media not print {
  .overflow-hidden-except-print {
    overflow: hidden;
  }
}
.grid1 {
  display: grid;
  grid-template-columns: 2fr 10px 1fr;
}
.grid2 {
  display: grid;
  grid-template-columns: 120px 2fr 10px 1fr;
}
.grid3 {
  display: grid;
  grid-template-columns: 240px 2fr 10px 1fr;
}

.vertical-gutter {
  display: block;
  cursor: col-resize;
  background: #111;
  border: 1px solid #222;
}

@media (max-width: 768px) {
  .grid {
    display: block;
  }
  .vertical-gutter {
    display: none;
  }
}
.dragging .vertical-gutter {
  background: #bbb;
}
.vertical-gutter:hover {
  background: #333;
}
.column-1 {

}
.column-3 {
  background: #222;
  color: white;
  font-size: 85%;
}
.right-separator {
  width: 10px;
  background: #ccc;
}
.mv-overflow-auto {
  overflow: auto;
  min-height: 400px;
}
@media print, (max-width: 768px) {
  .mv-overflow-auto {
    overflow: none;
  }
}

@media print {
  .dont-print {
    display: none;
  }
}

.mv-thumb-label {
  text-overflow: ellipsis;
}
</style>