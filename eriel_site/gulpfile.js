'use strict';

/* PACKAGES */
var gulp = require('gulp');
var gulp_war = require('gulp-war');
var gulp_zip = require('gulp-zip');


gulp.task('war', function () {
    gulp.src([
                '**/**/*'
            ])
        .pipe(gulp_war({
            welcome: 'index.html',
            displayName: 'eriel',
        }))
        .pipe(gulp_zip('databucker-website.war'))
        .pipe(gulp.dest("./"));
});