function myFunc(vars) {
  return vars;
}

// Mobile menu toggle
$(document).ready(function() {
  $(".navTrigger").click(function () {
    $(this).toggleClass("active");
    $("#mainListDiv").toggleClass("show_list");
  });

  // Close mobile menu when a nav link is clicked
  $(".navlinks a").click(function() {
    if ($(window).width() <= 768) {
      $(".navTrigger").removeClass("active");
      $("#mainListDiv").removeClass("show_list");
    }
  });
});
