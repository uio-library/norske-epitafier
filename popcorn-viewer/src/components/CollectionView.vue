<template>
  <div class="flex-grow bg-gray-200 flex flex-col">

    <div class="bg-gray-300">
      <search-bar :collection-data="collection"></search-bar>
    </div>

    <div class="flex items-start">
      <div class="flex-shrink-0 facets">
        <facets :collection-data="collection" :query="query" />
      </div>
      <div class="flex-shrink flex-grow collection">
        <div v-for="member in members" :key="member.key">
          <router-link :to="{path: `/${member.rep_id}` }">
            <img :src="member.thumb" alt="Thumbnail">
            <div>{{ member.title }}. {{ member.dateRaw }}</div>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Facets from './Facets'
import { every } from 'lodash'
import collectionData from '../../../dist/collection.json'
import { parseQuery } from '../query-parser'
import { settings} from '../settings'
import SearchBar from './SearchBar'

export default {
  components: {
    Facets,
    SearchBar,
  },
  computed: {
    collection () {
      return collectionData
    },
    query() {
      return parseQuery(this.$route.query.q)
    },
    sort () {
      return this.$route.query.sort || settings.default_sort
    },
    members () {
      const data = this.collection.members
        .filter(member => {
          if ( ! this.query.length ) {
            return true
          }
          let matches = this.query.map(queryPart => {
            const queryValue = new RegExp(queryPart.value, 'i')
            if (queryPart.field == 'stift') {
              if (member.record.diocese && member.record.diocese.search(queryValue) !== -1) {
                return true
              }
            }
            if (queryPart.field == 'sted') {
              if (member.record.originalLocation && member.record.originalLocation.search(queryValue) !== -1) {
                return true
              }
              if (member.record.location && member.record.location.search(queryValue) !== -1) {
                return true
              }
            }
            console.log(member.record)
            if (queryPart.field == 'any') {
              if (member.title.search(queryValue) !== -1) {
                return true
              }
              if (member.catalogue_code && member.catalogue_code.search(queryValue) !== -1) {
                return true
              }
              const searchFields = ['date', 'originalLocation', 'location', 'artist', '{http://purl.org/dc/terms/}description']

              for (let index = 0; index < searchFields.length; index++) {
                if (member.record[searchFields[index]] && member.record[searchFields[index]].search(queryValue) !== -1) {
                  return true
                }
              }
            }
            return false
          })
          return every(matches)
        })
        .map(member => ({
          key: member.catalogue_code,
          title: member.title,
          // mms_id: member.mms_id,
          rep_id: member.representation_id,
          thumb: member.thumbnail,
          dateRaw: member.record.date,
          date: member.record.date.replace(/[^0-9]/g, '') || '9999',  // for sorting, udaterte til slutt (ønske fra K)
          location: member.record.originalLocation,
        }))
        .sort((itemA, itemB) => {
          if (itemA[this.sort]) {
            return itemA[this.sort].localeCompare(itemB[this.sort], 'nb')
          }
          return 0
        })
      return data
    }
  },
}
</script>

<style scoped>
.facets {
  width: 350px;
}
@media (max-width: 768px) {
  .facets {
    display: none;
  }
}
.collection {
  margin: 10px;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
}
.collection > div{
  font-size: 13px;
  text-align: center;
  padding: 4px;
}
.collection > div > a {
  display: flex;
  flex-direction: column;
  justify-content: center;
  background: white;
  min-height: 250px;
  height: 100%;
  padding: 8px;
  box-shadow: 1px 1px 2px #999;
}
.collection > div > a:hover {
  text-decoration: none;
  color: blue;
}
.collection > div > a:active {
  background: #888;
  color: white;
}
.collection > div img {
  margin: 0 auto;
  margin-bottom: 2px;
}
</style>