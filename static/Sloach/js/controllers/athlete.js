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
                if (data.athleteSessions.length > 0){
                    $scope.nextTrainingSession = data.athleteSessions.sortBy(function(s){return s.fromtime;})[0];
                }
                else $scope.selectedAthlete.nextTrainingSession = {};

                if($scope.selectedAthlete.nextTrainingSession && $scope.selectedAthlete.nextTrainingSession.fromtime > new Date()){
                    $scope.nextTrainingSession.fromtime_readable = moment($scope.selectedAthletenextTrainingSession.fromtime).fromNow();
                    $scope.nextTrainingSession.totime_readable = moment($scope.selectedAthletenextTrainingSession.totime).fromNow();

                    $scope.nextTrainingSessionDisplay = moment($scope.selectedAthlete.nextTrainingSession.fromtime_readable).fromNow() + " - " +
                                                                moment($scope.selectedAthlete.nextTrainingSession.totime_readable).fromNow();
                }
                else{
                    $scope.nextTrainingSession.fromtime_readable = "";
                    $scope.nextTrainingSession.totime_readable = "";
                    $scope.nextTrainingSessionDisplay = "Ingen mer träning :( \nSkapa ett nytt träningspass för gruppen!";
                }

            })
            .error(function(data, status, headers, config){
                $scope.selectedAthlete.trainingSessions = [];
            });
        };

        $scope.trainingResults = [];

        $scope.getTrainingResults = function(){
            var getTrainingResultsPromise = athletes.getResultsForAthlete($scope.selectedAthlete.id);

            getTrainingResultsPromise.success(function(data, status, headers, config){
                angular.copy(data.trainingResults, $scope.trainingResults);
            })
            .error(function(data, status, header, config){
                alert(data);
            });

        };



        //Init
        $scope.setSelectedAthlete();
        $scope.getNextTrainingSession();
        $scope.getTrainingResults();

        $scope.graphOptions = {
            scales: {
              yAxes: [
                {
                  id: 'y-axis-1',
                  type: 'linear',
                  display: true,
                  position: 'left'
                },
                {
                  id: 'y-axis-2',
                  type: 'linear',
                  display: true,
                  position: 'right'
                }
              ]
            }
          };
        $scope.graphLabels = [];
        $scope.graphData = [];
        //Create Graph
        if($scope.trainingResults){
            for(i = 0;i< $scope.trainingResults.length;i++){
                $scope.graphLabels.push(moment($scope.trainingResults[i].achievedondate).format('YY-MMMM'));
                $scope.graphData.push(moment($scope.trainingresults[i].timeresult.duration));
            }
        }

}]);