angular.module('sloach').controller('profileCtrl', ['$scope', '$rootScope', 'ProfileService', function($scope, $rootScope, profiles){
    $scope.profile = $rootScope.session.profile;

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