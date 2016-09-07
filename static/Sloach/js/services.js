angular.module('sloach').factory('ProfileService', function ($http) {



    return {
        getProfile: function (iduser) {
            if($rootScope && $rootScope.session){
                return $rootScope.session.profile;
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

angular.module('sloach').factory('AthleteService',function($http){
    return{
        getAthletes: function(clubkey){
            var url = "http://localhost:5000/clubs/" + String(clubkey) + "/athletes";

            return $http.get(url);
        },
        getNextTrainingSession: function(idclub, idathlete){
            var url = "http://localhost:5000/clubs/" + String(idclub) + "/athletes/"+ idathlete + "/sessions"
            return $http.get(url)
        },
        addAthlete: function(clubkey, athlete){
            var url = "http://localhost:5000/clubs/" + String(clubkey) + "/athletes";

            return $http.post(url, athlete)
        },
        getResultsForAthlete:function(idathlete){
            var url = "http://localhost:5000/clubs/" + String(clubkey) + "/athletes/" + String(idathlete);
            return $http.get(url);
        }
    };
});

angular.module('sloach').factory('ClubService',function($http){
    return{
        getClub: function (rowkey) {
            var profile;
            var url = "http://localhost:5000/clubs/" + String(rowkey) ;

            return $http.get(url);
        },
        updateClub: function(clubkey, club){
            var url = "http://localhost:5000/clubs/" + club.rowkey;
            return $http.post(url, club);
        },
        updateClubPicture: function(clubkey, picture){
            var url = "http://localhost:5000/clubs/" + clubkey + "/picture"
            return $http.post(url,picture);
        }

    };

});

angular.module('sloach').service('fileUpload', ['$http', function ($http) {
    this.uploadFileToUrl = function(file, uploadUrl){
        var fd = new FormData();
        fd.append('file', file);
        return $http.post(uploadUrl, fd, {
            transformRequest: angular.identity,
            headers: {'Content-Type': undefined}
        });
    },
    this.getFile = function(uploadUrl){
        return $http.get(uploadUrl);
    }
}]);

