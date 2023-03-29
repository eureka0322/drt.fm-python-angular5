from django_assets import Bundle, register

components = Bundle(
    'underscore/underscore.js',
    # 'angular/angular.js',
    # 'angular-sanitize/angular-sanitize.js',
    # 'angular-resource/angular-resource.js',
    # 'angular-animate/angular-animate.js',
    'restangular/dist/restangular.js',
    'angular-ui-router/release/angular-ui-router.js',
    'angular-ui-router/release/stateEvents.js',
    'angular-cookies/angular-cookies.js',
    'angular-svg-base-fix/src/svgBaseFix.js',
    'ngInfiniteScroll/build/ng-infinite-scroll.js',
    'vanilla-tilt.js/dist/vanilla-tilt.min.js',
    'ngtweet/dist/ngtweet.js',
    'slick-carousel/slick/slick.js',
    'angular-slick-carousel/dist/angular-slick.js',
    'plyr/src/js/plyr.js',
    output='gen/components.js', filters='jsmin')
register('components', components)

app = Bundle(
    'angularjs/app.coffee',
    'angularjs/config.coffee',
    'angularjs/routes.coffee',
    'angularjs/services.coffee',
    'angularjs/drt.player.coffee',
    'angularjs/controllers.coffee',
    'angularjs/directives.coffee',
    output='gen/app.js', filters='coffeescript, jsmin')
register('app', app)

index = Bundle(
    'angularjs/index/app.coffee',
    'angularjs/index/routes.coffee',
    'angularjs/index/models.coffee',
    'angularjs/index/controllers.coffee',
    'angularjs/index/posts.factory.coffee',
    'angularjs/index/jobs.factory.coffee',
    output='gen/index.js', filters='coffeescript, jsmin')
register('index', index)
