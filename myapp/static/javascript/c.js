$('.post-wrapper').slick({
 slidesToShow: 3,
 slidesToScroll:1,
 autoplay:true,
 autoplaySpeed:2000,
 nextArrow:$('.next'),
 prevArrow:$('.prev'),
 nextArrow: $('.next'),
 prevArrow: $('.prev'),
 responsive:[
    {
        breakpoint:1024,
        settings:{
            slidesToshow:3,
            slidesTScroll:3,
            infinite:true,
            dots:true,
        }
    },
    {
        breakpoint:600,
        settings:{
            slidesToShow:2,
            slidesToScroll:2,
        }
    },
    {
        breakpoint:480,
        settings:{
            slidesToShow:1,
            slidesToScroll:1
        }
    }
 ]
});
