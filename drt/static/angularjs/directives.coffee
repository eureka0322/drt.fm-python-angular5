angular.module("app.directives").directive "tiltHover", () ->
  restrict: 'A',
  link: (scope, element) ->
    VanillaTilt.init element[0],
      max: 10,
      speed: 700
