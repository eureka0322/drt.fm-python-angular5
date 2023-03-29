IndexCtrl = ($scope, $state, $stateParams, $cookies, $timeout, Posts, drtPlayerService, anchorSmoothScroll) ->

  vm = this
  vm.posts = Posts
  vm.player = drtPlayerService
  vm.progress = 0
  vm.duration = 0
  vm.selected_id = 0

  $scope.$on 'track:progress', (event, data) ->
    vm.progress = data

  $scope.$on 'currentTrack:duration', (event, data) ->
    vm.duration = data

  $scope.$on 'search:canceled', (event, data) ->
    $scope.$emit 'list:filtered'

  $scope.$on 'search:triggered', (event, data) ->
    if data
      Posts.reloadWithFilter {search: data}
      $timeout () ->
        anchorSmoothScroll('main-nav-section')
      , 500
    $scope.$emit 'list:filtered'

  $scope.$on 'feature:show', (event, data) ->
    vm.selected_id = data.id
    $state.go('drt.index.card', {card: data.slug})

  vm.play = (card) ->
    if(card.selected && drtPlayerService._playing) # pause
      drtPlayerService.pause()
    else if(card.selected) # play
      drtPlayerService.play()
    else
      vm.select card, true

  vm.pause = () ->
    drtPlayerService.pause()

  vm.select = (card, autoplay) ->
    if !vm.posts.select(card)
      return card

    if $stateParams.card == card.slug
      return card

    if drtPlayerService._started && !autoplay
      return card

    drtPlayerService.setSource card, autoplay

  vm.show = (card) ->
    vm.selected_id = card.id
    $state.go('drt.index.card', {card: card.slug})

  showSubscribeFunc = () ->
    if $cookies.get('subscribed_user')
      return

    if !$cookies.get('subscription_page_seen')
      $timeout () ->
        expireDate = new Date();
        expireDate.setDate(expireDate.getDate() + 1);
        $cookies.put('subscription_page_seen', 1, {'expires': expireDate})
        if $state.current.name == "drt.index.about"
          $state.go('drt.index.about.subscribe')
        else if $state.current.name == "drt.index.card"
          $state.go('drt.index.card.subscribe')
        else
          $state.go('drt.index.subscribe')
      , 12000
  if $state.current.name == "drt.index"
    showSubscribeFunc()

  checkDevice = () ->
#    if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini|Mobile|mobile|CriOS/i.test navigator.userAgent) || (window.innerWidth <= 640)
    if window.innerWidth <= 640
      vm.deviceCheck = 'mobile'
    else
      vm.deviceCheck = 'desktop'

  $(window).resize ->
    $scope.$apply checkDevice

  checkDevice()

  return vm

angular.module("index.controllers").controller "IndexCtrl", IndexCtrl
IndexCtrl.$inject = [
  "$scope"
  "$state"
  "$stateParams"
  "$cookies"
  "$timeout"
  "PostFactory"
  "drtPlayerService"
  "anchorSmoothScroll"
]

ProfileCtrl = ($scope, $timeout, $state, $stateParams, $sce, Style, Posts, drtPlayerService, JobsFactory, $http, $cookies, serializer) ->
  vm = this
  vm.selected = null
  vm.player = drtPlayerService
  vm.encodedImageURI = null
  vm.sponsorship = ''
  vm.sponsorship_image = ''
  vm.about = ''
  vm.transcript = ''
  vm.transcriptTrimmed = true
  vm.submitBtn = 'Sign Up'
  vm.subscriptionLoading = false
  vm.posts = Posts.one $stateParams.card, (selected, err = null) ->
    console.log 'SELECTED CARD', selected
    if err
      $state.go 'drt.index'
    vm.selected = selected
    vm.selected.visible = true
    image = selected.image + "?w=700&h=400&fit=crop&crop=faces&sat=-100&auto=format,compress&cs=tinysrgb"
    vm.encodedImageURI = 'https://drt-resources.imgix.net/uploads/images/388dd5.png?bm=softlight&balph=80&blend=' + encodeURIComponent(image)
    vm.sponsorship = $sce.trustAsHtml(selected.sponsorship)
    vm.sponsorship_image = selected.sponsorship_image
    vm.sponsorship_image_text = $sce.trustAsHtml(selected.sponsorship_image_text)
    vm.about = $sce.trustAsHtml(selected.about)
    vm.transcript = $sce.trustAsHtml(selected.transcript)
    if !drtPlayerService._started
      drtPlayerService.setSource selected, false

    Style.title = selected.title + ' - ' + selected.guest + ', ' + selected.job + ' | Dorm Room Tycoon'
    $timeout () ->
      setLinkAttribute()
