var gulp = require("gulp");
var less = require("gulp-less");
var concat = require("gulp-concat");
var uglify = require("gulp-uglify");
var plumber = require("gulp-plumber");
var minifycss = require("gulp-cssnano");
var gutil = require("gulp-util");
var PRODUCTION = gutil.env.production || process.env.NODE_ENV == "production";

var STATIC_SRC_PATH = "asylum/static_src/";
var STATIC_DEST_PATH = "asylum/static/";
var BOWER_PATH = "bower_components/"

gulp.task("less", function() {
    return gulp.src([
        STATIC_SRC_PATH + "less/style.less"
    ])
        .pipe(plumber({}))
        .pipe(less().on("error", function(err) {
            console.log(err.message);
            this.emit("end");
        }))
        .pipe(concat("asylum.css"))
        .pipe((PRODUCTION ? minifycss() : gutil.noop()))
        .pipe(gulp.dest(STATIC_DEST_PATH + "css/"));
});

gulp.task("less:watch", ["less"], function() {
    gulp.watch([STATIC_SRC_PATH + "less/**/*.less"], ["less"]);
});

gulp.task("js", function() {
    return gulp.src([
        BOWER_PATH + "jquery/dist/jquery.min.js",
        BOWER_PATH + "bootstrap/dist/js/bootstrap.min.js",
        STATIC_SRC_PATH + "js/asylum.js",
    ])
        .pipe(plumber({}))
        .pipe(concat("asylum.js"))
        .pipe((PRODUCTION ? uglify() : gutil.noop()))
        .pipe(gulp.dest(STATIC_DEST_PATH + "js/"));
});

gulp.task("js:watch", ["js"], function() {
    gulp.watch([STATIC_SRC_PATH + "js/**/*.js"], ["js"]);
});

gulp.task("copy_fonts", function() {
    return gulp.src([
        BOWER_PATH + "font-awesome/fonts/*"
    ]).pipe(gulp.dest(STATIC_DEST_PATH + "fonts/"));
});

gulp.task("default", ["js", "less", "copy_fonts"]);

gulp.task("watch", ["js:watch", "less:watch"]);
