angular.module('sloach').controller('athleteCtrl', ['$scope', '$rootScope', '$location', 'AthleteService', function($scope, $rootScope, $location, athletes){

        $scope.selectedAthlete = {};

        $scope.setSelectedAthlete = function(){
            $scope.selectedAthlete = $rootScope.selectedAthlete;

        }

        $scope.cancelEdit = function(){
            $location.path = '/athlete/view'
        }

        $scope.getAthlete = function(){
            var getAthletesPromise = athletes.getAthletes($rootScope.session.profile.clubkey, $scope.selectedAthlete);
            getAthletesPromise.success(function(data, status, headers, config){
                $rootScope.club.athletes = data.athletes;

            })
            .error(function(data,status,headers,config){
                alert(JSON.stringify(data));
            });
        };

        $scope.nextTrainingSessionDisplay = "";

        $scope.getNextTrainingSession = function(){

            var getNextTrainingSessionPromise = athletes.getNextTrainingSession($rootScope.session.profile.clubkey, $scope.selectedAthlete.id);


            getNextTrainingSessionPromise.success(function(data,status, headers, config){
                $scope.selectedAthlete.trainingSessions = data.athleteSessions;
                var selectedAthlete = $scope.selectedAthlete;
                $scope.selectedAthlete.nextTrainingSession = data.athleteSessions.sortBy(function(s){return s.fromtime;})[0];
                if($scope.selectedAthlete.nextTrainingSession.fromtime > new Date()){
                    $scope.selectedAthlete.nextTrainingSession.fromtime_readable = moment($scope.selectedAthletenextTrainingSession.fromtime).fromNow();
                    $scope.selectedAthlete.nextTrainingSession.totime_readable = moment($scope.selectedAthletenextTrainingSession.totime).fromNow();

                    $scope.nextTrainingSessionDisplay = moment($scope.selectedAthlete.nextTrainingSession.fromtime_readable).fromNow() + " - " +
                                                                moment($scope.selectedAthlete.nextTrainingSession.totime_readable).fromNow();
                }
                else{
                    $scope.selectedAthlete.nextTrainingSession.fromtime_readable = "";
                    $scope.selectedAthlete.nextTrainingSession.totime_readable = "";
                    $scope.selectedAthlete.nextTrainingSessionDisplay = "Ingen mer träning :( \nSkapa ett nytt träningspass för gruppen!";
                }

            })
            .error(function(data, status, headers, config){
                alert(JSON.stringify(data));
            });
        };

        $scope.setSelectedAthlete();
        $scope.getNextTrainingSession();
}]);