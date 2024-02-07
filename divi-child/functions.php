<?php
add_action( 'wp_enqueue_scripts', 'divi_child_enqueue_styles' );
function divi_child_enqueue_styles() {
    wp_enqueue_style( 'parent-style', get_template_directory_uri() . '/style.css' );
}


// Remove meta information such as post publish date and comment count
function remove_post_meta_from_content($content) {
    if (is_single() && 'post' == get_post_type()) {
        // Using regex to remove the post meta pattern
        $content = preg_replace('/<p class="post-meta">.*?<\/p>/', '', $content);
    }
    return $content;
}

add_filter('the_content', 'remove_post_meta_from_content');
