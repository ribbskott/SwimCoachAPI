angular.module('sloach', ['ngMaterial','ngCookies','ngRoute', 'ngMessages'])
    .config(['$routeProvider','$locationProvider','$mdThemingProvider' ,function($routeProvider, $locationProvider, $mdThemingProvider){
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
            .when('/profile',{
                templateUrl:'partials/profile.html',
                controller:'profileCtrl'
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
        }
    })
    .controller('InfoCtrl',['$scope', function($scope){

    }])
    .controller('appCtrl', ['$scope', '$mdSidenav', /*'$mdThemingProvider',*/ 'AuthService', '$mdDialog', '$cookies','$location', '$log', '$timeout', '$rootScope',
                function($scope, $mdSidenav, /*$mdThemingProvider,*/ AuthService, $mdDialog, $cookies, $location, $log, $timeout, $rootScope){
        $scope.signupUrl = 'signup';
        $scope.loginUrl = 'login';
        $scope.myclubUrl = 'myclub';
        $scope.credentials = { email: "", password: "" };
        $scope.errorMessage = "";
        $scope.login = function () {
        $scope.isLoggedIn = false;


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
        var loginPromise = AuthService.getUserSession($scope.credentials);
        loginPromise.success(function (data, status, headers, config) {
                        $cookies.put('sessiontoken', data.token);
                        $scope.isLoggedIn = true;
                        $location.url("/info");
                        $rootScope.sessiontoken = data.token;
                        $rootScope.iduser = data.iduser;
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
      $scope.navigateProfile = function(){
            $location.path("/profile");
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