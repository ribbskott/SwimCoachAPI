angular.module('sloach').controller('clubCtrl', ['$scope', '$rootScope', '$location', 'ClubService','AthleteService', function($scope, $rootScope, $location, clubs, athletes){

    $scope.profile = $rootScope.session.profile;

    $scope.editClub = function(){
        $location.path('/club/edit');
    };
    $scope.cancelEdit = function(){
        $location.path('/club/view');
    };


    $scope.viewAthlete = function(athlete){
        $rootScope.selectedAthlete = athlete;
        $location.path('/athlete/view');
    };

    var doGetClub = function(){

        var getClubPromise = clubs.getClub($rootScope.session.profile.clubkey);
        getClubPromise.success(function (data, status, headers, config) {
                            $rootScope.club = data;
                            $scope.getAthletes();
                        })
                        .error(function(data, status,headers,config){
                            alert(JSON.stringify(data));
                        });
    };


    $scope.getClub = function(){
        doGetClub();
    }



    $scope.updateClub = function(){

        var updateClubPromise = clubs.updateClub($rootScope.session.profile.clubkey, $scope.club);
        updateClubPromise.success(function (data, status, headers, config) {
                            $rootScope.club = data;
                        })
                        .error(function(data, status,headers,config){
                            $scope.error = data;
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