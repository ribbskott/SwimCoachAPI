angular.module('sloach').controller('clubCtrl', ['$scope', '$rootScope', '$location', 'ClubService','AthleteService', 'fileUpload', 'GroupService', function($scope, $rootScope, $location, clubs, athletes, fileUpload, groups){

    $scope.profile = $rootScope.session.profile;

    $scope.editClub = function(){
        $location.path('/club/edit');
    };
    $scope.cancelEdit = function(){
        $location.path('/club/view');
    };

    $scope.clubpicture = "";
    $scope.clubPictureUrl = "";
    $scope.search = "";
    var getPicture = function(){
        var uploadUrl = "http:///localhost:5000/clubs/" + $rootScope.session.profile.clubkey + "/picture";
        var getfilePromise = fileUpload.getFile(uploadUrl);
        getfilePromise.success(function(data,status,headers,config){
            $scope.clubPictureUrl = data.filename;
        }).error(function(data, status, headers, config){
            alert("hej");
        });

    };

    $scope.groups = {};

    $scope.viewGroup = function(group){
        $rootScope.selectedGroup = group;
        $location.path('/group/view');
    }

    $scope.viewAthlete = function(athlete){
        $rootScope.selectedAthlete = athlete;
        $location.path('/athlete/view');
    };

    $scope.uploadFile = function(){
        var file = $scope.clubpicture;
        console.log('file is ' );
        console.dir(file);
        var uploadUrl = "http:///localhost:5000/clubs/" + $rootScope.session.profile.clubkey + "/picture";
        fileUpload.uploadFileToUrl(file, uploadUrl);
    };

    var doGetClub = function(){

        var getClubPromise = clubs.getClub($rootScope.session.profile.clubkey);
        getClubPromise.success(function (data, status, headers, config) {
                $rootScope.club = data;
                $scope.getAthletes();
                $scope.getGroups();
            })
            .error(function(data, status,headers,config){
                alert(JSON.stringify(data));
            });
    };


    $scope.getClub = function(){
        doGetClub();
        getPicture();
    }

    $scope.clubPicture = "";

    $scope.fileNameChanged = function (ele) {
      var files = ele.files;
      var l = files.length;
      var namesArr = [];

      for (var i = 0; i < l; i++) {
        namesArr.push(files[i].name);
      }
    }


    $scope.updateClub = function(){

        var updateClubPromise = clubs.updateClub($rootScope.session.profile.clubkey, $scope.club);
        updateClubPromise.success(function (data, status, headers, config) {
                            $rootScope.club = data;
                        })
                        .error(function(data, status,headers,config){
                            $scope.error = data;
                        });
    };

    $scope.getAthletes = function(){
        var getAthletesPromise = athletes.getAthletes($rootScope.session.profile.clubkey);
        getAthletesPromise.success(function(data, status, headers, config){
            $rootScope.club.athletes = data.athletes;

        })

    };

    $scope.getGroups = function(){
        var getGroupsPromise = groups.getGroups($rootScope.session.profile.clubkey);
        getGroupsPromise.success(function(data,status, header, config){
            $rootScope.club.groups = data.groups;

        })
        .error(function(data, status, header, config){
            alert(data);
       })
    };

    if($rootScope.club === undefined){
        $scope.getClub();
    }



}]);