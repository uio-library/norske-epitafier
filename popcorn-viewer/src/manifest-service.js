import axios from 'axios'
import { settings} from './settings'

export default {
  listeners: [],
  manifest: null,
  loadManifest: function (manifestId) {
    return new Promise((resolve,reject) => {
      if (!manifestId) {
        this.setManifest(null)
        return reject()
      }
      console.info('loadManifest:', manifestId)
      const http = axios.create({ credentials: true })
      http
        .get(settings.iiifServiceUrl(manifestId))
        .then(res => res.data)
        .then(manifest => {
          this.setManifest(manifest)
          resolve(manifest)
        })
        .catch(err => reject(err))
    })
  },
  setManifest: function(manifest) {
    this.manifest = manifest
    console.info(`Notifying ${this.listeners.length} listeners`)
    this.listeners.forEach(listener => listener(manifest))

  },
  getManifest: function() {
    return this.manifest
  },
  onChanged: function(listener) {
    this.listeners.push(listener)
  },
}