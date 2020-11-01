<template>
  <div class="group inline-block">
    <button
      class="text-left text-blue-700 focus:border-blue-500  px-3 py-1 bg-white outline-none focus:outline-none focus:shadow-outline rounded-sm flex items-center min-w-32"
      @click.stop="open = !open"
    >
      <span class="pr-1 flex-1">{{ selectedLabel }}</span>
      <span>
        <svg
          :class="{'-rotate-180': open}"
          class="fill-current h-4 w-4 transform
          transition duration-150 ease-in-out"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 20 20"
        >
          <path
            d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"
          />
        </svg>
      </span>
    </button>
    <transition name="slide-down">
      <ul v-if="open" class="bg-white border rounded-sm dropDownContent absolute origin-top min-w-32">
        <li v-for="(item, key) in options" :key="key"
          class="rounded-sm"
        >
          <button @click="selectItem(key)" class="block w-full text-left px-3 py-1 hover:bg-blue-100 focus:bg-gray:200">{{ item.nb }}</button></li>
      </ul>
    </transition>
  </div>
</template>
<script>
export default {
  props: {
    options: Object,
    selected: String,
  },
  data () {
    return {
      open: false,
    }
  },
  methods: {
    clickAnywhere() {
      this.open = false
    },
    selectItem(key) {
      this.$emit('value', key)
    },
  },
  mounted () {
    this.clickAnywhereHandler = this.clickAnywhere.bind(this)
    window.addEventListener('click', this.clickAnywhereHandler)
  },
  beforeDestroy() {
    window.removeEventListener('click', this.clickAnywhereHandler)
  },
  computed: {
    selectedLabel () {
      if (!this.options[this.selected]) {
        return 'Invalid sort'
      }
      return this.options[this.selected].nb
    }
  }
}
</script>

<style scoped>

.slide-down-enter-active, .slide-down-leave-active {
  transition: transform .15s;
}
.slide-down-enter, .slide-down-leave-to /* .fade-leave-active below version 2.1.8 */ {
  transform: scaleY(0);
}

  /* since nested groupes are not supported we have to use 
     regular css for the nested dropdowns 
  */
  li>ul                 { transform: translatex(100%) scale(0) }
  li:hover>ul           { transform: translatex(101%) scale(1) }
  li > button svg       { transform: rotate(-90deg) }
  li:hover > button svg { transform: rotate(-270deg) }

  /* Below styles fake what can be achieved with the tailwind config
     you need to add the group-hover variant to scale and define your custom
     min width style.
  	 See https://codesandbox.io/s/tailwindcss-multilevel-dropdown-y91j7?file=/index.html
  	 for implementation with config file
  */
  .group:hover .group-hover\:scale-100 { transform: scale(1) }
  .group:hover .group-hover\:-rotate-180 { transform: rotate(180deg) }
  .scale-0 { transform: scale(0) }
  .min-w-32 { min-width: 10rem }
</style>