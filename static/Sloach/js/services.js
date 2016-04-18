'use strict';

angular.module('sloach').factory('ProfileService', function ($http) {
    var url = "localhost:5000/profile";
    return {
        getProfile: function (sessiontoken) {
            return $http.get(url, sessiontoken);
        }
    };
});

