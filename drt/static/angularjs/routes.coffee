config = ($stateProvider, $urlRouterProvider) ->
  $urlRouterProvider
    .otherwise('/')

  $stateProvider
    .state "drt",
      url: ""
      views:
        "wrapper":
          templateUrl: "static/angularjs/wrapper.html"
        "masthead@drt":
          templateUrl: "static/angularjs/masthead.html"
          controller: "MastheadCtrl"
          controllerAs: "vm"
        "navigation@drt":
          templateUrl: "static/angularjs/navigation.html"
          controller: "CategoryCtrl"
          controllerAs: "vm"
        "player@drt":
          templateUrl: "static/angularjs/player.html"
          controller: "PlayerCtrl"
          controllerAs: "vm"
      abstract: true

  return

angular.module("app.config").config config
config.$inject = [
  "$stateProvider"
  "$urlRouterProvider"
]
