
function init_stars() {
  select_stars($(".feedback__quest--stars"), 0);
}

function star_hovered(star) {
  let rating = $(star).data("rating");
  select_stars($(star).parent(), rating);
};

function star_unhovered(star) {
  let rating = $(star).parent().find("#star_input").val();
  select_stars($(star).parent(), rating);
};

function star_clicked(star) {
  let rating = $(star).data("rating");
  $(star).parent().find("#star_input").val(rating);
}

function select_stars(stars, rating) {
  if (rating == 0) {
    rating = stars.find("#star_input").val();
  }
  stars.children("svg").each(function(i, svg) {
     if ($(svg).data("rating") <= rating) {
        $(svg).find("path").css("fill", "green");
     } else {
        $(svg).find("path").css("fill", "blue");
     }
  });
}

init_stars();
