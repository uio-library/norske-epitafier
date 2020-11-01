<template>
  <div>
    <div class="flex flex-row items-center">
      <div class="flex-1 flex p-2">
        <input 
          type="text" 
          v-model="queryInput" 
          placeholder="Du kan f.eks. søke etter kirke, museum, motiv eller person" 
          class="flex-1 px-5 py-2 bg-gray-100 focus:bg-blue-100 placeholder-gray-800 text-teal-900 focus:text-blue-900 outline-none focus:shadow-outline" 
          @input="search()"
        >
      </div>

      <div class="p-2">
        Sortering: 
        <LystettRullegardinMeny
          :options="sortOptions"
          :selected="sort"
          @value="onSortChanged($event)" 
        />
      </div>
    </div>
  </div>
</template>
<script>
import { groupBy, debounce } from 'lodash'
import LystettRullegardinMeny from './LystettRullegardinMeny'
import { settings } from '../settings'

export default {
  components: {
    LystettRullegardinMeny,
  },
  props: {
    collectionData: Object,
  },
  data () {
    return {
      queryInput: this.$route.query.q || '',
      query: this.$route.query.q || '',
      sort: this.$route.query.sort || settings.default_sort,
      sortOptions: {
        title: {
          nb: 'Avbildet person',
        },
        date: {
          nb: 'År',
        },
        location: {
          nb: 'Kirke',
        },
      }
    }
  },
  mounted () {
    this.updateSuggestions()
  },
  methods: {
    onSortChanged: function(newValue) {
      console.log('new sort:', newValue)
      this.sort = newValue
      this.$router.push({ path: '/', query: { q: this.query, sort: newValue } })
    },
    search: debounce(function() {
      console.log('Search:', this.queryInput)
      this.query = this.queryInput
      this.$router.push({ path: '/', query: { q: this.query } })
    }, 200),
    updateSuggestions() {
     

    },
  },
  watch: {
    collectionData() {
      this.updateSuggestions()
    },
    $route(route) {
      if (route.query.q != this.query) {
        this.query = route.query.q
        this.queryInput = route.query.q
      }
      if (route.query.sort != this.sort) {
        this.sort = route.query.sort || settings.default_sort
      }
    }
  },
}
</script>