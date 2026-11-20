source: client-work (own site CI)

SEO checks CI failed on ubuntu-latest: "An error occurred while installing commonmarker (0.23.11), and Bundler
cannot continue." Comes from github-pages 228 -> jekyll-commonmark-ghpages -> jekyll-commonmark -> commonmarker.
Compile errors: unknown type name 'bool' in Ruby's own headers. Worked locally in the ruby:3.2 Docker image.
Moved the job into container: ruby:3.2-trixie and it passed. Why only on ubuntu-latest? Ran a matrix:
26.04/Ruby 3.2 fail, 26.04/Ruby 3.3 ok, 24.04/Ruby 3.2 ok (run 44744308438). GCC 15 defaults to C23.
Anyone with a Jekyll/GitHub Pages site and their own Actions build will hit this.
