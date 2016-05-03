angular.module('sloach').factory('ProfileService', function ($http) {



    return {
        getProfile: function (iduser) {
            if($rootScope && $rootScope.session){
                return $rootScope.session;
            }
            var url = "http://localhost:5000/users/" + String(iduser) + "/profile";

            return $http.get(url, iduser);
        },

        createProfile: function(iduser, profile){
            var url = "http://localhost:5000/users/" + String(iduser) + "/profile";
            return $http.post(url, profile);
        },

        updateProfile: function(iduser, profile){
            var url = "http://localhost:5000/users/" + String(iduser) + "/profile";
            return $http.post(url, profile);
         }


    };
});

