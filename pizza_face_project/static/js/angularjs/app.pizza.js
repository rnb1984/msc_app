var pizzaApp = angular.module('pizzaApp',[])
    .config(['$httpProvider', function($httpProvider) {
        // set CSRF for Django
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }]);
console.log("first here");

// Controller for pizzas
pizzaApp.controller('pizzaController', function ($scope, $http, $rootScope ) {
    // App for single pizza
    var pk = parseInt(document.title);
    console.log("got here", pk+1);
    $scope.lingd = true;
    $http.get("/pizza/"+pk+"/").success(function(data){
        $scope.pizzas = data;
    });
});