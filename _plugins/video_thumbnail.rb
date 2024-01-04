require 'fileutils'

require 'streamio-ffmpeg'

module Jekyll
  module VideoThumbnailFilter
    def video_thumbnail(path)
      site = @context.registers[:site]
      cacheRoot = File.join(site.source, ".jekyll-cache", "video_thumbnail")

      video = FFMPEG::Movie.new(path)

      destination_rel = File.join("thumbnails", File.dirname(path), File.basename(path, File.extname(path)) + ".png")
      destination_abs = File.join(cacheRoot, destination_rel)
      destination_rel = destination_rel.prepend('/')
      if not site.static_files.find{|file| file.path == destination_abs}
        site.static_files << StaticFile.new(site, cacheRoot, File.dirname(destination_rel), File.basename(destination_rel))
      end

      if not File.exist?(destination_abs) or File.mtime(path) > File.mtime(destination_abs)
        FileUtils.mkdir_p(File.dirname(destination_abs))
        video.screenshot(destination_abs)
      end

      return destination_rel
    end
  end
end

Liquid::Template.register_filter(Jekyll::VideoThumbnailFilter)
