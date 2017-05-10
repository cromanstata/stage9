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
//});