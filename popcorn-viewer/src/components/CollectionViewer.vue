<template>
  <div class="collection">
    <div v-for="member in members" :key="member.key">
      <router-link :to="{path: '', query: { id: member.rep_id }}">
        <img :src="member.thumb" alt="Thumbnail">
        {{ member.title }}
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  components: {
  },
  props: {
    collectionData: Object,
    query: String,
  },
  computed: {
    members () {
      return this.collectionData.members
        .filter(member => {
          if (!this.query) return true
          const query = new RegExp(this.query, 'i')
          if (member.title.search(query) !== -1) {
            return true
          }
          if (member.catalogue_code && member.catalogue_code.search(query) !== -1) {
            return true
          }
          return false
        })
        .map(member => ({
          key: member.catalogue_code,
          title: member.title,
          // mms_id: member.mms_id,
          rep_id: member.representation_id,
          thumb: member.thumbnail,
        }))
    }
  },
}
</script>

<style scoped>
.collection {
  margin: 10px;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
}
.collection > div{
  font-size: 13px;
  text-align: center;
  height: 100%;
  padding: 4px;
}
.collection > div > a {
  display: block;
  background: white;
  padding: 4px;
  height: 100%;
  border-radius: 2px;
}
.collection > div > a:hover {
  text-decoration: none;
  color: blue;
  background: #efefef;
}
.collection > div img {
  margin: 0 auto;
  margin-bottom: 2px;
}
</style>