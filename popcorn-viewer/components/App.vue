<template>
  <div class="flex flex-col min-h-full sm:h-full">

    <h1 class="bg-gray-900 px-4 py-3">
      <a href="../index.html" @click.prevent="loadManifest('')">Alma Digital IIIF test</a>
    </h1>

    <div class="pt-6 pb-3 bg-white border-b border-gray-400">
      <div class="max-w-6xl px-3 mx-auto">
        <form
          class="flex flex-row flex-sm-col items-baseline"
          @submit.prevent="loadManifest()"
        >
          <input
            v-model="representation_input"
            type="text"
            class="text-input mr-2 flex-grow"
            placeholder="Alma Representation ID"
          />
          <button type="submit" class="btn">Open</button>
        </form>
        <div class="mt-2">
          <span class="mr-2">Examples:</span>
          <span v-for="samp in samples" :key="samp.id" class="mr-2">
            <a :href="'?representation=' + samp.id" @click.prevent="loadManifest(representation_input=samp.id)" >{{ samp.label }}</a>
          </span>
        </div>
      </div>
    </div>

    <div class="bg-gray-200 flex-grow flex flex-col h-full overflow-auto">

      <div v-if="loading" class="px-6 py-8 text-gray-500">Loading manifest...</div>

      <div v-if="error" class="p-3 bg-red-700 text-white">
        Could not find an Alma Digital representation with ID "{{ representation }}".
      </div>

      <manifest-viewer v-if="manifest" :manifest="manifest" class="flex-grow h-full overflow-auto"></manifest-viewer>

      <div v-if="manifest" class="px-3 py-2 text-sm bg-teal-500 text-white text-center">
        Note: If tiles fail to load, it's most likely because the URLs are inactive.
        This is a known bug that we have reported to Ex Libris.
        To re-active the URL, visit
        <a
          target="_blank"
          class="text-white underline"
          :href="'https://bibsys-k.alma.exlibrisgroup.com/view/UniversalViewer/47BIBSYS_UBO/' + representation"
        >Alma Universal Viewer</a>.
        Then wait a few seconds and reload this page.
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import ManifestViewer from './ManifestViewer'

export default {
  components: {
    ManifestViewer
  },
  data() {
    return {
      loading: false,
      representation: null,
      representation_input: '',
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
    loadManifest(input) {
      if (input !== undefined) {
        this.representation_input = input
      }

      this.representation = this.representation_input
      this.error = null

      if (!this.popcorn) {
        if (!this.representation) {
          history.pushState(null, null, './')
        } else {
          history.pushState(null, null, '?representation=' + this.representation)
        }
        this.popcorn = false
      }

      if (!this.representation_input) {
        this.manifest = null
        return
      }

      console.log('Load manifest for represenation: ' + this.representation)
      const http = axios.create({ credentials: true })

      this.loading = true
      this.manifest = null

      

      // Get IIIF Manifest
      http
        .get(
          `https://bibsys-k.userservices.exlibrisgroup.com/view/iiif/presentation/${this.representation}/manifest`
        )
        .then(res => res.data)
        .then(manifest => {
          console.log(manifest)
          this.manifest = manifest
          this.loading = false
        })
        .catch(err => {
          this.error = err
          this.loading = false
        })
    }
  },
  mounted() {
    const searchParams = new URLSearchParams(document.location.search)
    this.representation_input = searchParams.get('representation')

    this.loadManifest()

    window.addEventListener('popstate', () => {
      this.popcorn = true
      const searchParams = new URLSearchParams(document.location.search)
      const repr = searchParams.get('representation')
      if (repr) {
        this.representation_input = repr
        this.loadManifest()
      }
    })
  }
}
</script>