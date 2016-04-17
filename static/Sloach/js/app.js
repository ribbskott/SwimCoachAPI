var app = angular.module('sloach', ['ngMaterial','ngCookies','ngRoute', 'ngMessages'])
    app.config(['$routeProvider','$locationProvider','$mdThemingProvider' ,function($routeProvider, $locationProvider, $mdThemingProvider){
        $routeProvider
            .when('/info',{
                templateUrl:'partials/info.html',
                controller: 'InfoCtrl'
            })
            .when('/login',{
                templateUrl:'partials/auth.html',
                controller:'auth'
            })
            .when('/signup',{
                templateUrl:'partials/signup.html',
                controller:'auth'
            })
            .otherwise({
                redirectTo:'/info'
            });
        $mdThemingProvider.theme("default").primaryPalette("blue").accentPalette("red");

        $locationProvider.html5Mode(true);
    }]);
    app.factory('UserLoginService', function ($http) {
        var userServiceFactory = {};
        userServiceFactory.url = "localhost:5000/login";
        userServiceFactory.login = function (credentials) {
                return $http.post(url + '/login', credentials);
            };
        return userServiceFactory;
    });

    app.service('LoginService', function(UserLoginService){
        this.login = function(credentials){
            return UserLoginService.login({username: 'hej', password:'då'});
        }
    });
    app.controller('InfoCtrl',['$scope', function($scope){

    }]);
    app.controller('appCtrl', ['$scope', '$mdSidenav', /*'$mdThemingProvider',*/ 'AuthService', '$mdDialog', function($scope, $mdSidenav, /*$mdThemingProvider,*/ AuthService, $mdDialog){
      $scope.signupUrl = 'signup';
      $scope.loginUrl = 'login';
      $scope.myclubUrl = 'myclub';
      $scope.credentials = { email: "", password: "" };
      $scope.errorMessage = "";
      $scope.login = function () {
      $scope.isLoggedIn = false;

        var loginPromise = AuthService.getUserSession($scope.credentials);
        loginPromise.success(function (data, status, headers, config) {
                        $cookies.put('sessiontoken', data.token);
                        $scope.isLoggedIn = true;
                      })
                    .error(function (data, status, headers, config) {
                        $scope.isLoggedIn = false;
                        $scope.errorMessage = data;
                        $mdDialog.show(
                          $mdDialog.alert()
                            .parent(angular.element(document.querySelector('#popupContainer')))
                            .clickOutsideToClose(true)
                            .title('Whoops!')
                            .textContent(data)
                            .ariaLabel('Whoops!')
                            .ok('OK')
                        );
                    });
      };
      $scope.signup = function () {

        var signupPromise =  AuthService.signup($scope.credentials);

        signupPromise.success(function (data, status, headers, config) {
                        $cookies.put('sessiontoken', data.token);
                        $scope.isLoggedIn = true;
                    })
                    .error(function (data, status, headers, config) {
                        $scope.errorMessage = data;
                        $scope.isLoggedIn = false;
                         $mdDialog.show(
                          $mdDialog.alert()
                            .parent(angular.element(document.querySelector('#popupContainer')))
                            .clickOutsideToClose(true)
                            .title('Whoops!')
                            .textContent(data)
                            .ariaLabel('Whoops!')
                            .ok('OK')
                        );
                    });

      };

    }]);