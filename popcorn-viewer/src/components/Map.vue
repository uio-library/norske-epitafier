<template>
  <div class="flex-grow flex flex-col">
    <iframe :src="mapUrl" class="h-full"></iframe>
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
  }
}
</script>
