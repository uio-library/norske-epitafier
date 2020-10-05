<template>
  <div class="flex flex-col app-container">

    <header class="bg-gray-900 px-4 py-5 text-white">
      <h1>
        <span v-if="!collection && !manifest">...</span>
        <span v-if="collection">
          <router-link :to="{path: '', query: {}}">{{ collection.name }}</router-link><span v-if="manifest">:</span>
        </span>
        {{ manifest ? manifest.label : '' }}
      </h1>
      <a href="https://tf.uio.no/forskning/forskergrupper/protestantisme/norske-epitafier-1537-1700/">Om katalogen</a>
    </header>
    <input 
      type="text" 
      v-model="queryInput" 
      placeholder="Search" 
      class="px-5 py-2 bg-gray-300 text-teal-600 focus:text-blue-600 outline-none focus:shadow-outline focus:bg-blue-100" 
      @input="search()">
<!--
    <div v-if="!loading && !manifest" class="pt-6 pb-3 bg-white border-b border-gray-400">
      <div class="max-w-6xl px-3 mx-auto">
        <form
          class="flex flex-row flex-sm-col items-baseline"
          @submit.prevent="loadManifest()"
        >
          <input
            v-model="id_input"
            type="text"
            class="text-input mr-2 flex-grow"
            placeholder="Alma Representation <s>or MMS ID</s>"
          />
          <button type="submit" class="btn">Open</button>
        </form>
        <div class="mt-2">
          <span class="mr-2">Examples:</span>
          <span v-for="samp in samples" :key="samp.id" class="mr-2">
            <a :href="'?id=' + samp.id" @click.prevent="loadManifest(id_input=samp.id)" >{{ samp.label }}</a>
          </span>
        </div>
      </div>
    </div>-->

    <div class="bg-gray-800 flex-grow flex flex-col h-full-except-print"><!-- flex-grow flex flex-col h-full overflow-auto -->

      <div v-if="loading" class="px-6 py-8 text-gray-500">Loading manifest...</div>

      <div v-if="error" class="p-3 bg-red-700 text-white">
        Could not find an Alma Digital representation with ID "{{ id }}".
      </div>

      <manifest-viewer 
        v-if="manifest" 
        :id="id"
        :manifest="manifest" 
        class="flex-grow h-full-except-print"
      ></manifest-viewer>


      <collection-viewer 
        v-if="collection && !manifest && !error && !loading"
        :collection-data="collection" 
        :query="query"
      ></collection-viewer>

      <!--

      <div v-if="manifest" class="dont-print px-3 py-2 text-sm bg-teal-500 text-white text-center">
        Note: If tiles fail to load, it's most likely because the URLs are inactive.
        This is a known bug that we have reported to Ex Libris.
        To re-active the URL, visit
        <a
          target="_blank"
          class="text-white underline"
          :href="'manifest.php?id=' + id"
        >Alma Universal Viewer</a>.
        Then wait a few seconds and reload this page.
      </div>
      -->
    </div>
  </div>
</template>

<style>
@media only screen {
  .h-full-except-print {
    height: 100%;
    overflow: auto;
  }
  .app-container {
    min-height: 100%;
  } 
}
@media only screen and (min-width: 768px) {
  .app-container {
    height: 100%;
  }
}
@media print {
  .dont-print {
    display: none;
  }
}

</style>

<script>
import axios from 'axios'
import ManifestViewer from './ManifestViewer'
import CollectionViewer from './CollectionViewer'
import { debounce } from 'lodash'
import collectionData from '../../../dist/collection.json'
import { settings} from '../settings'

export default {
  components: {
    ManifestViewer,
    CollectionViewer,
  },
  data() {
    return {
      queryInput: this.$route.query.q || '',
      query: this.$route.query.q || '',
      id: this.$route.query.id || null,
      collection: null,
      loading: false,
      // id_input: '',
      manifest: null,
      error: null,
      samples: [
        {
          id: '12247651280002204',
          label: 'bergen-05'
        },
        {
          label: 'kristiansand-22',
          id: '12248721410002204'
        },
        {
          label: 'ukjent-01',
          id: '12248721440002204'
        },
        {
          label: 'kristiania-06',
          id: '12248720930002204'
        },
        {
          label: 'kristiania-04 (virker ikke) ',
          id: '12248721420002204'
        },
        {
          label: 'trondheim-06',
          id: '12248730430002204'
        }
      ]
    }
  },
  methods: {
    search: debounce(function() {
      console.log('Search:', this.queryInput)
      this.query = this.queryInput
      this.$router.push({ path: '', query: { q: this.query } })
    }, 200),
    loadCollection() {
      // axios.get('collection.json')
      // .then(res => res.data)
      // .then(data => {
      //   console.log('GOT DATA', data)
      //   this.collection = data
      // })
      // .catch(err => {
      //   console.error('Failed to load collection!')
      // })
    },
    loadManifest() {
      this.error = null

      // if (!this.popcorn) {
      //   if (!this.id) {
      //     history.pushState(null, null, './')
      //   } else {
      //     history.pushState(null, null, '?id=' + this.id)
      //   }
      //   this.popcorn = false
      // }

      if (!this.id) {
        this.manifest = null
        return
      }

      const http = axios.create({ credentials: true })

      console.log('loadManifest:', this.id)

      this.loading = true
      this.manifest = null

      // Get IIIF Manifest
      http
        .get(
          settings.iiifServiceUrl(this.id)
        )
        .then(res => res.data)
        .then(manifest => {
          this.manifest = manifest
          this.loading = false
        })
        .catch(err => {
          console.error(err)
          this.error = err
          this.loading = false
        })
    },
  },
  mounted() {
    //const searchParams = new URLSearchParams(document.location.search)
    //this.id_input = searchParams.get('id')

    this.collection = collectionData
    // this.loadCollection()
    this.loadManifest()

    /*window.addEventListener('popstate', () => {
      this.popcorn = true
      const searchParams = new URLSearchParams(document.location.search)
      const repr = searchParams.get('id')
      if (repr) {
        this.id_input = repr
        this.loadManifest()
      }
    })*/
  },
  watch: {
    $route(val) {
      if (val.query.q != this.query) {
        this.query = val.query.q
        this.queryInput = val.query.q
      }
      if (val.query.id != this.id) {
        this.id = val.query.id
        this.loadManifest()
      }
    }
  },
}
</script>