angular.module('sloach').controller('athleteCtrl', ['$scope', '$rootScope', '$location', 'AthleteService', function($scope, $rootScope, $location, athletes){

        $scope.selectedAthlete = {};

        $scope.setSelectedAthlete = function(){
            $scope.selectedAthlete = $rootScope.selectedAthlete;
        }

        $scope.cancelEdit = function(){
            $location.path = '/athlete/view'
        }



        $scope.labels = ["January", "February", "March", "April", "May", "June", "July"];


        $scope.series = ['Series A', 'Series B'];
        //hämta data baserat på träningsresultatstyp
        $scope.data = [
            [65, 59, 80, 81, 56, 55, 40],
            [28, 48, 40, 19, 86, 27, 90]
          ];


        $scope.datasetOverride = [{ yAxisID: 'y-axis-1' }, { yAxisID: 'y-axis-2' }];
        $scope.options = {
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
        $scope.getAthlete = function(){
            var getAthletesPromise = athletes.getAthletes($rootScope.session.profile.clubkey, $scope.selectedAthlete);
            getAthletesPromise.success(function(data, status, headers, config){
                $rootScope.club.athletes = data.athletes;

            })
            .error(function(data,status,headers,config){
                alert(JSON.stringify(data));
            });
        }


        $scope.setSelectedAthlete();
}]);