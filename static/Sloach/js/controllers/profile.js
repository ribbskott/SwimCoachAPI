angular.module('sloach').controller('profileCtrl', ['$scope', '$rootScope', 'ProfileService', '$location', function($scope, $rootScope, profiles, $location){
    $scope.profile = $rootScope.session.profile;


    $scope.editProfile = function(){
        $location.path('/profile/edit');
    };

    $scope.updateProfile = function(){
        profiles.updateProfile($rootScope.session.iduser, $scope.profile);
    };

    $scope.getProfile = function(){
        var getProfilePromise = profiles.getProfile($rootScope.session.iduser);
        getProfilePromise.success(function (data, status, headers, config) {
                        $rootScope.profile = data;
                        })
                        .error(function(data, status,headers,config){
                            alert(JSON.stringify(data));
                        });
    };

    $scope.getClub = function(){
        var getClubPromise = profiles.getClub($rootScope.session.iduser);

    };

}]);