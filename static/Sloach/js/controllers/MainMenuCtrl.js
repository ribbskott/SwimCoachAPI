angular.module('sloach')
    .controller('mainMenuCtrl', function ($scope, $location, $mdSidenav) {
        $scope.close = function () {
          // Component lookup should always be available since we are not using `ng-if`
          $mdSidenav('mainMenu').close();
        };
        $scope.navigateProfile = function(){
            $mdSidenav('mainMenu').close();
            $location.path("/profile");
        };
      });