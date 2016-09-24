var permissionApp = angular.module('permissionApp',[])
    .config(['$httpProvider', function($httpProvider) {
        // set CSRF for Django
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }]);
    
// Controller for last page
permissionApp.controller('permissionExpOneController',permissionExpOneController)
permissionApp.controller('permissionController', permissionController)

function permissionController($scope, $http, $rootScope ) {
    // urls
    console.log('got here', document.title);
    
        // set paramaters
        $scope.endmessage ='Please answer';
        $scope.answered = false;
      $scope.answer = function(result){
        // Post answer back
            $scope.answered = true;
            var data = {answer: result };
            console.log(data)
            $http.post("/results/",data).success(function(data){
                 $scope.endmessage = data;
            });
        }
     
};

// Controller for last page
function permissionExpOneController ($scope, $http, $rootScope ) {

    // urls
    console.log('got here EXP one', document.title);
    
        // set paramaters
        $scope.endmessage ='Please answer';
        $scope.answered = false;
      $scope.answer = function(result){
        // Post answer back
            $scope.answered = true;
            var data = {answer: result };
            console.log(data)
            $http.post("/expone/end/",data).success(function(data){
                 $scope.endmessage = data;
            });
        }
     
};