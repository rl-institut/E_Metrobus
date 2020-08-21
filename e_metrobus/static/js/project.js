/* Project specific Javascript goes here. */

// Plugin @RokoCB :: Return the visible amount of px
// of any element currently in viewport.
// stackoverflow.com/questions/24768795/

// display elements on scroll on tablet/desktop
;(function($, win) {
  $.fn.inViewport = function(cb) {
    return this.each(function(i,el){
      function visPx(){
        var H = $(this).height(),
          r = el.getBoundingClientRect(), t=r.top, b=r.bottom;
        return cb.call(el, Math.max(0, t>0? H-t : (b<H?b:H)));  
      } visPx();
      $(win).on("resize scroll", visPx);
    });
  };
}(jQuery, window));

$(".animate-desktop").inViewport(function(px){
  // sure to target only devices that are above 640px width
  // otherwise smaller tablets don't display all elements from landing page after loading
    if(px && $(window).width() > 640) {
      $(this).addClass("triggeredCSS3");
    }
});