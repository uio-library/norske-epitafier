<template>
  <div class="pbar"
    ref="el" 
    v-show="visible"
    :style="{width: width}"
  ></div>
</template>

<script>
export default {
  props: {
    loading: Number,
    loaded: Number,
  },

  data () {
    return {
      width: '50%',
      visible: true,
    }
  },

  watch: {
    loading (newValue) {
      if (newValue && !this.visible) {
        this.visible = true
      }
      this.update()
    },
    loaded () {
      setTimeout(() => {
        this.update()
      }, 100)
    },
  },

  methods: {
    update() {

      if (this.loading == 0) {
        console.log('Loading done')
        this.width = '0'
        this.visible = false
        return
      }

      console.log(`Loaded ${this.loaded} of ${this.loading} tiles`)

      this.width = ((this.loaded / this.loading) * 100).toFixed(1) + '%'
      if (this.loaded >= this.loading) {
        setTimeout(() => {
          if (this.loaded >= this.loading) {
            this.$emit('done')
          }
        }, 500)
      }
    },
  }
}
</script>

<style lang="sass" scoped>
.pbar
  background: rgba(0, 255, 28, 0.5)
  transition: width 300ms
</style>