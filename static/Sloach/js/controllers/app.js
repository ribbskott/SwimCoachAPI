moment.locale('sv');
angular.module('sloach', ['ngMaterial','ngCookies','ngRoute', 'ngMessages','chart.js'])
    .config(['$routeProvider','$locationProvider','$mdThemingProvider', 'ChartJsProvider' ,function($routeProvider, $locationProvider, $mdThemingProvider,ChartJsProvider){
        (function (ChartJsProvider) {
          ChartJsProvider.setOptions({ colors : [ '#803690', '#00ADF9', '#DCDCDC', '#46BFBD', '#FDB45C', '#949FB1', '#4D5360'] });
        });

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
            .when('/profile/view',{
                templateUrl:'partials/profile.html',
                controller:'profileCtrl'
            })
            .when('/profile/edit',{
                templateUrl:'partials/forms/profile.edit.html',
                controller: 'profileCtrl'
            })
            .when('/club',{
                templateUrl:'partials/club.html',
                controller:'clubCtrl'
            })
            .when('/club/edit',{
                templateUrl:'partials/forms/club.edit.html',
                controller: 'clubCtrl'
            })
            .when('/athlete/view',{
                templateUrl:'partials/athlete.html',
                controller: 'athleteCtrl'
            })
            .when('/athlete/edit',{
                templateUrl:'partials/forms/athlete.edit.html',
                controller: 'athleteCtrl'
            })
            .when('/group/view',{
                templateUrl:'partials/group.html',
                controller: 'groupCtrl'
            })
            .otherwise({
                redirectTo:'/info'
            });

        $mdThemingProvider.theme("default").primaryPalette("blue-grey").accentPalette("grey");

        $locationProvider.html5Mode(true);
    }])

    // Click to navigate
    // similar to <a href="#/partial"> but hash is not required,
    // e.g. <div click-link="/partial">
    .directive('clickLink', ['$location', function($location) {
        return {
            link: function(scope, element, attrs) {
                element.on('click', function() {
                    scope.$apply(function() {
                        $location.path(attrs.clickLink);
                    });
                });
            }
        }
    }])

    .directive('fileModel', ['$parse', function ($parse) {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            var model = $parse(attrs.fileModel);
            var modelSetter = model.assign;

            element.bind('change', function(){
                scope.$apply(function(){
                    modelSetter(scope, element[0].files[0]);
                });
            });
        }
    };
    }])


    .factory('UserLoginService', function ($http) {
        var userServiceFactory = {};
        userServiceFactory.url = "localhost:5000/login";
        userServiceFactory.login = function (credentials) {
                return $http.post(url + '/login', credentials);
            };
        return userServiceFactory;
    })
    .service('LoginService', function(UserLoginService){
        this.login = function(credentials){
            return UserLoginService.login({username: 'hej', password:'då'});
        },
        this.logout = function(){
            return UserLoginService.logout();
        }
    })
    .controller('InfoCtrl',['$scope', function($scope){

    }])
    .controller('appCtrl', ['$scope', '$mdSidenav', /*'$mdThemingProvider',*/ 'AuthService', '$mdDialog', '$cookies','$location', '$log', '$timeout', '$rootScope','$http',
                function($scope, $mdSidenav, /*$mdThemingProvider,*/ AuthService, $mdDialog, $cookies, $location, $log, $timeout, $rootScope,$http){
        $scope.signupUrl = 'signup';
        $scope.loginUrl = 'login';
        $scope.myclubUrl = 'myclub';
        $scope.credentials = { email: "", password: "" };
        $scope.errorMessage = "";

        $scope.isLoggedIn = false;

        $scope.showProfile = function(){
            $location.path('/profile/view');
        }

        /**
         * Supplies a function that will continue to operate until the
         * time is up.
         */
        function debounce(func, wait, context) {
          var timer;

          return function debounced() {
            var context = $scope,
                args = Array.prototype.slice.call(arguments);
            $timeout.cancel(timer);
            timer = $timeout(function() {
              timer = undefined;
              func.apply(context, args);
            }, wait || 10);
          };
        };
        /**
         * Build handler to open/close a SideNav; when animation finishes
         * report completion in console
         */
        function buildDelayedToggler(navID) {
          return debounce(function() {
            // Component lookup should always be available since we are not using `ng-if`
            $mdSidenav(navID).toggle();
          }, 200);
        };
        function buildToggler(navID) {
          return function() {
            // Component lookup should always be available since we are not using `ng-if`
            $mdSidenav(navID).toggle();
          }
        };
        $scope.showMenu = buildDelayedToggler('mainMenu');
        $scope.login = function () {
            var loginPromise = AuthService.getUserSession($scope.credentials);
            loginPromise.success(function (data, status, headers, config) {
                        $cookies.put('sessiontoken', data.token);
                        $scope.isLoggedIn = true;
                        $http.defaults.headers.common['sessiontoken'] = data.token;
                        $rootScope.session = {  iduser: data.iduser,
                                                profile: data.profile,
                                                sessiontoken: data.token};
                        $scope.session = $rootScope.session;
                        $location.url("/info");

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
      $scope.logout = function(){
        var sessiontoken = $cookies.get('sessiontoken');
        if (sessiontoken){
            var logoutPromise = AuthService.logout(sessiontoken);
            logoutPromise.success(function(data,status,header,config){
                $cookies.put('sessiontoken', null);
                $scope.isLoggedIn = false;
                $http.defaults.headers.common['sessiontoken'] = null;
                $rootScope.session = null;
                $scope.session = null;
                $location.url("/info");
            });
        }


      };
      $scope.navigateProfile = function(){
            $location.path("/profile/view");
      };
      $scope.signup = function () {

        var signupPromise =  AuthService.signup($scope.credentials);

        signupPromise.success(function (data, status, headers, config) {
                        $cookies.put('sessiontoken', data.token);
                        $scope.isLoggedIn = true;
                        $http.defaults.headers.common['sessiontoken'] = data.token;
                        $rootScope.session = {  iduser: data.iduser,
                                                profile: data.profile,
                                                sessiontoken: data.token};
                        $location.url("/info");
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