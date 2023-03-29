BaseCtrl = ($rootScope, $scope, $state, $timeout, Category, Style, Posts) ->
  vm = this
  vm.showContent = true
  window.onload = () ->
    $timeout () ->
      vm.showContent = true
      document.body.scrollTop = 0
    , 0

  toTitleCase = (str) ->
     str.replace '-', ' '
     .replace /\b\w/g, (l) ->
        return l.toUpperCase()

  $rootScope.$on '$stateChangeStart', (event, toState, toParams, fromState, fromParams) ->
    if fromState.name == 'drt.index.about' || toState.name == 'drt.index.about'
      $timeout () ->
        document.body.scrollTop = 0
      , 0
    Style.body = switch
      when toState.name == 'drt.index' then 'list-view'
      when toState.name == 'drt.index.card' then 'profile-view'
      when toState.name == 'drt.index.about' then 'about-page'
      when toState.name == 'drt.index.subscribe' then 'subscribe-page'
      else ''

    Style.title = switch
      when toState.name == 'drt.index' then 'Dorm Room Tycoon'
      when toState.name == 'drt.index.card' then toTitleCase(toParams.card) + ' | Dorm Room Tycoon'
      when toState.name == 'drt.index.about' then 'About | Dorm Room Tycoon'
      when toState.name == 'drt.index.about.subscribe' then 'About | Dorm Room Tycoon'
      when toState.name == 'drt.index.subscribe' then 'Dorm Room Tycoon | DRT.fm'

  $scope.$on 'search:reapply', () ->
    vm.search(true)

  vm.style = Style
  vm.category = Category
  vm.category.search = ''
  vm.category.search_old = ''

  vm.home = () ->
    Style.body = 'list-view'
    $state.go('drt.index')
    vm.category.reset()
    Posts.reloadWithFilter {}

  vm.cancel = (e) ->
    if e.keyCode == 27
      cancel()

  vm.search = (force=false) ->
    $state.go('drt.index')
    if force || vm.category.search != vm.category.search_old
      $rootScope.$broadcast('search:triggered', vm.category.search)
      vm.category.search_old = vm.category.search

  cancel = () ->
    $state.go('drt.index')
    if vm.category.search
      vm.category.search = ''
      vm.category.search_old = ''
      $rootScope.$broadcast('search:triggered', '')
      Posts.reloadWithFilter {}

  return vm

angular.module("app.controllers").controller "BaseCtrl", BaseCtrl
BaseCtrl.$inject = [
  "$rootScope"
  "$scope"
  "$state"
  "$timeout"
  "CategoryService"
  "StyleService"
  "PostFactory"
]

CategoryCtrl = ($scope, $timeout, Category, Restangular, Posts, anchorSmoothScroll) ->

  vm = this
  vm.category = Category
  vm.items = []

  $scope.$on 'search:triggered', (event, data) ->
    log 'CAT list:filtered', data
    if data == ''
      vm.all()
    else
      vm.category.reset()
      vm.category.select
        name: 'search'
        color: "#ED1178"


  Restangular.all('/api/category').getList().then (response) ->
    vm.items = response
    vm.all()

  vm.search = () ->
    $scope.$emit 'search:reapply'
    vm.category.reset()
    vm.category.select
      name: 'search'
      color: "#ED1178"
    vm.scrollToElement()

  vm.all = ->
    if vm.category.selected == null
      return

    vm.category.reset()
    Posts.reloadWithFilter {}

  vm.clickedAll = ->
    vm.scrollToElement()

    vm.all()

  vm.popular = ->
    if vm.category.selected != null
      if vm.category.selected.slug == 'popular'
        return

    vm.category.reset()
    vm.category.select
      slug: 'popular'
      name: 'Popular'
      color: "#ED7118"
    Posts.reloadWithFilter {popular: 'True'}
    vm.scrollToElement()

  vm.select = (tab) ->
    if vm.selected == tab
      return

#    vm.category.search = ''
    vm.category.select tab
    Posts.reloadWithFilter {category__slug: tab.slug}
    vm.scrollToElement()

  vm.scrollToElement = () ->
    $timeout () ->
      anchorSmoothScroll('main-nav-section')
    , 500

  return vm

angular.module("app.controllers").controller "CategoryCtrl", CategoryCtrl
CategoryCtrl.$inject = [
  "$scope"
  "$timeout"
  "CategoryService"
  "Restangular"
  "PostFactory"
  "anchorSmoothScroll"
]

PlayerCtrl = (drtPlayerService, Posts) ->
  vm = this

  vm.player = drtPlayerService
  vm.player.onSetItem ->
    if !vm.player.item.download_url
      Posts.getDownloadUrl(vm.player.item).then (response) ->
        vm.player.item.download_url = response.download_url

  return vm

angular.module("app.controllers").controller "PlayerCtrl", PlayerCtrl
PlayerCtrl.$inject = [
  "drtPlayerService",
  "PostFactory"
]

MastheadCtrl = ($rootScope, $state, $timeout, drtPlayerService, Posts) ->
  vm = this

  Posts.getFeatured().then (featured) ->
    vm.featured = featured

  vm.player = drtPlayerService

  vm.toggle = () ->
    if(vm.featured==drtPlayerService.item && drtPlayerService._playing ) # pause
      drtPlayerService.pause()
    else if(vm.featured==drtPlayerService.item) # pause
      drtPlayerService.play()
    else if(vm.featured) # play
      drtPlayerService.setSource vm.featured, true

  vm.showSubscribe = () ->
    $state.go('drt.index.subscribe')

  vm.showProfile = () ->
    $rootScope.$broadcast('feature:show', vm.featured)

  return vm

angular.module("app.controllers").controller "MastheadCtrl", MastheadCtrl
MastheadCtrl.$inject = [
  "$rootScope",
  "$state",
  "$timeout",
  "drtPlayerService",
  "PostFactory"
]
