var gulp  = require('gulp'),
    gutil = require('gulp-util'),
    sass  = require('gulp-sass'),
    jshint = require('gulp-jshint')

var apps = ['core', 'artcase']

gulp.task('watch', function() {
    gulp.watch('./**/*.scss', ['build_css'])
    gulp.watch('./**/*.js',   ['build_js'])
})

gulp.task('build_css', function() {
    // each app: parallel src/*.scss & static/*.css
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

gulp.task('build_js', function() {
    // each app: parallel src/*.js & static/*.js
    apps.forEach(function(app_name) {
        var src  = './'+ app_name +'/src/**/*.js',
            dest = './'+ app_name +'/static/'
        build(src, dest)
    })

    function build(src, dest) {
        return gulp.src(src)
        .pipe(jshint({asi: true}))
        .pipe(jshint.reporter('jshint-stylish'))
        .pipe(gulp.dest(dest))
    } 
})