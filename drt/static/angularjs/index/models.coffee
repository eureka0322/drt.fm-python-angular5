RestService = (Restangular) ->

  extend = (url, callback) ->
    """ Get rest angular base service """
    self = Restangular.service url
    """ Extending rest angular service base functionality """
    angular.extend self, {
      getString: (label) ->
        self = this
        log label, self
    }
    """ Extend rest angular model - use to extend models """
    Restangular.extendModel url, (obj) ->
      callback(obj)
    return self

  return extend

angular.module('app.services').factory "RestService", RestService
RestService.$inject = [
  "Restangular"
]

Category = (RestService) ->

  RestService "category", () ->
    return

angular.module("index.models").service "Category", Category
Category.$inject = [
  "RestService"
]

Card = (RestService) ->

  RestService "post", () ->
    return

angular.module("index.models").service "Card", Card
Card.$inject = [
  "RestService"
]