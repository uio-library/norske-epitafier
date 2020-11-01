export const parseQuery = (query) => {
  if (!query) {
    return []
  }
  const pattern = new RegExp('([a-z]+):"(.*?)"', 'g')
  const matches = [...query.matchAll(pattern)].map(x => ({field: x[1], value: x[2]}))
  const rest = query.replace(pattern, '').trim()
  if (rest) {
    matches.push({field: 'any', value: rest})
  }
  return matches
}