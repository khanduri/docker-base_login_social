'use strict';


var gulp = require('gulp'),
    size = require('gulp-size'),
    react = require('gulp-react'),
    concat = require('gulp-concat'),
    clean = require('gulp-clean'),
    uglify = require('gulp-uglify'),
    sass = require('gulp-sass');


// Tasks
gulp.task('default', function(){
  gulp.start('transform');
  gulp.watch('static/styles/scss/*.scss', ['sass']);
  gulp.watch('static/scripts/jsx/*.jsx', ['transform']);
});

gulp.task('build', ['clean', 'sass'], function(){
  return gulp.src('static/scripts/jsx/*.jsx')
    .pipe(react({harmony: false,}))
    .pipe(uglify())
    .pipe(concat('main.js'))
    .pipe(gulp.dest('static/scripts/js/compiled'))
    .pipe(size());
});

gulp.task('transform', ['clean'], function(){
  return gulp.src('static/scripts/jsx/*.jsx')
    .pipe(react({harmony: false,}))
    .pipe(concat('main.js'))
    .pipe(gulp.dest('static/scripts/js'))
    .pipe(size());
});

gulp.task('clean', function(){
  return gulp.src(['static/scripts/js'], {read: false})
    .pipe(clean());
});

gulp.task('sass', function () {
  return gulp.src('static/styles/scss/main.scss')
    .pipe(sass.sync().on('error', sass.logError))
    .pipe(gulp.dest('static/styles/css'));
});
