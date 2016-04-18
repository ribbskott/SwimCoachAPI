angular.module('sloach')
    .controller('mainMenuCtrl', function ($scope, $timeout, $mdSidenav, $log) {
        $scope.close = function () {
          // Component lookup should always be available since we are not using `ng-if`
          $mdSidenav('mainMenu').close();
        };
      });