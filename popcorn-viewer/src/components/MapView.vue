<template>
  <!-- Note: The reason we use flexbox here with w-full (width: 100%) is
       because Safari didn't grow the iframe to match the parent container
       correctly otherwise. 
       Ref: https://stackoverflow.com/a/56949292/489916 -->
  <div class="flex-grow flex w-full">
    <iframe :src="mapUrl" class="w-full"></iframe>
  </div>
</template>
<script>
import { settings} from '../settings'

export default {
  data() {
    return {
      mapUrl: settings.baseUrl + 'kart.html' 
      + (this.$route.query.id  ? `?id=${this.$route.query.id}` : ''),
    }
  },
  mounted () {
    document.body.parentNode.classList.add('h-full')
    document.body.classList.add('h-full')
  },
  beforeDestroy () {
    document.body.parentNode.classList.remove('h-full')
    document.body.classList.remove('h-full')
  }
}
</script>
