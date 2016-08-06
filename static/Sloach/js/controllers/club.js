angular.module('sloach').controller('clubCtrl', ['$scope', '$rootScope', '$location', 'ClubService','AthleteService', function($scope, $rootScope, $location, clubs, athletes){

    $scope.profile = $rootScope.session.profile;

    $scope.editClub = function(){
        $location.path('/club/edit');
    };
    $scope.cancelEdit = function(){
        $location.path('/club/view');
    };

//    $scope.updateProfile = function(){
//        profiles.updateClub($rootScope.session.iduser, $scope.profile);
//    };


    $scope.viewAthlete = function(){
        $location.path('/athlete/view');
    };

    $scope.getClub = function(){

        var getClubPromise = clubs.getClub($rootScope.session.profile.clubkey);
        getClubPromise.success(function (data, status, headers, config) {
                            $rootScope.club = data;
                            $scope.getAthletes();
                        })
                        .error(function(data, status,headers,config){
                            alert(JSON.stringify(data));
                        });
    };

    $scope.updateClub = function(){

        var updateClubPromise = clubs.updateClub($rootScope.session.profile.clubkey, $scope.club);
        getClubPromise.success(function (data, status, headers, config) {
                            $rootScope.club = data;
                            $scope.getAthletes();
                        })
                        .error(function(data, status,headers,config){
                            alert(JSON.stringify(data));
                        });
    };

    $scope.getAthletes = function(){
        var getAthletesPromise = athletes.getAthletes($rootScope.session.profile.clubkey);
        getAthletesPromise.success(function(data, status, headers, config){
            $rootScope.club.athletes = data.athletes;

        })

    };

    if($rootScope.club === undefined){
        $scope.getClub();
    }



}]);