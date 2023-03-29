PostFactory = ($stateParams, $timeout, Restangular) ->

  url = '/api/post'
  end = true
  Posts = {
#    selected: null
    items: []
    busy: false
    filter: false
  }

  Posts.init = () ->
    end = false
#    this.selected = null
    this.items = []
    this.busy = false
    this.filter = {
      limit: 12
      offset: 0
    }

  Posts.reloadWithFilter = (data) ->
    end = false
    this.filter = {
      limit: 12
      offset: 0
    }
    this.filter = angular.extend(this.filter, data)
    if this.busy || end || !this.filter
      return

    this.busy = true;

    Restangular.one(url).get(this.filter).then (response) ->
      if !response.results.length
        end = true
      Posts.items = []
      Posts.items.push item for item in response.results
      Posts.filter.offset += Posts.filter.limit
      Posts.busy = false;

  Posts.more = () ->
    if this.busy || end || !this.filter
      return

    this.busy = true;

    Restangular.one(url).get(this.filter).then (response) ->
      if !response.results.length
        end = true
      Posts.items.push item for item in response.results
      Posts.filter.offset += Posts.filter.limit
      $timeout () ->
        Posts.busy = false;
      , 1000

  Posts.select = (card) ->
    if card.selected
      return false

#    Posts.selected = card

    post.selected = false for post in Posts.items
    card.selected = true

  Posts.one = (slug, callback) ->
    Restangular.one(url, slug).get().then (response) ->
      Posts.select(response)
      callback(response)
    , (err) ->
        if err.status && err.status == 500
          callback(null, err)
    return Posts

  Posts.getFeatured = () ->
    Restangular.one(url).get({ featured: 'True' }).then (response) ->
      if !response.results.length
        return false
      response.results[0]

  Posts.getDownloadUrl = (item) ->
    Restangular.one(url, item.slug).get('download_url')

  return Posts

angular.module("index.models").factory "PostFactory", PostFactory
PostFactory.$inject = [
  "$stateParams"
  "$timeout"
  "Restangular"
]
