angular.module('sloach').controller('profileCtrl', ['$scope', 'ProfileService', function($scope, profiles){
    $scope.greet = function(){
        alert("hej från profileCtrl");
    };
    $scope.greet();
}]);