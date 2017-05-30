/**
 * Created by Admin on 5/9/2017.
 */
//$(function () {

    var findOne = function (haystack, arr) {
        return arr.some(function (v) {
            return haystack.indexOf(v) >= 0;
        });
    };

    var anyMatchInArray = function (target, toMatch) {
        var found, targetMap, i, j, cur;
        "use strict";

        found = false;
        targetMap = {};

        // Put all values in the `target` array into a map, where
        //  the keys are the values from the array
        for (i = 0, j = target.length; i < j; i++) {
            cur = target[i];
            targetMap[cur] = true;
        }

        // Loop over all items in the `toMatch` array and see if any of
        //  their values are in the map from before
        for (i = 0, j = toMatch.length; !found && (i < j); i++) {
            cur = toMatch[i];
            found = !!targetMap[cur];
            // If found, `targetMap[cur]` will return true, otherwise it
            //  will return `undefined`...that's what the `!!` is for
        }

        return found;
    };

    var getFields = function (input, field) {
        var output = [];
            for (var i=0; i < input.length ; ++i)
                output.push(input[i][field]);
        return output;
    };

/**************************
 * Check if an element has a class
 **************************/
function hasClass (el, name) {
    return (' ' + el.className + ' ').indexOf(' ' + name + ' ') > -1;
}


/**************************
 * Find parent element
 **************************/
function findParent(el, className) {
    var parentNode = el.parentNode;
    while (hasClass(parentNode, className) === false) {
        if (parentNode.parentNode === undefined) {
            return null;
        }
        parentNode = parentNode.parentNode;
    }
    return parentNode
}

/**************************
 * Create stars froma float
 **************************/

$.fn.stars = function() {
    return $(this).each(function() {
        // Get the value
        var val = parseFloat($(this).html());
        // Make sure that the value is in 0 - 5 range, multiply to get width
        var size = Math.max(0, (Math.min(5, val))) * 16;
        // Create stars holder
        var $span = $('<span />').width(size);
        // Replace the numerical value with stars
        $(this).html($span);
    });
}
//});