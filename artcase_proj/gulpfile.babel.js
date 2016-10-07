'use strict'

import gulp from 'gulp'
import watchify from 'watchify'
import browserify from 'browserify'
import gutil from 'gulp-util'
import sass from 'gulp-sass'
import jshint from 'gulp-jshint'
import riot from 'gulp-riot'
import rename from 'gulp-rename'


//
// config
//

var apps = ['core', 'artcase']

var custom_browserify_options = {
    entries: ['./core/src/core/base.js'],
    debug: true
}
var o = Object.assign({}, watchify.args, custom_browserify_options)
var b = watchify(browserify(o))


//
// tasks
//

gulp.task('watch', () => {
    gulp.watch('./**/*.scss', ['css'])
    gulp.watch('./**/*.js',   ['js'])
    gulp.watch('./**/*.tag',  ['components'])
})

gulp.task('css', () => {
    // each app: parallel src/*.scss & static/*.css
    apps.forEach(function(app_name) {
        var src  = './'+ app_name +'/src/**/*.scss',
            dest = './'+ app_name +'/static/'
        gulp.src(src)
            .pipe(sass())
            .pipe(gulp.dest(dest))
    })
})

gulp.task('js', () => {
    // each app: parallel src/*.js & static/*.js
    apps.forEach(function(app_name) {
        var src  = './'+ app_name +'/src/**/*.js',
            dest = './'+ app_name +'/static/'
        gulp.src(src)
            .pipe(jshint({asi: true}))
            .pipe(jshint.reporter('jshint-stylish'))
            .pipe(jshint.reporter('jshint-stylish'))
            .pipe(gulp.dest(dest))
    })
})

gulp.task('components', () => {
    // each app: parallel riot components
    apps.forEach(function(app_name) {
        var src  = './'+ app_name +'/src/**/*.tag',
            dest = './'+ app_name +'/static/'
        gulp.src(src)
            .pipe(riot())
            .pipe(rename(function (path) {
                path.extname = ".tag.js"
            }))
            .pipe(gulp.dest(dest))
    })
})