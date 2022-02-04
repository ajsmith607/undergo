
This is my personal custom Hugo base theme implemented as a Hugo module. 

My basic approach to creating this theme:

    - I started with the Hugo base theme, which provides complete, but skeletal templates. This was the best starting point I could find for my needs.
    - I further refactored default templates to facilitate finer-grained overriding. I added shortcodes and additional partials as their need arose and tried to make them generalizable. For example, I created my own figure shortcode that links images with their corresponding metadata to display in the figure footer, etc. 
    - I added Javascript and CSS resource bundling. Bundle CSS according to sorted filenames to allow a simple approach to overriding styles on sites where it is used. In this way, I can get an initial site up instantly, and efficiently customize it in a predictable way.
    - Bundled CSS is executed as a Hugo template to allow substitution of values from Hugo site config. 
    - I had initially incorporated SASS preprocessing, but have decided to move to CSS variables and calc() instead. This obviously simplifies the architecture and makes it so the theme doesn't require the Hugo extended version to compile SASS code.

In an attempt to introduce as little CSS as possible in the base theme, and keep the base CSS as clean, logical and disciplined as my limited expertise allows, I made a number of simplifying decisions, some of which include:

    - Use browser default body text size (16px on desktop). (A minimal approach implies only deviating from defaults when absolutely needed.)
    - Use rems for all sizing.
    - Default line height is 150% (1.5 rem) by default, adjust to 1.6 for small screens.
    - Default margin size is 1.5 rem. Margins are defined in one direction.
    - Assume 1 character = 1 rem.
    - Default (essentially, the maximum) line length = 65 rem.
    - There is only one breakpoint, so only two sizes designed for: small screens vs. large screens.
    - Small screen body width is 100%.
    - Large screen max body width is line length + 3 rem (line length and two margins of 1.5 rem). Naturally, this value is sole the breakpoint in the base CSS.


