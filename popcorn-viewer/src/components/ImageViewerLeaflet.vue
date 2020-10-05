<template>
  <div class="bg-gray-900 text-white p-3">Not implemented yet.</div>
</template>

<script>
export default {
  props: {
    id: String,
    canvas: Object,
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
    canvas () {
      this.initialize()
    }
  },
  methods: {
    initialize() {
      this.error = null
    }
  }
}
</script>