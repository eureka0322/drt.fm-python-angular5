angular.module "drt.player", []

drtPlayerService = ($timeout, $sce) ->

  controls = ["<div class='plyr__controls'>",
    "<button type='button' data-plyr='play'>",
        "<svg><use xlink:href='#plyr-play'></use></svg>",
        "<span class='plyr__sr-only'>Play</span>",
    "</button>",
    "<button type='button' data-plyr='pause'>",
        "<svg><use xlink:href='#plyr-pause'></use></svg>",
        "<span class='plyr__sr-only'>Pause</span>",
    "</button>",
    "<span class='plyr__time'>",
        "<span class='plyr__sr-only'>Current time</span>",
        "<span class='plyr__time--current'>00:00</span>",
    "</span>",
    "<span class='plyr__progress'>",
        "<label for='seek{id}' class='plyr__sr-only'>Seek</label>",
        "<input id='seek{id}' class='plyr__progress--seek' type='range' min='0' max='100' step='0.1' value='0' data-plyr='seek'>",
        "<progress class='plyr__progress--played' max='100' value='0' role='presentation'></progress>",
        "<progress class='plyr__progress--buffer' max='100' value='0'>",
            "<span>0</span>% buffered",
        "</progress>",
        "<span class='plyr__tooltip'>00:00</span>",
    "</span>",
    "<span class='plyr__time'>",
        "<span class='plyr__sr-only'>Duration</span>",
        "<span class='plyr__time--duration'>00:00</span>",
    "</span>",
    "<button type='button' data-plyr='mute'>",
        "<svg class='icon--muted'><use xlink:href='#plyr-muted'></use></svg>",
        "<svg><use xlink:href='#plyr-volume'></use></svg>",
        "<span class='plyr__sr-only'>Toggle Mute</span>",
    "</button>",
    "<span class='plyr__volume'>",
        "<label for='volume{id}' class='plyr__sr-only'>Volume</label>",
        "<input id='volume{id}' class='plyr__volume--input' type='range' min='0' max='10' value='10' data-plyr='volume'>",
        "<progress class='plyr__volume--display' max='10' value='0' role='presentation'></progress>",
    "</span>",
    "</div>"].join("")

  settings =
    debug: false
    html: controls
    volume: 10

  onPlayCallback = null
  onPauseCallback = null
  onLoadStartedCallback = null
  onSetItemCallback = null

  init = (element) ->
    player = plyr.setup(element, settings)

    drtPlayerService.player = player[0]

    drtPlayerService.player.on 'loadstart', (event) ->
      $timeout ->
        drtPlayerService._loading = true
        drtPlayerService._playing = false
        drtPlayerService._paused = false
      if onLoadStartedCallback
        onLoadStartedCallback()

    drtPlayerService.player.on 'error', (event) ->

    drtPlayerService.player.on 'play', (event) ->
      $timeout ->
        drtPlayerService.play()

    drtPlayerService.player.on 'playing', (event) ->
      $timeout ->
        drtPlayerService._playing = true
        drtPlayerService._paused = false
        drtPlayerService._loading = false
      if onPlayCallback
        onPlayCallback()

    drtPlayerService.player.on 'pause', (event) ->
      $timeout ->
        drtPlayerService._playing = false
        drtPlayerService._paused = true
        drtPlayerService._loading = false
      if onPauseCallback
        onPauseCallback()

  onSetItem = (callback) ->
    onSetItemCallback = callback

  onLoadStarted = (callback) ->
    onLoadStartedCallback = callback

  onPlay = (callback) ->
    onPlayCallback = callback

  onPause = (callback) ->
    onPauseCallback = callback

  setSource = (item, autoplay) ->
    drtPlayerService._started = autoplay
    drtPlayerService.item = item

    if onSetItemCallback
        onSetItemCallback()

    if autoplay
      _setSource item.title, item.url
      drtPlayerService.player.play()

  _setSource = (title, url) ->
    drtPlayerService.player.source
        type:       'audio'
        title:      title
        sources: [
          src:      url
          type:     'audio/mp3'
        ]

  isPlaying = ->
    drtPlayerService._playing

  play = ->
    if drtPlayerService.item and not drtPlayerService._started
      log 'PLAY STARTED', drtPlayerService.item
      drtPlayerService._started = true
      _setSource drtPlayerService.item.title, drtPlayerService.item.url

    drtPlayerService.player.play()

  pause = ->
    drtPlayerService.player.pause()

  getTrustedUrl = (url) ->
    $sce.trustAsResourceUrl(url)

  drtPlayerService =
    player: null
    isPlaying: isPlaying
    _playing: false
    _paused: false
    _loading: false
    _started: false
    getTrustedUrl: getTrustedUrl
    setSource: setSource
    onPlay: onPlay
    onPause: onPause
    onLoadStarted: onLoadStarted
    onSetItem: onSetItem
    play: play
    pause: pause
    init: init
    item: null

angular.module("drt.player").service "drtPlayerService", drtPlayerService
drtPlayerService.$inject = ["$timeout", "$sce"]

drtPlyrCtrl = ($scope, drtPlayerService) ->
  vm = this
  vm.init = drtPlayerService.init
  return vm

drtPlyrCtrl.$inject = ["$scope", "drtPlayerService"]

drtPlyr = ->
  template: '<audio class="col-6" controls></audio>'
  controller: drtPlyrCtrl
  link: (scope, element, attrs, $ctrl) ->
    $ctrl.init(element)
  replace: true

angular.module("drt.player").directive "drtPlyr", drtPlyr
