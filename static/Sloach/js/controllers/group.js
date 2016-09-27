var app = angular.module('sloach');
app.controller('groupCtrl', ['$scope', '$rootScope', '$location', 'GroupService', 'TrainingSessionService', 'AthleteService', function($scope, $rootScope, $location, groups, trainingsessions, athletes){

    $scope.editGroup = function(){
        $location.path('/group/edit');
    };
    $scope.cancelEdit = function(){
        $location.path('/group/view');
    };

    $scope.searchAthlete = "";

    $scope.athletes = {};

    $scope.viewAthlete = function(athlete){
        $rootScope.selectedAthlete = athlete;
        $location.path('/athlete/view');
    };
    $scope.group = $rootScope.selectedGroup;
    $scope.getAthletes = function(group){
        var getAthletesPromise = groups.getAthletesInGroup($rootScope.session.profile.clubkey, group.id);
        getAthletesPromise.success(function(data, status, headers, config){
            $scope.group.athletes = data.athletes;
        })
        .error(function(data, status, headers, config){
            alert(data);
        });

    };




    /*$scope.getTrainingSessions = function(group){
        var getSessionsPromise = trainingsessions.getSessionsForGroup($rootScope.session.profile.clubkey, group.idgroup);
        getSessionsPromise.success(function(data, status, headers, config){
            $scope.group.trainingsessions = data.trainingsessions;
        })
        .error(function(data,status,headers,config){
            alert(data);
        });

    };*/

    $scope.getAthletes($scope.group);
    //$scope.getTrainingSessions($scope.group);

}]);

app.filter("fromNow",function(){
    return function(input){
        if(input){
            return moment(input).fromNow();
        }
    }
});