#      Style.body = Style.body + ' overflow-hidden'
    , 500

  vm.jobs = JobsFactory
  vm.jobs.load()

  vm.validate = () ->
    emailPattern = /^([\w.-]+)@([\w.-]+)\.([a-zA-Z.]{2,6})$/i
    email = $scope.email
    if !email || !(email.match emailPattern)
      vm.submitBtn = 'Invalid Email'
      return false
    true

  vm.restoreBtn = () ->
    vm.submitBtn = 'Sign Up' if $scope.subscribeForm.$dirty

  vm.doSubmit = (e) ->
    e.preventDefault()
    if !vm.validate() || vm.subscriptionLoading
      return

    vm.subscriptionLoading = true
    params =
      'subscriber[email]': $scope.email
      'mb_cf16df1182ce43a695b327281db3f0ad': ''
    config =
      headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' }

    $http
      .post $scope.subscribeForm.$$element[0].action, serializer(params), config
      .then(
        (data) ->
            vm.submitBtn = 'Success!'
            $cookies.put('subscribed_user', 1)
        (error) -> vm.submitBtn = 'Already Registered' if error.status == 422
      )
      .finally(() -> vm.subscriptionLoading = false)

  vm.toggleTrim = () ->
    $(document).ready () ->
      $('#profile-transcript-container').toggleClass('trimmed')
      $scope.$apply () ->
        vm.transcriptTrimmed = !vm.transcriptTrimmed

  vm.toggle = () ->
    if(vm.selected==drtPlayerService.item && drtPlayerService._playing ) # pause
      drtPlayerService.pause()
    else if(vm.selected==drtPlayerService.item) # pause
      drtPlayerService.play()
    else if(vm.selected) # play
      drtPlayerService.setSource vm.selected, true
    console.log(vm.player)
    console.log(vm.player.item)
    console.log(vm.selected)

  vm.close = () ->
    vm.selected.visible = false
    $timeout () ->
      vm.selected = null
      Style.body = 'list-view'
      $state.go('drt.index')
    , 550

  setLinkAttribute = () ->
    a = document.getElementById('profile-sponsor-container').getElementsByTagName('a')
    aLink.setAttribute('target', '_blank') for aLink in a
    b = document.getElementById('profile-about-container').getElementsByTagName('a')
    bLink.setAttribute('target', '_blank') for bLink in b

  return vm

angular.module("index.controllers").controller "ProfileCtrl", ProfileCtrl
ProfileCtrl.$inject = ["$scope", "$timeout", "$state", "$stateParams", "$sce", "StyleService",  "PostFactory", "drtPlayerService",
  "JobsFactory",
  "$http",
  "$cookies",
  "$httpParamSerializer"]

SubscribeCtrl = ($scope, $state, $http, $cookies, serializer, Style) ->
  vm = this
  vm.submitBtn = 'INSPIRE ME'
  vm.loading = false

  vm.validate = () ->
    emailPattern = /^([\w.-]+)@([\w.-]+)\.([a-zA-Z.]{2,6})$/i
    email = $scope.email
    if !email || !(email.match emailPattern)
      vm.submitBtn = 'INVALID EMAIL'
      return false
    true

  vm.restoreBtn = () ->
    vm.submitBtn = 'INSPIRE ME' if $scope.subscribeForm.$dirty

  vm.doSubmit = (e) ->
    e.preventDefault()
    if !vm.validate() || vm.loading
      return

    vm.loading = true
    params =
      'subscriber[email]': $scope.email
      'mb_cf16df1182ce43a695b327281db3f0ad': ''
    config =
      headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' }

    $http
      .post $scope.subscribeForm.$$element[0].action, serializer(params), config
      .then(
        (data) ->
            vm.submitBtn = 'SUCCESS!'
            $cookies.put('subscribed_user', 1)
        (error) -> vm.submitBtn = 'ALREADY REGISTERED' if error.status == 422
      )
      .finally(() -> vm.loading = false)

  vm.closeSubscribe = (e) ->
    e.preventDefault()
    console.log $state.current.name
    if $state.current.name == "drt.index.about.subscribe"
      $state.go("drt.index.about")
    if $state.current.name == "drt.index.card.subscribe"
      $state.go('drt.index.card')
    else if $state.current.name == "drt.index.subscribe"
      $state.go("drt.index")

  return vm

angular.module("index.controllers").controller "SubscribeCtrl", SubscribeCtrl
SubscribeCtrl.$inject = [
  "$scope",
  "$state",
  "$http",
  "$cookies",
  "$httpParamSerializer"
  "StyleService"
]

AboutCtrl = ($scope, $state, $timeout) ->
  vm = this
#  vm.tweetIds = ['783763102743441408', '760180067674710016', '745000776880164864', '737999725178261504', '848763228234633216', '844926017089228800', '843882395250049024', '839127218324451333']
  vm.tweetIds = [
      '877629204891934720',
      '848763228234633216',
      '853989537411981312',
      '852470116465954816',
      '851445765864120322',
      '849120060295835648',
      '843882395250049024',
      '839127218324451333',
      '829238534133383169',
      '783763102743441408',
      '760180067674710016',
      '745000776880164864',
      '737999725178261504'
  ]
  vm.responsiveConfig = [
    {
      breakpoint: 1400,
      settings: { slidesToShow: 2 }
    }
    {
      breakpoint: 1020,
      settings: { slidesToShow: 1 }
    }
    {
      breakpoint: 830,
      settings: { slidesToShow: 2 }
    }
    {
      breakpoint: 640,
      settings: { slidesToShow: 1 }
    }
  ]

  $(document).ready () ->
    $("iframe").contents().find('.EmbeddedTweet').css("border", "none")

  vm.onTweetWidgetLoad = () ->
#    if (vm.tweetLoaded)
#      return;
    vm.tweetLoaded = true
    $(document).ready () ->
      twitterElement = $("iframe").contents().find('.EmbeddedTweet')
      if(twitterElement.length)
        twitterElement.css('border', 'none')
      else
        twitterElements = document.getElementsByTagName("twitterwidget")
        el.shadowRoot.querySelector('.EmbeddedTweet').style.border = 'none' for el in twitterElements

  vm.openNewletter = (e) ->
    e.preventDefault()
    $state.go('drt.index.about.subscribe')

  return vm

angular.module("index.controllers").controller "AboutCtrl", AboutCtrl
AboutCtrl.$inject = ["$scope", "$state", "$timeout"]
