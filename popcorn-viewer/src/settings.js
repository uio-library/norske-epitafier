export const settings = {
  
  baseUrl: process.env.BASE_URL === 'production' ? '/norske-epitafier-1537-1700/' : '/',
  
  iiifServiceUrl: id => `https://ub-media.uio.no/norske-epitafier-1537-1700/manifest.php?id=${id}`,
  // `https://bibsys-k.userservices.exlibrisgroup.com/view/iiif/presentation/${this.id}/manifest`  # NOT WORKING WITH MMS IDs atm.

}
