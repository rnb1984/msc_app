 var routeApp = angular.module("myApp", ["ngRoute"]);


// routers for urls
routeApp.config( [
         '$routeProvider',function($routeProvider) {
    console.log('got here router')
    $routeProvider
    .when("/", {
        templateUrl : "//pizza_ml/pref-pairs.html",
    })
    .when("/details", {
        templateUrl : "//templates/pizza_ml/partials/details.htm",
    })
    .when("/pizzas", {
        templateUrl : "//static/templates/pizza_ml/partials/pizzas.htm",
    })
    .when("/prediction", {
        templateUrl : "//static/templates/pizza_ml/partials/prediction.htm",
    });
}]);



//routeApp.directive("testView", function() {
//    return {
//        template : "<h1>Made by a directive!</h1>"
//    };
//});
