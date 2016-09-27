angular.module('sloach').factory('GroupService', function($http){
    return{
        getGroup: function(clubkey, idgroup){
            var url = "http://localhost:5000/clubs/" + clubkey + "/groups/" + idgroup;
            return $http.get(url);
        },
        getGroups: function(clubkey){
            var url = "http://localhost:5000/clubs/" + clubkey +"/groups"
            return $http.get(url);
        },
        getAthletesInGroup(clubkey,idgroup){
            var url = "http://localhost:5000/clubs/" + clubkey + "/groups/" + idgroup + "/athletes";
            return $http.get(url);
        },
        getSessionsForGroup(clubkey,idgroup){
            var url = "http://localhost:5000/clubs/" + clubkey + "/groups/" + idgroup + "/trainingsessions";
            return $http.get(url);
        }
    };
});