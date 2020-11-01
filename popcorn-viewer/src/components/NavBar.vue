<template>
  <header class="bg-gray-800 text-white">

    <div class="uio-header bg-black px-4 py-1">
      <a href="https://www.uio.no/" title="Universitetet i Oslo"><img src="../yndlingsuniversitetet-ditt.svg" alt="Universitetet i Oslo"></a>
      <!-- Dette ser kanskje litt teit ut, men vi er pålagt å ha det her -->
    </div>

    <div class="px-4 pt-5 pb-3">
      <h1>
        <span v-if="!collection">...</span>
        <span v-else>
          <router-link :to="{path: '/', query: {}}">{{ collection.name }}</router-link><span v-if="manifest">:</span>
        </span>
        {{ manifest ? manifest.label : '' }}
      </h1>

      <div class="links">
        <router-link :to="{path: '/', query: {}}">Søk i katalogen</router-link>
        | 
        <router-link :to="{path: '/kart', query: {}}">Kart</router-link>
        | 
        <a href="https://tf.uio.no/forskning/forskergrupper/protestantisme/norske-epitafier-1537-1700/">Om katalogen</a>
      </div>
    </div>

  </header>
</template>
<script>
import collectionData from '../../../dist/collection.json'
import manifestService from '../manifest-service.js'
export default {
  data () {
    return {
      collection: null,
      manifest: null
    }
  },
  mounted() {
    this.collection = collectionData
    this.manifest = manifestService.getManifest()
    manifestService.onChanged(manifest => {
      this.manifest = manifest
    })
  },
}
</script>
<style scoped>
.uio-header img {
  height: 14px;
}
@media print {
  h1 * {
    color: black;
  }
  .links {
    display: none;
  }
}
.links a {
  color: rgb(153 204 210);
}
</style>