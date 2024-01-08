require 'fileutils'

require 'mini_magick'

module Jekyll
  module ImageSrcsetFilter
    def _generate_filename_for_ratio_width(originalPath, ratio, baseWidth)
      File.join("srcset", File.dirname(originalPath), "#{File.basename(originalPath, File.extname(originalPath))}-#{(ratio * baseWidth).round()}w#{File.extname(originalPath)}")
    end

    def image_srcset_width(path, width)
      site = @context.registers[:site]
      cacheRoot = File.join(site.source, ".jekyll-cache", "image_srcset")

      path_prefixed = path.start_with?('/') ? path : ('/' + path)
      path_abs = site.static_files.find{|file| file.relative_path == path_prefixed }.path
      image = MiniMagick::Image.open(path_abs)
      originalWidth = image.width
      originalHeight = image.height

      neededRatios = []
      # 2^-2 = 0.25 2^2 = 4
      -2.step(by: 0.5, to: 2) { |i|
        ratio = 2**i
        # don't scale up, don't make lots of tiny files
        if ratio * width <= originalWidth && ratio * width >= 150
          neededRatios << ratio
        end
      }

      neededRatios.each { |ratio|
        image = MiniMagick::Image.open(path_abs)

        destination_rel = _generate_filename_for_ratio_width(path, ratio, width)
        destination_abs = File.join(cacheRoot, destination_rel)
        destination_rel = destination_rel.prepend('/')
        if not site.static_files.find{|file| file.path == destination_abs}
          site.static_files << StaticFile.new(site, cacheRoot, File.dirname(destination_rel), File.basename(destination_rel))
        end

        if not File.exist?(destination_abs) or File.mtime(path_abs) > File.mtime(destination_abs)
          FileUtils.mkdir_p(File.dirname(destination_abs))
          image.resize "#{(width * ratio).round()}x#{(width * originalHeight * ratio / originalHeight).round()}"
          image.write destination_abs
        end
      }

      srcset = []
      neededRatios.each { |ratio|
        srcset << Liquid::Template.parse("{% link #{_generate_filename_for_ratio_width(path, ratio, width)} %} #{ratio.round(3)}x").render(@context)
      }
      return "srcset=\"#{srcset.join(", ")}\""
    end
  end
end

Liquid::Template.register_filter(Jekyll::ImageSrcsetFilter)
