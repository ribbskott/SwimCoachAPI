angular.module('sloach').controller('athleteCtrl', ['$scope', '$rootScope', '$location', 'AthleteService', function($scope, $rootScope, $location, athletes){

        $scope.selectedAthlete = {};

        $scope.setSelectedAthlete = function(athlete){
            $scope.selectedAthlete = athlete;
        }

        $scope.cancelEdit = function(){
            $location.path = '/athlete/view'
        }

        $scope.getAthletes = function(){
            var getAthletesPromise = athletes.getAthletes($rootScope.session.profile.clubkey, $scope.selectedAthllete);
            getAthletesPromise.success(function(data, status, headers, config){
                $rootScope.club.athletes = data.athletes;

            })
            .error(function(data,status,headers,config){
                alert(JSON.stringify(data));
            });
        }
}]);