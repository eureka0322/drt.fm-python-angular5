angular.module "app.config", []

unhandledRejections = ($qProvider) ->
  $qProvider.errorOnUnhandledRejections(false)

resourceConfig = ($resourceProvider) ->
  $resourceProvider.defaults.stripTrailingSlashes = false

restAngularConfig = (RestangularProvider) ->
  RestangularProvider.setBaseUrl('https://drt.fm/')
#  RestangularProvider.setBaseUrl('http://52.71.60.10/')
#  RestangularProvider.setBaseUrl('http://localhost:8000/')
#  RestangularProvider.setBaseUrl('http://0.0.0.0:8000/')
  RestangularProvider.setRequestSuffix "/"

httpConfig = ($httpProvider) ->
  $httpProvider.interceptors.push "AuthInterceptor"

locationConfig = ($locationProvider) ->
  $locationProvider.html5Mode
    enabled: true,
    requireBase: false

run = ($http, $cookies) ->
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken
  $http.defaults.headers.put['X-CSRFToken'] = $cookies.csrftoken
  $http.defaults.headers.patch['X-CSRFToken'] = $cookies.csrftoken
  $http.defaults.headers.delete =
    'X-CSRFToken': $cookies.csrftoken
    'Content-Type': 'application/json'
  return

angular.module("app.config").config unhandledRejections
angular.module("app.config").config resourceConfig
angular.module("app.config").config restAngularConfig
angular.module("app.config").config locationConfig

#angular.module("app.config").config httpConfig
#angular.module("app").run run

httpConfig.$inject = ["$httpProvider"]
locationConfig.$inject = ["$locationProvider"]
unhandledRejections.$inject = ["$qProvider"]

DEBUG = false

log = (string, args...) ->
  if DEBUG
    console.log "{DEBUG} #{string}"
    i = 1
    args.forEach (arg) ->
      console.log arg
      i++
