// Hive Omnix System
// Copyright (c) 2008-2015 Hive Solutions Lda.
//
// This file is part of Hive Omnix System.
//
// Hive Omnix System is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// Hive Omnix System is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with Hive Omnix System. If not, see <http://www.gnu.org/licenses/>.

// __author__    = João Magalhães <joamag@hive.pt>
// __version__   = 1.0.0
// __revision__  = $LastChangedRevision$
// __date__      = $LastChangedDate$
// __copyright__ = Copyright (c) 2008-2015 Hive Solutions Lda.
// __license__   = GNU General Public License (GPL), Version 3

(function(jQuery) {
    jQuery.fn.uapply = function(options) {
        // sets the jquery matched object
        var matchedObject = this;

        // retrieves the reference to the media preview object
        // so that the proper plugin is registered
        var mediaPreview = jQuery(".media-preview", matchedObject);
        mediaPreview.umediapreview();

        // returns the current context to the caller method so that
        // it may be used for chained operations
        return this;
    };
})(jQuery);

(function(jQuery) {
    jQuery.fn.umediapreview = function(options) {
        var matchedObject = this;
        var objectId = jQuery(".text-field[name=object_id]", matchedObject);
        var previewPanel = jQuery(".preview-panel", matchedObject);

        previewPanel.hide();

        objectId.bind("value_change", function() {
            var element = jQuery(this);
            var form = element.parents("form");
            var mediaPreview = element.parents(".media-preview");
            var previewPanel = jQuery(".preview-panel", mediaPreview);
            var mediaTarget = jQuery(".media-target", previewPanel);
            var classInput = jQuery("input[name=class]", mediaPreview);
            var representationInput = jQuery("input[name=representation]",
                    mediaPreview);
            var url = form.attr("action");
            var mediaUrl = form.attr("data-media");
            var value = element.uxvalue();
            previewPanel.hide();
            mediaTarget.empty();
            jQuery.ajax({
                url : url,
                type : "post",
                data : {
                    object_id : value
                },
                success : function(data) {
                    var media = data.media;
                    for (var index = 0; index < media.length; index++) {
                        var item = media[index];
                        var itemUrl = mediaUrl + String(item.object_id);
                        var imageContainer = jQuery("<div class=\"image-container\"></div>");
                        var imageLink = jQuery("<a href=\"" + itemUrl + "\"></a>");
                        var image = jQuery("<img src=\"" + item.image_url
                                + "\" />");
                        var title = jQuery("<h2>" + item.label + "</h2>");
                        var subTitle = jQuery("<h3>"
                                + (item.dimensions || "unset") + "</h3>");
                        imageLink.append(image);
                        imageLink.append(title);
                        imageLink.append(subTitle);
                        imageContainer.append(imageLink);
                        mediaTarget.append(imageContainer);
                    }
                    classInput.val(data._class);
                    representationInput.val(data.representation);
                    previewPanel.show();
                }
            });
        });

        return this;
    };
})(jQuery);

jQuery(document).ready(function() {
            var _body = jQuery("body");
            _body.bind("applied", function(event, base) {
                        base.uapply();
                    });
        });
