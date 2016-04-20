angular.module('sloach').factory('ProfileService', function ($http) {

    return {
        getProfile: function (iduser) {
            var url = "http://localhost:5000/user/" + String(iduser) + "/profile";
            return $http.get(url, iduser);
        },

        createProfile: function(iduser, profile){
            var url = "http://localhost:5000/user/" + String(iduser) + "/profile";
            return $http.post(url, iduser, profile);
        }
    };
});

