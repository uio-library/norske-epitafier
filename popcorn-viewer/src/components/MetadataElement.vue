<template>
  <div class="my-3">
    <div class="metadataHeader">{{ label }}:</div>
    <div 
      class="metadataValue"
    >
      <div :class="{'fade': canReadMore && !isReadingMore}">
      <div v-html="value" ref="collapsable" class="collapsable"></div>
      </div>
      <a href="#" @click.prevent="expand" v-if="canReadMore && !isReadingMore" class="readMore">[Vis mer]</a>
      <a href="#" @click.prevent="collapse" v-if="canReadMore && isReadingMore" class="readMore">[Vis mindre]</a>
    </div>
    
  </div>
</template>

<script>
export default {
  props: {
    label: String,
    value: String,
  },
  data () {
    return {
      canReadMore: false,
      isReadingMore: false,
    }
  },
  mounted () {
    const el = this.$refs.collapsable
    if (el.scrollHeight > el.clientHeight) {
      this.canReadMore = true
    }
  },
  methods: {
    expand () {
      const el = this.$refs.collapsable
      this.isReadingMore = true
      el.style['max-height'] = el.scrollHeight + 'px'
    },
    collapse () {
      const el = this.$refs.collapsable
      this.isReadingMore = false
      el.style['max-height'] = '100px'
    },
  }
}
</script>

<style>

.fade {
    position: relative;
}
.readMore {
  font-size: 90%;
}
.fade:after {
  content: "";
  position: absolute;
  z-index: 1;
  bottom: 0;
  left: 0;
  pointer-events: none;
/*  background-image: linear-gradient(to bottom, rgba(50,50,50,0), rgb(50, 50,50,1) 90%);*/
  width: 100%;
  height: 1.2em;
}
.collapsable {
  display: block;
  overflow: hidden; 
  max-height: 100px; 
  transition: max-height .25s ease-in;
}
.metadataHeader {
  border-bottom: 1px solid #ccc; 
  color: #aaa; 
  display: block;
  margin-bottom: 5px;
}
@media print {
  .collapsable {
    max-height: none !important;
  }
  .readMore {
    display: none;
  }
}
</style>