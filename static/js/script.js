/*
  * @package Bizcraft
  * @subpackage Bizcraft HTML
  * 
  * Template Scripts
  * Created by Tripples
  
   1.    Style Switcher
   2.    Navigation
   3.    Fixed Header
   4.    Main Slideshow (Carousel)
   5.    Counter
   6.    Owl Carousel
   7.    Flex Slider
   8.    Wow Animation
   10.   Video Background
   11.   Back To Top

  
*/


jQuery(function ($) {
  'use strict';


  /* ----------------------------------------------------------- */
  /*  Style Switcher
  /* ----------------------------------------------------------- */
    $(document).ready(function () {
      $('.style-switch-button').click(function () {
        $('.style-switch-wrapper').toggleClass('active');
      });
      $('a.close-styler').click(function () {
        $('.style-switch-wrapper').removeClass('active');
      });
    });



  /* ----------------------------------------------------------- */
  /*  Fixed header
  /* ----------------------------------------------------------- */

  $(window).on('scroll', function () {

    if ($(window).scrollTop() > 100) {

      $('.header').addClass('header-solid animated fadeInDown');
    } else {

      $('.header').removeClass('header-solid animated fadeInDown');

    }

  });

  $(window).on('scroll', function () {

    if ($(window).scrollTop() > 200) {

      $('.header2').addClass('header-bgnone animated fadeInDown');
    } else {

      $('.header2').removeClass('header-bgnone animated fadeInDown');

    }

  });



  /* ----------------------------------------------------------- */
  /*  Main slideshow
  /* ----------------------------------------------------------- */

  /* Home 2 */

  $('.flexSlideshow').flexslider({
    slideshowSpeed: 5000,
    animationSpeed: 600
  });

  /* Home 3 and 4 */

  $('#main-slide').carousel({
    pause: true,
    interval: 100000
  });


  /* ----------------------------------------------------------- */
  /*  Counter
  /* ----------------------------------------------------------- */

  $('.counter').counterUp({
    delay: 10,
    time: 1000
  });



  /* ----------------------------------------------------------- */
  /*  Owl Carousel
  /* ----------------------------------------------------------- */


  //Testimonial

  $('#testimonial-carousel').owlCarousel({

    navigation: false, // Show next and prev buttons
    slideSpeed: 600,
    pagination: true,
    singleItem: true

  });

  // Custom Navigation Events
  var owl = $('#testimonial-carousel');


  // Custom Navigation Events
  $('.next').click(function () {
    owl.trigger('owl.next');
  });
  $('.prev').click(function () {
    owl.trigger('owl.prev');
  });
  $('.play').click(function () {
    owl.trigger('owl.play', 1000); //owl.play event accept autoPlay speed as second parameter
  });
  $('.stop').click(function () {
    owl.trigger('owl.stop');
  });


  //Clients

  $('#client-carousel').owlCarousel({

    navigation: false, // Show next and prev buttons
    slideSpeed: 400,
    pagination: false,
    items: 5,
    rewindNav: true,
    itemsDesktop: [1199, 3],
    itemsDesktopSmall: [979, 3],
    stopOnHover: true,
    autoPlay: true

  });

  //App gallery
  $('#app-gallery-carousel').owlCarousel({

    navigation: false, // Show next and prev buttons
    slideSpeed: 400,
    pagination: true,
    items: 4,
    rewindNav: true,
    itemsDesktop: [1199, 3],
    itemsDesktopSmall: [979, 3],
    stopOnHover: true
  });



  /* ----------------------------------------------------------- */
  /*  Flex slider
  /* ----------------------------------------------------------- */

  //Second item slider
  $(window).load(function () {
    $('.flexSlideshow').flexslider({
      animation: 'fade',
      controlNav: false,
      directionNav: true,
      slideshowSpeed: 8000
    });
  });


  //Portfolio item slider
  $(window).load(function () {
    $('.flexportfolio').flexslider({
      animation: 'fade',
      controlNav: false,
      directionNav: true,
      slideshowSpeed: 8000
    });
  });


  /* ----------------------------------------------------------- */
  /*  Animation
  /* ----------------------------------------------------------- */
  //Wow
  new WOW().init();


  /* ----------------------------------------------------------- */
  /*  Prettyphoto
  /* ----------------------------------------------------------- */

  $('a[data-rel^=\'prettyPhoto\']').prettyPhoto();


  /* ----------------------------------------------------------- */
  /* Video background
  /* ----------------------------------------------------------- */

  var resizeVideoBackground = function () {

    $('.video-background').each(function (i, el) {
      var $el = $(el),
        $section = $el.parent(),
        min_w = 300,
        video_w = 16,
        video_h = 9,
        section_w = $section.outerWidth(),
        section_h = $section.outerHeight(),
        scale_w = section_w / video_w,
        scale_h = section_h / video_h,
        scale = scale_w > scale_h ? scale_w : scale_h,
        new_video_w, new_video_h, offet_top, offet_left;


      if (scale * video_w < min_w) {
        scale = min_w / video_w;
      }

      new_video_w = scale * video_w;
      new_video_h = scale * video_h;
      offet_left = (new_video_w - section_w) / 2 * -1;
      offet_top = (new_video_h - section_h) / 2 * -1;

      $el.css('width', new_video_w);
      $el.css('height', new_video_h);
      $el.css('marginTop', offet_top);
      $el.css('marginLeft', offet_left);
    });

  };

  $(window).on('resize', function () {
    resizeVideoBackground();
  });

  resizeVideoBackground();
  
  body {font-family: Arial, Helvetica, sans-serif;}
* {box-sizing: border-box;}

/* Full-width input fields */
input[type=text], input[type=password] {
  width: 100%;
  padding: 15px;
  margin: 5px 0 22px 0;
  display: inline-block;
  border: none;
  background: #f1f1f1;
}

/* Add a background color when the inputs get focus */
input[type=text]:focus, input[type=password]:focus {
  background-color: #ddd;
  outline: none;
}

/* Set a style for all buttons */
button {
  background-color: #4CAF50;
  color: white;
  padding: 14px 20px;
  margin: 8px 0;
  border: none;
  cursor: pointer;
  width: 100%;
  opacity: 0.9;
}

button:hover {
  opacity:1;
}

/* Extra styles for the cancel button */
.cancelbtn {
  padding: 14px 20px;
  background-color: #f44336;
}

/* Float cancel and signup buttons and add an equal width */
.cancelbtn, .signupbtn {
  float: left;
  width: 50%;
}

/* Add padding to container elements */
.container {
  padding: 16px;
}

/* The Modal (background) */
.modal {
  display: none; /* Hidden by default */
  position: fixed; /* Stay in place */
  z-index: 1; /* Sit on top */
  left: 0;
  top: 0;
  width: 100%; /* Full width */
  height: 100%; /* Full height */
  overflow: auto; /* Enable scroll if needed */
  background-color: #474e5d;
  padding-top: 50px;
}

/* Modal Content/Box */
.modal-content {
  background-color: #fefefe;
  margin: 5% auto 15% auto; /* 5% from the top, 15% from the bottom and centered */
  border: 1px solid #888;
  width: 80%; /* Could be more or less, depending on screen size */
}

/* Style the horizontal ruler */
hr {
  border: 1px solid #f1f1f1;
  margin-bottom: 25px;
}
 
/* The Close Button (x) */
.close {
  position: absolute;
  right: 35px;
  top: 15px;
  font-size: 40px;
  font-weight: bold;
  color: #f1f1f1;
}

.close:hover,
.close:focus {
  color: #f44336;
  cursor: pointer;
}

/* Clear floats */
.clearfix::after {
  content: "";
  clear: both;
  display: table;
}

/* Change styles for cancel button and signup button on extra small screens */
@media screen and (max-width: 300px) {
  .cancelbtn, .signupbtn {
     width: 100%;
  }
}

  /* ----------------------------------------------------------- */
  /*  Back to top
  /* ----------------------------------------------------------- */

  $(window).scroll(function () {
    if ($(this).scrollTop() > 50) {
      $('#back-to-top').fadeIn();
    } else {
      $('#back-to-top').fadeOut();
    }
  });
  // scroll body to 0px on click
  $('#back-to-top').click(function () {
    $('#back-to-top').tooltip('hide');
    $('body,html').animate({
      scrollTop: 0
    }, 800);
    return false;
  });

  $('#back-to-top').tooltip('hide');

});