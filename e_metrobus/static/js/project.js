/* Project specific Javascript goes here. */

// Animate onboarding part

// hide route and start yellow circle animation
setTimeout(function() {
  $('#onboardingAnimateRoute').hide();
  $('#onboardingAnimateBackground').show();
  $('#onboardingAnimateText1').show();
}, 2000);

setTimeout(function() {
  $('#onboardingAnimateText1').hide();
  $('#onboardingAnimateText2').show();
}, 4000);

setTimeout(function() {
  $('#onboardingAnimateText2').hide();
  $('#onboardingAnimateText3').show();
}, 6000);

setTimeout(function() {
  $('#onboardingAnimateText3').hide();
  $('#onboardingAnimateText4').show();
}, 8000);

// finish yellow circle animation
setTimeout(function() {
  $('#onboardingAnimateBackground').hide();
  $('#onboardingAnimateText4').hide();
  $('#onboardingAnimateChart').show();
  console.log('hey');
}, 10000);