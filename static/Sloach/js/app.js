var app = angular.module('sloach', ['ngMaterial','ngCookies','ngRoute'])
    app.config(['$routeProvider','$locationProvider','$mdThemingProvider' ,function($routeProvider, $locationProvider, $mdThemingProvider){
        $routeProvider
            .when('/info',{
                templateUrl:'partials/auth.html',
                controller: 'auth'
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
                redirectTo:'/login'
            });
        $mdThemingProvider.theme("default").primaryColor("blue").accentColor("red");

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
    app.controller('appCtrl', ['$scope', '$mdSidenav', /*'$mdThemingProvider',*/ 'LoginService', function($scope, $mdSidenav, /*$mdThemingProvider,*/ LoginService){
      $scope.signupUrl = 'signup';
      $scope.loginUrl = 'login';
      $scope.login =  function(LoginService, $scope){
        alert(UserService.login({'email': $scope.email, 'password': $scope.password}));
      };

    }]);