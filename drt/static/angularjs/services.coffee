StyleService = () ->

  StyleService =
    body: '',
    title: 'Dorm Room Tycoon | DRT.fm'

  return StyleService
angular.module("app.services").service "StyleService", StyleService
StyleService.$inject = []

CategoryService = () ->

  CategoryService =
    selected: null

  CategoryService.select = (cat) ->
    CategoryService.selected = cat

  CategoryService.reset = () ->
    CategoryService.selected =
      name: 'all'
      color: "#388DD5"

  CategoryService.reset()

  return CategoryService
angular.module("app.services").service "CategoryService", CategoryService
CategoryService.$inject = []

secondsToDateTime = ->
  return (seconds) ->
    return new Date(1970, 0, 1).setSeconds(seconds)

angular.module("app.services").filter "secondsToDateTime", secondsToDateTime



anchorSmoothScroll = () ->

  scrollToElement = (eID) ->
    currentYPosition = ->
      # Firefox, Chrome, Opera, Safari
      if self.pageYOffset
        return self.pageYOffset
      # Internet Explorer 6 - standards mode
      if document.documentElement and document.documentElement.scrollTop
        return document.documentElement.scrollTop
      # Internet Explorer 6, 7 and 8
      if document.body.scrollTop
        return document.body.scrollTop
      0

    elmYPosition = (eID) ->
      elm = angular.element(document.querySelector("##{eID}"))
      y = elm.prop('offsetTop')
      node = elm
      while node.prop('offsetParent') and node.prop('offsetParent') != document.body
        node = node.prop('offsetParent')
        y += node.prop('offsetTop')
      y
    `var i`
    startY = currentYPosition()
    elmPosition = elmYPosition(eID)
    stopY = if elmPosition > 80 then elmPosition - 80 else 0
    distance = if stopY > startY then stopY - startY else startY - stopY

    if distance < 100
      scrollTo 0, stopY
      return
    speed = Math.round(distance / 100)
    if speed >= 20
      speed = 20
    step = Math.round(distance / 70)
    leapY = if stopY > startY then startY + step else startY - step
    timer = 0
    if stopY > startY
      i = startY
      while i < stopY
        setTimeout 'window.scrollTo(0, ' + leapY + ')', timer * speed
        leapY += step
        if leapY > stopY
          leapY = stopY
        timer++
        i += step
      return
    i = startY
    while i > stopY
      setTimeout 'window.scrollTo(0, ' + leapY + ')', timer * speed
      leapY -= step
      if leapY < stopY
        leapY = stopY
      timer++
      i -= step

  return scrollToElement


angular.module("app.services").service "anchorSmoothScroll", anchorSmoothScroll
anchorSmoothScroll.$inject = []
