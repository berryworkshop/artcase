/* File: gulpfile.js */

// grab our gulp packages
var gulp  = require('gulp'),
    gutil = require('gulp-util'),
    sass   = require('gulp-sass')

gulp.task('default', function() {
  return gutil.log('Gulp functional.')
})

gulp.task('watch', function() {
    gulp.watch('./**/*.scss', ['build_css'])
})

gulp.task('build_css', function() {
    var apps = ['core', 'artcase']

    apps.forEach(function(app_name) {
        var src  = './'+ app_name +'/src/**/*.scss',
            dest = './'+ app_name +'/static/'
        build(src, dest)
    })

    function build(src, dest) {
        return gulp.src(src)
            .pipe(sass())
            .pipe(gulp.dest(dest))
    } 
})