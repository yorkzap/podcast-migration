<?php

get_header();

$show_default_title = get_post_meta( get_the_ID(), '_et_pb_show_title', true );

$is_page_builder_used = et_pb_is_pagebuilder_used( get_the_ID() );

?>

<div id="main-content">
    <?php
        if ( et_builder_is_product_tour_enabled() ):
            // load fullwidth page in Product Tour mode
            while ( have_posts() ): the_post(); ?>

                <article id="post-<?php the_ID(); ?>" <?php post_class( 'et_pb_post' ); ?>>
                    <div class="entry-content">
                    <?php
                        the_content();
                    ?>
                    </div>

                </article>

        <?php endwhile;
        else:
        ?>
    <div class="container">
        <div id="content-area" class="clearfix">
            <div id="left-area">
            <?php while ( have_posts() ) : the_post(); ?>
                <?php
                /**
                 * Fires before the title and post meta on single posts.
                 *
                 * @since 3.18.8
                 */
                do_action( 'et_before_post' );
                ?>
               <article id="post-<?php the_ID(); ?>" <?php post_class( 'et_pb_post' ); ?>>
					<?php if ( ( 'off' !== $show_default_title && $is_page_builder_used ) || ! $is_page_builder_used ) { ?>
						<?php 
							// Extract the main title (without the episode number)
							$full_title = get_the_title();
							$title_parts = preg_split('/\s*-\s*/', $full_title, 2); 
							$main_title = isset($title_parts[1]) ? $title_parts[1] : $full_title;
							

							// Get the published date
							$published_date = get_the_date();

                            // Get ACF fields
                            $acf_episode_number = get_field('episode');
                            $acf_title = get_field('title');

                            
						?>
						<div class="podcast-banner">
							<div class="nav-button prev-button">
								<!-- SVG for left arrow -->
								<svg viewBox="0 0 24 24" fill="none">
									<path d="M15 6l-6 6 6 6" stroke="#0A1E39" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
								</svg>
							</div>
							<div class="podcast-content">
								<div class="podcast-air-date">Aired on <?php echo esc_html($published_date); ?></div>
								<div class="podcast-episode-number">Episode <?php echo esc_html($acf_episode_number); ?></div>
								<div class="podcast-divider"></div>
								<div class="podcast-series"><?php echo esc_html($acf_title); ?></div>
								<a href="#player" class="podcast-listen-button">Listen Now</a>
							</div>
						
						<div class="podcast-summary">
                            <?php 
                                $podcast_summary = get_field('podcast_summary');
                                if ($podcast_summary) {
                                    echo wp_kses_post($podcast_summary);
                                } else {
                                    echo 'No summary available.'; // You can change this to any default message you prefer
                                }
                            ?>
						</div>
						
							<div class="nav-button next-button">
								<!-- SVG for right arrow -->
								<svg viewBox="0 0 24 24" fill="none">
									<path d="M9 6l6 6-6 6" stroke="#0A1E39" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
								</svg>
							</div>
						</div>


                        <!-- Include Post Body from ACF -->
                        <?php 
                        $post_body = get_field('post_body');
                        if ($post_body) {
                            echo '<div class="post-body-content">';
                            echo wp_kses_post($post_body); // Output the content of the post_body field
                            
                            
                            
                            echo '</div>';
                        }
                        ?>

                        

        

                        <?php
                            if ( ! post_password_required() ) :

                                $thumb = '';

                                $width = (int) apply_filters( 'et_pb_index_blog_image_width', 1080 );

                                $height = (int) apply_filters( 'et_pb_index_blog_image_height', 675 );
                                $classtext = 'et_featured_image';
                                $titletext = get_the_title();
                                $alttext = get_post_meta( get_post_thumbnail_id(), '_wp_attachment_image_alt', true );
                                $thumbnail = get_thumbnail( $width, $height, $classtext, $alttext, $titletext, false, 'Blogimage' );
                                $thumb = $thumbnail["thumb"];

                                $post_format = et_pb_post_format();

                                if ( 'video' === $post_format && false !== ( $first_video = et_get_first_video() ) ) {
                                    printf(
                                        '<div class="et_main_video_container">
                                            %1$s
                                        </div>',
                                        et_core_esc_previously( $first_video )
                                    );
                                } /*else if ( ! in_array( $post_format, array( 'gallery', 'link', 'quote' ) ) && 'on' === et_get_option( 'divi_thumbnails', 'on' ) && '' !== $thumb ) {
                                    print_thumbnail( $thumb, $thumbnail["use_timthumb"], $alttext, $width, $height );
                                } */else if ( 'gallery' === $post_format ) {
                                    et_pb_gallery_images();
                                }
                            ?>

                        <?php
                            $iframe_link = get_field('iframe_link');
                            if ($iframe_link) {
                                echo '<div id="player" class="podcast-player-container">';
                                echo $iframe_link;
                                echo '</div>';
                            }
                        ?>

                            <?php
                                $text_color_class = et_divi_get_post_text_color();

                                $inline_style = et_divi_get_post_bg_inline_style();

                                switch ( $post_format ) {
                                    case 'audio' :
                                        $audio_player = et_pb_get_audio_player();

                                        if ( $audio_player ) {
                                            printf(
                                                '<div class="et_audio_content%1$s"%2$s>
                                                    %3$s
                                                </div>',
                                                esc_attr( $text_color_class ),
                                                et_core_esc_previously( $inline_style ),
                                                et_core_esc_previously( $audio_player )
                                            );
                                        }

                                        break;
                                    case 'quote' :
                                        printf(
                                            '<div class="et_quote_content%2$s"%3$s>
                                                %1$s
                                            </div>',
                                            et_core_esc_previously( et_get_blockquote_in_content() ),
                                            esc_attr( $text_color_class ),
                                            et_core_esc_previously( $inline_style )
                                        );

                                        break;
                                    case 'link' :
                                        printf(
                                            '<div class="et_link_content%3$s"%4$s>
                                                <a href="%1$s" class="et_link_main_url">%2$s</a>
                                            </div>',
                                            esc_url( et_get_link_url() ),
                                            esc_html( et_get_link_url() ),
                                            esc_attr( $text_color_class ),
                                            et_core_esc_previously( $inline_style )
                                        );

                                        break;
                                }

                            endif;
                        ?>
                        </div>
                    <?php  } ?>

                    <div class="entry-content">
                    <?php
                        do_action( 'et_before_content' );

                        the_content();

                        wp_link_pages( array( 'before' => '<div class="page-links">' . esc_html__( 'Pages:', 'Divi' ), 'after' => '</div>' ) );
                    ?>
                    </div>
                    <div class="et_post_meta_wrapper">
                    <?php
                    if ( et_get_option('divi_468_enable') === 'on' ){
                        echo '<div class="et-single-post-ad">';
                        if ( et_get_option('divi_468_adsense') !== '' ) echo et_core_intentionally_unescaped( et_core_fix_unclosed_html_tags( et_get_option('divi_468_adsense') ), 'html' );
                        else { ?>
                            <a href="<?php echo esc_url(et_get_option('divi_468_url')); ?>"><img src="<?php echo esc_attr(et_get_option('divi_468_image')); ?>" alt="468" class="foursixeight" /></a>
                <?php   }
                        echo '</div>';
                    }

                    /**
                     * Fires after the post content on single posts.
                     *
                     * @since 3.18.8
                     */
                    do_action( 'et_after_post' );

					/*
                        if ( ( comments_open() || get_comments_number() ) && 'on' === et_get_option( 'divi_show_postcomments', 'on' ) ) {
                            comments_template( '', true );
                        }
					*/



                    ?>
                    </div>
                </article>

            <?php endwhile; ?>
            </div> 

            <?php get_sidebar(); ?>
        </div>
    </div>
    <?php endif; ?>
</div>

<?php

get_footer();
