# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project tries to adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

### Added
- added ellpsis/nowrap to tabs

### Changed
- increased small button height
- highlicht "smartphones" on desktop LP instead of URL
- changed to heart BVG logo
- updated desktop LP text and images
- changed on scroll animations (desktop LP) to automatic animations for smaller screens
- hid flag on small/landscape views on summary page

## [0.18.0] - 2020-07-29
### Added
- added scroll animation to desktop LP

### Changed
- removed bottom space from multiple choice layout
- reduced vertical margins on share reveal for smaller screens
- updated image on route page
- remove upper part from summary page
- update wording
- switch buttons order on my route page

### Fixed
- removed CSS for lanscape mobile from desktop LP CSS
- adjusted LP for tablet screens

## [0.17.1] - 2020-07-17
### Fixed
- blocktrans error on environment page

## [0.17.0] - 2020-07-17
### Changed
- bus fleet distance is calculated dynamically from project start

## [0.16.0] - 2020-07-15
### Added
- answered questions of finished category can be re-seen

### Changed
- merged landscape view into portrait view
- app checks for mobile/desktop view and shows only related parts
- major redesign of answer page (question form is shown with correct/wrong answers)

### Fixed
- share links

## [0.15.0] - 2020-07-13
### Added 
- slogan to finished and share link
- imprint and privacy infos on desktop and legal page

### Changed
- changing route from environment returns to environment page

### Fixed
- server errors due to missing/wrong image sources
- soft keyboard activating landscape view
 
## [0.14.0] - 2020-07-06
### Added
- new questions for all categories
- feedback form on landing page
- posthog for anonymous session tracking
- landing page and default route for non-bus-users
- implemented flashes at finished page
- finished quiz includes link back to dashboard 
- titles and alternative texts to minder barriers

### Changed 
- link (to welcome page) and text for sharing the app
- redesigned landing page
- comparison chart is loaded dynamically (ajax)
- Implemented tabs on summary page
- Replaced progress bar on question page with flashes
- environment/my_route page to show comparison charts

## [0.13.0] - 2020-06-29
### Changed
- Removed answer score page; correct/wrong answer is showed on answer page
- welcome tour design (added animation)
- moved feedback and bug report to legal page
- dashboard circles to flashes

## [0.12.0] - 2020-06-26
### Added
- BMWI and NOW logo to landing page (desktop & mobile)

## [0.11.0] - 2020-06-17
### Added
- bug reports can be send
- single page tour after comparison page
- privacy policy banner on landing page

### Changed 
- progress bar/cirle shows correct and wrong answers
- added share link on navigation bar
- used tabs in favor of accordion on questions-as-text page
- footer icons and added labels
- legal page uses tabs
 
## [0.10.0] - 2020-06-09
### Added
- Data for E-PKW
- e-Bus favicon
- CO2 in gram on display route page

### Fixed
- Answer shows up shortly before answer score animation

## [0.9.0] - 2020-05-19
### Added 
- social media links

### Changed
- comparison chart is static (no zoom possible)
- new icons and colors for comparison chart
- enabled route dropdown as default route
- landing page screenshot

### Fixed
- questions as text page
- environment page redirects to stations if not yet selected
- accordion on question_as_text page
- body height too tall on android browser

## [0.8.0] - 2020-05-12
### Added
- feedback page
- data tables

### Changed
- first question is answered after display route
- if third station is selected, selection is undone
- on landing page, switching language skips fade-in

## [0.7.0] - 2020-04-09
### Added 
- real station data
- icons and images to landing page

### Changed
- timed display route to carousel
- Departure station can be changed
- category icons to filled and line icons
- Answer animation can be skipped

### Fixed
- First dashboard popup layout

## [0.6.0] - 2020-02-19
### Added
- Environment page.
- english language support
- Score can be saved and shared via link.
- Score animation on dashboard.

### Changed
- leaf footer links
- onboard animation speed (slowed down)
- answer page layout fixed
- dashboard icons
- trophy icons
- removed back arrow on dashboard

## [0.5.0] - 2020-02-05
### Added
- Legal page

## [0.4.0] - 2020-02-05
### Changed 
- Landing page holds project information
- Footer links for display_route and comparison page

## [0.3.0] - 2020-02-05
### Added
- Category finished page.
- Score animation when answering a question.
- "Choose your route" text.
- Popup at first-time-visit on dashboard.

### Changed
- Color variables (BVG original)

## [0.2.0] - 2020-01-13
### Added
- Right/wrong animation.
- Layout for answers.
- First tests.

### Changed
- Landing page layout.

### Fixed
- Docker compose files to adapt right network.
- Chart icons to avoid blurring.

## [0.1.0] - 2019-12-10
- First beta-release deployed on server via docker.
