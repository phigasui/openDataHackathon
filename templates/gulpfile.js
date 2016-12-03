var gulp = require('gulp');
var sass = require('gulp-sass');
 
 
// Sassコンパイルタスク
gulp.task("sass", function() {
    gulp.src("sass/**/*scss")
        .pipe(sass())
        .pipe(gulp.dest("./css"));
});

gulp.task("default", function() {
    gulp.watch("sass/**/*.scss",["sass"]);
});
 