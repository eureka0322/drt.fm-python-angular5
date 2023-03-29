config = ($stateProvider, $urlRouterProvider) ->

  $urlRouterProvider
    .otherwise('/')

  ruleFunc = ($injector, $location) ->
      path = $location.path()
      hasTrailingSlash = path[path.length-1] == '/'
      if(hasTrailingSlash)
        newPath = path.substr(0, path.length - 1);
        return newPath

  $urlRouterProvider.rule(ruleFunc)

  $stateProvider
    .state "drt.index",
      url: "/"
      views:
        "content@drt":
          templateUrl: "static/angularjs/index/index.html"
          controller: "IndexCtrl"
          controllerAs: "vm"
      resolve:
        setBodyStyle: (StyleService) ->
          StyleService.body = 'list-view'

    .state "drt.index.about",
      url: "about"
      views:
        "static@drt":
          templateUrl: "static/angularjs/index/about.html"
          controller: "AboutCtrl"
          controllerAs: "vm"
      resolve:
        setBodyStyle: (StyleService) ->
          StyleService.body = 'about-page'

    .state "drt.index.about.subscribe",
#      url: "subscribe"
      views:
        "subscribe@drt":
          templateUrl: "static/angularjs/index/subscribe.html"
          controller: "SubscribeCtrl"
          controllerAs: "vm"
      resolve:
        setBodyStyle: (StyleService) ->
          StyleService.body = 'subscribe-page about-page'

    .state "drt.index.subscribe",
#      url: "subscribe"
      views:
        "subscribe@drt":
          templateUrl: "static/angularjs/index/subscribe.html"
          controller: "SubscribeCtrl"
          controllerAs: "vm"
      resolve:
        setBodyStyle: (StyleService) ->
          StyleService.body = 'subscribe-page'

#    .state "drt.index.p404",
#      url: "404"
#      views:
#        "static@drt":
#          templateUrl: "static/angularjs/index/p404.html"
#          controller: "P404Ctrl"
#          controllerAs: "vm"
#      resolve:
#        setBodyStyle: (StyleService) ->
#          StyleService.body = '404-view'

    .state "drt.index.card",
      url: ":card"
      views:
        "profile@drt":
          templateUrl: "static/angularjs/index/profile.html"
          controller: "ProfileCtrl"
          controllerAs: "vm"
      resolve:
        setBodyStyle: (StyleService) ->
          StyleService.body = 'profile-view'

    .state "drt.index.card.subscribe",
      views:
        "subscribe@drt":
          templateUrl: "static/angularjs/index/subscribe.html"
          controller: "SubscribeCtrl"
          controllerAs: "vm"
      resolve:
        setBodyStyle: (StyleService) ->
          StyleService.body = 'subscribe-page profile-view'
  return

angular.module("index.routes").config config
config.$inject = ["$stateProvider", "$urlRouterProvider"]
