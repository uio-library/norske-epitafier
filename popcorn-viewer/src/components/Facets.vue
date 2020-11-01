<template>
  <div class="p-3">

    <div v-for="facet in facets">
      <div class="px-1 py-1 text-sm rounded font-bold bg-gray-300">
        {{ facet.key }}
      </div>
      <div>
        <ul  class="px-1 mb-3 text-sm">
          <li v-for="item in facet.values" :key="item.key">
            <div>
              <a href="#" 
                :class="{ 'font-bold': selected && (selected == item || selected.parent == item) }" 
                @click.prevent="selectValue(item)"
              >{{ item.key }} ({{ item.count }})</a>
            </div>
            <ul
              class="px-3 mb-1 collapsable"
              :class="{
                'expanded': selected && (selected == item || selected.parent == item) && item.values
              }"
            >
              <li v-for="child in item.values" :key="child.key">
                <a href="#" @click.prevent="selectValue(child)" 
                  class="text-sm"
                  :class="{ 'font-bold': selected && (selected == child) }">{{ child.key }} ({{ child.count }})</a>
              </li>
            </ul>
          </li>
        </ul>
      </div>
    </div>

  </div>
</template>

<script lang="ts">
import { chain, cloneDeep, some } from 'lodash'
//import simplebar from 'simplebar-vue'
//import 'simplebar/dist/simplebar.min.css' 

const museumslista = [
  'Norsk Folkemuseum',
  'Oslo Museum - Bymuseet', // ->Oslo Bymuseum
  'Stavanger Museum',
  'Universitetsmuseet i Bergen',
  'NTNU Vitenskapsmuseet',
  'Drammen museum',
  'Vingelen kirke- og skolemuseum',
  'Fredrikstad Museum',
  'Tromsø Museum - Universitetsmuseet'
]

export default {
  props: {
    collectionData: Object,
    query: Array,
  },
  components: {
    //simplebar,
  },
  computed: {

    cleaned () {
      if (!this.collectionData) return []
      return this.collectionData.members.map(rec => {
        rec = cloneDeep(rec)
        rec.record.location = rec.record.location.replace(/ \(.*?\)$/, '')
          .replace(/, .*?$/, '')
          //.replace(/- .*?$/, '')
          .replace(/\./, '')
        rec.record.originalLocation = rec.record.originalLocation.replace(/ \(.*?\)$/, '')
        return rec
      })
    },
  },

  data() {
    return {
      selected: null,
      facets: [],
    }
  },
  mounted () {
    this.updateFacets()
  },
  watch: {
    query () {
      this.updateFacets()
    },
    collectionData () {
      this.updateFacets()
    }
  },
  methods: {
    selectValue(item) {
      this.selected = item
      if (item.parent) {
        this.search(`${item.parent.field}:"${item.parent.key}" ${item.field}:"${item.key}"`)
      } else {
        this.search(`${item.field}:"${item.key}"`)
      }
    },
    search(query) {
      this.$router.push({ path: '', query: { q: query } })
    },

    updateFacets () {
      if ( ! this.collectionData ) return []

      const locations = chain(this.cleaned)
        .groupBy(rec => rec.record.diocese)
        .map((values, key) => {
          const item = {
            key,
            field: 'stift',
            count: values.length,
          }
          item.values = chain(values)
            .groupBy(rec => rec.record.originalLocation)
            .map((values, key) => ({
              key, 
              field: 'sted',
              parent: item,
              count: values.length,
            }))
            .sort((a,b) => a.key.localeCompare(b.key, 'nb'))
            .value()
          return item
        })
        .sort((a,b) => a.key.localeCompare(b.key, 'nb')) 
        .value()

      const institutions = chain(this.cleaned)
        .filter(rec => museumslista.indexOf(rec.record.location) !== -1)
        .groupBy(rec => rec.record.location)
        .map((values, key) => ({
          key,
          field: 'sted', 
          count: values.length,
        }))
        .sort((a,b) => a.key.localeCompare(b.key, 'nb'))
        .value()

      this.facets = [
        {key: 'Kirker etter stift', values: locations},
        {key: 'Institusjoner og samlinger', values: institutions},
      ]

      this.selected = null
      this.facets.forEach(facet => {
        facet.values.forEach(item => {
          if (some(this.query, qp => qp.field == item.field && qp.value == item.key)) {
            this.selected = item
          }
          if (item.values) {
            item.values.forEach(child => {
              if (
                some(this.query, qp => qp.field == child.field && qp.value == child.key)
                && some(this.query, qp => qp.field == child.parent.field && qp.value == child.parent.key)
              ) {
                this.selected = child
              }
            })
          }
        })
      })
    },
  },
}
</script>

<style scoped>
.collapsable {
  opacity: 0;
  visibility: hidden;
  max-height: 0;
  overflow: hidden;
  transition: opacity .2s ease-out;
}
.expanded {
  opacity: 100;
  max-height: none;
  visibility: visible;
  transition: opacity .2s ease-out;
}
</style>