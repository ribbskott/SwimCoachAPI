'use strict';

angular.module('sloach').factory('UserService', function ($http) {
    //var url = config.analytics.url;
    var url = "localhost:5000/login";
    return {
        login: function (credentials) {
            return $http.post(url + '/auth', credentials);
        }
    };
});

angular.module('sloach').factory('httpInterceptor', function httpInterceptor($q, $window, $location) {
    return function (promise) {
        var success = function (response) {
            return response;
        };

        var error = function (response) {
            if (response.status === 401) {
                $location.url('/login');
            }

            return $q.reject(response);
        };

        return promise.then(success, error);
    };
});


angular.module('sloach').factory('api', function ($http, $cookies) {
    return {
        init: function (token) {
            $http.defaults.headers.common['X-Access-Token'] = token || $cookies.token;
        }
    };
});