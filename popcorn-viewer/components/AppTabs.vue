<template>
  <ul class="list-reset border-gray-900 pl-3 flex" :class="{ 'border-b pt-2': position === 'top', 'border-t pb-2': position === 'bottom' }">
    <li
      v-for="item in items"
      :key="item.value"
      class="mr-1"
      :class="{'-mb-px': item.value === activeItem}"
    >
      <a
        href="#"
        class="bg-white inline-block py-2 px-4 font-semibold hover:no-underline"
        :class="{'bg-gray-700 text-gray-200': item.value === activeItem, 'text-blue hover:text-blue-darker': item.value !== activeItem, 'rounded-t': position === 'top', 'rounded-b': position === 'bottom'}"
        @click.prevent="selectItem(item)"
      >{{ item.label }}</a>
    </li>
  </ul>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  props: {
    items: Array,
    selected: String,
    position: {
      type: String,
      default: 'top',
      validator (position: string) {
        return position === 'top' || position === 'bottom'
      },
    },
  },
  data() {
    console.log('INIT', this.selected)
    return {
      activeItem: this.selected
    }
  },
  watch: {
    selected (newValue: string) {
      this.activeItem = newValue
    }
  },
  methods: {
    selectItem(item) {
      this.activeItem = item.value
      this.$emit('change', item.value)
    }
  }
})
</script>
