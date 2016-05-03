angular.module('sloach')
    .controller('mainMenuCtrl', function ($scope,$rootScope, $location, $mdSidenav) {


        $scope.close = function () {
          // Component lookup should always be available since we are not using `ng-if`
          $mdSidenav('mainMenu').close();
        };
        $scope.navigateClub = function(){
            $mdSidenav('mainMenu').close();
            $location.path("/club");
        };
        $scope.navigateProfile = function(){
            $mdSidenav('mainMenu').close();
            $location.path('/profile');
        };
      });