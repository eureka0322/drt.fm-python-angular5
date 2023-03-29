var gulp = require('gulp');
var postcss = require('gulp-postcss');
var autoprefixer = require('gulp-autoprefixer');
var concat = require('gulp-concat');
var rename = require("gulp-rename");
var cleanCSS = require('gulp-clean-css');
var sourcemaps = require('gulp-sourcemaps');

gulp.task('css', function() {
  return gulp.src(['static/css/fonts.css', 'static/vendor/bower_components/plyr/dist/plyr.css', 'static/css/basscss.min.css', 'static/css/styles.css', 'static/css/additional-updates.css'])
  .pipe(postcss([
    require("postcss-cssnext")()
  ]))
  .pipe(autoprefixer())
  .pipe(cleanCSS())
  .pipe(concat('style.min.css'))
  .pipe(gulp.dest('static/dest'));
});

gulp.task('watch', function(){
  gulp.watch('static/css/**/*.css', ['css']);
});
