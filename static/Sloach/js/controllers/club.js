angular.module('sloach').controller('clubCtrl', ['$scope', '$rootScope', 'ClubService', function($scope, $rootScope, clubs){

    $scope.profile = $rootScope.session.profile;

    $scope.editClub = function(){
        $location.path('/club/edit');
    };
    $scope.navigateBack = function(){
        $location.path('/club/view');
    };

//    $scope.updateProfile = function(){
//        profiles.updateClub($rootScope.session.iduser, $scope.profile);
//    };

    $scope.getClub = function(){

        var getClubPromise = clubs.getClub($rootScope.session.profile.clubkey);
        getClubPromise.success(function (data, status, headers, config) {
                            $rootScope.club = data;

                        })
                        .error(function(data, status,headers,config){
                            alert(JSON.stringify(data));
                        });
    };

    if($scope.club === undefined){
        console.log("undefined");
        $scope.getClub();
    }


}]);